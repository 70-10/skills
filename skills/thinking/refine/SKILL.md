---
name: refine
description: Use to refine a GitHub Issue so a subsequent agent can autonomously investigate, design, implement, and verify the work while escalating only decisions that materially affect the required outcome or safety of execution.
---

Turn one identifiable GitHub Issue for repository-contained work into a self-contained issue body that a subsequent agent can use to autonomously investigate, design, implement, and verify the work without access to the conversation history. Do not implement the issue.

Read the issue body, comments, linked material, and relevant repository content before asking questions. Resolve facts through investigation. Ask the user only about material decisions: those that change the requirement or expected outcome, affect the scope, compatibility, or externally observable behavior, or commit to an action that is irreversible or costly to recover from. Ask one question at a time and wait for each answer.

Leave every other decision to the subsequent agent, and do not require implementation details to be settled merely because multiple valid approaches exist. Unresolved information does not block refinement when the subsequent agent can investigate or decide it from the repository; record every such point in the issue body so that a delegated decision cannot be mistaken for an oversight.

Before presenting the body, inventory all decisions left to the subsequent agent across investigation, design, implementation, and verification. Explicitly enumerate them in the body, including the scope and limits of each delegation. Cover routine implementation choices without requiring their details to be settled. State in the body that an unlisted decision is not delegated: the subsequent agent must stop and ask for clarification before deciding it. Check for omissions so that this fallback does not turn routine choices into unnecessary escalations. Omissions include behavior the body leaves unspecified and effects of the change that the body does not mention. Resolve each one as a material decision, an explicit delegation, or stated behavior to expect.

The revised issue body must convey:

- The purpose, background, and expected outcome
- The scope and constraints
- Objective completion criteria and verification methods
- Decisions intentionally delegated to the subsequent agent
- Conditions under which execution must stop and ask for clarification
- Implementation direction, only when needed to preserve an agreed decision

Place the completion criteria, the delegated decisions, and the stop conditions where each can be located on its own, without reading the surrounding prose; a subsequent agent returns to these three while executing.

Make every completion criterion objectively judgeable, and include concrete test, lint, type-check, or other commands when they can be established from the repository. When the verification procedure cannot be determined without implementation work, state the observable expected result and leave only the procedure to the subsequent agent. When verification cannot be automated, give specific manual steps and expected results.

A completion criterion that expresses the required outcome must not already hold in the current state; one the repository already satisfies before any work is done does not separate the current state from the finished one, so strengthen it until it does. This does not apply to a criterion that states behavior which must not regress. Where a criterion depends on a starting state, state that starting state in the body.

For each decision that defines the required outcome or a constraint, reverse it and check that at least one completion criterion would fail. If all criteria still pass, add or strengthen a criterion and its verification method to distinguish the agreed behavior from its opposite, including relevant edge cases. Keep delegated implementation choices open when either alternative satisfies the required outcome and constraints.

Write every stop condition as an observable trigger the subsequent agent can evaluate without a person present. Pair each trigger with the kind of reason for stopping, such as an undelegated decision, conflicting requirements, a compatibility change outside the agreed scope, or an irreversible action outside the agreed authorization. Specify the evidence or state that triggers the stop rather than relying on someone to notice a problem during execution.

Do not invent requirements, outcomes, constraints, or agreed decisions. State facts established by inspecting the repository together with the point at which they were observed. Do not present the expected result of other work as an established fact; record it as a dependency on that work. Preserve useful source information while restructuring the full issue body. Surface contradictions and obsolete requirements instead of silently choosing between them.

The issue body is ready to present when the expected outcome and important constraints are clear, every material decision has been resolved, the boundary between delegated decisions and conditions requiring escalation is clear, and the subsequent agent can begin investigation and implementation autonomously.

Present the complete proposed issue body and obtain explicit approval. After approval, replace the GitHub Issue body using the available GitHub tooling and report the updated issue. Do not change the title, labels, or other issue metadata.

If the target issue cannot be identified, ask for it once. If a material decision cannot be resolved, state what is missing, ask the next required question, and leave the issue unchanged.

Do not search for other candidate issues, add readiness markers, or handle work whose outcome depends on external operations or unresolved stakeholder coordination.
