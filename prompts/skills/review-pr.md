# Skill: Review PR

## Trigger
`/review-pr [number]` or "review this PR" or "review PR #123"

## Purpose
Review a pull request for bugs, security issues, code quality, and adherence to conventions.

---

## Process

### 1. Gather PR Information

```bash
# Get PR details
gh pr view [number]

# Get diff
gh pr diff [number]

# Get files changed
gh pr view [number] --json files

# Check CI status
gh pr checks [number]
```

### 2. Review Checklist

```
## PR Review: #[number]

### Overview
- **Title:** [title]
- **Author:** [author]
- **Base:** [base branch] ← [head branch]
- **Files Changed:** [count]
- **Lines:** +[added] -[removed]

### CI Status
- [ ] Tests: [pass/fail]
- [ ] Lint: [pass/fail]
- [ ] Build: [pass/fail]
```

### 3. Code Review

```
### Code Review

#### Bugs / Logic Errors
| File | Line | Issue | Severity |
|------|------|-------|----------|
| [file] | [line] | [issue] | [High/Med/Low] |

#### Security Concerns
| File | Line | Issue | Severity |
|------|------|-------|----------|

#### Code Quality
| File | Line | Issue | Suggestion |
|------|------|-------|------------|

#### Positive Observations
- [Good thing noticed]
```

### 4. Verdict

```
### Verdict

**Decision:** [APPROVE / REQUEST_CHANGES / COMMENT]

**Summary:**
[1-2 sentence summary]

**Blocking Issues:**
1. [Must fix before merge]

**Suggestions (non-blocking):**
1. [Nice to have]

**Questions:**
1. [Clarification needed]
```

---

## Review Criteria

### Must Check
- [ ] Logic correctness
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No security vulnerabilities
- [ ] No secrets/credentials
- [ ] Tests added/updated
- [ ] No breaking changes (or documented)

### Should Check
- [ ] Code is readable
- [ ] Naming is clear
- [ ] No unnecessary complexity
- [ ] DRY principles followed
- [ ] Consistent with codebase style

### Nice to Check
- [ ] Performance implications
- [ ] Documentation updated
- [ ] Commit messages clear

---

## Comment Templates

**Bug:**
```
🐛 **Bug:** [description]

This will cause [problem] when [condition].

Suggested fix:
```[language]
[code]
```
```

**Security:**
```
🔒 **Security:** [description]

This could allow [attack vector].

Recommend: [mitigation]
```

**Suggestion:**
```
💡 **Suggestion:** [description]

Consider [alternative] because [reason].
```

**Question:**
```
❓ **Question:** [question]

I'm not sure I understand [what]. Could you clarify?
```

**Praise:**
```
✨ Nice! [what's good about it]
```
