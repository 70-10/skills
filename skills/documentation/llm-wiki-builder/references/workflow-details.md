# Workflow checklists

Use these with the corresponding steps in [SKILL.md](../SKILL.md).

## Investigation

- Check the branch and uncommitted changes. Resolve any branch choice during design confirmation if other work is in progress.
- Read README files, minutes, plans, policies, code, agent guidance, local skills, and rules. Find the actual location of human-facing documents.
- Identify recurring questions, implicit assumptions, and evidence for the [context kind](context-kinds/README.md).
- Establish the output language from explicit user instructions, then repository rules and existing documents. Ask if unclear.
- Locate source inputs and any workflows that produce them. Ask about external locations; offer workflow integration during design confirmation.
- Identify overlapping knowledge stores and external dependencies; decide which source owns each fact during schema design.
- Check for `uv`, or Python 3.11+ with PyYAML, to run `context.py`.

Do not collect personnel evaluations or other HR-sensitive information.

## Design confirmation

Present these together before generation:

- Kind and rationale, including departures from its definition.
- Output language and the conventions supporting it.
- Directory, type, and update-protocol table; required and optional keys and sections.
- Authoritative-source table and the policy for overlap with human-facing documents.
- Complete draft `schema.yaml`, with prose and required headings adapted to the selected language.
- Generated paths: bundle, tool, maintenance skill, and additions to agent guidance.
- Runtime choice: `uv`, or Python with PyYAML. Record the commands in the local skill; keep the agent-guidance entry short.
- Proposed integrations with existing source-producing workflows.
- Sources to ingest now and those to defer.
- Working branch, if investigation identified a choice to resolve.

## Report

- List generated files and summarize the kind, language, and schema. Explain departures from the approved design.
- Copy per-type page counts from `audit --report`.
- List deferred sources, how to request their ingestion, and remaining audit warnings.
- Explain human verification and how to request `verified` marks.
- Report the branch and suggest a commit message and next steps for commit or PR creation, respecting any existing authorization.
- If no kind fit, propose a new kind definition.
- State how many questions need human confirmation and offer the optional verification step.
