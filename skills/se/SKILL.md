---
name: se
description: "Staff Engineer v2 — same engineering rigor as /staff-engineer but with 3-7x fewer tokens. Uses complexity-based routing, context packages, and inline diffs to eliminate redundant file reads across subagents."
argument-hint: Description of the feature or task to implement
---

# Staff Engineer v2 (`/se`)

You are executing the Staff Engineer v2 workflow. Same quality as `/staff-engineer`, dramatically fewer tokens. Three optimizations make this possible:

1. **Complexity Routing** — Classify task complexity and skip agents that won't add value
2. **Context Package** — Read key files ONCE, write to shared file, all downstream agents read ONE file
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

## Phase -1: First-Principles Strategic Filter

**Goal**: Decompose the request to its fundamentals before investing compute. Ensure we're solving the RIGHT problem.

### 1. Problem Decomposition (First Principles)
- **What is the user ACTUALLY trying to achieve?** (not what they asked for — what outcome do they need?)
- **What are the fundamental constraints?** (physics of the problem: data flow, latency requirements, consistency needs)
- **Which constraints are REAL vs. ASSUMED?** (inherited conventions ≠ hard requirements. Challenge: "we do it this way because we always have")

### 2. Causal Chain Analysis (MANDATORY — ask "why" until you hit bedrock)
- **Trace the full causal chain**: Don't stop at the first cause. Ask "why is this happening?" recursively.
  - Example: "Wrong data saved to DB" → WHY? → "No validation rejects it" → WHY does bad data arrive? → "Upstream component selects wrong item" → WHY? → "Selector logic is ambiguous + no disambiguation step + cached state replays wrong choice"
  - Each "why" level = a layer that needs fixing. Count the layers — this directly affects complexity classification.
- **Fix ALL layers, not just the last one**: If you only add output validation but don't fix the upstream selector, the symptom is masked but the root cause persists (wasted processing, wrong data cached for next time).
- **Surface multi-layer scope to user in Phase 0**: "This problem has N causal layers. Should I fix all of them?"

### 3. Solution Validation
- **Simplest possible solution?** Could we solve this by removing code, changing config, or doing nothing? The best code is no code.
- **Chesterton's Fence**: If changing existing behavior, do we understand WHY it was built that way? If not, find out before changing it.

### 4. Strategic Check
- **Opportunity cost**: Is this the highest-leverage work right now?
- **Second-order effects**: What does this change make easier or harder in the future?

If any red flags → surface to user with your reasoning before proceeding.
If all clear → proceed to Phase 0 with your decomposition as context.

---

## Phase 0: Discovery & Prompt Refinement

**Goal**: Transform the user's request into a precise task specification.

1. Create todo list with all phases (-1 through 8)
2. Analyze the request — identify what's clear, ambiguous, and missing
3. Present analysis AND ask clarifying questions in one interaction:

```
## Task Analysis

### What I Understand
- [Explicit requirements]

### Causal Chain (from Phase -1)
- Layer 1: [immediate symptom] — WHY? →
- Layer 2: [cause] — WHY? →
- Layer 3: [root cause]
(Each layer likely needs its own fix)

### Questions Before I Proceed

**Scope:**
- [What's in vs. out?]
- Should I fix all [N] causal layers, or just the immediate symptom?

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
- ≤3 files need to change AND ≤5 files need to be **understood**
- The problem has a single causal layer (not "wrong output because wrong input because wrong navigation")
- Requirements are clear and unambiguous
- You're familiar with this codebase area (from CLAUDE.md, MEMORY.md, or prior work)
- No external APIs or unfamiliar libraries involved
- No architectural decisions needed

**MEDIUM** — Pick this when ANY of these are true:
- 4-15 files will change, OR ≤5 files change but 6+ files must be understood
- The problem spans multiple subsystems (e.g., parser + navigator + memory)
- Some ambiguity in approach (but not fundamental uncertainty)
- Need to research one unfamiliar API or pattern
- Moderate blast radius but traceable
- The causal chain has 2+ layers (Phase -1 revealed multiple "why" levels)

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
| Implementation | You implement directly | You implement directly | You implement directly |
| Validation | Build + test only | Build + test + 1-2 conditional validators | Build + test + 2-4 conditional validators |
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
3. **Write the context package**:

```
Write to: /tmp/se-<task-name>/context-package.md

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

Use `/tmp/se-<task-name>/context-package.md` as the path. Create the directory first:
```bash
mkdir -p /tmp/se-<task-name>
```

4. **Remember the path** — you'll pass it to every downstream agent

### Downstream Agent Instruction (include in ALL agent prompts)

Every subagent prompt MUST include this block:

```
## Pre-Loaded Context
Read the context package at /tmp/se-<task-name>/context-package.md.
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

### First-Principles Reasoning
[1-2 sentences: Why this approach is fundamentally correct, not just conventional]

### Changes
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
    Read the context package at /tmp/se-<task-name>/context-package.md.
    It contains the task spec, research summary, blast radius, and pre-loaded
    file contents. Only use Read/Grep for files NOT already in this package.

    ## Planning Requirements

    ### First-Principles Analysis (required)
    Before proposing solutions, decompose the problem:
    - What are the fundamental operations this feature needs to perform?
    - What are the hard constraints (latency, consistency, data size)?
    - What are the soft constraints (conventions, preferences)?
    - If building from scratch with no legacy, what would the ideal design look like?

    ### Alternatives Analysis (required)
    1. Generate 2-3 viable approaches
    2. For each: pros, cons, complexity estimate, risk level
    3. Reason from first principles about WHY one approach is fundamentally
       better (not just 'it's the common pattern')
    4. Recommend one with explicit trade-off documentation

    ### Implementation Plan
    Address: OOP, DRY, Clean Code, Naming, Testability
    Include requirements traceability (map each requirement to plan items)
    Flag risk areas from the blast radius analysis

    ### ADR Output (required)
    Include an Architecture Decision Record:
    - Context: What problem triggered this decision
    - Decision: What we chose and WHY (first-principles reasoning)
    - Alternatives: What we rejected and WHY
    - Trade-offs: What we're accepting and its consequences
    - Chesterton's Fence: If changing existing behavior, WHY it existed

    Use WebSearch if the context package mentions unfamiliar APIs or patterns.
  "
```

2. **Self-critique** the plan inline (you, not another agent):
   - Does it cover every requirement?
   - Any scope creep?
   - Over-engineered anywhere?
   - Missing edge cases?
   - Are the trade-offs of the chosen approach clearly documented?
3. Refine the plan yourself if needed

### FULL Path
1. **Generate**: Launch Opus architect:

```
Task (Opus Architect):
  subagent_type: "system-architect"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at /tmp/se-<task-name>/context-package.md.
    It contains the task spec, research summary, blast radius, and pre-loaded
    file contents. Only use Read/Grep for files NOT already in this package.

    ## Planning Requirements

    ### First-Principles Analysis (required)
    Before proposing solutions, decompose the problem:
    - What are the fundamental operations this feature needs to perform?
    - What are the hard constraints (latency, consistency, data size)?
    - What are the soft constraints (conventions, preferences)?
    - If building from scratch with no legacy, what would the ideal design look like?

    ### Alternatives Analysis (required)
    1. Generate 2-3 viable approaches
    2. For each: pros, cons, complexity estimate, risk level
    3. Reason from first principles about WHY one approach is fundamentally
       better (not just 'it's the common pattern')
    4. Recommend one with explicit trade-off documentation

    ### Implementation Plan
    Address: OOP, DRY, Clean Code, Naming, Testability
    Include requirements traceability (map each requirement to plan items)
    Emphasize architecture decisions and their rationale

    ### ADR Output (required)
    Include an Architecture Decision Record:
    - Context: What problem triggered this decision
    - Decision: What we chose and WHY (first-principles reasoning)
    - Alternatives: What we rejected and WHY
    - Trade-offs: What we're accepting and its consequences
    - Chesterton's Fence: If changing existing behavior, WHY it existed

    Use WebSearch to research best practices before finalizing.
  "
```

2. **Critique**: Launch Sonnet evaluator:

```
Task (Sonnet Critic):
  subagent_type: "system-architect-sonnet"
  prompt: "
    ## Pre-Loaded Context
    Read the context package at /tmp/se-<task-name>/context-package.md.

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
    Read the context package at /tmp/se-<task-name>/context-package.md.

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

### Rollback Strategy (MEDIUM/FULL — document before coding)
```
### Rollback Strategy
- **Pre-deploy**: `git branch -D se/<name>` (discard branch)
- **Post-deploy (if applicable)**: [How to reverse — revert commit,
  feature flag, config change, etc.]
- **Data migration**: [If schema changes: backward-compatible?
  Rollback SQL available?]
- **Dependencies**: [If new deps added: can old version run without them?]
```

### Implementation Approach (ALL tiers — implement directly)

You already have all context from the context package. Implement directly — no subagent needed.

1. Implement items **one at a time**, in dependency order
2. Make edits using Edit/Write tools (parallelize independent edits within an item)
3. Follow existing codebase patterns
4. Apply engineering principles:
   - DRY — no duplicate logic
   - Clean Code — functions < 20 lines, single purpose
   - Naming — intention-revealing names, verb-noun for functions
   - Match existing codebase patterns
5. **Defensive audit** before testing (see detailed checklist below)
6. After **all items** are implemented, run the project's build + test commands:
   ```bash
   # Use the project's build/test commands (e.g., npm run build, go build, cargo build, etc.)
   # Check CLAUDE.md or README for project-specific commands
   ```
7. Fix any compilation/test errors immediately

### Defensive Audit (BEFORE testing)

After implementation, audit your changes for completeness:

1. **Multi-signal/multi-check functions**: If you modified a function that validates via multiple checks
   (e.g., checking text AND selector AND header), audit ALL checks — not just the one you changed.
   Common false-positive sources:
   - `document.body.innerText` includes ALL `<option>` text (not just selected)
   - `[class*="keyword"]` CSS selectors match containers that wrap the actual element
   - `textContent` of parent elements includes all children's text

2. **All callers**: Verify every call site of the changed function handles the new behavior correctly.

3. **Sibling code paths**: If you fixed path A of a switch/if-else, check paths B and C for the same bug class.

**Rule: Fix all instances of a bug pattern in one pass.** Don't fix one, test, discover another, fix, test again.
Each test cycle costs 3-5 minutes of wall time (build + app launch + sync).

**For integration-test-only projects** (no unit tests, must test in running app):
- Write a focused smoke test script that exercises the specific change
- Include diagnostic logging so failures are debuggable in one round

**If build/tests fail**: Fix directly before Phase 5. Do NOT launch validators against broken code.

### Post-Test Cleanup (ALWAYS run after testing)

Tests leave background processes and state that make the app unusable. **Always clean up** after
any test run — whether it passed or failed:

```bash
# Kill test-spawned processes
pkill -f "electron" 2>/dev/null
pkill -f "vite" 2>/dev/null
sleep 2

# Verify nothing is lingering on dev server ports
lsof -i :5173 2>/dev/null && echo "WARNING: port 5173 still in use" || echo "Clean"
```

**Why this matters**: Test frameworks can spawn app instances that may not fully
terminate. Backgrounded dev servers persist across test runs. Leftover processes hold
ports, corrupt IPC state, or block single-instance locks — making the real app unlaunchable
until manually killed.

**Rule**: The user should be able to open their app normally immediately after your test completes.
If you spawned it, you clean it up.

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
  Read the context package at /tmp/se-<task-name>/context-package.md for
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
  Read the context package at /tmp/se-<task-name>/context-package.md.

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
        Re-run: build + test

    ELIF iteration == 2 (FULL only):
        # First-Principles Debug — don't just patch, UNDERSTAND
        - Why did the first fix not work? Trace to root cause.
        - Are we fixing a symptom of a deeper design issue?
        - Re-examine our assumptions: is the original approach
          fundamentally sound, or do we need to rethink?
        - If the design is flawed, propose a pivot to user
          (don't keep patching a broken foundation)
        Re-run: build + test

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

### System Health Delta (MEDIUM/FULL)
| Metric | Before | After | Trend |
|--------|--------|-------|-------|
| Files in module | [N] | [N] | [+/-N] |
| Cyclomatic complexity | [level] | [level] | [Stable/Increased/Decreased] |
| Test coverage | [%] | [%] | [Improved/Same/Degraded] |
| New dependencies | — | [N] | [Clean/Added N] |
| Similar code patterns | [N] | [N] | [No new duplication/+N] |

**Net assessment**: [Healthier / Neutral / Degraded + brief why]

### Rollback Strategy
[From Phase 4 — include final rollback plan here]

### Final Verdict
- **ALL PASS** — All criteria met, all validators passed
- **PASS WITH ITERATIONS** — All criteria met after [N] rounds
- **PARTIAL** — [N] criteria unmet (see Acceptance Test)
```

---

## Phase 8: Knowledge Capture (Retrospective)

**Goal**: Extract and persist institutional knowledge from this task. Takes 30-60 seconds and compounds over time.

### Generalization Rule (MANDATORY)

All MEMORY.md entries MUST be **generic and reusable** — applicable beyond this specific task. Before writing:
1. **Strip specifics**: Remove file names, bug IDs, dates, one-time details
2. **Extract the principle**: What general rule prevents this *class* of problem?
3. **Test**: "Would this help on a completely different bug/feature?" If no, rewrite.

Exception: Architecture notes and file path documentation should stay project-specific.

### First-Principles Learnings
- **What fundamental insight did we gain about this problem domain?** (not just "I learned the API" — what underlying principle?)
- **Were any of our initial assumptions wrong?** Record them to avoid repeating the mistake.

### Pattern Extraction
- Did we discover a reusable pattern? → Update MEMORY.md (as a generic principle, not a specific fix)

### Pitfall Recording
- Did we hit non-obvious issues? → Record in MEMORY.md "Common Pitfalls" (generalized — "always check X before Y", not "file Z had bug W")

### Iteration Analysis
- What caused iteration loops? What validators caught and why? → Record to prevent repeat mistakes

### Codebase Observation
- Tech debt or improvement opportunities noticed outside scope? → Note briefly (don't fix — record for future)

### ADR Persistence (MEDIUM/FULL)
- If an ADR was generated during planning, verify it was written to `docs/decisions/` (or the project's ADR directory). If no ADR directory exists, note the decision in MEMORY.md instead.

---

## Execution Rules

1. **First-principles FIRST** — Phase -1 challenges the premise before committing compute
2. **Classify complexity early** — Phase 0.5 determines your entire execution path
3. **Build the context package** — Phase 1.5 is the biggest token saver. Do it well.
4. **Include the pre-loaded context instruction** in EVERY subagent prompt
5. **Include the diff inline** for EVERY validator — they should NOT re-run git diff
6. **NEVER skip user review** — Phase 3 is mandatory
7. **Smoke test before validation** — Build + test before launching validators
8. **Run independent agents IN PARALLEL** — Single message, multiple Task calls
9. **Code-simplifier runs ONCE at end** — Not after every implementation item
10. **Circuit breaker on iteration** — Same failure twice = stop and escalate
11. **Announce tier and agent count** — User should know the efficiency gains
12. **Document WHY, not just WHAT** — Alternatives and trade-offs in planning (MEDIUM/FULL)
13. **Capture knowledge** — Phase 8 retrospective updates MEMORY.md. Never skip.

## When to Recommend /staff-engineer Instead

If during Phase 0.5 you realize the task has:
- Fundamental architectural uncertainty that needs true dual-model debate
- 20+ file blast radius with cross-cutting concerns across multiple systems
- Multiple stakeholder concerns (security + performance + compliance + API design)

...recommend the user switch to `/staff-engineer` for the full treatment. But default to `/se` — most tasks are LIGHT or MEDIUM.

## Token Budget Targets

Phase -1 and Phase 8 add ~500-1000 tokens each (inline reasoning, no agents). Net impact is minimal.

| Tier | /se Target | /staff-engineer | Savings |
|------|-----------|-----------------|---------|
| Light | 30-50K | 200-250K | 4-7x |
| Medium | 45-75K | 250-300K | 3-5x |
| Full | 90-165K | 300-450K | 2-4x |
