# Choosing a context kind

The kind determines the bundle name, recurring questions, candidate types, and source inputs.

| Kind | Bundle | Subject | End | Changes | Definition |
| --- | --- | --- | --- | --- | --- |
| `project` | `projectcontext/` | An effort with goals and completion criteria | Yes | Work and discussions accumulate facts; decisions may be replaced | [project.md](project.md) |
| `org` | `orgcontext/` | Policies, rules, values, and practices | No | Formal revisions and gradual changes in practice | [org.md](org.md) |

## Selection criteria

- **Contents:** Minutes, requirements, and plans suggest project; policies and guidelines suggest org.
- **Completion:** A deadline or completion condition suggests project. Continuing rules suggest org.
- **Questions:** Decisions and ownership suggest project. Rationale and applicability of rules suggest org.

When evidence is weak, ask what questions the AI should answer, whether the effort has an end, and where facts come from.

## When neither fits

Start from the closest kind and record differences in the schema design. Propose adding a kind in the report; do not modify this builder's references during its execution.

## Kind definitions

Each definition covers subject, lifecycle, recurring questions, assumptions, source inputs, candidate types, authoritative sources, ingestion considerations, and common failures. Use the same structure for new kinds. Example questions and headings should be adapted to the target language.
