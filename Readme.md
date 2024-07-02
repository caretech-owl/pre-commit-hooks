# Pre-commit Hooks

A collection of custom pre-commit hooks to assist development.

Add this repo to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/caretech-owl/pre-commit-hooks
    rev: v0.1.0
    hooks:
        # add ids here
```

## Hooks

### Detect Env Leakage

This hook checks for leaking environment variables.

- id: `detect-env-leakage`
- requires: `python-dotenv`