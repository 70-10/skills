# Task file template

Write the handoff to `.claude/todos/{slug}.md` under the project root. Keep the field names and section headings as shown for compatibility with existing stashes. Use the user's language for the text under those headings.

```markdown
---
task: Task title
status: paused
project: Project directory name
---

## 目的
What the work needs to achieve and why.

## 経緯
What was tried, which decisions were made, and why.

## 進捗
- [x] Completed work
- [ ] Next incomplete item

## 成果物
Links or paths to artifacts, commits, PRs, and plans.

## 次のアクション
1. First concrete step a new session can take.

## 推奨スキル
Skills relevant to the next action and when to use them.

## 注意点
Blockers, uncommitted changes, worktree location, or environment details.
```

`session.sh ref --append` sets `stashed_at` and, when it can resolve a local transcript, inserts the `## セッションログ` section. Each row gives the save time, a session reference, and a short description of what that session covered. Keep existing rows when updating the task summary.

Use `in-progress`, `blocked`, or `paused` for active tasks. `pop` sets `popped`, and `drop` sets `dropped`. Both statuses hide the task from `list` and can be reverted by restoring its previous status.
