# Repository Standards

Version: v1.0.0  
Status: Initial standard

## Repository Purpose

- Every repository must have a clear purpose.
- Documentation repositories must not be mixed with application code unless intentionally approved.
- Application repositories must include setup, testing, deployment, and ownership notes.

## Required Files

- `README.md`
- `.gitignore`
- Dependency manifest where applicable.
- Environment example file where applicable.
- Documentation for setup, test, deployment, and operations.

## Git Workflow

- Keep commits focused.
- Do not mix unrelated application changes with documentation-only changes.
- Do not commit secrets, credentials, private keys, production data, or temporary generated files.
- Review status before every commit.

## Pull Request Rules

- PRs must explain what changed and why.
- PRs must list tests or verification performed.
- PRs must call out risks, migrations, deployment needs, and rollback notes.
- PRs must update relevant documentation.

## Code Review Rules

- Review for correctness, security, maintainability, tests, documentation, and operational impact.
- Prefer specific actionable feedback.
- Do not approve changes that introduce unclear ownership, hidden credentials, or undocumented production risk.
