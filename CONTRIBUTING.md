# Contributing to AutoComply

Thank you for your interest in contributing to AutoComply.

## Development Setup
```bash
git clone https://github.com/morba/autocomply.git
cd autocomply
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Code Standards

This project enforces the following standards on every commit:

- **Formatting:** `black` — no style debates, just run it
- **Linting:** `ruff` — fast, comprehensive
- **Type checking:** `mypy` in strict mode — all code must be fully typed
- **Tests:** `pytest` — all changes must include tests

## Branching Strategy

- `main` — stable, production-ready code only
- `feat/<name>` — new features
- `fix/<name>` — bug fixes

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):
```
feat: add CIS Controls v8 evidence collector
fix: correct compliance score calculation
docs: update architecture diagram
test: add unit tests for risk model
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`feat/your-feature`)
3. Ensure all checks pass (`ruff`, `black`, `mypy`, `pytest`)
4. Submit a pull request with a clear description of the change