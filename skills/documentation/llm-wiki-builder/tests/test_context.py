import datetime as dt
import importlib.util
import re
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "scripts" / "context.py"
FIXTURE = HERE / "fixtures" / "ok"
TODAY = dt.date(2026, 2, 1)


def load_module():
    spec = importlib.util.spec_from_file_location("context", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


ctx = load_module()


def reindex(wiki):
    (wiki / "index.md").write_text(ctx.build_index(ctx.load(wiki)), encoding="utf-8")


def findings(wiki, reindex_first=True):
    if reindex_first:
        reindex(wiki)
    return ctx.audit(ctx.load(wiki), today=TODAY)


def codes(wiki, level=None, reindex_first=True):
    return {f.code for f in findings(wiki, reindex_first) if level is None or f.level == level}


def edit(path, old, new):
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} not in {path}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


@pytest.fixture
def repo(tmp_path):
    dst = tmp_path / "repo"
    shutil.copytree(FIXTURE, dst)
    reindex(dst / "wiki")
    return dst


@pytest.fixture
def wiki(repo):
    return repo / "wiki"


def add_stream(wiki):
    """A second decision that can replace adopt-queue.md."""
    new = wiki / "decisions" / "adopt-stream.md"
    shutil.copy(wiki / "decisions" / "adopt-queue.md", new)
    edit(new, "title: Adopt a queue", "title: Adopt a stream")
    return new


# ---- index


def test_index_lists_every_page(wiki):
    index = (wiki / "index.md").read_text(encoding="utf-8")
    assert index.startswith(ctx.INDEX_MARK)
    assert "# Example wiki" in index
    rows = re.findall(r"^\| \[([^\]]+)\]", index, flags=re.MULTILINE)
    assert rows == ["decisions/adopt-queue.md", "entities/system-a.md", "people.md"]
    assert ("| [entities/system-a.md](entities/system-a.md) | system | System A | billing "
            "| The billing system that the project connects to. |") in index


def test_index_is_stable(wiki):
    assert ctx.build_index(ctx.load(wiki)) == (wiki / "index.md").read_text(encoding="utf-8")


def test_index_out_of_date_fails(wiki):
    edit(wiki / "entities" / "system-a.md", "title: System A", "title: System A2")
    assert "index" in codes(wiki, "FAIL", reindex_first=False)


# ---- CLI


def test_cli_exit_codes(wiki, capsys):
    assert ctx.main(["--root", str(wiki), "audit"]) == 0
    edit(wiki / "entities" / "system-a.md", "type: system", "type: robot")
    reindex(wiki)
    assert ctx.main(["--root", str(wiki), "audit"]) == 1
    out = capsys.readouterr().out
    assert "FAIL" in out and "unknown-type" in out


def test_cli_index_writes_the_file(wiki):
    (wiki / "index.md").unlink()
    assert ctx.main(["--root", str(wiki), "index"]) == 0
    assert (wiki / "index.md").read_text(encoding="utf-8") == ctx.build_index(ctx.load(wiki))


# ---- FAIL: the valid bundle passes, and one broken spot fails


def test_valid_bundle_has_no_findings(wiki):
    assert findings(wiki) == []


BROKEN = [
    # (code, file, old, new)
    ("frontmatter", "entities/system-a.md", "---\ntype: system", "type: system"),
    ("missing-key", "entities/system-a.md", "description: The billing system that the project connects to.\n", ""),
    ("missing-key", "decisions/adopt-queue.md", "decided_at: 2026-01-05\n", ""),
    ("unknown-type", "entities/system-a.md", "type: system", "type: decision"),
    ("unknown-key", "entities/system-a.md", "aliases: [billing]", "owner: alice"),
    ("enum", "decisions/adopt-queue.md", "status: active", "status: maybe"),
    ("date", "decisions/adopt-queue.md", "decided_at: 2026-01-05", "decided_at: 2026-02-30"),
    ("date", "decisions/adopt-queue.md", "decided_at: 2026-01-05", "decided_at: last week"),
    ("broken-link", "entities/system-a.md", "../decisions/adopt-queue.md", "../decisions/missing.md"),
    ("broken-link", "entities/system-a.md", "resource: meeting-minutes/2026-01-05.md",
     "resource: meeting-minutes/2026-01-55.md"),
    ("missing-section", "decisions/adopt-queue.md", "## Context", "## Background"),
    ("unknown-person", "decisions/adopt-queue.md", "[human:alice]", "[human:carol]"),
    ("unknown-person", "decisions/adopt-queue.md", "[human:alice]", "[alcie]"),
    ("unknown-person", "decisions/adopt-queue.md", "by: human:bob", "by: human:dave"),
    ("verified", "decisions/adopt-queue.md", "verified: {by: human:bob, at: 2026-01-06}", "verified: true"),
    ("alias-conflict", "decisions/adopt-queue.md", "title: Adopt a queue", "title: Adopt a queue\naliases: [billing]"),
    ("alias-conflict", "decisions/adopt-queue.md", "title: Adopt a queue", "title: Adopt a queue\naliases: [System A]"),
]


@pytest.mark.parametrize("code,file,old,new", BROKEN, ids=[f"{b[0]}:{b[1]}:{b[3][:15]}" for b in BROKEN])
def test_each_check_fails(wiki, code, file, old, new):
    edit(wiki / file, old, new)
    assert code in codes(wiki, "FAIL")


def test_filename_rule(wiki):
    (wiki / "entities" / "system-a.md").rename(wiki / "entities" / "System_A.md")
    edit(wiki / "decisions" / "adopt-queue.md", "../entities/system-a.md", "../entities/System_A.md")
    assert "filename" in codes(wiki, "FAIL")


def test_page_outside_the_schema_directories(wiki):
    (wiki / "misc").mkdir()
    shutil.copy(wiki / "entities" / "system-a.md", wiki / "misc" / "note.md")
    assert "unknown-dir" in codes(wiki, "FAIL")


def test_source_kind_outside_the_vocabulary_fails(wiki):
    edit(wiki / "schema.yaml", "max_body_lines: 40", "max_body_lines: 40\nsource_kinds: [minutes, doc]")
    assert findings(wiki) == []
    edit(wiki / "entities" / "system-a.md", "{kind: minutes,", "{kind: rumor,")
    assert "enum" in codes(wiki, "FAIL")


def test_type_enum_overrides_the_common_enum(wiki):
    edit(wiki / "schema.yaml", "    sections: [Context, Decision]",
         "    sections: [Context, Decision]\n    enums: {status: [active, superseded, draft]}")
    edit(wiki / "decisions" / "adopt-queue.md", "status: active", "status: draft")
    assert "enum" not in codes(wiki)


def test_verified_must_name_a_person_and_a_date(wiki):
    edit(wiki / "decisions" / "adopt-queue.md", "verified: {by: human:bob, at: 2026-01-06}", "verified: true")
    reindex(wiki)
    assert "decisions/adopt-queue.md" in ctx.report(ctx.load(wiki))["unverified"]


# ---- FAIL: supersede


def test_supersede_needs_both_sides(wiki):
    new = add_stream(wiki)
    edit(wiki / "decisions" / "adopt-queue.md", "status: active", "status: superseded\nsuperseded_by: adopt-stream.md")
    assert "supersede" in codes(wiki, "FAIL")
    edit(new, "status: active", "status: active\nsupersedes: adopt-queue.md")
    assert "supersede" not in codes(wiki)


def test_supersedes_alone_is_one_side(wiki):
    new = add_stream(wiki)
    edit(new, "status: active", "status: active\nsupersedes: adopt-queue.md")
    assert "supersede" in codes(wiki, "FAIL")


def test_superseded_page_must_say_so_in_status(wiki):
    new = add_stream(wiki)
    edit(new, "status: active", "status: active\nsupersedes: adopt-queue.md")
    edit(wiki / "decisions" / "adopt-queue.md", "status: active", "status: active\nsuperseded_by: adopt-stream.md")
    assert "supersede" in codes(wiki, "FAIL")


def test_supersede_path_from_the_repository_root(wiki):
    new = add_stream(wiki)
    edit(new, "status: active", "status: active\nsupersedes: /wiki/decisions/adopt-queue.md")
    edit(wiki / "decisions" / "adopt-queue.md", "status: active",
         "status: superseded\nsuperseded_by: /wiki/decisions/adopt-stream.md")
    assert "supersede" not in codes(wiki)


# ---- links


def test_related_counts_as_a_link(wiki):
    edit(wiki / "schema.yaml", "rendered_in]", "rendered_in, related]")
    edit(wiki / "decisions" / "adopt-queue.md", "[System A](../entities/system-a.md)", "System A")
    edit(wiki / "decisions" / "adopt-queue.md", "status: active", "status: active\nrelated: [../entities/system-a.md]")
    assert "orphan" not in codes(wiki)
    edit(wiki / "decisions" / "adopt-queue.md", "related: [../entities/system-a.md]", "related: [../entities/nope.md]")
    assert "broken-link" in codes(wiki, "FAIL")


def test_links_inside_code_are_ignored(wiki):
    edit(wiki / "entities" / "system-a.md", "System A sends invoices.",
         "System A sends invoices.\n\n```markdown\n[x](nope.md)\n```\n\nWrite `[y](nope2.md)` like this.")
    assert "broken-link" not in codes(wiki)


def test_leading_slash_link_starts_at_the_repository_root(wiki):
    edit(wiki / "entities" / "system-a.md", "System A sends invoices.",
         "System A sends invoices ([minutes](/meeting-minutes/2026-01-05.md)).")
    assert "broken-link" not in codes(wiki)


def test_source_that_is_not_a_file_is_not_checked(wiki):
    edit(wiki / "entities" / "system-a.md", "  - {kind: minutes, resource: meeting-minutes/2026-01-05.md}",
         "  - {kind: minutes, resource: meeting-minutes/2026-01-05.md}\n"
         "  - {kind: conversation, resource: 'conversation:2026-01-06'}")
    assert findings(wiki) == []


def test_crlf_page_is_readable(wiki):
    p = wiki / "entities" / "system-a.md"
    p.write_bytes(p.read_bytes().replace(b"\n", b"\r\n"))
    assert "frontmatter" not in codes(wiki)


# ---- inflows


def test_inflow_not_referenced_is_a_miss(repo, wiki):
    (repo / "meeting-minutes" / "2026-01-12.md").write_text("# 2026-01-12\n", encoding="utf-8")
    assert "inflow" in codes(wiki, "FAIL")


def test_inflow_referenced_by_a_body_link_counts(repo, wiki):
    (repo / "meeting-minutes" / "2026-01-12.md").write_text("# 2026-01-12\n", encoding="utf-8")
    edit(wiki / "entities" / "system-a.md", "System A sends invoices.",
         "System A sends invoices ([minutes](../../meeting-minutes/2026-01-12.md)).")
    assert "inflow" not in codes(wiki)


def test_percent_encoded_link_is_decoded(repo, wiki):
    (repo / "meeting-minutes" / "2026-01-12 weekly.md").write_text("# weekly\n", encoding="utf-8")
    edit(wiki / "entities" / "system-a.md", "System A sends invoices.",
         "System A sends invoices ([weekly](../../meeting-minutes/2026-01-12%20weekly.md)).")
    assert not {"broken-link", "inflow"} & codes(wiki)


def test_deferred_inflow_is_a_warning_not_a_fail(repo, wiki):
    (repo / "meeting-minutes" / "2026-01-12.md").write_text("# 2026-01-12\n", encoding="utf-8")
    edit(wiki / "schema.yaml", "max_body_lines: 40", "max_body_lines: 40\ndeferred: ['meeting-minutes/2026-01-12.md']")
    assert "inflow" not in codes(wiki, "FAIL")
    assert "deferred" in codes(wiki, "WARN")


# ---- WARN


def test_stale_after_passed_is_a_warning(wiki):
    edit(wiki / "entities" / "system-a.md", "aliases: [billing]", "aliases: [billing]\nstale_after: 2026-01-15")
    assert "stale" in codes(wiki, "WARN")
    assert "stale" not in codes(wiki, "FAIL")


def test_long_body_is_a_warning(wiki):
    edit(wiki / "entities" / "system-a.md", "System A sends invoices.", "System A sends invoices.\n" + "line\n" * 50)
    assert "long-body" in codes(wiki, "WARN")


def test_orphan_page_is_a_warning(wiki):
    edit(wiki / "decisions" / "adopt-queue.md", "[System A](../entities/system-a.md)", "System A")
    assert "orphan" in codes(wiki, "WARN")


# ---- report


def test_report_counts_by_type_and_lists_unverified(wiki):
    report = ctx.report(ctx.load(wiki))
    assert report["counts"] == {"decision": 1, "person": 1, "system": 1}
    assert report["unverified"] == ["entities/system-a.md", "people.md"]
    assert report["superseded"] == []


# ---- schema errors stop the run


SCHEMA_ERRORS = [
    ("kind: project", "kind: project\nfolders: {}"),
    ("people: people.md\n", ""),
    ("    sections: [Context, Decision]", "    section: [Context, Decision]"),
    ("  status: [active, superseded]", "  status: active"),
    ("{types: [decision], protocol: append-only}", "{types: decision, protocol: append-only}"),
    ("date_keys: [decided_at, stale_after]", "date_keys: decided_at"),
]


@pytest.mark.parametrize("old,new", SCHEMA_ERRORS, ids=[e[1][:25] or "no-people" for e in SCHEMA_ERRORS])
def test_broken_schema_is_rejected(wiki, old, new):
    edit(wiki / "schema.yaml", old, new)
    with pytest.raises(ctx.SchemaError):
        ctx.load(wiki)
    assert ctx.main(["--root", str(wiki), "audit"]) == 2
