# Skills System

Skills are reusable commands that can be invoked with a slash prefix (e.g., `/commit`, `/review-pr`).

## Available Skills

| Skill | Trigger | Purpose |
|-------|---------|--------|
| [commit](commit.md) | `/commit` | Create a well-formatted git commit |
| [review-pr](review-pr.md) | `/review-pr` | Review a pull request |
| [create-pr](create-pr.md) | `/create-pr` | Create a pull request with template |
| [test](test.md) | `/test` | Run and analyze tests |
| [lint](lint.md) | `/lint` | Run linters and fix issues |
| [explain](explain.md) | `/explain` | Explain code or concepts |
| [refactor](refactor.md) | `/refactor` | Refactor selected code |
| [debug](debug.md) | `/debug` | Debug an issue |

## Creating New Skills

Skills follow this structure:

```markdown
# Skill: [name]

## Trigger
`/[command]` or `[keyword]`

## Purpose
[What this skill does]

## Input
[What the skill expects]

## Process
[Steps the skill follows]

## Output
[What the skill produces]
```

## Skill vs Agent

| Aspect | Skill | Agent |
|--------|-------|-------|
| Scope | Single focused task | Complex multi-step workflow |
| Duration | Quick (seconds-minutes) | Longer (minutes-hours) |
| User interaction | Minimal | May checkpoint with user |
| Examples | `/commit`, `/lint` | `staff-engineer`, `deep-research` |
