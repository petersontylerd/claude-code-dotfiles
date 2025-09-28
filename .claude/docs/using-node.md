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