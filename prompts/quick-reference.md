# Agent System - Quick Reference

## Workflow Keywords (for Orchestrator)
```
full-review      → security + lint + verify + perf
pre-deploy       → security + deps + architect + tests
new-feature      → explore + architect + api-design
security-audit   → fortress + reviewer + deps
code-quality     → lint + verify + refactor + tests
trading-review   → quant + security + perf
documentation    → docs + api-design + explore
deep-analysis    → architect + explore + perf + security
staff-engineer   → Full lifecycle implementation
```

## Primary Routing
```
Default for generic coding tasks → staff-engineer
Legacy generic skills            → explicit user request only
Specialized/tooling skills       → route when domain/tool clearly matches
```

## Domain Specialist Routing
```
Database task?      → database-specialist
Frontend/React?     → frontend-specialist
Electron app?       → electron-specialist
LLM integration?    → llm-specialist
RAG system?         → rag-specialist
CI/CD/DevOps?       → devops-specialist
Real-time feature?  → realtime-specialist
Search feature?     → search-specialist
API integration?    → api-integration-specialist
Trading algo?       → quant-trading-engineer
```

## Staff Engineer v2 - Complexity Routing
```
Simple (1-2 files)     → Plan → Implement → Lint/Test
Medium (3-5 files)     → Research → Plan → Commit loop → Validate
Complex (6+ files)     → Research → Debate? → Plan → Approve → Commit loop → Full validate
```

## Plan Checklist Format
```
- [ ] [Action] in `[file:line]` → commit: `type(scope): msg`
```

## Codex CLI Fast Path
```bash
# Non-interactive implementation run
codex exec "Implement X in src/foo.ts and run targeted tests"

# Non-interactive code review
codex review --help

# Enable live web research when recency matters
codex --search

# Continue prior context quickly
codex resume --last

# Apply latest generated patch to git working tree
codex apply
```

## Commit Protocol
```bash
# Before commit: lint ✓ typecheck ✓ tests ✓
git add [specific files]
git commit -m "type(scope): description"
# Types: feat|fix|refactor|test|docs|chore|migrate
```

## Rollback Commands
```bash
git reset --soft HEAD~1        # Undo last commit, keep staged
git restore --staged [file]    # Unstage specific file
git restore [file]             # Discard unstaged changes in one file
git stash -m "WIP: desc"       # Save work in progress
# Use hard reset only with explicit user approval
```

## Validation Matrix
```
Types only       → typecheck
Pure function    → typecheck + unit test
API endpoint     → typecheck + lint + unit + integration + security?
Auth changes     → ALL validators
DB queries       → typecheck + tests + perf check
New dependency   → dep audit + security
```

## Stuck Protocol
```
3 failures same issue → STOP
1. Stash/commit WIP
2. Report: Issue + Attempts + Analysis + Options
3. WAIT for user choice
4. Reset to safe state
5. Try chosen approach
```

## Handoff Format
```json
{
  "status": "ready_for_implementation",
  "files_to_create": [{"path": "...", "content": "..."}],
  "files_to_modify": [{"path": "...", "changes": "..."}],
  "rollback_plan": "...",
  "validation_needed": ["security-reviewer"]
}
```

## Phase Flow
```
┌─────────────────────────────────────────────────┐
│ 0.Triage → 1.Research → 2.Debate?               │
│     ↓                                           │
│ 3.Plan → 4.Approve → 5.Implement                │
│                         ↓                       │
│            ┌────────────┴────────────┐          │
│            ↓                         ↓          │
│         PASS                      FAIL          │
│            ↓                         ↓          │
│      6.Validate              7.Stuck Proto      │
│            ↓                         ↓          │
│       8.Summary              Fix→Retry(3x)      │
│                                     ↓           │
│                              Report→User        │
└─────────────────────────────────────────────────┘
```

## Core Agents
| Agent | Use For |
|-------|---------|
| staff-engineer | Full implementation |
| system-architect | Design, impact analysis |
| deep-research | Context gathering |
| codebase-explorer | Project mapping |
| security-fortress | Full security audit |
| security-reviewer | Code security review |
| performance-analyzer | Perf bottlenecks |
| test-generator | Test creation |
| change-validator-linter | Lint/validate |
| change-verifier | Change verification |

## Key Rules
1. Require plan approval for complex/high-risk tasks
2. Never skip validation
3. Commit only when tests pass
4. Always know how to rollback
5. Stop at 3 failures, don't spiral
6. Match validation to change type
7. Checkpoint on complex tasks
8. Delegate to specialists for domain expertise
