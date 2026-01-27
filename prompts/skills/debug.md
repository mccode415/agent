# Skill: Debug

## Trigger
`/debug [issue]` or "debug this" or "why is this failing"

## Purpose
Systematically debug an issue to find root cause and fix.

---

## Process

### 1. Understand the Problem

```
## Problem Statement

**Symptom:** [What's happening]
**Expected:** [What should happen]
**Frequency:** [Always / Sometimes / Random]
**Recent Changes:** [What changed recently]
```

### 2. Gather Information

```bash
# Check error logs
[log command]

# Check recent changes
git log --oneline -10
git diff HEAD~5

# Check environment
[env check commands]
```

### 3. Form Hypotheses

```
## Hypotheses

| # | Hypothesis | Likelihood | Test |
|---|------------|------------|------|
| 1 | [guess] | [High/Med/Low] | [how to verify] |
| 2 | [guess] | [High/Med/Low] | [how to verify] |
| 3 | [guess] | [High/Med/Low] | [how to verify] |
```

### 4. Test Hypotheses

Start with most likely:
```
## Testing Hypothesis 1: [description]

**Test:** [what we're checking]
**Result:** [what we found]
**Conclusion:** [confirmed/ruled out]
```

### 5. Root Cause Analysis

```
## Root Cause

**What:** [The actual cause]
**Where:** [File:line]
**Why:** [How this causes the symptom]

### Evidence
- [Evidence 1]
- [Evidence 2]
```

### 6. Fix

```
## Fix

**Change:**
```[language]
[code change]
```

**Why This Fixes It:**
[Explanation]

**Verification:**
```bash
[command to verify fix]
```
```

---

## Debugging Techniques

### Binary Search
Narrow down when/where issue started:
```bash
git bisect start
git bisect bad HEAD
git bisect good [known-good-commit]
# Test each commit git bisect suggests
```

### Add Logging
```typescript
console.log('[DEBUG] variable:', variable);
console.log('[DEBUG] reached checkpoint 1');
```

### Isolate
- Comment out sections
- Test with minimal input
- Remove dependencies one by one

### Compare
- Working vs broken environment
- Working vs broken input
- Before vs after change

---

## Output Format

```
## Debug: [issue summary]

### Problem
[Description]

### Investigation
[What was checked]

### Root Cause
[What's actually wrong]

### Fix
[Solution]

### Prevention
[How to prevent this in future]
```
