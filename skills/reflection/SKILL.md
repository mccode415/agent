---
name: reflection
description: "Post-session retrospective that analyzes what went well and what needs improvement. Produces actionable findings and optionally updates skills, MEMORY.md, or CLAUDE.md based on lessons learned."
argument-hint: "Optional: specific skill or area to reflect on (e.g., 'se-team', 'debugging', 'testing')"
---

# Session Reflection (`/reflection`)

You are running a structured retrospective on the current session. The goal is to extract actionable lessons that improve future sessions — not just list observations.

## Input

$ARGUMENTS

If a specific skill is mentioned, focus the reflection on how that skill performed. Otherwise, reflect on the full session.

## Reflection Framework

Work through these sections in order. Be brutally honest — the point is improvement, not self-congratulation.

### Phase 1: Session Reconstruction

Reconstruct the timeline of what happened:

1. **Read the conversation context** — scan for key decision points, errors, retries, and user frustrations
2. **Map the causal chain**: What was attempted → What happened → What was the response → How long did it take
3. **Identify iteration loops**: Places where the same type of action was repeated 2+ times before success

### Phase 2: Analysis (use these exact headers in output)

#### What Went Well
- Things that worked on the first try
- Good architectural decisions
- Effective debugging approaches
- Time saved by good practices

#### What Went Wrong
- Errors that required multiple fix attempts
- Root causes that were missed initially
- Time wasted on wrong approaches
- User friction points (had to ask twice, expressed frustration)

#### Root Cause Analysis
For each "what went wrong" item, ask **why** 3 times:
```
Problem: [what happened]
  → Why? [immediate cause]
    → Why? [deeper cause]
      → Why? [systemic cause / skill gap / missing check]
```

#### Skill/Workflow Gaps
- Which skill phases were skipped or ineffective?
- Where did the workflow diverge from the skill's instructions?
- What checks would have caught the issue earlier?

#### Wasted Cycles
- Compute/time spent on things that didn't contribute to the outcome
- Unnecessary agent spawns or file reads
- Tests that needed to run multiple times due to infrastructure issues

### Phase 3: Actionable Recommendations

For each finding, produce a specific, implementable recommendation:

```
FINDING: [one-sentence description]
IMPACT: [high/medium/low] — how much time/quality this would save
FIX TYPE: [skill-update | memory-update | claude-md-update | new-check | process-change]
SPECIFIC CHANGE: [exact text to add/modify, or exact check to implement]
WHERE: [file path and section to update]
```

#### Where to Put It: Memory vs. Skill vs. CLAUDE.md

Route each finding to the right place using this decision tree:

```
Is this about HOW a workflow/skill should operate?
  (e.g., "the skill should check X before Y", "Phase 3 should include a validation step")
  → YES → skill-update (modify the skill file that governs this workflow)

Is this a project-specific fact? (architecture, file paths, API patterns, tool configs)
  → YES → memory-update (MEMORY.md — keep it specific, this IS documentation)

Is this a reusable debugging/engineering principle?
  (e.g., "trace data pipelines before fixing symptoms", "commit only after E2E verification")
  → YES → memory-update (MEMORY.md — but generalize it, strip specifics)

Is this a user preference or project-wide rule?
  (e.g., "never use /fast", "always test in Electron context")
  → YES → claude-md-update or memory-update depending on scope
```

**Key distinction**: Skills define *process* (steps, checks, decision points). Memory stores *knowledge* (facts, principles, patterns). If a finding reveals a missing step or check in a workflow, fix the skill. If it reveals a reusable insight, add it to memory.

**When both apply**: A finding like "we should have traced the data pipeline first" means:
- **Skill update**: Add a "trace data pipeline" check to the relevant skill phase (e.g., Phase -1 or Phase 1)
- **Memory update**: Record the generic principle ("trace pipelines before fixing symptoms")

Always consider both. Don't just dump everything into memory when the skill itself should be improved.

### Phase 4: Apply Changes

#### Generalization Rule (MANDATORY for memory/skill lesson entries)

Lessons and debugging patterns written to MEMORY.md or skills MUST be **generic and reusable** — applicable to future sessions on different bugs, features, and codebases. Before writing any lesson entry:

1. **Strip specifics**: Remove file names, bug IDs, dates, variable names, and one-time details
2. **Extract the principle**: What general rule would have prevented this class of problem?
3. **Test generality**: "Would this help someone working on a completely different part of the codebase?" If no, rewrite it.

**Bad** (too specific):
> "The Recology parser regex failed on 'CAI, MATTHEW' because it didn't handle spaces after commas"

**Good** (generic principle):
> "When parsing text extracted from PDFs, never assume exact whitespace — output varies by generator. Use flexible whitespace matching."

**Bad**:
> "intelligent-navigator.ts caused 8 context compactions because it's 7000 lines"

**Good**:
> "Read only relevant line ranges of large files, not entire files. Each unnecessary full-file read accelerates context compaction."

Exception: Project-specific facts (architecture notes, file paths, API patterns) in MEMORY.md should stay specific — the generalization rule applies to **lessons and patterns**, not factual documentation.

#### Applying Updates

For **skill updates**:
1. Read the target skill file
2. Identify the specific phase/section where the process gap exists
3. Add the missing check, step, or decision point (use Edit tool, not full rewrite)
4. Verify the change fits the skill's existing structure and doesn't conflict
5. Summarize what changed and why

For **memory updates**:
1. Read MEMORY.md
2. Route entry to the correct section (Debugging Patterns, Common Pitfalls, Architecture, etc.)
3. Apply the Generalization Rule — rewrite any specific findings as generic principles
4. Keep entries concise and actionable

For **both** (common case):
1. Update the skill to prevent the process failure
2. Add a generic principle to MEMORY.md as a safety net
3. The skill change is the primary fix; the memory entry is backup context

## Output Format

```
# Session Reflection: [session date]

## Timeline Summary
[3-5 bullet chronological summary]

## What Went Well
- [item with evidence]

## What Went Wrong
- [item with root cause chain]

## Recommendations
| # | Finding | Impact | Fix Type | Status |
|---|---------|--------|----------|--------|
| 1 | [finding] | high | skill-update | applied/pending |

## Changes Applied
- [file]: [what changed]
```

## Principles

- **Evidence over opinion**: Cite specific moments from the session
- **Systemic over symptomatic**: Fix the process, not just the instance
- **Concise over comprehensive**: 5 actionable items > 20 observations
- **Honest over flattering**: If the skill workflow was ignored, say so
- **Forward-looking**: Frame findings as "next time, do X" not "should have done X"
