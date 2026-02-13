---
name: staff-engineer
description: Full-lifecycle engineering workflow with deep research, evaluator-optimizer planning, blast-radius analysis, conditional validation, and tiered iteration. Use for significant features, architectural changes, or any task that needs "the full engineering treatment."
argument-hint: Description of the feature or task to implement
---

# Staff Engineer Workflow

You are executing the Staff Engineer workflow — a multi-phase engineering process that coordinates specialized subagents to deliver high-quality implementations efficiently.

## Task

$ARGUMENTS

## Core Principles

- **Clarify before researching**: Refine the task into a precise, unambiguous spec before anything else
- **Dual-track research**: Codebase exploration and external web research (design patterns, tech blogs, architecture references) run in parallel
- **Feasibility gate**: Surface blockers early before spending compute on planning
- **Evaluator-optimizer planning**: Opus generates, Sonnet critiques, Opus refines (not parallel independent plans — research shows that degrades sequential tasks 39-70%)
- **Context compression**: Summarize research and plan outputs before passing downstream to prevent context overflow
- **User review checkpoint**: NEVER implement without explicit user approval
- **Blast-radius analysis**: Map impact before coding so validators know where to focus
- **Git safety**: Always work on a feature branch so changes are isolated and rollback-friendly
- **Smoke test before validation**: Verify the build/tests pass before launching validation agents
- **Conditional validation**: Only activate validators relevant to the change type
- **Tiered iteration**: Cheap fixes first (Sonnet), expensive fixes second (Opus), human escalation third
- **Acceptance testing**: Verify success criteria from Phase 0 are met at the end
- **Thread the spec**: Pass the Refined Task Specification to ALL downstream phases
- **Use TodoWrite**: Track all phases and progress throughout

---

## Phase -1: First-Principles Strategic Filter

**Goal**: Decompose the request to its fundamentals before investing compute. Ensure we're solving the RIGHT problem.

### 1. Problem Decomposition (First Principles)
- **What is the user ACTUALLY trying to achieve?** (not what they asked for — what outcome do they need?)
- **What are the fundamental constraints?** (physics of the problem: data flow, latency requirements, consistency needs)
- **Which constraints are REAL vs. ASSUMED?** (inherited conventions ≠ hard requirements. Challenge: "we do it this way because we always have")

### 2. Solution Validation
- **Root cause or symptom?** If this is patching a symptom, identify the root cause and surface it to the user
- **Simplest possible solution?** Could we solve this by removing code, changing config, or doing nothing? The best code is no code.
- **Chesterton's Fence**: If changing existing behavior, do we understand WHY it was built that way? If not, find out before changing it.

### 3. Strategic Check
- **Opportunity cost**: Is this the highest-leverage work right now?
- **Second-order effects**: What does this change make easier or harder in the future?

If any red flags → surface to user with your reasoning before proceeding.
If all clear → proceed to Phase 0 with your decomposition as context.

---

## Phase 0: Discovery & Prompt Refinement

**Goal**: Transform the user's raw request into a precise, comprehensive task specification.

**Actions**:
1. Create todo list with all phases (-1 through 9)
2. Analyze the raw request and identify what's clear, ambiguous, and missing
3. **Present your analysis AND ask clarifying questions in a single interaction:**

```
## Task Analysis

### What I Understand
- [Explicit requirements the user stated]

### Questions Before I Proceed

**Scope:**
- [Question about boundaries — what's in vs. out?]

**Behavior:**
- [Question about how it should work, edge cases]

**Constraints:**
- [Question about limitations, compatibility, performance]

If any of these are "whatever you think is best", just say so.
```

4. **WAIT for user answers.** Do NOT proceed until the user responds.

5. Synthesize AND present the **Refined Task Specification** for confirmation:

```
## Refined Task Specification

### Summary
[One clear sentence describing what will be built]

### Requirements
1. [Requirement 1 — explicit]
2. [Requirement 2 — clarified from user answers]

### Scope
- **In scope**: [what we're building]
- **Out of scope**: [what we're NOT building]

### Constraints
- [Constraint 1]

### Success Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

Does this capture what you want?
```

6. **WAIT for confirmation.** Then use this refined spec for ALL subsequent phases.

---

## Phase 1: Dual-Track Research (Parallel) + Feasibility Gate

**Goal**: Simultaneously gather codebase context AND external design knowledge.

**Actions**:
1. Launch BOTH research tracks IN PARALLEL (single message, two Task calls):

```
Task 1 (Codebase Research):
  subagent_type: "deep-research"
  prompt: "
    Focus on CODEBASE analysis only (no web research — a parallel agent handles that).
    Use subagents for thorough exploration.

    ## Refined Task Specification
    [FULL SPEC]

    Deliverables:
    - Codebase architecture analysis
    - Relevant files and existing patterns (with file:line references)
    - How similar features are implemented in this codebase
    - Technical constraints (framework limits, API contracts, DB schema)
    - Dependency map (what this change touches, what depends on it)
    - Gap analysis (current → desired)
    - Feasibility assessment: blockers, risks
    - 5-10 key files to read (INCLUDE key file contents in your output
      so downstream agents don't need to re-read them)
  "

Task 2 (External Research):
  subagent_type: "deep-research"
  prompt: "
    Focus EXCLUSIVELY on web research. Do NOT explore the codebase.
    Use WebSearch and WebFetch extensively.

    ## Refined Task Specification
    [FULL SPEC]

    Research thoroughly:

    ### 1. Design Patterns
    - GoF patterns, architectural patterns (Repository, CQRS, etc.), domain-specific patterns
    - Search: '[problem type] design pattern', '[technology] [feature] pattern'

    ### 2. Clean Code & Architecture References
    - SOLID application, Clean Architecture, guidance from Fowler/Martin/Beck
    - Search: 'clean code [feature type]', 'SOLID principle [problem]'

    ### 3. Real-World Implementations
    - Tech blog posts from companies that solved similar problems
    - Open source implementations
    - Search: '[company] engineering blog [feature]', 'github [feature] [language]'

    ### 4. Framework/Library Best Practices
    - Official docs, recommended patterns, anti-patterns to avoid

    ### 5. Trade-off Analysis
    - How teams chose between approaches, scaling considerations

    Deliverables (with source URLs):
    - Applicable Design Patterns (name, why it fits, reference URL)
    - Architecture Recommendations (with citations)
    - Real-World Examples (blog links with brief summary)
    - Anti-Patterns to Avoid (with sources)
    - Framework-Specific Guidance
    - Recommended Approach (synthesis citing sources)
  "
```

2. Wait for BOTH to complete
3. Read key files identified by codebase research
4. **Context Compression**: Summarize both outputs into a **Unified Research Brief** (target: 2000-3000 tokens). Keep the full outputs available but pass only the brief to downstream agents:

```
## Unified Research Brief

### Codebase Summary
- Architecture: [type]
- Key patterns: [list with file refs]
- Constraints: [top 3-5]
- Key files: [list]

### External Research Summary
- Recommended patterns: [pattern] (source: [url])
- Anti-patterns: [list]
- Architecture approach: [recommendation with citation]

### Feasibility: [GO / CONCERN: details]
```

5. **Feasibility Gate**: If research reveals blockers, present to user with options before continuing.

---

## Phase 2: Evaluator-Optimizer Planning

**Goal**: Generate a high-quality implementation plan through structured critique-and-refine cycles (not parallel independent generation — DeepMind research shows that degrades sequential tasks).

**Actions**:
1. **Cycle 1 — Generate**: Launch Opus architect to create the initial plan:

```
Task (Opus Architect):
  subagent_type: "system-architect"
  prompt: "
    ## Refined Task Specification
    [FULL SPEC]

    ## Unified Research Brief
    [COMPRESSED RESEARCH FROM PHASE 1]

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
    - Reference specific design patterns from the research
    - Cite architecture decisions with sources
    - Avoid anti-patterns identified in research
    - Address OOP, DRY, Clean Code, Naming, Testability
    - Include a requirements traceability matrix
    - Ensure the plan satisfies ALL success criteria

    ### ADR Output (required)
    Include an Architecture Decision Record:
    - Context: What problem triggered this decision
    - Decision: What we chose and WHY (first-principles reasoning)
    - Alternatives: What we rejected and WHY
    - Trade-offs: What we're accepting and its consequences
    - Chesterton's Fence: If changing existing behavior, WHY it existed
  "
```

2. **Cycle 1 — Critique**: Launch Sonnet to evaluate the plan:

```
Task (Sonnet Critic):
  subagent_type: "system-architect-sonnet"
  prompt: "
    ## Refined Task Specification (source of truth)
    [FULL SPEC]

    ## Plan to Critique
    [OPUS_PLAN]

    Evaluate against:
    1. Requirements coverage — does it address every requirement?
    2. Scope compliance — any scope creep?
    3. Success criteria — can this plan satisfy each criterion?
    4. Coding principles — OOP/SOLID, DRY, Clean Code violations?
    5. Over-engineering — anything unnecessarily complex?
    6. Missing edge cases — what could go wrong?
    7. Feasibility — is this realistic given the codebase?

    Output a structured critique with specific, actionable feedback.
  "
```

3. **Cycle 2 — Refine**: If the critique has substantive issues, have Opus refine:

```
Task (Opus Refinement):
  subagent_type: "system-architect"
  prompt: "
    ## Original Plan
    [OPUS_PLAN]

    ## Critique
    [SONNET_CRITIQUE]

    Refine the plan addressing each critique point. Mark what changed and why.
    If a critique point is wrong, explain why you're keeping the original approach.
  "
```

4. **Early Exit**: If Sonnet's critique has no substantive issues (only minor suggestions), skip the refinement cycle and proceed.

5. **Compress the final plan** to a focused implementation spec before passing downstream.

---

## Phase 3: Visual Summary + User Review

**Goal**: Present the plan clearly and get user approval before implementation.

**CRITICAL: DO NOT SKIP. NEVER IMPLEMENT WITHOUT APPROVAL.**

**Actions**:
1. Launch plan-visualizer:

```
Task(subagent_type="plan-visualizer", prompt="
  Create a visual summary of this engineering plan:
  [FINAL_PLAN]")
```

2. Present the visual summary to the user
3. Ask for approval:

```
## Ready for Implementation

**Options:**
- **"Go ahead"** — I'll create a feature branch and start implementing
- **"Changes needed"** — Tell me what to adjust
- **"Stop"** — Halt the workflow
```

4. **WAIT for explicit approval.**

---

## Phase 4: Blast-Radius Analysis + Implementation

**Goal**: Map impact, then implement safely on a feature branch.

### 4a. Git Safety
```bash
git checkout -b staff-eng/<short-task-name>
```

### 4a.1. Rollback Strategy (document before coding)
```
### Rollback Strategy
- **Pre-deploy**: `git branch -D staff-eng/<name>` (discard branch)
- **Post-deploy (if applicable)**: [How to reverse — revert commit,
  feature flag, config change, etc.]
- **Data migration**: [If schema changes: backward-compatible?
  Rollback SQL available?]
- **Dependencies**: [If new deps added: can old version run without them?]
```

### 4b. Blast-Radius Analysis
Launch the blast-radius-analyzer to map impact BEFORE coding:

```
Task(subagent_type="blast-radius-analyzer", prompt="
  ## Implementation Plan
  [FINAL_PLAN]

  Analyze the blast radius of these planned changes.
  Map affected files, tests, dependencies, and API contracts.
  Flag uncovered code and breaking changes.
  Identify which validators should focus where.
")
```

Save the blast-radius report — it will be passed to validators in Phase 5.

### 4c. Implementation
Launch ralph-implementer:

```
Task(subagent_type="ralph-implementer", prompt="
  ## Refined Task Specification
  [FULL SPEC — so implementer knows success criteria]

  ## Implementation Plan
  [FINAL_PLAN]

  ## Blast-Radius Report
  [BLAST_RADIUS_OUTPUT — so implementer knows high-risk areas]

  ### Items to Implement
  1. [Item 1]
  2. [Item 2]
  ...

  ### Implementation Rules
  - OOP/SOLID principles enforced
  - DRY — no duplicate code
  - Clean Code — functions < 20 lines, single purpose
  - Naming — intention-revealing names, verb-noun for functions
")
```

### 4d. Build & Test Smoke Check
```bash
# Run the project's build and test commands
npm run build && npm test   # adapt to project
```

**If build/tests fail**: Fix directly before Phase 5. Do NOT launch validators against broken code.

---

## Phase 5: Conditional Validation

**Goal**: Verify the implementation, activating only relevant validators based on the blast-radius report.

**Actions**:
1. **Always run** (these are cheap and universal):
   - `change-validator-linter` (Sonnet) — lint and static analysis
   - `change-verifier` (Sonnet) — design pattern alignment

2. **Conditionally run** based on blast-radius report:
   - `test-generator` (Sonnet) — IF blast-radius flagged uncovered code
   - `security-fortress` (Opus) — IF changes touch auth, crypto, user data, payments, or config
   - `performance-analyzer` (Sonnet) — IF changes touch hot paths, DB queries, or loops
   - `docs-generator` (Haiku) — IF changes modify public APIs or create new modules

3. Pass the blast-radius report AND refined spec to each validator so they know WHERE to focus:

```
Task: subagent_type="change-validator-linter"
  prompt: "
    ## Refined Task Specification
    [SPEC]
    ## Blast-Radius Report (focus areas)
    [BLAST_RADIUS]
    Validate and lint all changes on branch staff-eng/<name>."

Task: subagent_type="security-fortress"  (instead of security-reviewer)
  prompt: "
    ## Refined Task Specification
    [SPEC]
    ## Blast-Radius Report (security-relevant areas)
    [BLAST_RADIUS]
    Review implemented changes for security issues.
    Focus on: [high-risk areas from blast-radius]"

(similar for other activated validators)
```

4. Launch all activated validators IN PARALLEL
5. Collect results, aggregate, deduplicate

---

## Phase 6: Tiered Iteration Loop

**Goal**: Fix validation failures efficiently using the cheapest effective approach.

**Logic**:
```
iteration = 0
MAX = 3

while any_failures AND iteration < MAX:
    iteration += 1

    IF iteration == 1:
        # Round 1: Cheap fixes (Sonnet-level reasoning)
        Fix issues directly using straightforward corrections
        Re-run build/test smoke check

    ELIF iteration == 2:
        # Round 2: First-Principles Debug — don't just patch, UNDERSTAND
        - Why did the first fix not work? Trace to root cause.
        - Are we fixing a symptom of a deeper design issue?
        - Re-examine our assumptions: is the original approach
          fundamentally sound, or do we need to rethink?
        - If the design is flawed, propose a pivot to user
          (don't keep patching a broken foundation)
        Re-run build/test smoke check

    ELIF iteration == 3:
        # Round 3: Human escalation
        Present remaining issues to user with detailed context:
        "These issues resisted 2 fix attempts. Options:
         1. I'll try a different approach: [suggest alternative]
         2. Accept as-is with known issues
         3. You fix manually and I'll re-validate"

    # Re-run ONLY failing validators
    # Circuit breaker: if same validation fails 2x with identical error, skip it
    #   and flag for human review
```

**Circuit Breaker**: If no progress between rounds (same failures), stop iterating and report.

---

## Phase 7: Checkpoint & Recovery

**Between phases, persist state so we can resume on failure:**

```
## Checkpoint: Phase [N] Complete

### Artifacts Produced
- Refined spec: [stored in conversation]
- Research brief: [compressed summary]
- Implementation plan: [compressed summary]
- Blast-radius report: [key findings]
- Git branch: staff-eng/<name>
- Validation results: [summary]

### To Resume From Here
If the workflow failed, you can resume from Phase [N+1]
with the artifacts above.
```

This is NOT a separate user-facing phase — it's an internal practice. After each major phase, briefly note what was produced so context is recoverable.

---

## Phase 8: Final Summary + Acceptance Testing

**Goal**: Verify success criteria, document everything.

**Actions**:
1. Mark all todos complete
2. **Acceptance Test** — check each criterion from Phase 0:

```
## Acceptance Testing

### Success Criteria Results
- [x] [Criterion 1] — PASS: [evidence]
- [x] [Criterion 2] — PASS: [evidence]
- [ ] [Criterion 3] — FAIL: [what's missing]
```

3. Present summary:

```
## Staff Engineer Workflow Complete

### Task
[One-sentence summary]

### Acceptance Test
| Criterion | Status | Evidence |
|-----------|--------|----------|
| [criterion] | PASS/FAIL | [verification] |

### Changes Made
| File | Change | Description |
|------|--------|-------------|

### Branch
`staff-eng/<name>`
- Merge: `git checkout main && git merge staff-eng/<name>`
- Discard: `git branch -D staff-eng/<name>`

### Validation Results
| Check | Status | Model | Notes |
|-------|--------|-------|-------|
| Lint | PASS/FAIL | Sonnet | |
| Design Patterns | PASS/FAIL | Sonnet | |
| Tests | PASS/FAIL | Sonnet | |
| Security | PASS/FAIL | Opus | |
| Performance | PASS/FAIL | Sonnet | |
| Docs | PASS/FAIL | Haiku | |

### Iteration Summary
| Round | Approach | Fixed | Remaining |
|-------|----------|-------|-----------|
| 1 | Direct fix | [N] | [N] |
| 2 | Deep analysis | [N] | [N] |
| 3 | Human escalation | [N] | [N] |

### System Health Delta
| Metric | Before | After | Trend |
|--------|--------|-------|-------|
| Files in module | [N] | [N] | [+/-N] |
| Cyclomatic complexity | [level] | [level] | [Stable/Increased/Decreased] |
| Test coverage | [%] | [%] | [Improved/Same/Degraded] |
| New dependencies | — | [N] | [Clean/Added N] |
| Similar code patterns | [N] | [N] | [No new duplication/+N] |

**Net assessment**: [Healthier / Neutral / Degraded + brief why]

### Rollback Strategy
[From Phase 4a.1 — include final rollback plan here]

### Final Verdict
- **ALL PASS** — All criteria met, all validators passed
- **PASS WITH ITERATIONS** — All criteria met after [N] rounds
- **PARTIAL** — [N] criteria unmet (see Acceptance Test)

### Compute Efficiency
- Validators activated: [N] of 6 (conditional activation saved [N] agent calls)
- Iteration rounds used: [N] of 3
- Models used: Opus ([N] calls), Sonnet ([N] calls), Haiku ([N] calls)
```

---

## Phase 9: Knowledge Capture (Retrospective)

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

### ADR Persistence
- If an ADR was generated during planning, verify it was written to `docs/decisions/` (or the project's ADR directory). If no ADR directory exists, note the decision in MEMORY.md instead.

---

## Execution Rules

1. **First-principles FIRST** — Phase -1 challenges the premise before committing compute
2. **Thread the refined spec** — Pass the FULL spec to every subagent
3. **Compress context between phases** — Summarize outputs before passing downstream; keep full outputs available but don't flood subagent prompts
4. **Run independent agents in PARALLEL** — Single message, multiple Task calls
5. **NEVER skip user review** — Phase 3 is mandatory
6. **Git branch isolation** — Create feature branch before implementation
7. **Document rollback strategy** — Phase 4a.1 before any code changes
8. **Blast-radius before coding** — Run impact analysis to focus validators
9. **Smoke test before validation** — Build + test before launching validators
10. **Conditional validation** — Only activate relevant validators based on blast-radius
11. **Tiered iteration with first-principles debug** — Cheap fixes first, root-cause analysis second, human third
12. **Circuit breaker** — No progress after 2 identical failures → stop and escalate
13. **Checkpoint state** — Note key artifacts after each phase for recovery
14. **Acceptance test at the end** — Verify every success criterion from Phase 0
15. **Document WHY, not just WHAT** — Alternatives and trade-offs in planning (ADR)
16. **Capture knowledge** — Phase 9 retrospective updates MEMORY.md. Never skip.
17. **Use the right model** — Opus for planning/architecture, Sonnet for validation/review, Haiku for docs/exploration
