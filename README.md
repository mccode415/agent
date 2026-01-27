# Agent Prompts

Custom agent prompts for Claude Code and similar AI coding assistants.

## Quick Start

```bash
git clone https://github.com/mccode415/agent.git
```

## Agents

### Core Workflow
| Agent | Purpose |
|-------|--------|
| [staff-engineer](prompts/staff-engineer.md) | Full-lifecycle engineering (v2 with triage, rollback, incremental commits) |
| [agent-orchestrator](prompts/agent-orchestrator.md) | Multi-agent workflow coordinator |
| [deep-research](prompts/deep-research.md) | Codebase and external research before planning |
| [system-architect](prompts/system-architect.md) | Impact analysis and architecture decisions |

### Validation & Quality
| Agent | Purpose |
|-------|--------|
| [security-fortress](prompts/security-fortress.md) | Comprehensive security analysis (OWASP, infra, financial) |
| [change-validator-linter](prompts/change-validator-linter.md) | Code quality and linting |
| [change-verifier](prompts/change-verifier.md) | Design alignment and use case verification |
| [performance-analyzer](prompts/performance-analyzer.md) | Performance bottleneck detection |
| [dependency-auditor](prompts/dependency-auditor.md) | Security, updates, and license compliance |

### Development
| Agent | Purpose |
|-------|--------|
| [test-generator](prompts/test-generator.md) | Comprehensive test generation |
| [docs-generator](prompts/docs-generator.md) | API and code documentation |
| [api-designer](prompts/api-designer.md) | REST API design and review |
| [refactor-assistant](prompts/refactor-assistant.md) | Code improvement and cleanup |

### Exploration
| Agent | Purpose |
|-------|--------|
| [codebase-explorer](prompts/codebase-explorer.md) | Map unfamiliar codebases |
| [plan-visualizer](prompts/plan-visualizer.md) | Create visual plan summaries |

### Specialized
| Agent | Purpose |
|-------|--------|
| [quant-trading-engineer](prompts/quant-trading-engineer.md) | Trading systems and backtesting |

## Skills (Commands)

Quick commands invoked with `/command` syntax.

| Skill | Trigger | Purpose |
|-------|---------|--------|
| [commit](prompts/skills/commit.md) | `/commit` | Create well-formatted git commit |
| [review-pr](prompts/skills/review-pr.md) | `/review-pr` | Review a pull request |
| [create-pr](prompts/skills/create-pr.md) | `/create-pr` | Create a pull request |
| [test](prompts/skills/test.md) | `/test` | Run and analyze tests |
| [lint](prompts/skills/lint.md) | `/lint` | Run linters and fix issues |
| [explain](prompts/skills/explain.md) | `/explain` | Explain code or concepts |
| [debug](prompts/skills/debug.md) | `/debug` | Debug an issue |
| [refactor](prompts/skills/refactor.md) | `/refactor` | Refactor code |

## Orchestration Workflows

Trigger multi-agent workflows with keywords:

| Keyword | Agents Run |
|---------|------------|
| `full-review` | security-fortress + change-validator + change-verifier + performance-analyzer |
| `pre-deploy` | security-fortress + dependency-auditor + system-architect + test-generator |
| `new-feature` | codebase-explorer + system-architect + api-designer |
| `security-audit` | security-fortress + security-reviewer + dependency-auditor |
| `code-quality` | change-validator + change-verifier + refactor-assistant + test-generator |
| `documentation` | docs-generator + api-designer + codebase-explorer |
| `deep-analysis` | system-architect + codebase-explorer + performance-analyzer + security-fortress |
| `staff-engineer` | Full lifecycle with research, planning, implementation, validation |

## Quick Reference

- [staff-engineer-quick-ref](prompts/quick-reference.md) - Cheat sheet for staff-engineer workflow

## Usage

These prompts can be used as:
1. **System prompts** when building with Claude API
2. **Custom agent definitions** in Claude Code (if supported)
3. **Reference** for guiding Claude through engineering workflows

## Philosophy

- **Concrete over vague**: Checklists, not prose
- **Safe by default**: Always know how to rollback
- **Right-sized process**: Simple tasks get simple workflows
- **Incremental**: Commit working increments, validate early
- **Selective**: Only run relevant validators

## Repository Structure

```
agent/
├── README.md
└── prompts/
    ├── staff-engineer.md        # Core agent (v2)
    ├── agent-orchestrator.md    # Multi-agent coordinator
    ├── quick-reference.md       # Cheat sheet
    │
    ├── deep-research.md
    ├── system-architect.md
    ├── codebase-explorer.md
    ├── plan-visualizer.md
    │
    ├── security-fortress.md
    ├── change-validator-linter.md
    ├── change-verifier.md
    ├── performance-analyzer.md
    ├── dependency-auditor.md
    │
    ├── test-generator.md
    ├── docs-generator.md
    ├── api-designer.md
    ├── refactor-assistant.md
    │
    ├── quant-trading-engineer.md
    │
    └── skills/
        ├── README.md
        ├── commit.md
        ├── review-pr.md
        ├── create-pr.md
        ├── test.md
        ├── lint.md
        ├── explain.md
        ├── debug.md
        └── refactor.md
```
