# Commit Conventions

_(stub)_

## Overview
Commit message standards for the Cimeika ecosystem.

## Format
```
<type>(<scope>): <short summary>
```

## Types
| Type       | Description                                      |
|------------|--------------------------------------------------|
| `feat`     | New feature                                      |
| `fix`      | Bug fix                                          |
| `docs`     | Documentation only changes                       |
| `chore`    | Maintenance tasks (builds, tooling, config)      |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or updating tests                         |
| `ci`       | Changes to CI/CD configuration                   |

## Rules
- Use the imperative mood in the summary: "add feature" not "added feature".
- Keep the summary line under 72 characters.
- Reference issue numbers where applicable: `fix(backend): handle null pointer (#42)`.
- No direct commits to `main` — all changes via PRs.
