# Building TacMap

## Build Package

```bash
cd tacmap
pip install build twine
python -m build
```

Creates:
- `dist/tacmap-1.0.0-py3-none-any.whl`
- `dist/tacmap-1.0.0.tar.gz`

## Test Locally

```bash
pip install dist/tacmap-1.0.0-py3-none-any.whl
tacmap
tacmap-scanner
```

## Upload to PyPI

```bash
twine upload dist/*
```

Prompts for:
- Username: `__token__`
- Password: Your PyPI API token

## Get PyPI Token

1. Register at https://pypi.org
2. Go to https://pypi.org/manage/account/token/
3. Create token named "tacmap-upload"
4. Save token (starts with `pypi-`)

## Update Version

Edit version in:
- `setup.py`
- `pyproject.toml`
- `tacmap/__init__.py`

Then rebuild and upload.

---

See [PUBLISH.md](PUBLISH.md) for step-by-step guide.
