---
name: stash
description: Save, list, resume, or discard project task context between Claude Code and Codex sessions. Use when asked to stash work, pause and pick up later, or resume a saved task.
---

# Stash

Use the project root as the working directory. Task files live in `.claude/todos/{slug}.md` in that project. Their summaries are shared by Claude Code and Codex. Local transcript references are optional. Write enough context for someone to continue from the task file alone. Keep credentials, personal information, and raw transcripts out of task files.

Interpret `/stash [command] [name]` in Claude Code and `$stash [command] [name]` in Codex. In Claude Code the supplied arguments are `$ARGUMENTS`. For natural-language requests, use the requested operation. Default to `save` when invoked without a command.

- `save [name]` creates or updates a handoff. See [save](references/procedures.md#save).
- `pop [name]` briefs the user, then marks the task popped after confirmation. See [pop](references/procedures.md#pop).
- `apply [name]` briefs the user and leaves the task in the list. See [apply](references/procedures.md#apply).
- `list` shows active tasks, newest save first.
- `drop [name]` shows the task and marks it dropped after confirmation. See [drop](references/procedures.md#drop).

Use the [task template](references/task-template.md) for the file structure. Resolve the scripts from the installed skill directory, meaning the directory containing this `SKILL.md`. Run them from the target project root. They use Bash and `column` for listing and Python 3.11 or newer for session references.

## Script commands

In Claude Code, list with `bash "${CLAUDE_SKILL_DIR}/scripts/list.sh"`. After writing a summary, run:

```sh
CLAUDE_SESSION_ID="${CLAUDE_SESSION_ID}" bash "${CLAUDE_SKILL_DIR}/scripts/session.sh" ref ".claude/todos/<slug>.md" --agent claude-code --append "<note>"
```

In Codex, replace `<skill-dir>` with the absolute directory containing the loaded skill. List with `bash "<skill-dir>/scripts/list.sh"`. After writing a summary, run:

```sh
bash "<skill-dir>/scripts/session.sh" ref ".claude/todos/<slug>.md" --agent codex --append "<note>"
```

For a specific question the summary cannot answer, run `bash "<skill-dir>/scripts/session.sh" find "<reference>"` or add a quoted search term. In Claude Code use `${CLAUDE_SKILL_DIR}` for that directory. Quote references, notes, and search terms as literal shell arguments.
