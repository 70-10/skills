---
name: land
description: Use to carry an agreed specification or design through to a pull request — work in an isolated worktree, commit, push, open the pull request, and remove the worktree. Not for only turning already committed changes into a pull request, committing only, work where what to build is not yet settled, or responding to review comments on an existing pull request.
---

Take an agreed specification or design, carry out the task in an isolated worktree, open a pull request, and remove the worktree. The work is complete only when the pull request has been opened, the behavior of the changes has been verified, and no worktree remains.

Take as input either the specification or design agreed in the current session, or the contents of a specification file given as an argument. When no agreed input can be found, say so and stop without doing anything. Do not create a worktree while what to build is still undecided.

Before starting, check the starting point. When the target is not under version control, say that an isolated worktree cannot be created and stop. When the original working location has uncommitted changes, say that they will not be carried into the worktree, stop, and ask how to handle them.

Then proceed in this order:

1. Create an isolated worktree and enter it, with a name derived from the input specification.
2. Carry out the task according to the input.
3. Commit the changes and push them to the remote.
4. Open a pull request from the state of the worktree.
5. Remove the worktree.

Remove the worktree without asking for approval only when it can be verified mechanically that its commits have been pushed to the remote; the commits remain on the remote and are not lost. When the push cannot be verified, or a submodule has commits that have not been pushed, stop and ask instead of removing it.

Remove the worktree within this same run rather than leaving it for later. Some agents can remove a worktree only from the session that created it, so one carried over may become impossible to remove.
