# Agent Prompts

A comprehensive collection of AI agent prompts for software engineering workflows.

## Quick Start

```bash
git clone https://github.com/mccode415/agent.git
```

## Agents Overview

### Core Workflow
| Agent | Purpose |
|-------|--------|
| [staff-engineer](prompts/staff-engineer.md) | Full-lifecycle engineering (v2 with triage, rollback, incremental commits) |
| [agent-orchestrator](prompts/agent-orchestrator.md) | Multi-agent workflow coordinator |
| [handoff-protocol](prompts/handoff-protocol.md) | Agent-to-agent communication standard |
| [deep-research](prompts/deep-research.md) | Codebase and external research before planning |
| [system-architect](prompts/system-architect.md) | Impact analysis and architecture decisions |

### Validation & Quality
| Agent | Purpose |
|-------|--------|
| [security-fortress](prompts/security-fortress.md) | Comprehensive security analysis (OWASP, infra, financial) |
| [security-reviewer](prompts/security-reviewer.md) | Targeted code security review |
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

### Domain Specialists
| Agent | Purpose |
|-------|--------|
| [electron-specialist](prompts/domain/electron-specialist.md) | Electron desktop app development |
| [llm-specialist](prompts/domain/llm-specialist.md) | LLM integration, prompts, production patterns |
| [rag-specialist](prompts/domain/rag-specialist.md) | Retrieval-augmented generation systems |
| [database-specialist](prompts/domain/database-specialist.md) | Schema design, queries, migrations, optimization |
| [frontend-specialist](prompts/domain/frontend-specialist.md) | React, CSS, performance, accessibility |
| [devops-specialist](prompts/domain/devops-specialist.md) | CI/CD, Docker, Kubernetes, infrastructure |
| [api-integration-specialist](prompts/domain/api-integration-specialist.md) | Third-party APIs, OAuth, webhooks |
| [realtime-specialist](prompts/domain/realtime-specialist.md) | WebSockets, SSE, presence systems |
| [search-specialist](prompts/domain/search-specialist.md) | Full-text, vector, and hybrid search |
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
| `trading-review` | quant-trading-engineer + security-fortress + performance-analyzer |
| `documentation` | docs-generator + api-designer + codebase-explorer |
| `deep-analysis` | system-architect + codebase-explorer + performance-analyzer + security-fortress |
| `database-design` | database-specialist + system-architect |
| `api-integration` | api-integration-specialist + security-reviewer |
| `realtime-feature` | realtime-specialist + performance-analyzer |
| `staff-engineer` | Full lifecycle with research, planning, implementation, validation |

## Repository Structure

```
agent/
├── README.md
├── AGENT_TEMPLATE.md              # Standard template for all agents
└── prompts/
    ├── staff-engineer.md          # Core workflow agent (v2)
    ├── agent-orchestrator.md      # Multi-agent coordinator
    ├── handoff-protocol.md        # Agent communication
    ├── quick-reference.md         # Cheat sheet
    │
    ├── deep-research.md
    ├── system-architect.md
    ├── codebase-explorer.md
    ├── plan-visualizer.md
    │
    ├── security-fortress.md
    ├── security-reviewer.md
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
    ├── domain/                    # Domain specialists
    │   ├── electron-specialist.md
    │   ├── llm-specialist.md
    │   ├── rag-specialist.md
    │   ├── database-specialist.md
    │   ├── frontend-specialist.md
    │   ├── devops-specialist.md
    │   ├── api-integration-specialist.md
    │   ├── realtime-specialist.md
    │   └── search-specialist.md
    │
    └── skills/                    # Quick commands
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

## Philosophy

- **Concrete over vague**: Checklists, not prose
- **Safe by default**: Always know how to rollback
- **Right-sized process**: Simple tasks get simple workflows
- **Incremental**: Commit working increments, validate early
- **Selective**: Only run relevant validators
- **Domain expertise**: Specialized knowledge for complex areas

## Usage

These prompts can be used as:
1. **System prompts** when building with Claude API
2. **Custom agent definitions** in Claude Code (if supported)
3. **Reference** for guiding Claude through engineering workflows
4. **Templates** for building your own agents

## Contributing

To add or improve agents:
1. Follow [AGENT_TEMPLATE.md](AGENT_TEMPLATE.md) for consistent structure
2. Include Role/Trigger/Receives/Hands off header
3. Define Input/Process/Output/Handoff sections
4. Provide concrete output templates with JSON formats
5. Include quality checklists
6. Add to this README
