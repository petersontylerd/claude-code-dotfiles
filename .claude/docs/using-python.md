# Python Development Standards

## Environment Setup
- **Python Version**: >=3.11 (use latest stable)
- **Package Manager**: uv required. NEVER use pip, pip with venv, or poetry
- **Dependency Management**: Use pyproject.toml, lock dependencies with uv.lock

## Code Quality Tools
- **Linter & Formatter**: Ruff (replaces Black, isort, and more)
- **Type Checker**: MyPy with strict settings (--strict flag)
- **Testing**: pytest with coverage (min 80%)

## Essential Commands
```bash
uv sync --dev              # Install dependencies
uv run python -m app.main  # Run application
uv run pytest             # Test
uv run ruff format .      # Format code
uv run ruff check .       # Lint
uv run ruff check --fix . # Lint and auto-fix
uv run mypy src/          # Type check
```

## Python-Specific Standards
- Use type hints for all functions (including return types)
- Prefer dataclasses or Pydantic models for data structures
- Use pathlib for file operations, never os.path
- Context managers for resource handling (with statements)
- Async/await for I/O operations when beneficial
- Follow PEP 8 naming: snake_case for functions/variables, PascalCase for classes

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