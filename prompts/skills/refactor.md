# Skill: Refactor

## Trigger
`/refactor [file/code]` or "refactor this" or "clean up this code"

## Purpose
Improve code structure without changing behavior.

---

## Process

### 1. Analyze Current Code

```
## Current State

### Code Smells Detected
- [ ] Long function (> 30 lines)
- [ ] Deep nesting (> 3 levels)
- [ ] Duplicate code
- [ ] Magic numbers/strings
- [ ] Poor naming
- [ ] God class/function
- [ ] Feature envy
- [ ] Long parameter list

### Metrics
- Lines: [count]
- Complexity: [low/medium/high]
- Dependencies: [count]
```

### 2. Plan Refactoring

```
## Refactoring Plan

### Goals
1. [Specific improvement]
2. [Specific improvement]

### Techniques to Apply
- [ ] Extract function
- [ ] Extract variable
- [ ] Rename for clarity
- [ ] Remove duplication
- [ ] Simplify conditionals
- [ ] Introduce parameter object

### Order
1. [First change - safest]
2. [Second change]
```

### 3. Ensure Safety

```
## Safety Check

### Existing Tests
- [ ] Tests exist: [yes/no]
- [ ] Tests pass: [yes/no]

### If No Tests
Add characterization tests first:
```[language]
[test code]
```
```

### 4. Apply Refactoring

One change at a time:
```
## Change 1: [technique]

**Before:**
```[language]
[code]
```

**After:**
```[language]
[code]
```

**Why:** [Improvement]
**Tests:** Still passing ✓
```

---

## Common Refactorings

### Extract Function
```typescript
// Before
function process(data) {
  // validation logic here (10 lines)
  // processing logic here (20 lines)
}

// After
function validate(data) { /* 10 lines */ }
function transform(data) { /* 20 lines */ }
function process(data) {
  validate(data);
  return transform(data);
}
```

### Simplify Conditionals
```typescript
// Before
if (user) {
  if (user.isActive) {
    if (user.hasPermission) {
      doThing();
    }
  }
}

// After (guard clauses)
if (!user) return;
if (!user.isActive) return;
if (!user.hasPermission) return;
doThing();
```

### Extract Variable
```typescript
// Before
if (date.getTime() > Date.now() - 86400000 && user.role === 'admin') {

// After
const isRecent = date.getTime() > Date.now() - 86400000;
const isAdmin = user.role === 'admin';
if (isRecent && isAdmin) {
```

---

## Output Format

```
## Refactor: [file/function]

### Analysis
[Code smells found]

### Changes Made
1. [Change 1 summary]
2. [Change 2 summary]

### Before/After
[Show key improvements]

### Results
- Lines: [before] → [after]
- Complexity: [before] → [after]
- Tests: All passing ✓

### Commit
```bash
git commit -m "refactor(scope): [description]"
```
```
