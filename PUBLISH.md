# TacMap - Publishing Guide

## Quick Publish to PyPI

### 1. Install Tools
```bash
pip install build twine
```

### 2. Build Package
```bash
cd tacmap
python -m build
```

### 3. Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Use email: **antmanitis7@gmail.com**
3. Verify email
4. Enable 2FA (recommended)

### 4. Get API Token
1. Login to PyPI
2. Go to https://pypi.org/manage/account/token/
3. Click "Add API token"
4. Name it: "tacmap-upload"
5. Scope: "Entire account"
6. **SAVE THE TOKEN** - starts with `pypi-`

### 5. Upload to PyPI
```bash
twine upload dist/*

# When prompted:
# Username: __token__
# Password: pypi-YOUR-ACTUAL-TOKEN-HERE
```

### 6. Verify
```bash
pip install tacmap
tacmap
```

## Done! 🎉

Your package is now live at: https://pypi.org/project/tacmap/

Anyone can install it with:
```bash
pip install tacmap
```

---

## Updating Later

When you make changes:

1. Update version in `setup.py`, `pyproject.toml`, and `tacmap/__init__.py`
2. Rebuild: `python -m build`
3. Upload: `twine upload dist/*`

---

**Contact**: antmanitis7@gmail.com | Discord: S4nPV2Rx7F
