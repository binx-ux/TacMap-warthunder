# Contributing to TacMap

Thank you for your interest in contributing to TacMap! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on educational and learning purposes
- Do not encourage or facilitate cheating in online games
- Respect game developers and other players

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Include detailed steps to reproduce the bug
3. Include your Python version, OS, and War Thunder version
4. Include relevant error messages or logs

### Suggesting Enhancements

1. Check if the enhancement has already been suggested
2. Explain why this enhancement would be useful
3. Provide examples of how it would work

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/tacmap.git
cd tacmap

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Comment complex logic

### Testing

```bash
# Run tests
pytest

# Format code
black tacmap/

# Check code style
flake8 tacmap/

# Type checking
mypy tacmap/
```

## Areas for Contribution

### High Priority
- Improved entity tracking algorithms
- Better memory address detection
- Performance optimizations
- Cross-platform support (if possible)
- Documentation improvements

### Medium Priority
- Additional visualization options
- Custom themes and colors
- Export/import config profiles
- Replay functionality

### Low Priority
- UI/UX enhancements
- Additional statistics
- Integration with other tools

## Memory Address Discovery

If you discover reliable methods for finding memory addresses:

1. Document your methodology clearly
2. Test across multiple game versions if possible
3. Include offset patterns you discover
4. Share in Issues or Pull Requests

## Important Notes

- **Educational Purpose Only**: All contributions should maintain the educational nature of this project
- **No Game Modifications**: Code should only READ memory, never WRITE
- **ToS Awareness**: Include appropriate warnings about Terms of Service
- **No Malicious Code**: All code will be reviewed for safety

## Questions?

Feel free to open an Issue for:
- Questions about the codebase
- Clarification on contribution guidelines
- Discussion of new features
- General feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make TacMap better! 🚀
