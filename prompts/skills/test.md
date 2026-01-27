# Skill: Test

## Trigger
`/test` or `/test [pattern]` or "run tests"

## Purpose
Run tests and analyze results, suggesting fixes for failures.

---

## Process

### 1. Detect Test Framework

```
## Test Framework Detection

Checking for:
- package.json → jest, mocha, vitest
- pytest.ini, pyproject.toml → pytest
- Cargo.toml → cargo test
- go.mod → go test

**Detected:** [framework]
**Command:** [test command]
```

### 2. Run Tests

```bash
# Full test suite
npm test

# Specific pattern
npm test -- [pattern]

# With coverage
npm test -- --coverage

# Watch mode (if requested)
npm test -- --watch
```

### 3. Analyze Results

```
## Test Results

### Summary
- **Total:** [count]
- **Passed:** [count] ✓
- **Failed:** [count] ✗
- **Skipped:** [count] ○
- **Duration:** [time]

### Failed Tests
| Test | File | Error |
|------|------|-------|
| [test name] | [file:line] | [error summary] |

### Coverage (if available)
| Metric | Coverage |
|--------|----------|
| Statements | [%] |
| Branches | [%] |
| Functions | [%] |
| Lines | [%] |
```

### 4. Failure Analysis

For each failure:
```
## Failure: [test name]

**File:** [file:line]

**Error:**
```
[error message]
```

**Analysis:**
- [What the test expects]
- [What actually happened]
- [Likely cause]

**Suggested Fix:**
```[language]
[code fix]
```
```

---

## Output Format

```
## Test Run: [pattern or "all"]

### Results
[Summary as above]

### Failures
[Analysis for each failure]

### Recommendations
1. [What to fix first]
2. [What to fix second]

### Commands
```bash
# Re-run failed tests only
[command]

# Run specific failing test
[command]
```
```
