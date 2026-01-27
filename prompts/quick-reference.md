# Staff Engineer - Quick Reference

## Complexity Routing
```
Simple (1-2 files)     → Plan → Implement → Lint/Test
Medium (3-5 files)     → Research → Plan → Commit loop → Validate  
Complex (6+ files)     → Research → Plan → Approve → Commit loop → Full validate
```

## Plan Checklist Format
```
- [ ] [Action] in `[file:line]` → commit: `type(scope): msg`
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
git reset --soft HEAD~1     # Undo commit, keep staged
git reset HEAD~1            # Undo commit, keep unstaged
git checkout -- .           # Discard uncommitted
git reset --hard [hash]     # Return to commit
git stash -m "WIP: desc"    # Save work in progress
```

## Validation Matrix
```
Types only       → typecheck
Pure function    → typecheck + unit test
API endpoint     → typecheck + lint + unit + integration + security?
Auth changes     → ALL
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

## Phase Flow
```
┌─────────────────────────────────────────────┐
│ 0.Triage → 1.Research → 2.Plan             │
│     ↓                                       │
│ 3.Approve → 4.Implement                     │
│                 ↓                           │
│        ┌───────┴───────┐                    │
│        ↓               ↓                    │
│      PASS           FAIL                    │
│        ↓               ↓                    │
│   5.Validate    6.Stuck Proto               │
│        ↓               ↓                    │
│   7.Summary     Fix→Retry(3x)               │
│                       ↓                     │
│                 Report→User                 │
└─────────────────────────────────────────────┘
```

## Key Rules
1. Never implement without plan approval
2. Never skip validation
3. Commit only when tests pass
4. Always know how to rollback
5. Stop at 3 failures, don't spiral
6. Match validation to change type
```
