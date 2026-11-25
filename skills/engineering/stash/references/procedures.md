# Stash procedures

Resolve task paths from the target project's root. Treat a name as one filename stem inside `.claude/todos/`. Use new slugs such as `fix-import-cache`. Reject names that try to address a parent directory or another path. Use `save <name>` to save a task whose name matches a command.

## Save

1. Use the named task or propose a name and slug for a new task. If the request could update an existing task, list the active stashes and resolve the target before writing.
2. If the work used Git, check `git status --short` in the task's worktree or the project root. Report uncommitted changes and let the user decide whether to commit first or save the context with the changes still present. If saving now, record the uncommitted state in the handoff.
3. Write or update the task using the [template](task-template.md), including the reason for decisions, completed work, and the next concrete action. Choose the status that describes the saved work, such as `paused`. Preserve the existing session index and let `session.sh ref --append` set `stashed_at` and update the index. Pass a short, single-line note naming the work and decisions, with searchable details such as a file, symbol, or error. Repeated saves in the same session update its entry.
4. Report the saved slug and next action. If the script reports `summary-only`, say the summary was saved and the session log was unavailable. If it exits with an error, report that the index and timestamp update failed.

## Pop

1. Find the named task or list active stashes and ask which one to resume. If the task does not exist, report that and stop.
2. Read the task and brief the user on its purpose, decisions, progress, next action, recommended skills, and caveats. If the session index exists, mention the relevant entries as pointers. Read only project files directly relevant to the next action.
3. Search the referenced transcript only when the summary and relevant files leave a specific question that blocks the next action. Choose the session from the index and follow [transcript lookup](#transcript-lookup). Read older handoffs in their existing layout. If there is no index, resume from the summary.
4. Ask whether to continue. Once confirmed, set the task's frontmatter `status` to `popped` and continue with the agreed next action.

## Apply

Follow [pop](#pop) through the continuation confirmation. Keep the task status so it stays available for other sessions.

## Drop

Find the named task or list active stashes and ask which one to discard. Show its summary first. After confirmation, set its frontmatter `status` to `dropped`. Keep the task file so the status can be reverted.

## Transcript lookup

- The index is headed `Session Log` in new tasks. The helper also recognizes legacy Japanese headings for the log and artifacts. It updates an existing log in place or adds `Session Log` after the artifacts section, with the end of the file as the fallback.
- Pass the reference as written in the index. A bare UUID refers to a Claude Code session, including its subagent logs. A `codex:<thread-id>` reference identifies a Codex thread.
- `session.sh find <reference>` shows user messages. Add a search term to include assistant messages, tool calls, and results. Matching is case-insensitive and literal. The default output is at most 50 rows of 300 characters each, with timestamps in JST. Use `--max N` to change the row limit (`0` for all rows) and `--full` when you need the full text of a match.
- Look only in the selected session. If its local log is unavailable, continue using the saved summary. The task file can travel between machines, while the referenced transcripts stay where the agent recorded them.
