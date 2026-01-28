# Agent Template Standard

All agents in this repository MUST follow this template for consistency and proper handoff integration.

---

## Required Sections

### 1. Header
```markdown
# [Agent Name] Agent

> **Role**: [One sentence describing what this agent IS]
> **Trigger**: [When to invoke this agent]
> **Receives from**: [Which agents hand off to this one]
> **Hands off to**: [Which agents this one passes work to]
```

### 2. Expertise (for domain specialists)
```markdown
## Expertise
- [Area 1]
- [Area 2]
```

### 3. Input Specification
```markdown
## Input

### Required
- **task**: Description of what to do
- **context**: Relevant background

### Optional
- **constraints**: Limitations or requirements
- **prior_work**: Output from previous agents
```

### 4. Process (Step-by-Step)
```markdown
## Process

### Phase 1: [Name]
[What to do, how to do it]

### Phase 2: [Name]
[What to do, how to do it]

...
```

### 5. Output Specification
```markdown
## Output

### Format
```
[Exact output structure with placeholders]
```

### Must Include
- [Required field 1]
- [Required field 2]
```

### 6. Handoff Protocol
```markdown
## Handoff

### Receiving Work
When receiving from [Agent X]:
- Expect: [what data]
- Verify: [what to check]

### Passing Work
When handing to [Agent Y]:
- Include: [what data]
- Format: [structure]
```

### 7. Quality Checklist
```markdown
## Checklist

Before completing, verify:
- [ ] [Quality gate 1]
- [ ] [Quality gate 2]
```

---

## Template

```markdown
# [Name] Agent

> **Role**: [What this agent IS and DOES in one sentence]
> **Trigger**: [Conditions that invoke this agent]
> **Receives from**: [Agent names or "User" or "Orchestrator"]
> **Hands off to**: [Agent names or "User" or "None"]

---

## Expertise

- [Domain/skill area]
- [Domain/skill area]

---

## Input

### Required
| Field | Type | Description |
|-------|------|-------------|
| task | string | What to accomplish |
| context | object | Background information |

### Optional
| Field | Type | Description |
|-------|------|-------------|
| constraints | string[] | Limitations |
| prior_work | object | Previous agent output |

---

## Process

### Phase 1: [Name]

**Goal**: [What this phase accomplishes]

**Steps**:
1. [Step]
2. [Step]

**Output**: [What this phase produces]

### Phase 2: [Name]

[Same structure]

---

## Output

### Structure
```
## [Agent Name] Output

### Summary
[Brief overview]

### Findings
[Detailed results]

### Recommendations
[Actionable next steps]

### Handoff Data
[Structured data for next agent]
```

### Required Fields
- summary: Always present
- findings: Always present
- handoff_data: Required if passing to another agent

---

## Handoff

### Receiving

**From [Agent Name]**:
```json
{
  "task": "...",
  "context": "...",
  "prior_findings": "..."
}
```

**Verify before starting**:
- [ ] Task is clear
- [ ] Context is sufficient
- [ ] Prior work is accessible

### Sending

**To [Agent Name]**:
```json
{
  "completed_work": "...",
  "artifacts": [],
  "next_steps": "...",
  "blockers": []
}
```

---

## Checklist

Before marking complete:
- [ ] All process phases executed
- [ ] Output matches required structure
- [ ] Handoff data prepared (if applicable)
- [ ] No unresolved blockers
```

---

## Anti-Patterns to Avoid

### ❌ Knowledge Dump
```markdown
# Database Specialist

Here's everything about databases...
[500 lines of reference material]
```

**Problem**: This is a reference doc, not an agent prompt.

### ✅ Actionable Agent
```markdown
# Database Specialist Agent

> **Role**: Analyze database schemas, optimize queries, and design migrations
> **Trigger**: Task involves database design, query optimization, or migrations

## Process

### Phase 1: Analyze
1. Read the task requirements
2. Examine existing schema
3. Identify patterns and issues

### Phase 2: Design
...
```

**Better**: Tells the agent HOW to act, not just what to know.

---

### ❌ Vague Output
```markdown
## Output
Provide your findings and recommendations.
```

**Problem**: No structure, inconsistent results.

### ✅ Structured Output
```markdown
## Output

```
## Schema Analysis

### Issues Found
| Issue | Severity | Location | Recommendation |
|-------|----------|----------|----------------|

### Proposed Changes
| Change | File | Migration Required |
|--------|------|--------------------|

### Handoff
```json
{
  "schema_changes": [...],
  "migration_files": [...],
  "rollback_plan": "..."
}
```
```
```

**Better**: Exact structure that's parseable and consistent.

---

### ❌ No Handoff
```markdown
## Process
1. Do the work
2. Done!
```

**Problem**: Isolated agent, can't work in multi-agent flow.

### ✅ With Handoff
```markdown
## Handoff

### To staff-engineer
When analysis is complete, pass:
- Schema changes with SQL
- Migration files to create
- Rollback commands
- Estimated risk level

Format:
```json
{
  "status": "ready_for_implementation",
  "changes": [...],
  "risk": "low|medium|high"
}
```
```

**Better**: Clear interface for agent-to-agent communication.
