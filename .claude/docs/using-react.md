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