import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import heapq
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile


SESSION_ID = re.compile(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}")
JST = timezone(timedelta(hours=9))
LOG_HEADING = "## Session Log"
LOG_HEADINGS = (LOG_HEADING, "## セッションログ")
ARTIFACTS_HEADINGS = ("## Artifacts", "## 成果物")
LOG_ROW = re.compile(r"^- \d{4}-\d{2}-\d{2} \d{2}:\d{2} `([^`]+)` — ")


def session_reference(agent):
    claude_id = os.getenv("CLAUDE_CODE_SESSION_ID") or os.getenv("CLAUDE_SESSION_ID")
    codex_id = os.getenv("CODEX_THREAD_ID") or os.getenv("CODEX_SESSION_ID")
    if agent == "codex" or (agent is None and codex_id and not claude_id):
        return f"codex:{codex_id}" if codex_id else None
    return claude_id


def claude_projects():
    override = os.getenv("STASH_PROJECTS_DIR")
    if override:
        return Path(override)
    return Path(os.getenv("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"


def codex_log(session_id):
    home = Path(os.getenv("CODEX_HOME") or Path.home() / ".codex")
    for directory, pattern in (
        ("sessions", f"*/*/*/rollout-*-{session_id}.jsonl"),
        ("archived_sessions", f"rollout-*-{session_id}.jsonl"),
    ):
        for path in sorted((home / directory).glob(pattern), reverse=True):
            if path.is_file():
                return path
    return None


def session_logs(reference):
    is_codex = reference.startswith("codex:")
    session_id = reference.removeprefix("codex:")
    if not SESSION_ID.fullmatch(session_id):
        raise ValueError("Invalid session reference")

    if is_codex:
        path = codex_log(session_id)
        return [(path, "main")] if path else []

    root = claude_projects()
    parents = sorted(root.glob(f"*/{session_id}.jsonl"))
    children = sorted(root.glob(f"*/{session_id}/subagents/agent-*.jsonl"))
    return [(path, "main") for path in parents if path.is_file()][:1] + [
        (path, path.stem) for path in children if path.is_file()
    ]


def heading_range(lines, headings):
    start = next((i for i, line in enumerate(lines) if line.rstrip() in headings), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return start, end


def reference_row(lines, section, reference):
    if section is not None:
        start, end = section
        for index in range(start + 1, end):
            match = LOG_ROW.match(lines[index])
            if match and match[1] == reference:
                return index
    return None


def update_reference(lines, stamp, reference, note):
    section = heading_range(lines, LOG_HEADINGS)
    existing = reference_row(lines, section, reference)
    row = f"- {stamp} `{reference}` — {note}\n"
    if existing is not None:
        lines[existing] = row
        return "updated"

    if section is None:
        artifacts = heading_range(lines, ARTIFACTS_HEADINGS)
        index = artifacts[1] if artifacts else len(lines)
        if index and lines[index - 1].strip():
            lines.insert(index, "\n")
            index += 1
        lines[index:index] = [LOG_HEADING + "\n", "\n", row, "\n"]
    else:
        start, index = section
        while index > start + 1 and not lines[index - 1].strip():
            index -= 1
        lines.insert(index, row)
    return "new"


def update_timestamp(lines, stamp):
    if not lines or lines[0].strip() != "---":
        raise ValueError("Task file must start with YAML frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip() == "---"), None)
    if end is None:
        raise ValueError("Task file has unclosed YAML frontmatter")
    index = next((i for i in range(1, end) if lines[i].startswith("stashed_at:")), end)
    lines[index:min(index + 1, end)] = [f"stashed_at: {stamp}\n"]


@contextmanager
def lock_task_directory(directory):
    fd = os.open(directory, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)


def save_task(path, stamp, reference, note):
    with lock_task_directory(path.parent):
        mode = path.lstat().st_mode
        if not stat.S_ISREG(mode):
            raise ValueError("Task file must be a regular file")
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        update_timestamp(lines, stamp)
        state = update_reference(lines, stamp, reference, note) if reference else "summary-only"
        descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as output:
                output.writelines(lines)
                os.fchmod(output.fileno(), stat.S_IMODE(mode))
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)
    return state


def record_reference(args):
    if args.append is not None and (
        args.task is None or not args.append.strip() or len(args.append.splitlines()) != 1
        or "\n" in args.append or "\r" in args.append
    ):
        raise ValueError("--append requires a task file and a one-line note")

    reference = session_reference(args.agent)
    warning = None
    if not reference or not SESSION_ID.fullmatch(reference.removeprefix("codex:")):
        warning = "Current session ID is unavailable"
    elif not session_logs(reference):
        warning = "Local session log is unavailable"
    if warning:
        if args.append is None:
            raise ValueError(warning)
        reference = None

    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if args.append is not None:
        state = save_task(args.task, stamp, reference, args.append)
    else:
        state = "new"
        if args.task and args.task.is_file():
            lines = args.task.read_text(encoding="utf-8").splitlines()
            if reference_row(lines, heading_range(lines, LOG_HEADINGS), reference) is not None:
                state = "exists"

    if warning:
        print(f"{warning}; saved without a session reference.", file=sys.stderr)
    print(stamp, reference or "-", state, sep="\t")



def tool_output(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def claude_rows(record, timeline):
    role = record.get("type")
    if role not in ("user", "assistant"):
        return
    if timeline and (role != "user" or record.get("isMeta")):
        return
    content = record.get("message", {}).get("content")
    if isinstance(content, str):
        yield role, content
        return
    if not isinstance(content, list):
        return
    if timeline:
        yield role, " ".join(block.get("text", "") for block in content if block["type"] == "text")
        return

    for block in content:
        kind = block.get("type")
        if kind == "text":
            yield role, block.get("text", "")
        elif kind == "thinking":
            yield role, f"[thinking] {block.get('thinking', '')}"
        elif kind == "tool_use":
            yield role, f"[tool:{block.get('name', '?')}] {tool_output(block.get('input'))}"
        elif kind == "tool_result":
            yield role, f"[result] {tool_output(block.get('content'))}"


def codex_rows(record, timeline):
    if record.get("type") != "response_item":
        return
    item = record.get("payload", {})
    kind = item.get("type")
    if kind == "message":
        role = item.get("role")
        if role == "user" or (role == "assistant" and not timeline):
            yield role, " ".join(
                block.get("text", "") for block in item.get("content", [])
                if block.get("type") in ("input_text", "output_text")
            )
    elif not timeline:
        if kind in ("function_call", "custom_tool_call", "local_shell_call"):
            name = item.get("name") or "shell"
            value = item.get("arguments", item.get("input", item.get("action")))
            yield "assistant", f"[tool:{name}] {tool_output(value)}"
        elif kind in ("function_call_output", "custom_tool_call_output", "mcp_tool_call_output"):
            yield "tool", f"[result] {tool_output(item.get('output'))}"


def read_rows(path, source, extract, timeline):
    with path.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                timestamp = record.get("timestamp")
                if not timestamp:
                    continue
                for role, value in extract(record, timeline):
                    text = " ".join(value.split())
                    if text:
                        instant = datetime.fromisoformat(timestamp)
                        if instant.tzinfo is None:
                            raise ValueError("Timestamp has no time zone")
                        yield instant, f"{role}@{source}", text
            except (AttributeError, KeyError, TypeError, ValueError) as error:
                raise ValueError(f"Cannot parse session log {path.name}, line {number}") from error


def find_session(args):
    if args.max < 0:
        raise ValueError("--max requires a nonnegative integer")
    logs = session_logs(args.reference)
    if not logs:
        raise ValueError("Session log not found")
    extract = codex_rows if args.reference.startswith("codex:") else claude_rows
    pattern = args.pattern.casefold() if args.pattern else None
    total = 0

    def matches():
        nonlocal total
        for path, source in logs:
            for instant, role, text in read_rows(path, source, extract, pattern is None):
                stamp = instant.astimezone(JST).strftime("%m-%d %H:%M")
                prefix = f"{stamp}\t{role}\t"
                if pattern is None or pattern in (prefix + text).casefold():
                    total += 1
                    yield instant, prefix + (text if args.full else text[:300])

    def timestamp(row):
        return row[0]

    if args.max:
        rows = heapq.nsmallest(args.max, matches(), key=timestamp)
    else:
        rows = sorted(matches(), key=timestamp)
    for _, row in rows:
        print(row)
    if total == 0:
        print("No matches.", file=sys.stderr)
    elif len(rows) < total:
        print(f"Showing {len(rows)} of {total} matches. Narrow the search or increase --max.",
              file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(prog="session.sh")
    commands = parser.add_subparsers(dest="command", required=True)
    ref = commands.add_parser("ref")
    ref.add_argument("task", nargs="?", type=Path)
    ref.add_argument("--agent", choices=("claude-code", "codex"))
    ref.add_argument("--append", metavar="NOTE")
    ref.set_defaults(run=record_reference)
    find = commands.add_parser("find")
    find.add_argument("reference")
    find.add_argument("pattern", nargs="?")
    find.add_argument("--full", action="store_true")
    find.add_argument("--max", type=int, default=50)
    find.set_defaults(run=find_session)
    args = parser.parse_args()
    try:
        args.run(args)
    except (OSError, ValueError) as error:
        print(f"stash: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
