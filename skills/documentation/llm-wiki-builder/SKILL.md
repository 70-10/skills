---
name: llm-wiki-builder
description: Create or revise a repository-local LLM wiki for AI agents, including its schema, maintenance skill, index and audit tools, and initial source ingestion. Use when asked to introduce projectcontext or orgcontext, preserve project history and assumptions for AI, or revisit an existing wiki's structure.
---

# LLM wiki builder

Build a source-backed knowledge store for facts that code and documents alone do not explain: why things work this way, what has been decided, and which assumptions still hold. Generate a local skill to maintain it after setup.

Create a `<kind>context/` bundle containing pages, `schema.yaml`, a generated `index.md`, and `tools/context.py`; a local maintenance skill; and a short entry in `CLAUDE.md` or `AGENTS.md`. Keep generated artifacts self-contained in the target repository, with no dependency on this installed builder or user-level paths.

## Language

This distributed skill is maintained in English. Its language does not determine the language of generated content.

Follow the user's explicit language instructions first, then the target repository's rules and existing documentation. Ask during design confirmation if those do not establish a clear choice. Apply that choice to wiki prose, titles, descriptions, aliases, required section headings, generated local skill instructions, and additions to agent guidance. Preserve existing language conventions when revising a bundle. Keep schema keys, machine identifiers, CLI commands, and filename conventions unchanged. English examples are illustrative; adapt them rather than imposing English on the target.

## Workflow

For a conceptual question about LLM wikis, answer without creating files. If a bundle and its maintenance skill already exist, use [Revising an existing bundle](#revising-an-existing-bundle).

### 1. Investigate

Read [principles](references/principles.md) and the [investigation checklist](references/workflow-details.md#investigation). Identify recurring questions, assumptions, source locations, existing knowledge stores, and language conventions. Do not create files yet. Ask about external sources rather than inventing their locations.

### 2. Select a kind

Use the [kind guide](references/context-kinds/README.md) to narrow the options, explain the evidence, and let the user choose. Use one kind per repository and read its definition after selection.

### 3. Design the schema

Follow [ontology design](references/ontology-design.md) and adapt the [example schema](assets/schema.example.yaml). Decide directories, types, required keys and sections, vocabularies, collections, sources, and person references. Express repository-specific choices in `schema.yaml`.

### 4. Confirm the design

Present the [design checklist](references/workflow-details.md#design-confirmation), including the chosen language, complete draft schema, and generated file paths. Obtain approval before generation; this is the design approval point.

### 5. Generate and validate

Follow [generated artifacts](references/generated-skill.md). Copy `scripts/context.py` unchanged into the bundle; configure it through the schema. Generate the local skill and agent guidance in the chosen language.

Run index then audit before adding pages; require zero FAIL findings. Initially list existing source files in `deferred`. Temporarily introduce invalid pages to verify the checks promised by the local skill, then remove them. Use an empty people collection with frontmatter if the schema requires it.

### 6. Ingest existing sources

Use the generated skill's authoring instructions to create pages. If those instructions cannot handle the sources, fix them first.

- Prioritize important sources when the volume is large. Remove ingested files from `deferred` and report the remainder.
- Do not add `verified`; it records human confirmation.
- Finish with index then audit and zero FAIL findings. Deferred-source warnings may remain.

### 7. Report

Use the [report checklist](references/workflow-details.md#report). Copy counts from `audit --report`, not a manual tally. Do not commit or push unless the user has explicitly requested it.

### 8. Assist human verification when requested

Ask a few concrete questions at a time about gaps, contradictions, or person identities. Record answers as sources before applying them. Add `verified` only for pages the user has explicitly confirmed and asked you to mark.

## Revising an existing bundle

Read its schema, maintenance skill, and `git log -- <kind>context/`. Propose changes using the same design confirmation checklist.

- Differences from this builder are not automatically defects; offer to preserve or align them.
- Include page migration and link updates when changing types or headings, including their language.
- If the bundle uses another tool, offer whether to replace it with `context.py`.
