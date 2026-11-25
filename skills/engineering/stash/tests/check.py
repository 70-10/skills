import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


CLAUDE_ID = "71a4a200-1111-4444-8111-012345678901"
CODEX_ID = "019cc167-2222-7444-8222-012345678902"
LOG_HEADING = "## セッションログ"
SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


class StashTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.todos = self.root / ".claude/todos"
        self.todos.mkdir(parents=True)
        self.env = {
            key: value for key, value in os.environ.items()
            if key not in {
                "CLAUDE_CODE_SESSION_ID", "CLAUDE_SESSION_ID",
                "CODEX_THREAD_ID", "CODEX_SESSION_ID",
            }
        }
        self.env["STASH_PROJECTS_DIR"] = str(self.root / "claude-projects")
        self.env["CODEX_HOME"] = str(self.root / "codex")

    def invoke(self, script, *args, env=None):
        return subprocess.run(
            ["bash", str(SCRIPTS / script), *args],
            cwd=self.root, env=self.env | (env or {}), text=True,
            capture_output=True,
        )

    def task(self, name, frontmatter, body=""):
        path = self.todos / f"{name}.md"
        path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
        return path

    def log(self, relative_path, *records):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join(json.dumps(record) + "\n" for record in records), encoding="utf-8",
        )
        return path

    def test_list_orders_legacy_tasks_and_omits_inactive_tasks(self):
        self.assertEqual(self.invoke("list.sh").stdout, "(no stashed tasks)\n")
        self.task("older", "title: Legacy title\nstatus: blocked\nstashed_at: 2026-10-01")
        self.task("newer", "task: Current task\nstatus: paused\nstashed_at: 2026-11-01")
        self.task("popped", "task: Resumed\nstatus: popped")
        self.task("dropped", "task: Discarded\nstatus: dropped")
        result = self.invoke("list.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual([row.split()[1] for row in result.stdout.splitlines()],
                         ["SLUG", "newer", "older"])
        self.assertIn("Legacy title", result.stdout)


    def test_ref_appends_legacy_and_codex_refs_and_updates_only_the_matching_row(self):
        existing_ref = f"`{CLAUDE_ID}`"
        path = self.task(
            "task", "task: Carry over\nstatus: paused\nstashed_at: 2020-01-01",
            f"## 成果物\n- Mention of {existing_ref} outside the log\n\n## 注意点\n- Keep this\n",
        )
        self.log(f"claude-projects/project/{CLAUDE_ID}.jsonl")
        self.log(f"codex/sessions/2026/11/25/rollout-2026-11-25T10-00-00-{CODEX_ID}.jsonl")
        legacy_env = {"CLAUDE_SESSION_ID": CLAUDE_ID}
        self.assertTrue(self.invoke("session.sh", "ref", str(path),
                                    env=legacy_env).stdout.endswith("\tnew\n"))
        for agent, env, note, reference, state in (
            ("claude-code", legacy_env, "first session", CLAUDE_ID, "new"),
            ("codex", {"CODEX_THREAD_ID": CODEX_ID, "CODEX_SESSION_ID": CLAUDE_ID},
             "second session", f"codex:{CODEX_ID}", "new"),
            ("claude-code", legacy_env, r"literal \n and \t", CLAUDE_ID, "updated"),
        ):
            with self.subTest(agent=agent, state=state):
                result = self.invoke(
                    "session.sh", "ref", str(path), "--agent", agent, "--append", note, env=env,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                stamp, ref, actual_state = result.stdout.strip().split("\t")
                self.assertEqual((ref, actual_state), (reference, state))
                body = path.read_text(encoding="utf-8")
                self.assertIn(f"stashed_at: {stamp}\n", body)
                self.assertIn(f"- {stamp} `{reference}` — {note}\n", body)
        self.assertIn(f"Mention of {existing_ref} outside the log", body)
        self.assertNotIn("first session", body)
        self.assertIn("second session", body)
        self.assertLess(body.index("## 成果物"), body.index(LOG_HEADING))
        self.assertLess(body.index(LOG_HEADING), body.index("## 注意点"))

    def test_ref_saves_timestamp_without_local_session_log(self):
        for env in ({}, {"CODEX_SESSION_ID": CODEX_ID}):
            with self.subTest(env=env):
                path = self.task("offline", "task: Offline\nstatus: in-progress",
                                 "## 目的\nContinue without transcript.\n")
                result = self.invoke("session.sh", "ref", str(path), "--agent", "codex",
                                     "--append", "Offline", env=env)
                self.assertEqual(result.returncode, 0, result.stderr)
                stamp, ref, state = result.stdout.strip().split("\t")
                self.assertEqual((ref, state), ("-", "summary-only"))
                self.assertTrue(result.stderr.strip())
                body = path.read_text(encoding="utf-8")
                self.assertIn(f"stashed_at: {stamp}\n---", body)
                self.assertIn("Continue without transcript.", body)
                self.assertNotIn(LOG_HEADING, body)
        self.assertEqual(self.invoke("session.sh", "ref").returncode, 1)

    def test_ref_leaves_malformed_task_untouched(self):
        path = self.todos / "invalid.md"
        path.write_text("No frontmatter\n", encoding="utf-8")
        result = self.invoke("session.sh", "ref", str(path), "--append", "Summary")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(path.read_text(encoding="utf-8"), "No frontmatter\n")


    def test_find_merges_legacy_parent_and_subagent_timeline_and_tool_results(self):
        def event(second, role, content):
            return {
                "timestamp": f"2026-11-25T01:0{second}:00.000Z", "type": role,
                "message": {"content": content},
            }

        parent = self.log(f"claude-projects/project/{CLAUDE_ID}.jsonl",
                          event(1, "user", "First question"), event(3, "user", [
                              {"type": "tool_result", "content": "Status: Ready"},
                          ]), event(4, "user", "Last question"))
        child = self.log(f"claude-projects/project/{CLAUDE_ID}/subagents/agent-one.jsonl",
                         event(2, "user", [{"type": "text", "text": "Child question"}]))
        expected = [
            "11-25 10:01\tuser@main\tFirst question",
            "11-25 10:02\tuser@agent-one\tChild question",
            "11-25 10:04\tuser@main\tLast question",
        ]
        found = self.invoke("session.sh", "find", CLAUDE_ID)
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual(found.stdout.splitlines(), expected)
        found = self.invoke("session.sh", "find", CLAUDE_ID, "status: ready")
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertIn("[result] Status: Ready", found.stdout)
        parent.unlink()
        found = self.invoke("session.sh", "find", CLAUDE_ID)
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual(found.stdout.splitlines(), [expected[1]])
        self.assertTrue(child.is_file())

    def test_find_codex_archive_limits_output_and_searches_beyond_preview(self):
        def item(second, item_type, **content):
            return {
                "timestamp": f"2026-11-25T01:00:{second:02}.000Z", "type": "response_item",
                "payload": {"type": item_type, **content},
            }

        long_text = "長" * 305 + " literal[needle]"
        self.log(f"codex/archived_sessions/rollout-2026-11-25T10-00-00-{CODEX_ID}.jsonl",
                 {"type": "session_meta", "payload": {"id": CODEX_ID}},
                 item(0, "message", role="user", content=[{"type": "input_text", "text": long_text}]),
                 item(1, "message", role="assistant",
                      content=[{"type": "output_text", "text": "literal[needle] reply"}]),
                 item(2, "function_call", name="exec_command", arguments='{"cmd":"git status"}'),
                 item(3, "function_call_output", output="litERAL[NEEDLE] output"),
                 item(4, "message", role="developer",
                      content=[{"type": "input_text", "text": "literal[needle] developer"}]),
                 item(5, "custom_tool_call", name="apply_patch", input="literal[needle] patch"),
                 item(6, "custom_tool_call_output", output="literal[needle] applied"),
                 item(7, "event_msg", message=long_text))
        reference = f"codex:{CODEX_ID}"
        timeline = self.invoke("session.sh", "find", reference)
        self.assertEqual(timeline.returncode, 0, timeline.stderr)
        self.assertEqual(timeline.stdout.splitlines(), [f"11-25 10:00\tuser@main\t{'長' * 300}"])

        found = self.invoke("session.sh", "find", reference, "literal[needle]", "--max", "0", "--full")
        self.assertEqual(found.returncode, 0, found.stderr)
        self.assertEqual([line.split("\t", 2)[2] for line in found.stdout.splitlines()], [
            long_text, "literal[needle] reply", "[result] litERAL[NEEDLE] output",
            "[tool:apply_patch] literal[needle] patch", "[result] literal[needle] applied",
        ])
        preview = self.invoke("session.sh", "find", reference, "literal[needle]", "--max", "1")
        self.assertEqual(preview.stdout, timeline.stdout)
        self.assertIn("1 of 5", preview.stderr)
        command = self.invoke("session.sh", "find", reference, "git status")
        self.assertIn("[tool:exec_command]", command.stdout)

    def test_find_distinguishes_no_matches_from_missing_and_malformed_logs(self):
        reference = f"codex:{CODEX_ID}"
        absent = self.invoke("session.sh", "find", reference)
        self.assertEqual(absent.returncode, 1)
        self.assertIn("not found", absent.stderr)
        path = self.log(f"codex/sessions/2026/11/25/rollout-2026-11-25T10-00-00-{CODEX_ID}.jsonl",
                        {"type": "response_item", "timestamp": "2026-11-25T01:00:00Z",
                         "payload": {"type": "message", "role": "user",
                                     "content": [{"type": "input_text", "text": "Question"}]}})
        empty = self.invoke("session.sh", "find", reference, "not present")
        self.assertEqual((empty.returncode, empty.stdout), (0, ""))
        self.assertIn("No matches", empty.stderr)
        with path.open("a", encoding="utf-8") as log:
            log.write('{"type": "response_item"\n')
        broken = self.invoke("session.sh", "find", reference)
        self.assertEqual((broken.returncode, broken.stdout), (1, ""))
        self.assertIn("Cannot parse", broken.stderr)
        self.assertNotEqual(self.invoke("session.sh", "find", reference, "--max", "-1").returncode, 0)
        self.assertNotEqual(self.invoke("session.sh", "find", "../bad").returncode, 0)


if __name__ == "__main__":
    unittest.main()
