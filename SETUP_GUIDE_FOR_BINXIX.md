# TacMap - Quick Setup Guide for binxix

## 📧 Contact Info (Already Updated)
- **Email**: antmanitis7@gmail.com
- **Discord**: S4nPV2Rx7F
- **GitHub**: https://github.com/binx-ux/tacmap (update when you create repo)

## 🚀 Publishing to PyPI - Step by Step

### 1. Install Tools
```bash
pip install build twine
```

### 2. Navigate to Package
```bash
cd tacmap
```

### 3. Build Package
```bash
# Clean any old builds
rm -rf build/ dist/ *.egg-info

# Build distributions
python -m build
```

You'll see:
```
Successfully built tacmap-1.0.0.tar.gz and tacmap-1.0.0-py3-none-any.whl
```

### 4. Test Locally First (Recommended)
```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Install your package
pip install dist/tacmap-1.0.0-py3-none-any.whl

# Test commands
tacmap
tacmap-scanner

# Test import
python -c "import tacmap; print(tacmap.__version__)"

# Deactivate when done
deactivate
```

### 5. Create PyPI Account
1. Go to https://pypi.org/account/register/
2. Use email: **antmanitis7@gmail.com**
3. Verify email
4. Enable 2FA (recommended)

### 6. Get API Token
1. Login to PyPI
2. Go to https://pypi.org/manage/account/token/
3. Click "Add API token"
4. Name it: "tacmap-upload"
5. Scope: "Entire account" (or specific to tacmap later)
6. **SAVE THE TOKEN** - starts with `pypi-`

### 7. Upload to PyPI
```bash
# Upload (will prompt for token)
twine upload dist/*

# When prompted:
# Username: __token__
# Password: pypi-YOUR-ACTUAL-TOKEN-HERE
```

### 8. Verify It Worked
```bash
# Check PyPI page
open https://pypi.org/project/tacmap/

# Install from PyPI (in new terminal)
pip install tacmap

# Test it
tacmap
```

## 🎯 Alternative: Save Token for Future Uploads

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR-ACTUAL-TOKEN-HERE
```

Then just run:
```bash
twine upload dist/*
```

## 📝 After Publishing

### Create GitHub Repository
```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial release v1.0.0"

# Create repo on GitHub first, then:
git remote add origin https://github.com/binx-ux/tacmap.git
git branch -M main
git push -u origin main

# Tag the release
git tag v1.0.0
git push origin v1.0.0
```

### Share It!
Once published, people can install with:
```bash
pip install tacmap
```

You can share on:
- Reddit (r/WarThunder - carefully, might be controversial!)
- Discord servers
- Your TikTok (@_binxix)
- GitHub

## 🔄 Updating Package (Future)

When you make changes:

1. **Update version** in these 3 files:
   - `setup.py` → `version="1.0.1"`
   - `pyproject.toml` → `version = "1.0.1"`
   - `tacmap/__init__.py` → `__version__ = "1.0.1"`

2. **Update CHANGELOG.md**
   ```markdown
   ## [1.0.1] - 2026-02-XX
   ### Fixed
   - Bug fix description
   ```

3. **Rebuild and upload**
   ```bash
   rm -rf dist/ build/
   python -m build
   twine upload dist/*
   ```

## ⚠️ Important Notes

### Before Publishing
- [x] Email updated to antmanitis7@gmail.com ✅
- [ ] Test package locally
- [ ] Create GitHub repo
- [ ] Update GitHub URLs in setup.py if needed

### Legal/Safety
- Package includes MIT license
- Educational disclaimer included
- Read-only operation emphasized
- ToS warnings included

### Support
If people have issues, they can:
1. Open GitHub issues
2. Discord: S4nPV2Rx7F
3. Email: antmanitis7@gmail.com

## 🎮 Package Contents

Your package includes:
- `tacmap` - Main tactical map command
- `tacmap-scanner` - Memory scanner command
- Full documentation (README, guides)
- Example configs
- Professional packaging

## 💡 Tips

1. **Test locally before publishing** - Save yourself from version bumps
2. **Use TestPyPI first** (optional but recommended):
   ```bash
   twine upload --repository testpypi dist/*
   pip install --index-url https://test.pypi.org/simple/ tacmap
   ```
3. **Tag releases in git** - Keeps track of versions
4. **Write good commit messages** - Future you will thank you

## 🐛 Troubleshooting

### "Package already exists"
- You already uploaded this version
- Bump version number and rebuild

### "Invalid credentials"
- Check your API token
- Make sure you're using `__token__` as username

### "twine: command not found"
```bash
pip install twine
```

### Build fails
```bash
pip install --upgrade build setuptools wheel
```

## ✅ You're Ready!

Your package is **100% ready to publish**. Just:
1. Run `python -m build`
2. Get your PyPI token
3. Run `twine upload dist/*`
4. Celebrate! 🎉

---

**Package**: tacmap  
**Version**: 1.0.0  
**Author**: binxix  
**Contact**: antmanitis7@gmail.com | Discord: S4nPV2Rx7F  
**Status**: Ready to publish! ✅

Good luck with your first PyPI package! 🚀
