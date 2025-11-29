# MASTER_CLAUDE.md
Guidance for Claude Code - an experienced, pragmatic software engineer. Don't over-engineer when simple solutions work.

**Rule #1**: Get explicit permission from me for ANY rule exception. BREAKING RULES IS FAILURE.

## Working Together
- NEVER be a sycophant with phrases like "You're absolutely right!"
- NEVER lie or be agreeable just to be nice - I need honest and objective judgment
- Speak up immediately when uncertain or when you disagree (cite technical reasons)
- ALWAYS ask for clarification rather than making assumptions
- If having trouble, STOP and ask for help

## Development Philosophy
**Core Principles**: Simplicity, Readability, Performance, Maintainability, Testability, Extensibility, Focus, Build Iteratively
- Prefer simple, clean solutions over clever ones
- Good naming is critical - spell out names fully, no abbreviations
- Make smallest reasonable changes; ask permission before reimplementing from scratch
- Reduce code duplication even if refactoring takes effort
- Match existing code style for consistency
- NEVER throw away implementations without EXPLICIT permission
- Long-running tooling (tests, docker compose, migrations, etc.) must ALWAYS be invoked with sensible timeouts or in a non-interactive batch mode. NEVER leave a shell command waiting indefinitely - prefer explicit timeouts, scripted runs, or log polling after command exits.

## Coding Best Practices
- Use early returns, descriptive names, constants over functions, DRY principles
- Prefer functional, immutable approaches when not verbose
- Create staging/sandbox environments for testing - use real APIs, never mocks
- Balance file organization with simplicity
- Use language-appropriate package managers, formatters, linters, and type checkers
- Follow ecosystem conventions and idiomatic patterns for each language
- **MCPs**: You have several MCP servers at your disposal with useful tools. Use these early and often:

  * **`sequential-thinking`** → The Sequential Thinking MCP server gives the model a tool for step-by-step, reflective reasoning, managing and revising thought sequences as it works. In Claude Code, this helps with complex coding by externalizing the planning loop—decomposing tasks, checking intermediate steps, and producing more reliable solutions.

  * **`serena`** → The serena MCP server enables semantic, symbol-level understanding of code, allowing coding agents to navigate, retrieve, and edit projects with far greater precision and efficiency. This combination reduces token usage, improves code quality, and scales effectively for large or complex codebases by leveraging language-server integrations and structured tool calls. It provides a powerful, model-agnostic foundation for intelligent, context-aware code automation.

  * **`context7`** → The Context7 MCP server fetches version-specific documentation and code examples straight from upstream sources and injects them into the model's context. This is valuable for Claude Code because the agent can consult the exact API for the library/version you're using, reducing hallucinated APIs and enabling up-to-date, working code.

## Naming and Comments
- Names MUST describe what code does NOW, not implementation or history
- NEVER use temporal context (new, old, legacy, improved, enhanced)
- Comments describe current state only - no historical context
- NEVER remove comments unless provably false
- Follow language-specific naming conventions (snake_case, camelCase, PascalCase)

## Testing Requirements
**NO EXCEPTIONS**: ALL projects MUST have unit, integration, AND end-to-end tests
- Tests MUST comprehensively cover ALL functionality
- NEVER mock what you're testing - use real data and APIs
- NEVER ignore test output - logs contain CRITICAL information
- Test failures are YOUR responsibility
- Use language-standard test frameworks and assertion libraries

### TDD Process (MANDATORY):
1. Write failing test against real environment
2. Run test to confirm failure
3. Write minimum code to pass
4. Run full suite to confirm no regressions
5. Refactor while keeping tests green

## Systematic Debugging
ALWAYS find root cause - NEVER fix symptoms or add workarounds

### Phase 1: Investigation
- Read error messages carefully
- Reproduce consistently
- Check recent changes

### Phase 2: Pattern Analysis
- Find working examples in same language/framework
- Compare against references
- Identify differences
- Understand dependencies

### Phase 3: Hypothesis and Testing
- Form single hypothesis
- Test minimally
- Verify before continuing
- Say "I don't understand X" when stuck

### Phase 4: Implementation
- Have simplest failing test case
- NEVER add multiple fixes at once
- ALWAYS test after each change
- If first fix fails, STOP and re-analyze

## Version Control
- Use feature branches (fix/, feat/, chore/)
- Make atomic commits: type(scope): description
- Run language-appropriate quality checks before committing

### CRITICAL Git Rules
- If no git repo, STOP and ask permission to initialize
- STOP and ask how to handle uncommitted changes when starting
- Create WIP branch if no clear task branch exists
- Commit frequently throughout development
- NEVER use git add -A without git status first

### Pre-commit Hooks
**FORBIDDEN FLAGS**: --no-verify, --no-hooks, --no-pre-commit-hook

When hooks fail:
1. Read complete error output
2. Identify which tool failed and why
3. Explain fix addressing root cause
4. Apply fix and re-run
5. Only commit after all pass

NEVER bypass quality checks under pressure. Quality > Speed.

## Summarization
When using /compact, focus on recent conversation and significant tasks. Aggressively summarize older tasks, preserve context for recent ones.

# Repository Guidelines

## Project Structure & Module Organization
- Top-level configuration files such as `pyproject.toml`, `uv.lock`, and `config.toml` define the Python toolchain—update these instead of hand-editing generated lock data. Keep any experimental materials in clearly labeled subfolders; the root should remain limited to project-wide configuration.

## Build, Test, and Development Commands
- `UV_CACHE_DIR=.uv-cache uv sync` — install or update the Python environment defined in `pyproject.toml` and `uv.lock`.
- `UV_CACHE_DIR=.uv-cache uv run python scripts/dev_task.py` — preferred pattern for running repository Python scripts; replace the path with the actual entry point you need.
- `UV_CACHE_DIR=.uv-cache uv run pre-commit run --all-files` — format, lint, and type-check before pushing; mirrors the hook configuration.

## Coding Style & Naming Conventions
Target Python 3.X with four-space indentation, meaningful snake_case identifiers, and descriptive YAML keys. Let `ruff format` manage layout and `ruff check` enforce lint rules; do not hand-tune style conflicts. Type hints should cover public helpers, with `mypy` kept clean.

## Testing Guidelines
Adopt `pytest` for any executable Python modules you add. Place tests under `tests/` with names that mirror the module under test, e.g., `tests/test_product_plan.py`. Execute `UV_CACHE_DIR=.uv-cache uv run pytest` locally and require meaningful fixtures or sample YAML to exercise parsing logic. Aim for high-value assertions over blanket coverage, but flag regressions with focused regression cases.

## Commit & Pull Request Guidelines
Write imperative, present-tense commit subjects (~60 characters) and bundle related edits only. Pull requests should summarize intent, list test commands run, and attach before/after snippets for modified YAML or generated artifacts. Request review once CI-style checks (`pre-commit`, `pytest`, security scans) pass locally.

# Python Development Standards

## Environment Setup
- **Python Version**: >=3.12
- **Package Manager**: uv required. NEVER use pip, pip with venv, or poetry
- **Dependency Management**: Use pyproject.toml, lock dependencies with uv.lock

## Code Quality Tools
- **Linter & Formatter**: Ruff (replaces Black, isort, and more)
- **Type Checker**: MyPy with strict settings (--strict flag)
- **Testing**: pytest with coverage (min 90%)

## Essential Commands
```bash
UV_CACHE_DIR=.uv-cache uv sync --dev              # Install dependencies
UV_CACHE_DIR=.uv-cache uv run python -m app.main  # Run application
UV_CACHE_DIR=.uv-cache uv run pytest             # Test
UV_CACHE_DIR=.uv-cache uv run ruff format .      # Format code
UV_CACHE_DIR=.uv-cache uv run ruff check .       # Lint
UV_CACHE_DIR=.uv-cache uv run ruff check --fix . # Lint and auto-fix
UV_CACHE_DIR=.uv-cache uv run mypy src/          # Type check
```

## Python-Specific Standards
- Use type hints for all functions (including return types)
- Prefer dataclasses or Pydantic models for data structures
- Use pathlib for file operations, never os.path
- Context managers for resource handling (with statements)
- Async/await for I/O operations when beneficial
- Follow PEP 8 naming: snake_case for functions/variables, PascalCase for classes
- Use Google-style docstrings everywhere

## Common Patterns
- Use `if __name__ == "__main__":` for script entry points
- Prefer f-strings for formatting
- Use enumerate() instead of range(len())
- List comprehensions for simple transformations
- Generator expressions for memory efficiency

## Error Handling
- Specific exception types, never bare except
- Use logging module, not print() for debugging
- Raise exceptions early with clear messages

# React Development Standards

## Environment Setup
- **React Version**: >=18 (use latest stable)
- **Build Tool**: Vite (preferred) > Next.js > CRA
- **State Management**: Zustand > Redux Toolkit > Context
- **Routing**: TanStack Router > React Router
- **UI Libraries**: Shadcn/ui > MUI > Ant Design

## Code Quality Tools
- **Testing**: Vitest + React Testing Library
- **Component Testing**: Storybook for isolation
- **E2E Testing**: Playwright > Cypress

## Essential Commands
```bash
pnpm create vite@latest  # New project
pnpm dev                 # Development server
pnpm test               # Unit tests
pnpm storybook          # Component development
pnpm build              # Production build
```

## React-Specific Standards
- Functional components only (no class components)
- Custom hooks for logic reuse (use prefix)
- Strict mode enabled
- Error boundaries for fault tolerance
- Suspense for async operations
- Server Components where applicable (Next.js/Remix)

## Modern Patterns
- useState for local state
- useReducer for complex state logic
- useMemo/useCallback for optimization (measure first!)
- Custom hooks for shared logic
- Compound components for flexibility
- Render props only when necessary

## Performance Guidelines
- Lazy load routes and heavy components
- Optimize re-renders with React DevTools
- Use virtualization for long lists
- Implement proper loading states
- Optimize bundle size with code splitting

## Styling Approaches
- CSS Modules or Tailwind (preferred)
- CSS-in-JS only if necessary
- Consistent spacing scale
- Mobile-first responsive design
- Dark mode support from the start

# Node.js Development Standards

## Environment Setup
- **Node Version**: >=20 LTS (use latest LTS)
- **Package Manager**: pnpm (preferred) for workspace support
- **Node Version Manager**: Use volta or nvm
- **Process Manager**: PM2 for production

## Modern Node.js Practices
- Use ES modules (type: "module" in package.json)
- Native fetch API instead of axios/request
- Built-in test runner for simple tests
- Worker threads for CPU-intensive tasks
- Native crypto module for security

## Essential Commands
```bash
node --version           # Verify Node version
pnpm init               # Initialize project
pnpm add -D @types/node # TypeScript types
node --watch app.js     # Development with auto-reload
node --test            # Run native tests
node --inspect app.js   # Debug mode
```

## Performance Best Practices
- Use Node.js built-ins when possible (less dependencies)
- Stream large files instead of reading into memory
- Implement graceful shutdown handlers
- Use clustering for multi-core utilization
- Monitor memory usage and implement limits

## Security Standards
- Never use eval() or Function constructor
- Validate all inputs
- Use crypto.randomBytes() for tokens
- Implement rate limiting
- Keep dependencies updated (use Dependabot)
- Use .env for secrets, never commit them

## Modern APIs to Prefer
- fs.promises over callbacks
- Built-in readline for CLI interfaces
- Native URL and URLSearchParams
- AbortController for cancellation
- EventEmitter for pub/sub patterns

# Test-Driven Development (TDD) Standards

## Core TDD Philosophy
TDD is NOT optional - it's our primary development methodology. We write tests BEFORE implementation, always.

## The TDD Cycle (Red-Green-Refactor)
### 1. RED: Write a Failing Test
- Write the test FIRST, before any implementation
- Test must fail for the RIGHT reason (not syntax/import errors)
- Test should be minimal - only test ONE thing
- Use descriptive test names that explain the expected behavior

### 2. GREEN: Make It Pass
- Write MINIMUM code to make the test pass
- Don't add features the test doesn't require
- Resist the urge to write "better" code yet
- Focus only on making the test green

### 3. REFACTOR: Improve the Code
- NOW you can improve the implementation
- Clean up duplication
- Improve naming
- Extract functions/methods
- Tests MUST stay green during refactoring

## Testing Pyramid
### Unit Tests (70% of tests)
- Test individual functions/methods in isolation
- Fast execution (milliseconds)
- No external dependencies (database, API, filesystem)
- Use test doubles ONLY for dependencies, never for the unit under test

### Integration Tests (20% of tests)
- Test interaction between components
- May use real databases/services in test mode
- Test API endpoints, database operations
- Use test containers or staging environments

### End-to-End Tests (10% of tests)
- Test complete user workflows
- Use real environments (staging/sandbox)
- Test critical paths only (login, checkout, etc.)
- Accept slower execution for confidence

## Language-Specific TDD Practices

### Python
```python
# Test first (test_calculator.py)
def test_add_two_numbers():
    result = add(2, 3)
    assert result == 5

# Then implement (calculator.py)
def add(a: int, b: int) -> int:
    return a + b
```

### TypeScript/JavaScript
```typescript
// Test first (calculator.test.ts)
describe('Calculator', () => {
  it('should add two numbers', () => {
    expect(add(2, 3)).toBe(5);
  });
});

// Then implement (calculator.ts)
export function add(a: number, b: number): number {
  return a + b;
}
```

### Rust
```rust
// Test first (in same file or tests/ directory)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}

// Then implement
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Test Quality Standards
- **Descriptive Names**: `test_user_cannot_withdraw_more_than_balance` not `test_withdrawal`
- **Arrange-Act-Assert**: Clear structure in every test
- **Single Assertion**: One logical assertion per test (multiple checks OK if testing one concept)
- **Independent Tests**: Tests must not depend on execution order
- **Deterministic**: Same result every time (no random data without seeds)
- **Fast Feedback**: Unit tests should run in <1 second total

## What NOT to Test
- Third-party libraries (they have their own tests)
- Language features (trust that Python/JS/Rust work)
- Generated code (unless you generated it)
- Pure UI without logic (leave to manual/E2E testing)

## Testing Anti-Patterns to AVOID
- **Testing Implementation**: Test behavior, not how it's done
- **Excessive Mocking**: Indicates poor design or wrong test level
- **Ignored Tests**: Delete or fix, never ignore
- **Test-After**: Writing tests after code is NOT TDD
- **100% Coverage Obsession**: High coverage is good, but quality matters more

## Real Environment Testing
- NEVER mock the system under test
- Use real databases (in-memory or containerized)
- Use real message queues (RabbitMQ, Redis in test mode)
- Use staging/sandbox APIs for external services
- Accept slower tests for accuracy over fast but fake tests

## Continuous Testing
- Run tests on every save (use watch mode)
- Run full suite before commits
- Block merges if tests fail
- Monitor test execution time trends
- Refactor slow tests, don't skip them

## TDD Benefits We Expect
- Simpler designs (you only build what's needed)
- Living documentation (tests show how to use code)
- Confidence in refactoring (tests catch regressions)
- Faster debugging (tests pinpoint failures)
- Better API design (writing tests first reveals awkward interfaces)

## The TDD Commitment
"I will not write production code without a failing test that requires it."

This is not a suggestion - it's our development process. Exceptions require explicit permission from Tyler as per CLAUDE.md Rule #1.

# TypeScript Development Standards

## Environment Setup
- **TypeScript Version**: >=5.0 (use latest stable)
- **Runtime**: Node.js >=20 LTS
- **Package Manager**: pnpm (preferred) > npm > yarn
- **Config**: Strict tsconfig.json settings

## Code Quality Tools
- **Formatter**: Prettier (2 space indent, single quotes)
- **Linter**: ESLint with @typescript-eslint
- **Type Checker**: Built-in tsc with strict mode
- **Testing**: Vitest (preferred) or Jest

## Essential Commands
```bash
pnpm install              # Install dependencies
pnpm dev                  # Development server
pnpm test                # Test
pnpm format              # Format with Prettier
pnpm lint                # Lint with ESLint
pnpm typecheck           # Type check
pnpm build               # Production build
```

## TypeScript-Specific Standards
- Enable all strict flags in tsconfig.json
- Prefer interfaces over type aliases for objects
- Use const assertions for literal types
- Avoid any - use unknown and type guards
- Explicit return types for public APIs
- Use discriminated unions for state modeling

## Modern Patterns
- Prefer const over let, never use var
- Use optional chaining (?.) and nullish coalescing (??)
- Template literals for string interpolation
- Destructuring for cleaner code
- async/await over Promise chains
- Use Map/Set instead of objects for dictionaries

## Error Handling
- Use Error subclasses for custom errors
- Implement Result<T, E> pattern for expected errors
- Never ignore Promise rejections
- Use .catch() or try/catch with async/await

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
UV_CACHE_DIR=.uv-cache uv sync --dev              # Install dependencies with development tools
```

### Code Quality (Pre-commit Hooks)
```bash
UV_CACHE_DIR=.uv-cache uv run pre-commit run --all-files      # Run all checks (format, lint, type-check, security)
UV_CACHE_DIR=.uv-cache uv run ruff format .                   # Format code
UV_CACHE_DIR=.uv-cache uv run ruff check .                    # Lint code
UV_CACHE_DIR=.uv-cache uv run ruff check --fix .              # Lint and auto-fix
UV_CACHE_DIR=.uv-cache uv run mypy .                          # Type-check with strict settings
```

### Validation Scripts
```bash
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/validate-product-plan.py  # Full validation
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-vision.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-strategy.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-prd.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-roadmap.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-personas.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-metrics.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-brainstorm.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/foundation/validate-development-considerations.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/development/validate-epics.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/development/validate-features.py
UV_CACHE_DIR=.uv-cache uv run python .claude/scripts/validate-product-plan/development/validate-user-stories.py
```

### Testing (when tests exist)
```bash
UV_CACHE_DIR=.uv-cache uv run pytest              # Run all tests
UV_CACHE_DIR=.uv-cache uv run pytest -v           # Verbose output
UV_CACHE_DIR=.uv-cache uv run pytest --cov        # With coverage report
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

Run `UV_CACHE_DIR=.uv-cache uv run pre-commit run --all-files` to check all files before committing.

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

**NO EXCEPTIONS on quality**: All projects MUST have comprehensive test coverage using real data and APIs. The specific test pyramid structure (unit/integration/E2E ratios) varies by project type.

### Default Test Pyramid (70/20/10)
- **70% Unit Tests**: Individual functions/components in isolation
- **20% Integration Tests**: Component interactions, real services in test mode
- **10% End-to-End Tests**: Critical user workflows (varies by project type)

### Project-Specific Adjustments
- **Libraries**: 80/20/0 (heavy unit/integration, minimal E2E needed)
- **Web Apps**: 60/25/15 (E2E covers user journeys)
- **APIs**: 70/25/5 (E2E less critical than integration)
- **Infrastructure**: 50/40/10 (heavy integration focus)

### Non-Negotiable Requirements (All Projects)
- Write tests BEFORE implementation (Red-Green-Refactor)
- NEVER mock the system under test - use real data and APIs
- Achieve 90%+ coverage minimum (for code that matters)
- Test failures are development responsibility
- Use language-standard frameworks (pytest for Python, Vitest for TS, etc.)

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
