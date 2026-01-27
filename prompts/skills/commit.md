# Skill: Commit

## Trigger
`/commit` or "commit this" or "create a commit"

## Purpose
Create a well-formatted git commit with conventional commit message.

---

## Process

### 1. Gather Information
```bash
# Check status
git status

# See what's changed
git diff --staged
git diff

# See recent commit style
git log --oneline -10
```

### 2. Analyze Changes

```
## Changes Analysis

### Staged Changes
- [file]: [what changed]

### Unstaged Changes
- [file]: [what changed]

### Change Type
- [ ] feat: New feature
- [ ] fix: Bug fix
- [ ] refactor: Code restructure
- [ ] test: Adding tests
- [ ] docs: Documentation
- [ ] chore: Tooling/config
- [ ] style: Formatting
```

### 3. Draft Commit Message

Follow conventional commits:
```
type(scope): short description

[optional body - what and why]

[optional footer - breaking changes, issues closed]
```

**Rules:**
- Subject line ≤ 50 chars
- Body lines ≤ 72 chars
- Use imperative mood ("Add" not "Added")
- Explain WHY, not just WHAT

### 4. Stage and Commit

```bash
# Stage specific files (preferred)
git add [specific files]

# Commit with message
git commit -m "type(scope): description"
```

### 5. Verify

```bash
git status
git log -1
```

---

## Output Format

```
## Commit Created

**Hash:** [short hash]
**Message:**
```
[full commit message]
```

**Files:**
- [file] (+N, -M)

**Branch:** [current branch]
```

---

## Safety Checks

- [ ] No secrets in diff (.env, keys, passwords)
- [ ] No large binaries
- [ ] No unintended files
- [ ] Tests pass (if applicable)
- [ ] Lint passes (if applicable)

---

## Examples

**Simple feature:**
```
feat(auth): add password reset endpoint
```

**Bug fix with context:**
```
fix(cart): prevent duplicate items on rapid clicks

Added debounce to add-to-cart button to prevent
race condition when user clicks multiple times.

Fixes #123
```

**Breaking change:**
```
feat(api): change user endpoint response format

BREAKING CHANGE: User endpoint now returns
{ data: user } instead of user directly.
```
