# Skill: Create PR

## Trigger
`/create-pr` or "create a pull request" or "open a PR"

## Purpose
Create a well-documented pull request with proper description and checklist.

---

## Process

### 1. Gather Information

```bash
# Current branch and status
git status
git branch --show-current

# Commits to include
git log main..HEAD --oneline

# Files changed
git diff main...HEAD --stat

# Check if pushed
git log origin/[branch]..HEAD
```

### 2. Analyze Changes

```
## PR Analysis

### Branch
- **Current:** [branch name]
- **Base:** [main/master]
- **Commits:** [count]

### Changes Summary
- [High-level description]

### Files Changed
| File | Changes |
|------|---------|
| [file] | [what changed] |
```

### 3. Push if Needed

```bash
# Push branch with upstream tracking
git push -u origin [branch-name]
```

### 4. Create PR

```bash
gh pr create --title "[title]" --body "$(cat <<'EOF'
## Summary
[1-3 bullet points describing the change]

## Changes
- [Specific change 1]
- [Specific change 2]

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing done

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if needed)
- [ ] No new warnings introduced

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Related Issues
Closes #[issue number]

---
🤖 Generated with Claude Code
EOF
)"
```

---

## PR Title Conventions

Follow same format as commits:
```
type(scope): description
```

Examples:
- `feat(auth): add OAuth login support`
- `fix(cart): resolve duplicate item bug`
- `refactor(api): simplify error handling`

---

## Output Format

```
## Pull Request Created

**URL:** [PR URL]
**Number:** #[number]
**Title:** [title]

**Branch:** [head] → [base]
**Commits:** [count]
**Files Changed:** [count]

**Status:**
- [ ] CI running
- [ ] Ready for review

**Next Steps:**
- Request reviewers
- Monitor CI
```

---

## Templates

Check for PR templates in:
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/PULL_REQUEST_TEMPLATE/`
- `docs/PULL_REQUEST_TEMPLATE.md`

If template exists, use it.
