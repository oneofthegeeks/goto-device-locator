# Contributing to GoTo Connect Device Location Manager

Thank you for your interest in contributing to the GoTo Connect Device Location Manager! We welcome contributions from the community and are pleased to have you join us.

## 🤝 How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. **Check if the feature already exists** in open issues
2. **Describe the use case** clearly
3. **Explain the expected behavior**
4. **Consider implementation complexity**

### Code Contributions

#### Getting Started

1. **Fork the repository**
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/your-username/goto-device-locator.git
   cd goto-device-locator
   ```
3. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Set up development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your test credentials
   ```

#### Development Guidelines

##### Code Style
- Follow **PEP 8** Python style guide
- Use **meaningful variable and function names**
- Keep functions **small and focused**
- Add **docstrings** to all functions and classes
- Use **type hints** where appropriate

##### Example:
```python
def get_device_details(device_id: str, access_token: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve detailed information for a specific device.
    
    Args:
        device_id: The unique identifier for the device
        access_token: OAuth access token for API authentication
        
    Returns:
        Dictionary containing device details or None if not found
    """
    # Implementation here
```

##### Commit Messages
Use clear, descriptive commit messages:
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests

Examples:
```
feat: add phone number details view
fix: resolve authentication token refresh issue
docs: update Docker deployment guide
```

##### Testing
- **Test your changes** thoroughly
- **Add tests** for new functionality when possible
- **Ensure existing tests pass**
- **Test with different browsers** for UI changes

##### Documentation
- **Update README.md** if needed
- **Update Docker documentation** for deployment changes
- **Add inline comments** for complex logic
- **Update API documentation** for new endpoints

#### Pull Request Process

1. **Ensure your branch is up to date**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Test your changes**:
   ```bash
   # Run manual tests
   python app.py
   
   # Test Docker build
   ./docker-build.sh build
   ```

3. **Create pull request**:
   - Use descriptive title and description
   - Reference related issues
   - Include screenshots for UI changes
   - List any breaking changes

4. **Respond to feedback**:
   - Address review comments promptly
   - Make requested changes
   - Update documentation if needed

## 🏗️ Development Setup

### Prerequisites
- Python 3.11+
- Git
- GoTo Connect developer account
- Text editor or IDE

### Environment Setup

1. **Clone and setup**:
   ```bash
   git clone https://github.com/your-username/goto-device-locator.git
   cd goto-device-locator
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your GoTo Connect OAuth credentials
   ```

3. **Run development server**:
   ```bash
   export FLASK_ENV=development
   export FLASK_DEBUG=1
   python app.py
   ```

### Docker Development

1. **Build development image**:
   ```bash
   docker build -t goto-device-manager-dev .
   ```

2. **Run with development settings**:
   ```bash
   docker run -p 5000:5000 \
     -e FLASK_ENV=development \
     -e FLASK_DEBUG=1 \
     -v $(pwd):/app \
     goto-device-manager-dev
   ```

## 📝 Areas for Contribution

### High Priority
- **Test coverage** improvements
- **Error handling** enhancements
- **Performance optimizations**
- **Mobile UI** improvements
- **Accessibility** features

### Features Wanted
- **Dark mode** implementation
- **Export functionality** (CSV, JSON)
- **Advanced filtering** options
- **Bulk operations** improvements
- **API rate limiting** handling
- **Caching** mechanisms

### Documentation
- **API documentation** improvements
- **Deployment guides** for other platforms
- **Troubleshooting guides**
- **Video tutorials**
- **Translation** to other languages

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**:
   - OS and version
   - Python version
   - Browser (if web UI issue)
   - Docker version (if containerized)

2. **Steps to reproduce**:
   - Detailed step-by-step instructions
   - Expected behavior
   - Actual behavior
   - Screenshots or error messages

3. **Additional context**:
   - Recent changes made
   - Workarounds found
   - Impact on functionality

## 📋 Code Review Process

### For Contributors
- **Self-review** your code before submitting
- **Test thoroughly** in different scenarios
- **Document changes** in PR description
- **Be responsive** to feedback

### For Reviewers
- **Be constructive** and helpful
- **Focus on code quality** and maintainability
- **Test changes** when possible
- **Approve promptly** when satisfied

## 🚀 Release Process

1. **Version bumping** follows semantic versioning
2. **Changelog** is updated for each release
3. **Docker images** are built automatically
4. **Documentation** is updated as needed

## 🤔 Questions?

- **Open an issue** for technical questions
- **Start a discussion** for general questions
- **Check existing documentation** first

## 📜 Code of Conduct

We expect all contributors to:
- **Be respectful** and inclusive
- **Focus on constructive feedback**
- **Help others learn and grow**
- **Follow community guidelines**

## 🎉 Recognition

Contributors will be:
- **Listed in releases** when appropriate
- **Mentioned in documentation** for significant contributions
- **Thanked publicly** for their efforts

Thank you for contributing to the GoTo Connect Device Location Manager! 🙏