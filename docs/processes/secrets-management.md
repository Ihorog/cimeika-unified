# Secrets Management

_(stub)_

## Overview
Working with credentials securely in the Cimeika ecosystem.

## Rules
- **Never** commit secrets, credentials, or API keys to the repository.
- Use GitHub Secrets for CI/CD pipelines.
- Use environment variables (`.env` files) for local development — never commit `.env` files.
- Follow the principle of least privilege: each secret grants only the minimum required access.

## Local Development
- Copy `.env.example` to `.env` and fill in your values.
- `.env` is listed in `.gitignore` and must not be committed.

## GitHub Secrets
- Secrets are stored in **Settings → Secrets and variables → Actions**.
- Reference them in workflows as `${{ secrets.SECRET_NAME }}`.

## References
- See `.env.example` and `.env.template` for required variables.
- See `docs/GITHUB_SECRETS_GUIDE.md` for detailed setup instructions.
