# LLM wiki principles

The wiki serves AI agents alongside human-facing documents such as README files. Use one Markdown page per concept, YAML frontmatter for type, title, description, and sources, and relative links between pages.

These principles are defaults. Adapt them to the target repository and explain departures in schema comments.

## Structure

- **Organize by update behavior.** Mutable facts, decisions preserved through successors, and evolving questions need different authoring rules and checks.
- **Keep the page count useful.** Group people and short terms without independent status, successors, or sources under `## <id>` headings in collection files.
- **Generate the index.** Rebuild `index.md` from frontmatter with `context.py index`.
- **Close the type vocabulary.** New types require an explicit schema change.
- **Use lowercase ASCII letters, digits, and hyphens in page basenames.** Keep names in the target language in `title` and `aliases`.

## Authoring

- **Link instead of copying long explanations.** Keep the source summary to one `description` line; copied minutes and policy text drift from their originals.
- **Make facts discoverable.** Record abbreviations, former names, external terminology, and spelling variants as aliases. Conflicting names fail audit.
- **Distinguish AI authoring from human review.** AI writes `generated`; add `verified` only when a person has confirmed the page and requested the mark.
- **Preserve decisions.** Mark replaced decisions `superseded` and connect old and new pages with reciprocal `superseded_by` and `supersedes` references.
- **Require what a handover would lose.** Capture reasons, rejected alternatives, and conditions that invalidate decisions.
- **Use actual dates for `stale_after`.** Deadlines, handovers, and scheduled reviews are useful; arbitrary expiry dates are not.
- **Respect existing authoritative sources.** Summarize and link facts owned elsewhere.

## Maintenance

- **Audit ingestion coverage.** Unreferenced source files fail audit. Intentionally postponed sources belong in `deferred` and produce warnings.
- **Capture sources used to answer questions.** When an answer requires material absent from the index, create the corresponding page as part of the authorized maintenance work.
- **Separate open decisions from research gaps.** Stakeholder questions belong in the wiki; gaps in the agent's understanding belong in Issues or the report.
- **Use Git for history.** Use `git log -- <kind>context/` and `git log --follow <file>`, not a separate `log.md`.
