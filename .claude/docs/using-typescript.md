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