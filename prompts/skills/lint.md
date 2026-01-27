# Skill: Lint

## Trigger
`/lint` or `/lint [file]` or "run linter" or "fix lint errors"

## Purpose
Run linters, show issues, and auto-fix where possible.

---

## Process

### 1. Detect Linter

```
## Linter Detection

Checking for:
- .eslintrc* → ESLint
- .prettierrc* → Prettier
- pyproject.toml [tool.ruff] → Ruff
- .flake8, setup.cfg → Flake8
- rustfmt.toml → rustfmt

**Detected:** [linter(s)]
```

### 2. Run Linter

```bash
# ESLint
npx eslint . --ext .js,.ts,.tsx

# With auto-fix
npx eslint . --fix

# Prettier check
npx prettier --check .

# Prettier fix
npx prettier --write .
```

### 3. Report Results

```
## Lint Results

### Summary
- **Errors:** [count]
- **Warnings:** [count]
- **Auto-fixable:** [count]

### Issues by File
| File | Errors | Warnings |
|------|--------|----------|
| [file] | [n] | [n] |

### Issues Detail
| File:Line | Rule | Message | Fixable |
|-----------|------|---------|--------|
| [location] | [rule] | [message] | [yes/no] |
```

### 4. Fix Options

```
## Fix Options

### Auto-fix Command
```bash
[command to auto-fix]
```

### Manual Fixes Required
| Issue | Fix |
|-------|-----|
| [issue] | [how to fix] |
```

---

## Output Format

```
## Lint: [scope]

### Before
- Errors: [n]
- Warnings: [n]

### Auto-fixed
- [n] issues fixed automatically

### Remaining
| File | Line | Issue | Fix |
|------|------|-------|-----|

### Commands
```bash
# Fix all auto-fixable
[command]
```
```
