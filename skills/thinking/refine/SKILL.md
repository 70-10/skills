---
name: refine
description: Use to refine a GitHub Issue so a subsequent agent can autonomously investigate, design, implement, and verify the work while escalating only decisions that materially affect the required outcome or safety of execution.
---

Turn one identifiable GitHub Issue for repository-contained work into a self-contained issue body that a subsequent agent can use to autonomously investigate, design, implement, and verify the work without access to the conversation history. Do not implement the issue.

Read the issue body, comments, linked material, and relevant repository content before asking questions. Resolve facts through investigation. Ask the user only about material decisions: those that change the requirement or expected outcome, affect the scope, compatibility, or externally observable behavior, or commit to an action that is irreversible or costly to recover from. Ask one question at a time and wait for each answer.

Leave every other decision to the subsequent agent, and do not require implementation details to be settled merely because multiple valid approaches exist. Unresolved information does not block refinement when the subsequent agent can investigate or decide it from the repository; record every such point in the issue body so that a delegated decision cannot be mistaken for an oversight.

The revised issue body must convey:

- The purpose, background, and expected outcome
- The scope and constraints
- Objective completion criteria and verification methods
- Decisions intentionally delegated to the subsequent agent
- Conditions under which execution must stop and ask for clarification
- Implementation direction, only when needed to preserve an agreed decision

Make every completion criterion objectively judgeable, and include concrete test, lint, type-check, or other commands when they can be established from the repository. When the verification procedure cannot be determined without implementation work, state the observable expected result and leave only the procedure to the subsequent agent. When verification cannot be automated, give specific manual steps and expected results.

Do not invent requirements, outcomes, constraints, or agreed decisions. Preserve useful source information while restructuring the full issue body. Surface contradictions and obsolete requirements instead of silently choosing between them.

The issue body is ready to present when the expected outcome and important constraints are clear, every material decision has been resolved, the boundary between delegated decisions and conditions requiring escalation is clear, and the subsequent agent can begin investigation and implementation autonomously.

Present the complete proposed issue body and obtain explicit approval. After approval, replace the GitHub Issue body using the available GitHub tooling and report the updated issue. Do not change the title, labels, or other issue metadata.

If the target issue cannot be identified, ask for it once. If a material decision cannot be resolved, state what is missing, ask the next required question, and leave the issue unchanged.

Do not search for other candidate issues, add readiness markers, or handle work whose outcome depends on external operations or unresolved stakeholder coordination.
