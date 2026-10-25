# Project context

## Subject and lifecycle

An effort with goals and completion criteria: work projects, personal products, research, or ongoing hobby development. Its context ends when the effort ends. Facts accumulate through work and discussion; decisions can be replaced. Suitable `stale_after` dates include deadlines, handovers, and scheduled reviews.

## Recurring questions

- What happened, what was decided, and why?
- Who owns this or can answer questions?
- What remains undecided?
- What does this term mean, and what does this component connect to?

## Assumptions to capture

Decision rationale, rejected alternatives, invalidating conditions and external constraints, terminology variants, ownership, and decision authority.

## Source inputs

Inside the repository: minutes, plans, requirements, Issues, PRs, and commits. Outside it: chats and user conversations; ask where to find them.

## Candidate types

| Update behavior | Candidates | Useful requirements |
| --- | --- | --- |
| Overwrite | Systems, components, terms, collected people | Upstream and downstream dependencies for components |
| Preserve with successor | Decisions | Decision, rationale and rejected alternatives, invalidating conditions; `decided_at`, `decided_by` |
| Status transition | Open questions, hypotheses | `status`, then `resolved_by` when settled |

Section names above are examples to express in the selected output language.

## Authoritative sources

| Fact | Authority |
| --- | --- |
| Statements and discussion history | Minutes, referenced through `sources` |
| Decisions, ownership, open questions, terminology | Wiki |
| Goals, schedule, risks | Plan or README |
| Tasks and progress | Issues; do not duplicate task tracking |

## Ingestion considerations

Start with README files and plans to establish systems, people, and terms; then process minutes chronologically.

Treat ambiguous statements as open questions. Wishes and proposals become decisions only with evidence of acceptance by the relevant people.

Classify each new decision's relationship to earlier ones:

- A previous conclusion no longer holds: use reciprocal supersession links.
- The previous conclusion still holds with additional scope or conditions: create a separate decision and use `related`.
- A planned experiment produces its result: use `related`; following the plan does not supersede it.

## Common failures

Copying summaries of minutes, duplicating task lists, and recording conclusions without their rationale.
