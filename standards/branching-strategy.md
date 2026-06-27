# Branching Strategy

Version: v1.0.0  
Status: Initial standard

## Default Branch

- `main` is the stable branch.
- `main` should remain deployable or publishable depending on repository type.

## Branch Naming

Recommended branch names:

- `docs/topic-name`
- `feature/topic-name`
- `fix/topic-name`
- `security/topic-name`
- `chore/topic-name`

## Workflow

- Create focused branches for meaningful changes.
- Keep documentation-only branches separate from application-code branches when possible.
- Rebase or merge according to repository policy.
- Resolve conflicts carefully and avoid overwriting unrelated work.

## Pull Requests

- Open a PR for review before merging when collaboration is required.
- Keep PR scope clear.
- Include testing, documentation, deployment, and risk notes.

## Release Branches

- Use release branches only when a product requires stabilization, QA, or controlled deployment.
- Name release branches with version or release date where appropriate.
