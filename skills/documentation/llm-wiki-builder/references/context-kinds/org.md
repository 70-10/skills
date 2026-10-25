# Organizational context

## Subject and lifecycle

Policies, rules, values, and practices for organizations, teams, individuals, families, or small groups. There is no completion event. Formal revisions replace rules; practices evolve gradually. Suitable `stale_after` dates include revisions, effective dates, and scheduled reviews.

## Recurring questions

- Why does this rule exist, and what does it protect?
- Does it apply here, and is there a relevant precedent?
- Which practices are unwritten?
- Who can interpret or revise the rule?

## Assumptions to capture

Intent and applicability boundaries, previous interpretations and their reasoning, the distinction between practice and formal policy, and revision authority or contacts.

## Source inputs

Inside the repository: regulations, guidelines, policies, and revisions. Outside it: consultations and conversations; ask where to find them.

## Candidate types

| Update behavior | Candidates | Useful requirements |
| --- | --- | --- |
| Overwrite | Principles and values | Priorities and background sections |
| Overwrite | Background of individual policy sections | Link to the section, intent and applicability sections |
| Overwrite | Practices | Explicit indication that they are informal; scope of observed practice |
| Preserve with successor | Interpretations and precedents | Question, judgment, and rationale sections; `decided_at`, `decided_by` |
| Overwrite, collected | Terms and contacts | As needed |

Section names above are examples to express in the selected output language.

## Authoritative sources

| Fact | Authority |
| --- | --- |
| Policy wording | Original document; wiki links to the relevant section |
| Revision history | Git or document revision table |
| Rationale, intent, scope, precedents | Wiki |
| Unwritten practices | Wiki; replace with a link when formalized elsewhere |

## Ingestion considerations

Start from the policy table of contents to create background pages by section, then extract precedents from consultation records. Distinguish documented rules from practices without a formal source. After a policy revision, review pages citing the affected sections to see whether their rationale and precedents still apply.

## Common failures

Copying policy text that then drifts from the original, or presenting informal practices as formal rules.
