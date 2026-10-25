# Schema design

Design types for the target repository. Kind definitions and the [example schema](../assets/schema.example.yaml) are starting points. Store configuration in the keys below; unknown keys and invalid schema structure stop `context.py` with exit code 2.

## 1. Questions to answer

Combine the kind's recurring questions with those found during investigation. Adjust types until each question has an identifiable page to consult, or establish that it belongs outside the wiki.

## 2. Directories and types: `dirs`

Group by [update behavior](principles.md#structure). `protocol` documents authoring behavior; the script does not enforce it.

| Protocol | Behavior | Examples |
| --- | --- | --- |
| `overwrite` | Update the page in place | Systems, terms |
| `append-only` | Preserve the page and create a successor when replaced | Decisions, precedents |
| `status` | Advance status and link to the result when resolved | Open questions |

A top-level directory can hold multiple types, such as `types: [system, term]`. Pages outside listed directories fail `unknown-dir`; types not allowed in their directory fail `unknown-type`.

## 3. Pages or collections: `collections`, `people`

Group entries without their own status, successors, or sources into collection files.

- Map bundle-relative paths to a type in `collections`; files may live outside the listed directories.
- Collections need frontmatter, common required keys, and the declared type.
- Write entries as `## <id> <heading remainder>`, separating the first token from the remainder with a space.
- Collections are exempt from orphan warnings.
- Set `people` to the people collection; its heading IDs define valid `human:<id>` references.

## 4. Metadata

- **Common requirements:** Put `type`, `title`, `description`, and `sources` in `common.required`.
- **Optional keys:** Declare aliases, tags, generation and verification metadata, status, supersession, `related`, and `rendered_in` in `common.optional` or `types.<type>.optional`. Undeclared keys fail audit.
- **Type requirements:** Use `types.<type>.required` for facts that would otherwise be lost during handover.
- **Vocabularies:** `types.<type>.enums` overrides entries with the same key in global `enums`.
- **Dates:** Keys in `date_keys` must be real `YYYY-MM-DD` dates.
- **Verification:** `verified` must be `{by: human:<id>, at: YYYY-MM-DD}`. Malformed marks count as unverified in reports.
- **People:** Values in `person_keys` and `verified.by` use `human:<id>` and, when `people` is configured, must appear there. Configuring `person_keys` requires `people`. Use short stable alphanumeric IDs, such as account names.
- **Page references:** Body links, `related`, `superseded_by`, and `supersedes` are page-relative. Leading `/` starts at the repository root. Body links and `related` contribute to broken-link and orphan checks; links in code are ignored.

### Sources

Each page needs at least one source with `{kind, resource}`.

- Use a repository-relative file path or URL as `resource`. Keep locations such as line numbers in a separate key, for example `at`; ingestion coverage compares paths.
- Choose kinds appropriate to the context and list them in `source_kinds` to reject unknown values.
- Conversation evidence can use `kind: conversation` and `resource: conversation:YYYY-MM-DD`.
- Ask for confirmation instead of creating facts supported only by guesses.

## 5. Required sections: `types.<type>.sections`

Audit requires each configured `## <heading>`. Choose two to four sections that capture what a handover would lose. Write section names in the target language and use the same names in page templates; do not copy English headings into a repository that uses another language.

## 6. Filenames and length: `filename`, `max_body_lines`

Choose a basename regex and a body line limit. Exceeding the limit warns that a page may need links instead of copied detail.

## 7. Ingestion coverage: `inflows`, `deferred`

List repository-relative input globs, such as `meeting-minutes/*.md`, in `inflows`. A file not cited by `sources[].resource`, a body link, or `related` fails `inflow`.

- Put postponed files or globs in `deferred` to produce warnings instead of failures. Remove entries after ingestion; referenced files stop warning automatically.
- Exclude sources with no ingestion value from `inflows`, rather than deferring them indefinitely.

## 8. Authoritative sources

Define a table in the generated maintenance skill stating whether each fact belongs in the wiki, an original document, an Issue, or an external source. Resolve overlap with human-facing documents. If the wiki owns a fact rendered elsewhere, use `rendered_in` to identify the destination section and explicitly agree how updates propagate.

## 9. Research gaps

Do not mix gaps in the agent's understanding with stakeholder decisions. Track research gaps in Issues when available, otherwise report them to the user.

## Common design failures

Overly detailed topic directories that mix update protocols; one page per person or short term; excessive requirements that invite guessed values; arbitrary `stale_after` dates.
