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