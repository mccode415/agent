---
name: worktree
description: Create a git worktree for parallel development. Use when the user wants to work on a feature branch in a separate directory without switching branches.
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Git Worktree

Create a git worktree for working on a separate branch in parallel.

## Current State
- Repository: !`basename $(git rev-parse --show-toplevel)`
- Current branch: !`git branch --show-current`
- Existing worktrees: !`git worktree list`

## Instructions

Parse `$ARGUMENTS` to determine:
1. **Branch name** - required (first argument)
2. **Base branch** - optional (second argument, defaults to `main`)

### Workflow

1. **Determine the worktree path**: Use `../<repo-name>-<branch-name>` as the directory (sibling to the current repo).

2. **Check if the branch already exists**:
   ```bash
   git branch --list <branch-name>
   git branch -r --list "origin/<branch-name>"
   ```

3. **Create the worktree**:
   - If branch exists locally or remotely: `git worktree add <path> <branch-name>`
   - If new branch: `git worktree add -b <branch-name> <path> <base-branch>`

4. **Report the result** with the full path so the user can navigate to it.

### Examples

- `/worktree feature-auth` → Creates `../<repo>-feature-auth` on new branch `feature-auth` from `main`
- `/worktree fix-bug develop` → Creates `../<repo>-fix-bug` on new branch `fix-bug` from `develop`
- `/worktree existing-branch` → If branch exists, checks it out in a new worktree

### Cleanup Reminder

After reporting success, remind the user how to clean up when done:
```
git worktree remove <path>
# or to also delete the branch:
git worktree remove <path> && git branch -d <branch-name>
```
