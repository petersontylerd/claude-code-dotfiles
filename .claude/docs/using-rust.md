# Rust Development Standards

## Environment Setup
- **Rust Version**: Latest stable via rustup
- **Package Manager**: Cargo (built-in)
- **Toolchain**: rustfmt, clippy required
- **Testing**: Built-in test framework

## Code Quality Tools
- **Formatter**: rustfmt with default settings
- **Linter**: clippy with pedantic lints
- **Security Audit**: cargo-audit
- **Documentation**: rustdoc

## Essential Commands
```bash
cargo new project_name   # New project
cargo build --release   # Optimized build
cargo run              # Run debug build
cargo test             # Run tests
cargo fmt              # Format code
cargo clippy           # Lint code
cargo doc --open       # Generate docs
```

## Rust-Specific Standards
- Handle all Results and Options explicitly
- Prefer iterators over loops
- Use borrowing over cloning when possible
- Implement standard traits (Debug, Clone, etc.)
- Document public APIs with examples
- Use const generics over macros when possible

## Error Handling
- Use thiserror for error types
- Use anyhow for application errors
- Never use unwrap() in production code
- Use expect() with descriptive messages
- Implement proper error propagation with ?

## Memory & Performance
- Prefer &str over String for read-only
- Use Cow<str> for maybe-owned strings
- Arc<Mutex<T>> for shared state
- Use rayon for parallel processing
- Profile before optimizing
- Consider zero-copy patterns

## Safety Guidelines
- Minimize unsafe blocks
- Document all unsafe code thoroughly
- Use safe abstractions over raw pointers
- Validate all invariants at boundaries