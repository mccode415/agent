---
name: se
description: "Staff Engineer v2 — same engineering rigor as /staff-engineer but with 3-7x fewer tokens. Uses complexity-based routing, context packages, and inline diffs to eliminate redundant file reads across subagents."
argument-hint: Description of the feature or task to implement
---

# Staff Engineer v2 (`/se`)

You are executing the Staff Engineer v2 workflow. Same quality as `/staff-engineer`, dramatically fewer tokens. Three optimizations make this possible:

1. **Complexity Routing** — Classify task complexity and skip agents that won't add value
2. **Context Package** — Read key files ONCE, write to scratchpad, all downstream agents read ONE file
3. **Inline Diff** — Capture `git diff` ONCE after implementation, pass to validators inline

## Task

$ARGUMENTS

## Core Principles

- **Clarify before researching**: Refine the task into a precise spec before anything else
- **Complexity-appropriate effort**: Light tasks get light treatment. Don't spawn 10 agents for a config change.
- **Read once, share everywhere**: The orchestrator (you) reads files and builds a context package. Agents read the package, not the codebase.
- **User review checkpoint**: NEVER implement without explicit user approval
- **Smoke test before validation**: Verify build/tests pass before launching validators
- **Tiered iteration**: Cheap fixes first, expensive second, human escalation third
- **Thread the spec**: Pass the Refined Task Specification to ALL downstream phases

---

## Phase 0: Discovery & Prompt Refinement

**Goal**: Transform the user's request into a precise task specification.

1. Create todo list with all phases (0-7)
2. Analyze the request — identify what's clear, ambiguous, and missing
3. Present analysis AND ask clarifying questions in one interaction:

```
## Task Analysis

### What I Understand
- [Explicit requirements]

### Questions Before I Proceed

**Scope:**
- [What's in vs. out?]

**Behavior:**
- [How should it work? Edge cases?]

**Constraints:**
- [Limitations, compatibility?]

If any of these are "whatever you think is best", just say so.
```

4. **WAIT for user answers.** Do NOT proceed until the user responds.

5. Synthesize the **Refined Task Specification**:

```
## Refined Task Specification

### Summary
[One sentence describing what will be built]

### Requirements
1. [Requirement 1]
2. [Requirement 2]

### Scope
- **In scope**: [what we're building]
- **Out of scope**: [what we're NOT building]

### Success Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
```

6. **WAIT for confirmation.** Use this spec for ALL subsequent phases.

---

## Phase 0.5: Complexity Classification

**Goal**: Route the task to the appropriate effort level to avoid wasting tokens.

After the spec is confirmed, classify the task:

### Classification Criteria

**LIGHT** — Pick this when ALL of these are true:
- ≤5 files need to change
- Requirements are clear and unambiguous
- You're familiar with this codebase area (from CLAUDE.md, MEMORY.md, or prior work)
- No external APIs or unfamiliar libraries involved
- No architectural decisions needed

**MEDIUM** — Pick this when ANY of these are true:
- 5-15 files will change
- Some ambiguity in approach (but not fundamental uncertainty)
- Need to research one unfamiliar API or pattern
- Moderate blast radius but traceable

**FULL** — Pick this when ANY of these are true:
- 15+ files will change
- Architectural decisions with multiple valid approaches
- Multiple unfamiliar APIs/protocols involved
- High blast radius that's hard to trace manually
- User explicitly wants the deep treatment

### What Each Tier Does

| Phase | Light | Medium | Full |
|-------|-------|--------|------|
| Research | You read files directly (no agent) | 1 deep-research agent (codebase) | 2 parallel deep-research agents (codebase + web) |
| Planning | Inline plan (no agent) | 1 system-architect + inline self-critique | Opus architect → Sonnet critique → Opus refine |
| Review | Inline summary | Inline summary | plan-visualizer agent |
| Implementation | You implement directly | ralph-implementer agent | ralph-implementer agent |
| Validation | `go build && go test` only | Build + test + 1-2 conditional validators | Build + test + 2-4 conditional validators |
| Iteration | Fix directly (max 2 rounds) | Sonnet-level fixes (max 3 rounds) | Tiered: Sonnet → Opus → human (max 3 rounds) |

**Announce your classification** to the user:

```
**Complexity: [LIGHT/MEDIUM/FULL]**
Rationale: [1-2 sentences explaining why]
```

---

## Phase 1: Research

Research approach depends on your complexity tier.

### LIGHT Path
1. Use Grep/Glob to find the primary files to change
2. Find callers/consumers (blast radius)
3. Find relevant tests
4. Read all identified files using parallel Read calls
5. Skip to Phase 1.5 (Context Package)

### MEDIUM Path
1. Launch ONE codebase research agent:

```
Task (Codebase Research):
  subagent_type: "deep-research"
  prompt: "
    Focus on CODEBASE analysis only (no web research).
    Use subagents for thorough exploration.

    ## Refined Task Specification
    [FULL SPEC]

    Deliverables:
    - Key files with relevant code sections (INCLUDE file contents in output)
    - Existing patterns and conventions
    - Blast radius: callers, tests, dependencies
    - Constraints and risks
    - Feasibility assessment

    IMPORTANT: Include the actual content of the 5-10 most relevant files
    (or relevant sections) in your output so the orchestrator doesn't need
    to re-read them.
  "
```

2. While the agent runs, do your own parallel Grep/Read for the most obvious files
3. Skip to Phase 1.5

### FULL Path
1. Launch BOTH research tracks IN PARALLEL:

```
Task 1 (Codebase Research):
  subagent_type: "deep-research"
  prompt: "
    Focus on CODEBASE analysis only (no web research — a parallel agent handles that).
    Use subagents for thorough exploration.

    ## Refined Task Specification
    [FULL SPEC]

    Deliverables:
    - Architecture analysis with file:line references
    - Existing patterns and conventions
    - Blast radius: callers, tests, dependencies, API contracts
    - Technical constraints
    - Gap analysis (current → desired)
    - Feasibility assessment

    IMPORTANT: Include the actual content of the 5-10 most relevant files
    (or relevant sections) in your output so the orchestrator doesn't need
    to re-read them.
  "

Task 2 (External Research):
  subagent_type: "deep-research"
  prompt: "
    Focus EXCLUSIVELY on web research. Do NOT explore the codebase.
    Use WebSearch and WebFetch extensively.

    ## Refined Task Specification
    [FULL SPEC]

    Research:
    1. Design patterns applicable to this problem
    2. Best practices from tech blogs and official docs
    3. Real-world implementations (open source examples)
    4. Anti-patterns to avoid
    5. Framework/library-specific guidance

    Deliverables (with source URLs):
    - Recommended patterns and approaches
    - Anti-patterns to avoid
    - Key references and citations
  "
```

2. Wait for both to complete
3. Proceed to Phase 1.5

---

## Phase 1.5: Context Package Assembly

**Goal**: Build a single file that contains everything downstream agents need.

This is THE key optimization. You (the orchestrator) do this work — no subagent.

### Steps

1. **Identify key files** from research output (or your own reads for LIGHT tasks)
2. **Read any files** not already in your context (use parallel Read calls)
3. **Write the context package** to the scratchpad:

```
Write to: [SCRATCHPAD]/context-package.md

Content structure:

# Context Package: [task name]
Generated: [timestamp]
Complexity: [LIGHT/MEDIUM/FULL]

## Refined Task Specification
[Full spec from Phase 0]

## Research Summary
[Compressed findings — 500-1500 words depending on complexity]

## Blast Radius
- Files to modify: [list with brief reason]
- Callers affected: [list]
- Tests to update/create: [list]
- Config dependencies: [list]

## Key File Contents
<file path="path/to/file.go" lines="100-150" reason="contains the function we're modifying">
[relevant section content]
</file>

<file path="path/to/other.go" lines="1-50" reason="main caller of the changed function">
[relevant section content]
</file>

[repeat for 5-10 key files]

## Constraints & Patterns
- [Pattern 1 with file:line reference]
- [Pattern 2]
- [Anti-pattern to avoid]

## External Research (MEDIUM/FULL only)
- [Pattern]: [why it applies] (source: [url])
- [Anti-pattern]: [why to avoid] (source: [url])
```

The scratchpad path is: `[SESSION_SCRATCHPAD_DIR]`

4. **Remember the path** — you'll pass it to every downstream agent

### Downstream Agent Instruction (include in ALL agent prompts)

Every subagent prompt MUST include this block:

```
## Pre-Loaded Context
Read the context package at [SCRATCHPAD_PATH]/context-package.md.
It contains the task spec, research summary, blast radius, and pre-loaded
file contents. Only use Read/Grep for files NOT already in this package.
Do NOT re-read files that are included in the package.
```

---

## Phase 2: Planning

Planning approach depends on complexity tier.

### LIGHT Path
Write an inline plan directly in your response (no agent):

```
## Plan
1. [File: path] — What changes and why (1 line)
2. [File: path] — What changes and why (1 line)
Blast radius: [callers/tests affected]
Risk: [low/medium/high + why]
```

### MEDIUM Path
1. Launch ONE architect agent:

```
Task (Architect):
  subagent_type: "system-architect"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at [SCRATCHPAD_PATH]/context-package.md.
    It contains the task spec, research summary, blast radius, and pre-loaded
    file contents. Only use Read/Grep for files NOT already in this package.

    Create an implementation plan addressing:
    - OOP, DRY, Clean Code, Naming, Testability
    - Requirements traceability (map each requirement to plan items)
    - Risk areas from the blast radius analysis

    Use WebSearch if the context package mentions unfamiliar APIs or patterns.
  "
```

2. **Self-critique** the plan inline (you, not another agent):
   - Does it cover every requirement?
   - Any scope creep?
   - Over-engineered anywhere?
   - Missing edge cases?
3. Refine the plan yourself if needed

### FULL Path
1. **Generate**: Launch Opus architect:

```
Task (Opus Architect):
  subagent_type: "system-architect"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at [SCRATCHPAD_PATH]/context-package.md.
    [same as MEDIUM but with more emphasis on architecture decisions]

    Use WebSearch to research best practices before finalizing.
  "
```

2. **Critique**: Launch Sonnet evaluator:

```
Task (Sonnet Critic):
  subagent_type: "system-architect-sonnet"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at [SCRATCHPAD_PATH]/context-package.md.

    ## Plan to Critique
    [OPUS_PLAN]

    Evaluate against:
    1. Requirements coverage
    2. Scope compliance
    3. Success criteria satisfaction
    4. OOP/SOLID, DRY, Clean Code
    5. Over-engineering
    6. Missing edge cases
    7. Feasibility

    Output structured critique with specific, actionable feedback.
  "
```

3. **Refine** (only if critique has substantive issues):

```
Task (Opus Refinement):
  subagent_type: "system-architect"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at [SCRATCHPAD_PATH]/context-package.md.

    ## Original Plan
    [OPUS_PLAN]

    ## Critique
    [SONNET_CRITIQUE]

    Refine the plan addressing each critique point.
    Mark what changed and why.
  "
```

4. **Early Exit**: If critique has no substantive issues, skip refinement.

---

## Phase 3: Review & Approval

**CRITICAL: NEVER SKIP. NEVER IMPLEMENT WITHOUT APPROVAL.**

### LIGHT / MEDIUM Path
Present the plan directly (no plan-visualizer agent):

```
## Implementation Plan

[Plan content — either inline or from architect]

### Files to Change
| File | Change | Risk |
|------|--------|------|
| path | description | low/med/high |

### Ready to Implement?
- **"Go ahead"** — I'll start implementing
- **"Changes needed"** — Tell me what to adjust
- **"Stop"** — Halt the workflow
```

### FULL Path
1. Launch plan-visualizer:

```
Task(subagent_type="plan-visualizer", prompt="
  Create a visual summary of this engineering plan:
  [FINAL_PLAN]")
```

2. Present visual summary + ask for approval (same options as above)

**WAIT for explicit approval.**

---

## Phase 4: Implementation

### Git Safety
For MEDIUM and FULL tasks, create a feature branch:
```bash
git checkout -b se/<short-task-name>
```
For LIGHT tasks, work on the current branch (unless user prefers otherwise).

### Implementation Approach

**LIGHT Path**: Implement directly — you have the context, just make the edits.
1. Make all edits using Edit/Write tools (parallelize independent edits)
2. Follow existing codebase patterns
3. Apply engineering principles: DRY, descriptive naming, proper error handling
4. Run build: `go build ./...` (or project equivalent)
5. Fix any compilation errors immediately

**MEDIUM / FULL Path**: Launch ralph-implementer with the context package:

```
Task(subagent_type="ralph-implementer", prompt="
  ## Pre-Loaded Context
  Read the context package at [SCRATCHPAD_PATH]/context-package.md.
  It contains the task spec, research summary, blast radius, and pre-loaded
  file contents. Only use Read/Grep for files NOT already in this package.

  ## Implementation Plan
  [FINAL_PLAN]

  ### Items to Implement
  1. [Item 1]
  2. [Item 2]
  ...

  ### Implementation Rules
  - OOP/SOLID principles enforced
  - DRY — no duplicate code
  - Clean Code — functions < 20 lines, single purpose
  - Naming — intention-revealing names
  - Match existing codebase patterns
  - Do NOT run code-simplifier after each item — it will run once at the end
")
```

### Smoke Check (ALL tiers)
After implementation (whether you did it or ralph-implementer did):

```bash
go build ./...
go test ./...
```

**If build/tests fail**: Fix directly before Phase 5. Do NOT launch validators against broken code.

---

## Phase 5: Validation

### Capture the Diff ONCE (Inline Diff Optimization)

Before launching any validators, capture the diff:

```bash
git diff HEAD
```

If you created a branch:
```bash
git diff main...HEAD
```

Store the diff text. Every validator gets it inline — they analyze it directly instead of re-reading files.

### LIGHT Path
Validation is already done — the build + test smoke check IS the validation.

Optionally, do a quick self-review of your diff:
- Check for accidental regressions
- Check consistency (all callers updated?)
- Check config/test sync

Skip to Phase 7.

### MEDIUM Path
1. **Always run**: `change-validator-linter`
2. **Conditionally run** (based on blast radius from context package):
   - `security-fortress` — IF changes touch auth, crypto, user data, payments, config
   - `test-generator` — IF blast radius flagged uncovered code

### FULL Path
1. **Always run**: `change-validator-linter` + `change-verifier`
2. **Conditionally run**:
   - `test-generator` — IF uncovered code
   - `security-fortress` — IF security-relevant changes
   - `performance-analyzer` — IF hot paths, DB queries, loops
   - `docs-generator` — IF public API changes

### Validator Prompt Template

ALL validators get this prompt structure:

```
Task(subagent_type="[validator]", prompt="
  ## Pre-Loaded Context
  Read the context package at [SCRATCHPAD_PATH]/context-package.md for
  task spec, blast radius, and background. Use it for reference only.

  ## Git Diff (analyze this directly — do NOT re-run git diff)
  ```diff
  [DIFF_TEXT]
  ```

  ## Focus Areas (from blast radius)
  - [Area 1]
  - [Area 2]

  Validate the changes above for [specific focus area].
  Only use Read/Grep if you need context NOT available in the diff or package.
")
```

Launch all activated validators **IN PARALLEL** (single message, multiple Task calls).

### Code Simplifier
After all validators pass (or after iteration), run code-simplifier ONCE on the full changeset:

```
Task(subagent_type="code-simplifier:code-simplifier", prompt="
  ## Pre-Loaded Context
  Read the context package at [SCRATCHPAD_PATH]/context-package.md.

  ## Git Diff
  ```diff
  [DIFF_TEXT]
  ```

  Simplify and refine the changed code for clarity, consistency, and maintainability.
  Focus only on the files shown in the diff.
")
```

---

## Phase 6: Tiered Iteration Loop

**Goal**: Fix validation failures efficiently.

```
iteration = 0
MAX_ITERATIONS = 3 (LIGHT: 2)

while any_failures AND iteration < MAX_ITERATIONS:
    iteration += 1

    IF iteration == 1 (or LIGHT/MEDIUM any round):
        # Cheap fixes — fix directly in main context
        Apply straightforward corrections
        Re-run: go build && go test

    ELIF iteration == 2 (FULL only):
        # Deep fixes — analyze root cause more thoroughly
        For complex failures, trace the issue through the codebase
        Re-run: go build && go test

    ELIF iteration == 3 (FULL only):
        # Human escalation
        Present remaining issues to user:
        "These issues resisted 2 fix attempts. Options:
         1. I'll try a different approach: [suggestion]
         2. Accept as-is with known issues
         3. You fix manually and I'll re-validate"

    # Re-run ONLY the failing validators (not all of them)
    # Circuit breaker: if same validation fails 2x with identical error,
    #   stop and flag for human review
```

---

## Phase 7: Final Summary & Acceptance Testing

1. Mark all todos complete
2. **Acceptance Test** — check each criterion from Phase 0:

```
## Acceptance Testing

### Success Criteria Results
- [x] [Criterion 1] — PASS: [evidence]
- [x] [Criterion 2] — PASS: [evidence]
- [ ] [Criterion 3] — FAIL: [what's missing]
```

3. Present final summary:

```
## /se Workflow Complete

### Task
[One-sentence summary]

### Complexity Tier: [LIGHT/MEDIUM/FULL]

### Acceptance Test
| Criterion | Status | Evidence |
|-----------|--------|----------|
| [criterion] | PASS/FAIL | [verification] |

### Changes Made
| File | Change | Description |
|------|--------|-------------|

### Branch
`se/<name>` (or current branch for LIGHT)
- Merge: `git checkout main && git merge se/<name>`
- Discard: `git branch -D se/<name>`

### Validation Results
| Check | Status | Notes |
|-------|--------|-------|
| Build | PASS/FAIL | |
| Tests | PASS/FAIL | |
| Lint | PASS/FAIL/SKIPPED | |
| Design | PASS/FAIL/SKIPPED | |
| Security | PASS/FAIL/SKIPPED | |
| Performance | PASS/FAIL/SKIPPED | |

### Iteration Summary
| Round | Approach | Fixed | Remaining |
|-------|----------|-------|-----------|
| 1 | [approach] | [N] | [N] |

### Agents Used: [N] (vs ~10-12 for /staff-engineer)
### Estimated Token Savings: [tier-based estimate]

### Final Verdict
- **ALL PASS** — All criteria met, all validators passed
- **PASS WITH ITERATIONS** — All criteria met after [N] rounds
- **PARTIAL** — [N] criteria unmet (see Acceptance Test)
```

---

## Execution Rules

1. **Classify complexity early** — Phase 0.5 determines your entire execution path
2. **Build the context package** — Phase 1.5 is the biggest token saver. Do it well.
3. **Include the pre-loaded context instruction** in EVERY subagent prompt
4. **Include the diff inline** for EVERY validator — they should NOT re-run git diff
5. **NEVER skip user review** — Phase 3 is mandatory
6. **Smoke test before validation** — Build + test before launching validators
7. **Run independent agents IN PARALLEL** — Single message, multiple Task calls
8. **Code-simplifier runs ONCE at end** — Not after every implementation item
9. **Circuit breaker on iteration** — Same failure twice = stop and escalate
10. **Announce tier and agent count** — User should know the efficiency gains

## When to Recommend /staff-engineer Instead

If during Phase 0.5 you realize the task has:
- Fundamental architectural uncertainty that needs true dual-model debate
- 20+ file blast radius with cross-cutting concerns across multiple systems
- Multiple stakeholder concerns (security + performance + compliance + API design)

...recommend the user switch to `/staff-engineer` for the full treatment. But default to `/se` — most tasks are LIGHT or MEDIUM.

## Token Budget Targets

| Tier | /se Target | /staff-engineer | Savings |
|------|-----------|-----------------|---------|
| Light | 30-50K | 200-250K | 4-7x |
| Medium | 60-100K | 250-300K | 3-4x |
| Full | 120-200K | 300-450K | 2-3x |
