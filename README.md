# Agent Prompts

Custom agent prompts for Claude Code and similar AI coding assistants.

## Agents

### Core Workflow
- **[staff-engineer.md](prompts/staff-engineer.md)** - Full-lifecycle engineering agent (plan, implement, validate)
- **[deep-research.md](prompts/deep-research.md)** - Codebase and external research before planning
- **[system-architect.md](prompts/system-architect.md)** - Impact analysis and architecture decisions

### Validation & Quality
- **[security-fortress.md](prompts/security-fortress.md)** - Comprehensive security analysis
- **[change-validator-linter.md](prompts/change-validator-linter.md)** - Code quality and linting
- **[change-verifier.md](prompts/change-verifier.md)** - Design alignment and use case verification
- **[performance-analyzer.md](prompts/performance-analyzer.md)** - Performance bottleneck detection
- **[dependency-auditor.md](prompts/dependency-auditor.md)** - Security, updates, and license compliance

### Development
- **[test-generator.md](prompts/test-generator.md)** - Comprehensive test generation
- **[docs-generator.md](prompts/docs-generator.md)** - API and code documentation
- **[api-designer.md](prompts/api-designer.md)** - REST API design and review
- **[refactor-assistant.md](prompts/refactor-assistant.md)** - Code improvement and cleanup

### Exploration
- **[codebase-explorer.md](prompts/codebase-explorer.md)** - Map unfamiliar codebases
- **[plan-visualizer.md](prompts/plan-visualizer.md)** - Create visual plan summaries

### Specialized
- **[quant-trading-engineer.md](prompts/quant-trading-engineer.md)** - Trading systems and backtesting

## Quick Reference
- **[quick-reference.md](prompts/quick-reference.md)** - Staff engineer cheat sheet

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

## Contributing

To add or improve agents:
1. Follow the existing format
2. Include "When to Use" section
3. Provide concrete output templates
4. Add to this README
