# Generated artifacts

```text
<repo>/
  CLAUDE.md                         # Or AGENTS.md: a short entry
  <kind>context/
    schema.yaml                     # Types, keys, vocabularies, required headings
    index.md                        # Generated; do not edit by hand
    tools/context.py                # Unchanged copy from this skill
    <dir>/<page>.md
  .claude/skills/<repo>-<kind>-context/
    SKILL.md                        # Reading and maintenance entrypoint
    references/authoring.md          # Detailed authoring procedure
```

Place the bundle directly under the repository root. The tool resolves source paths and inflow globs from the bundle's parent.

Use the target repository's existing local-skill convention; the tree above illustrates Claude Code. For Codex, use `.agents/skills/` and `AGENTS.md` where appropriate. Default the skill name to `<repository-directory-name>-<kind>-context` and check for a conflicting installed skill where the environment exposes one.

## Language and portability

Use the language established during design confirmation for wiki prose, metadata descriptions, aliases, required section names, the generated maintenance skill, and agent guidance. Preserve machine keys, identifiers, and commands. Adapt every example below and in the schema asset to that language. Keep the generated skill self-contained: do not link back to builder references that will be unavailable after cloning.

Create `schema.yaml` from the [example](../assets/schema.example.yaml), removing its first two builder-specific comments. Localize titles, descriptions, comments, and required headings before generating pages.

## context.py

Copy [scripts/context.py](../scripts/context.py) unchanged into the bundle's `tools/` directory. Express repository differences in `schema.yaml`.

```sh
uv run <kind>context/tools/context.py index
uv run <kind>context/tools/context.py audit
uv run <kind>context/tools/context.py audit --report
```

`uv` supplies PyYAML. Without it, use a maintained Python 3.11+ installation with PyYAML and run `python3 <kind>context/tools/context.py ...`. Record the chosen commands in the generated skill. The CLI exits 1 for FAIL findings and 2 for a broken schema; `--report` adds JSON counts and lists.

Audit findings to explain in the generated skill:

| Level | Code | Meaning |
| --- | --- | --- |
| FAIL | `frontmatter` | Unreadable frontmatter |
| FAIL | `missing-key`, `unknown-key` | Missing requirement or undeclared key |
| FAIL | `unknown-dir`, `unknown-type` | Directory or type not allowed by the schema |
| FAIL | `enum`, `date`, `filename` | Invalid vocabulary, date, or filename |
| FAIL | `source` | Source is not a mapping with nonempty string `kind` and `resource` |
| FAIL | `missing-section` | Required heading absent |
| FAIL | `broken-link` | Missing body-link, `related`, or source-file target |
| FAIL | `unknown-person`, `verified` | Invalid person reference or verification mark |
| FAIL | `supersede` | Missing reciprocal reference or inconsistent superseded status |
| FAIL | `alias-conflict` | A title or alias identifies multiple pages |
| FAIL | `inflow`, `index` | Unreferenced input or outdated index |
| WARN | `deferred` | Input intentionally postponed |
| WARN | `stale`, `long-body`, `orphan` | Review date passed, body too long, or page has no incoming link |

## Agent guidance entry

Keep it short and delegate detail to the maintenance skill. Adapt this English example to the target language and local skill invocation convention:

```markdown
## <kind>context

Repository assumptions, history, and decisions live in `<kind>context/`.
Use the `<repo>-<kind>-context` skill before answering or working, and use
its authoring workflow when new facts emerge from conversations or work.
```

Add two or three relevant examples of new facts, such as decisions and ownership changes.

## Maintenance skill: SKILL.md

Include reading and writing triggers in its description, expressed in the target language. Cover:

1. Purpose, the boundary with human-facing documents, and `schema.yaml` as the authority for types.
2. Directory, type, and update-protocol table; authoritative-source table from the approved design.
3. Reading: search index titles, aliases, and descriptions; read matching pages and follow one link when needed. Follow successors of superseded pages. Disclose unverified evidence. If the index lacks an answer, consult original sources and capture the resulting facts.
4. Authoring: link to the self-contained `references/authoring.md` generated below.
5. Autonomy: maintain supported facts in the chosen language within the approved schema. Propose schema changes; add verification marks only on explicit instruction. Update human-facing documents only when authorized by the agreed propagation policy.
6. Validation commands and how to resolve audit findings.

## Authoring reference

Generate `references/authoring.md` with:

1. **Deduplication:** Consult the index before adding a concept; update existing pages when appropriate.
2. **Placement:** Explain pages versus collections and exclusions: meetings themselves, facts owned by human-facing documents, and research gaps.
3. **Frontmatter templates:** Provide a usable template per type with localized headings and prose. Record the active model and skill as `<model>/<skill-name>` plus date in `generated`; leave the model placeholder unfilled in templates. Quote YAML values containing comment-sensitive text such as a space followed by `#`.
4. **Aliases:** Explain spelling variants, abbreviations, former names, external vocabulary, transcription errors, and conflict resolution.
5. **Type rules:** Adapt the selected kind's ingestion guidance to the approved schema.
6. **Evidence:** Choose source kinds, keep resource paths separate from locations, and cite both sides of contradictory evidence.
7. **Propagation:** For pages with `rendered_in`, apply the agreed policy for updates to human-facing documents.
8. **Completion:** Run index then audit, require zero FAIL findings, list postponed inputs in `deferred`, and report changes with a proposed commit message.

## History

Use `git log -- <kind>context/` and `git log --follow <kind>context/<dir>/<page>.md`. Do not generate a separate `log.md`. Proposed commit messages should describe meaningful fact or decision changes rather than listing incidental spelling edits.
