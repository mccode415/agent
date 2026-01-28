# Handoff Protocol

How agents pass work to each other in multi-agent workflows.

---

## Handoff Document Structure

When one agent hands off to another, include:

```markdown
# Handoff: [Source Agent] → [Target Agent]

## Context
**Task:** [Original task description]
**Phase:** [Current phase in workflow]
**Complexity:** [Simple/Medium/Complex]

## Work Completed
- [What source agent accomplished]
- [Artifacts created: files, commits, etc.]

## Current State
- **Branch:** [git branch]
- **Last Commit:** [hash] - [message]
- **Files Changed:** [list]
- **Tests:** [passing/failing]

## Handoff Payload
[Specific data the target agent needs]

## Expected Output
[What target agent should produce]

## Constraints
- [Any limits or requirements]

## Return To
[Which agent to return to after completion]
```

---

## Common Handoff Patterns

### 1. Staff Engineer → Validation Agents

```markdown
# Handoff: staff-engineer → validation-suite

## Context
**Task:** Add OAuth authentication
**Phase:** Implementation complete, validation needed
**Complexity:** Medium

## Work Completed
- OAuth client implemented
- API endpoints added
- Unit tests written
- 5 commits on feat/oauth branch

## Current State
- **Branch:** feat/oauth
- **Last Commit:** abc1234 - "test(auth): add OAuth unit tests"
- **Files Changed:**
  - src/services/oauth-client.ts (new)
  - src/routes/auth.ts (modified)
  - src/types/auth.ts (modified)
- **Tests:** All passing

## Handoff Payload
```json
{
  "files_to_validate": [
    "src/services/oauth-client.ts",
    "src/routes/auth.ts"
  ],
  "change_type": ["auth", "api"],
  "has_tests": true,
  "has_migrations": false
}
```

## Expected Output
Validation report with:
- Security scan results
- Lint/type check results
- Test coverage
- Performance notes

## Constraints
- Run security checks (auth-related code)
- Skip performance deep-dive (no DB changes)

## Return To
staff-engineer (for fix iteration or summary)
```

### 2. Orchestrator → Research Agent

```markdown
# Handoff: orchestrator → deep-research

## Context
**Task:** Implement payment processing
**Phase:** Pre-planning research
**Complexity:** Complex

## Work Completed
- Task received from user
- Complexity assessed as Complex

## Current State
- **Branch:** main (no changes yet)
- **Files Changed:** none

## Handoff Payload
```json
{
  "task": "Implement Stripe payment processing",
  "focus_areas": [
    "existing payment code",
    "user model",
    "order/checkout flow",
    "environment config"
  ],
  "external_research": [
    "Stripe API best practices",
    "PCI compliance requirements"
  ]
}
```

## Expected Output
Research document with:
- Relevant files mapped
- Patterns identified
- Integration points
- External best practices
- Constraints discovered

## Return To
orchestrator (for planning phase)
```

### 3. Research → Architect

```markdown
# Handoff: deep-research → system-architect

## Context
**Task:** Implement payment processing
**Phase:** Planning
**Complexity:** Complex

## Work Completed
- Codebase explored
- Relevant files identified
- Patterns documented
- External research done

## Handoff Payload
```json
{
  "research_summary": "[full research document]",
  "key_files": [
    {"path": "src/services/order.ts", "relevance": "checkout flow"},
    {"path": "src/models/user.ts", "relevance": "payment methods"}
  ],
  "patterns": [
    {"name": "service pattern", "example": "src/services/auth.ts"}
  ],
  "constraints": [
    "Must support multiple payment methods",
    "PCI compliance required"
  ],
  "external_findings": [
    "Use Stripe PaymentIntents API",
    "Implement idempotency keys"
  ]
}
```

## Expected Output
Implementation plan with:
- Architecture decisions
- File changes planned
- Component design
- Risk assessment

## Return To
orchestrator (for plan synthesis)
```

### 4. Validation Agent → Staff Engineer (Failure)

```markdown
# Handoff: security-fortress → staff-engineer

## Context
**Task:** Add OAuth authentication
**Phase:** Validation failed - needs fixes
**Complexity:** Medium

## Work Completed
- Security scan completed
- Issues found

## Current State
- **Branch:** feat/oauth
- **Last Commit:** abc1234
- **Tests:** Passing (but security issues)

## Handoff Payload
```json
{
  "validation_type": "security",
  "status": "FAILED",
  "issues": [
    {
      "severity": "HIGH",
      "file": "src/services/oauth-client.ts",
      "line": 45,
      "issue": "Token stored in localStorage",
      "recommendation": "Use httpOnly cookie instead"
    },
    {
      "severity": "MEDIUM",
      "file": "src/routes/auth.ts",
      "line": 23,
      "issue": "Missing rate limiting on OAuth callback",
      "recommendation": "Add rate limiter middleware"
    }
  ]
}
```

## Expected Output
- Issues fixed
- Ready for re-validation

## Constraints
- Fix HIGH issues before re-validation
- MEDIUM can be addressed or documented

## Return To
orchestrator (to re-run validation)
```

---

## Handoff Rules

### 1. Always Include
- Current git state (branch, commit)
- What was done
- What needs to happen next
- How to return results

### 2. Payload Format
Use JSON for structured data:
```json
{
  "key": "value",
  "list": ["item1", "item2"],
  "nested": {"sub": "data"}
}
```

### 3. State Preservation
Before handoff:
```bash
# Commit or stash any work
git add -A && git commit -m "WIP: [state description]"
# Or
git stash -m "handoff: [description]"
```

### 4. Failure Handling
If receiving agent can't complete:
```markdown
## Handoff Failed

**Agent:** [name]
**Reason:** [why it couldn't complete]
**State:** [preserved/lost]
**Recommendation:** [what to do]
```

---

## Orchestrator Responsibilities

1. **Route handoffs** - Direct to correct agent
2. **Track state** - Know what each agent has done
3. **Handle failures** - Re-route or escalate
4. **Aggregate results** - Combine outputs from parallel agents
5. **Report to user** - Summarize multi-agent workflow

```
## Workflow State

| Agent | Status | Output |
|-------|--------|--------|
| deep-research | ✓ Complete | research.md |
| system-architect | ✓ Complete | plan-a.md |
| staff-engineer | → In Progress | 3/7 commits |
| security-fortress | ○ Pending | - |
```
