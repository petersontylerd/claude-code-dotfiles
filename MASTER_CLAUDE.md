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

  * **`context7`** → The Context7 MCP server fetches version-specific documentation and code examples straight from upstream sources and injects them into the model’s context. This is valuable for Claude Code because the agent can consult the exact API for the library/version you’re using, reducing hallucinated APIs and enabling up-to-date, working code.

## Naming and Comments
- Names MUST describe what code does NOW, not implementation or history
- NEVER use temporal context (new, old, legacy, improved, enhanced)
- Comments describe current state only - no historical context
- NEVER remove comments unless provably false
- Follow language-specific naming conventions (snake_case, camelCase, PascalCase)

## Testing Requirements
**NO EXCEPTIONS**: ALL projects MUST have unit, integration, AND end-to-end tests
- Critical functionality must be covered at appropriate levels; for micro changes (docs, config tweaks, single-line fixes) targeted unit/regression tests are acceptable with a follow-up card to extend coverage if needed.
- Prefer real data and APIs; when a real service is unavailable, flaky, or paid-only, use minimal contract/snapshot fakes and document a real-environment verification step.
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
**FORBIDDEN FLAGS**: --no-verify, --no-hooks, --no-pre-commit-hook, unless a hook is demonstrably broken or unrelated; log the issue, note the bypass in the commit description, and schedule a follow-up to fix the hook and rerun checks post-merge.

When hooks fail:
1. Read complete error output
2. Identify which tool failed and why
3. Explain fix addressing root cause
4. Apply fix and re-run
5. Only commit after all pass (or document an approved, temporary bypass as above)

For urgent hotfixes, a short-lived branch may ship quickly with a documented plan to rerun full hooks/tests immediately after release.

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
- Prefer exercising the real system under test; when the real dependency is unavailable, flaky, or paid-only, use the smallest contract/snapshot fake possible and schedule a real-environment verification.
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
