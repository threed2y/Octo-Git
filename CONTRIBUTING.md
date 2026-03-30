# Contributing to Octo

Thanks for taking the time to contribute! 🐙

## Development setup

```bash
git clone https://github.com/your-username/octo.git
cd octo
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Running locally

```bash
python -m octo
# or, after pip install -e .
octo
```

## Code style

- Python 3.10+ type hints throughout (`str | None`, not `Optional[str]`)
- All colours / styles declared as module-level constants — never hardcode `"cyan"` inline
- New features go in `octo/core.py`; large additions may warrant their own module under `octo/`
- Keep `_rule()`, `_ok()`, `_err()`, `_warn()`, `_info()`, `_panel()` as the only output
  primitives — don't call `console.print(...)` directly in feature functions

## Submitting a pull request

1. Fork the repo and create a branch: `git checkout -b feat/my-feature`
2. Make your changes with clear commit messages
3. Open a PR against `main` with a description of what changed and why
