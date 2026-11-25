# Task file template

Write the handoff to `.claude/todos/{slug}.md` under the project root. Use these fields and headings for new tasks. Write the task title and body in the user's language or follow the project's convention. Keep existing headings when updating a saved task.

```markdown
---
task: Task title
status: paused
project: Project directory name
---

## Goal
What the work needs to achieve and why.

## Context and Decisions
What was tried, which decisions were made, and why.

## Progress
- [x] Completed work
- [ ] Next incomplete item

## Artifacts
Links or paths to artifacts, commits, PRs, and plans.

## Next Actions
1. First concrete step a new session can take.

## Recommended Skills
Skills relevant to the next action and when to use them.

## Notes
Blockers, uncommitted changes, worktree location, or environment details.
```

`session.sh ref --append` sets `stashed_at` and, when it can resolve a local transcript, inserts the `## Session Log` section. Each row gives the save time, a session reference, and a short description of what that session covered. Keep existing rows when updating the task summary.

Use `in-progress`, `blocked`, or `paused` for active tasks. `pop` sets `popped`, and `drop` sets `dropped`. Both statuses hide the task from `list` and can be reverted by restoring its previous status.
