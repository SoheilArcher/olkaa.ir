# Coding Standards

Version: v1.0.0  
Status: Initial standard

## General Rules

- Write code for maintainability, clarity, and operational reliability.
- Prefer simple, explicit code over clever abstractions.
- Keep application logic separated from framework, database, and infrastructure concerns where practical.
- Avoid duplicating business rules across modules.
- Add comments only when they clarify non-obvious decisions or constraints.

## Clean Architecture

- Keep domain rules independent from delivery mechanisms.
- Separate entities, use cases, adapters, and infrastructure when the product complexity justifies it.
- Avoid importing web framework code into core business logic.
- Keep external systems behind interfaces or service boundaries where useful.

## SOLID Principles

- Single Responsibility: each module, class, or function should have one clear reason to change.
- Open/Closed: prefer extension points over editing stable code repeatedly.
- Liskov Substitution: derived or replacement implementations must preserve expected behavior.
- Interface Segregation: expose focused interfaces instead of large mixed contracts.
- Dependency Inversion: depend on abstractions for volatile external systems when it reduces coupling.

## Python Standards

- Follow PEP 8 naming and formatting conventions unless a project standard overrides them.
- Use type hints for public functions, service boundaries, and complex data structures.
- Prefer dataclasses or typed schemas for structured data.
- Keep functions small and named by business intent.
- Handle exceptions explicitly; do not hide failures with broad `except` blocks.
- Use virtual environments and pinned dependencies for deployable projects.

## FastAPI Standards

- Keep route handlers thin.
- Put business logic in services or use cases.
- Use Pydantic models for request and response validation.
- Version public APIs.
- Document authentication, authorization, error formats, and pagination.
- Include health checks for deployed services.

## Django Standards

- Keep models focused on data shape and essential invariants.
- Avoid putting large workflows directly in views.
- Use services, managers, or domain modules for complex business logic.
- Keep templates, forms, views, and permissions organized by feature.
- Use migrations deliberately and review generated migrations before commit.
- Protect admin actions with clear permissions and audit expectations.

## Naming Conventions

- Use descriptive names based on business meaning.
- Use `snake_case` for Python variables, functions, modules, and database fields.
- Use `PascalCase` for Python classes.
- Use lowercase hyphenated names for documentation files where appropriate.
- Name migrations, branches, commits, APIs, and modules so their purpose is clear.

## Test Strategy

- Add unit tests for business rules.
- Add integration tests for database, API, and external-service boundaries.
- Add regression tests for bug fixes.
- Add smoke tests for deployment-critical flows.
- Test coverage should scale with risk, customer impact, and code complexity.
