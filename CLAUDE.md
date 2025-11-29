# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a comprehensive dotfiles and tools collection for Claude Code providing:
- **Product Planning System**: YAML-based artifact templates with validation and slash commands
- **Checklist Workflow**: Structured initiative execution (plan → checklist → execute → verify)
- **Agent Definitions**: 15+ specialized AI agent prompts for domain-specific work
- **Development Standards**: Comprehensive MASTER_CLAUDE.md with language-specific best practices
- **MCP Configuration**: Sequential thinking, context7 documentation lookup, and serena semantic tools
- **Validation Infrastructure**: Python scripts for schema validation with JSON reporting

## Build, Test, and Development Commands

### Environment Setup
```bash
uv sync --dev              # Install dependencies with development tools
```

### Code Quality (Pre-commit Hooks)
```bash
uv run pre-commit run --all-files      # Run all checks (format, lint, type-check, security)
uv run ruff format .                   # Format code
uv run ruff check .                    # Lint code
uv run ruff check --fix .              # Lint and auto-fix
uv run mypy .                          # Type-check with strict settings
```

### Validation Scripts
```bash
uv run python .claude/scripts/validate-product-plan/validate-product-plan.py  # Full validation
uv run python .claude/scripts/validate-product-plan/foundation/validate-vision.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-strategy.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-prd.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-roadmap.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-personas.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-metrics.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-brainstorm.py
uv run python .claude/scripts/validate-product-plan/foundation/validate-development-considerations.py
uv run python .claude/scripts/validate-product-plan/development/validate-epics.py
uv run python .claude/scripts/validate-product-plan/development/validate-features.py
uv run python .claude/scripts/validate-product-plan/development/validate-user-stories.py
```

### Testing (when tests exist)
```bash
uv run pytest              # Run all tests
uv run pytest -v           # Verbose output
uv run pytest --cov        # With coverage report
```

## Repository Structure

### `.claude/` - Core Dotfiles and Tooling
- **`templates/product-plan/`**: YAML templates for foundation (vision, strategy, prd, roadmap, personas, metrics, brainstorm, development-considerations) and development (epics, features, user-stories) artifacts
- **`commands/`**: Slash command definitions for Claude Code:
  - `product-manager/`: Product planning commands (one per artifact)
  - `checklist-workflow/`: Initiative execution workflow (create-plan, plan-to-checklist, session-start, execute-next-task, session-end, review-checklist, etc.)
  - `agent-doublecheck/`: Review commands (plan-doublecheck, checklist-doublecheck, prompt-doublecheck)
  - `generators/`: Template generators for new agents and commands
  - `skunkworx/`: Rapid ideation commands for epics, features, user-stories
- **`agents/`**: Domain-specific agent prompts (~15 agents including data-engineer, typescript-engineer, python-engineer, react-engineer, ml-engineer, ai-engineer, etc.)
- **`scripts/validate-product-plan/`**: Python validation scripts for each artifact type with schema checking and JSON report generation
- **`docs/`**: Language-specific development guides (using-python.md, using-typescript.md, using-react.md, using-tdd.md, etc.)
- **`PRODUCTPLAN.md`**: Sequence for executing product planning workflow
- **`settings.local.json`**: Claude Code settings (local)
- **`memory.json`**: Memory state for Claude Code sessions

### Root Configuration Files
- **`MASTER_CLAUDE.md`**: Comprehensive development standards covering Python (>=3.12, uv, pytest, mypy, ruff), React, Node.js, TypeScript, TDD, version control, and testing philosophy
- **`pyproject.toml`**: Project metadata, dependencies (pyyaml), and tool configuration (ruff, mypy)
- **`.pre-commit-config.yaml`**: Git hooks for code quality (ruff format/lint pre-commit, mypy pre-commit, bandit pre-push, pip-audit pre-push)
- **`.mcp.json`**: MCP server configuration (sequential-thinking, context7 documentation, serena semantic tools)
- **`uv.lock`**: Locked dependency versions (managed by uv, do not edit manually)
- **`.python-version`**: Python version specification

## Architecture and Key Patterns

### Product Planning Workflow
1. Create foundation artifacts (vision → strategy → roadmap → personas → metrics → prd → development-considerations)
2. Validate foundation artifacts with `/product-manager:product-plan-foundation-validation-check`
3. Create development artifacts (epics → features → user-stories)
4. Validate development artifacts with `/product-manager:product-plan-development-validation-check`
5. Artifacts are YAML files stored in dedicated directories following the template schema

### Checklist-Based Initiative Execution
1. `/checklist-workflow:create-initiative-plan INITIATIVE_NAME=<name>` - Reads optimized prompt from `.scratchpaper/initiatives/$INITIATIVE_NAME/prompts/optimized/` and generates structured plan
2. `/checklist-workflow:plan-to-checklist INITIATIVE_NAME=<name>` - Converts plan to actionable checklist
3. `/checklist-workflow:session-start INITIATIVE_NAME=<name>` - Begin executing initiative
4. `/checklist-workflow:execute-next-task FEATURE_BRANCH=<branch>` - Execute pending task
5. `/checklist-workflow:session-end` - Close session and update checklist state
6. `/checklist-workflow:review-checklist INITIATIVE_NAME=<name>` - Deep verification of completed work

### Validation Architecture
- Each artifact type (vision, strategy, roadmap, etc.) has a corresponding Python validation script
- Scripts validate YAML structure against templates in `.claude/templates/product-plan/`
- Color-coded output: GREEN (pass), RED (fail), YELLOW (warnings), BLUE (info)
- Generates JSON reports for CI/CD integration
- Main orchestrator: `validate-product-plan.py` runs all foundation and development validations

## Code Style and Conventions

### Python
- **Version**: >=3.12
- **Package Manager**: uv (NEVER pip or poetry)
- **Style**: 4-space indentation, snake_case functions/variables, PascalCase classes
- **Type Hints**: All functions must have return type hints
- **Docstrings**: Google-style format
- **Imports**: Organized by standard library, third-party, local imports
- **Tools**: ruff for formatting/linting, mypy for type-checking (strict mode)
- **YAML Handling**: Use PyYAML (yaml.safe_load for loading)
- **File Operations**: pathlib.Path (not os.path)
- **Shebang**: For executable scripts: `#!/usr/bin/env -S uv run python`
- **ABOUTME Comment**: All Python files start with 2-line comment: `# ABOUTME: <purpose>\n# <additional detail>`

### YAML Templates
- Consistent indentation (2 spaces)
- Descriptive field names (no abbreviations)
- Include validation examples and comments
- Follow template patterns in `.claude/templates/product-plan/`

### Slash Commands
- Markdown files in `.claude/commands/`
- YAML frontmatter with description and argument-hint
- Clear step-by-step instructions
- Support both foundation and development artifact types

## Pre-commit Hooks and Quality Checks

The repository enforces quality standards with git pre-commit hooks:

### Pre-commit Stage (blocks commit)
- **ruff-format**: Formats Python code (replaces Black)
- **ruff**: Lints Python code (replaces flake8, isort, etc.)
- **mypy**: Type-checks Python with strict mode

### Pre-push Stage (blocks push)
- **bandit**: Security scanning
- **pip-audit**: Dependency vulnerability checking

Run `uv run pre-commit run --all-files` to check all files before committing.

## Configuration Details

### MCP Servers (.mcp.json)
- **sequential-thinking**: Enables step-by-step reasoning in Claude Code
- **context7**: Fetches version-specific library documentation (API keys configured)
- **serena**: Provides semantic code tools for precise symbol-level understanding and editing

### Development Dependencies (pyproject.toml)
- **pyyaml**: YAML parsing for artifact validation
- **bandit**: Security linting
- **mypy**: Type checking with strict rules
- **pip-audit**: Dependency security auditing
- **pre-commit**: Git hook framework
- **ruff**: Linting and formatting
- **types-pyyaml**: Type hints for PyYAML

## Testing Requirements

Refer to MASTER_CLAUDE.md for comprehensive TDD standards. Key principles:
- Write tests BEFORE implementation (Red-Green-Refactor)
- Use pytest with 90%+ coverage minimum
- Test pyramid: 70% unit, 20% integration, 10% E2E
- Never mock the system under test - use real data and APIs
- All test failures are development responsibility

## Important Development Rules from MASTER_CLAUDE.md

### Core Principles
- Prefer simple, clean solutions over clever ones
- Make smallest reasonable changes
- Match existing code style for consistency
- Use early returns and descriptive names
- Reduce code duplication

### Git Discipline
- Use feature branches (fix/, feat/, chore/)
- Atomic commits with clear messages (type(scope): description)
- Run quality checks before committing
- NEVER use --no-verify or bypass pre-commit hooks
- Commit frequently throughout development

### Testing Philosophy
- TDD is mandatory - no exceptions without explicit permission
- Tests MUST comprehensively cover functionality
- Never ignore test output - logs contain critical information
- Test failures are YOUR responsibility
- Use language-standard test frameworks (pytest for Python)

### When Stuck
- STOP and ask for help before guessing
- Read error messages carefully
- Never add workarounds without understanding root cause
- Speak up immediately when uncertain or disagreeing

## References

- **MASTER_CLAUDE.md**: Comprehensive development standards and philosophy
- **`.claude/PRODUCTPLAN.md`**: Product planning artifact sequence
- **`.claude/docs/`**: Language-specific development guides
- **`.pre-commit-config.yaml`**: Detailed hook configuration
- **`pyproject.toml`**: Dependency and tool specifications
