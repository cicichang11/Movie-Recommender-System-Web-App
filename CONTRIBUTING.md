# 🤝 Contributing to Hybrid Movie Recommender

Thank you for your interest in contributing to our movie recommendation system! This document provides guidelines and information for contributors.

## 🌟 How to Contribute

We welcome contributions from the community! Here are some ways you can help:

### **🐛 Report Bugs**
- Use the [GitHub issue tracker](https://github.com/yourusername/movie-recommender/issues)
- Include detailed steps to reproduce the bug
- Provide system information and error logs
- Use the bug report template

### **💡 Suggest Features**
- Open a feature request issue
- Describe the feature and its benefits
- Include mockups or examples if possible
- Discuss implementation approach

### **📝 Improve Documentation**
- Fix typos and grammar errors
- Add missing information
- Improve code examples
- Translate to other languages

### **🔧 Submit Code Changes**
- Fork the repository
- Create a feature branch
- Make your changes
- Submit a pull request

## 🚀 Development Setup

### **Prerequisites**
- Python 3.7+
- Git
- pip or conda
- 4GB RAM minimum

### **Local Development Environment**
```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender

# Add upstream remote
git remote add upstream https://github.com/yourusername/movie-recommender.git

# Create virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Create artifacts directory
mkdir -p artifacts

# Train models for testing
python train_model.py
```

### **Running Tests**
```bash
# Install testing dependencies
pip install pytest pytest-cov pytest-mock

# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_recommender.py
```

## 📋 Pull Request Guidelines

### **Before Submitting**
- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] Commit messages are clear and descriptive

### **Pull Request Template**
```markdown
## 📝 Description
Brief description of changes made

## 🔧 Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## 🧪 Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance benchmarks included

## 📚 Documentation
- [ ] README updated
- [ ] Code comments added
- [ ] API documentation updated
- [ ] Changelog updated

## 🔍 Additional Notes
Any additional information or context
```

### **Commit Message Format**
```
type(scope): description

Examples:
feat(recommender): add BERT embeddings support
fix(ui): resolve selectbox data type error
docs(readme): update installation instructions
test(ml): add unit tests for hybrid algorithm
```

## 🏗️ Project Structure

### **Core Components**
- `src/recommender.py` - Main recommendation engine
- `app_improved.py` - Streamlit web interface
- `train_model.py` - Model training script
- `demo_system.py` - Command-line demo

### **Data Files**
- `data/` - Raw datasets (TMDB movies and credits)
- `artifacts/` - Trained models and processed data

### **Documentation**
- `README.md` - Main project documentation
- `README_IMPROVED.md` - Technical implementation details
- `QUICK_START.md` - Fast setup guide
- `CONTRIBUTING.md` - This file

## 🧪 Testing Guidelines

### **Unit Tests**
- Test individual functions and methods
- Mock external dependencies
- Test edge cases and error conditions
- Aim for 90%+ code coverage

### **Integration Tests**
- Test component interactions
- Test end-to-end workflows
- Test with real data samples
- Verify model performance

### **Performance Tests**
- Benchmark recommendation speed
- Test memory usage
- Test scalability with larger datasets
- Compare with baseline implementations

## 📚 Code Standards

### **Python Style Guide**
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions
- Use type hints where appropriate
- Keep functions under 50 lines
- Use descriptive variable names

### **Documentation Standards**
- Add docstrings to all functions and classes
- Use Google or NumPy docstring format
- Include examples in docstrings
- Update README for new features

### **Error Handling**
- Use specific exception types
- Provide meaningful error messages
- Log errors appropriately
- Graceful fallbacks for failures

## 🔒 Security Guidelines

### **API Keys**
- Never commit API keys to version control
- Use environment variables for sensitive data
- Document required environment variables
- Provide example configuration files

### **Data Privacy**
- Don't commit user data or personal information
- Use synthetic data for testing
- Follow data protection regulations
- Document data handling practices

## 🚀 Release Process

### **Versioning**
- Use [Semantic Versioning](https://semver.org/)
- Update version in setup.py and __init__.py
- Tag releases in Git
- Update CHANGELOG.md

### **Release Checklist**
- [ ] All tests pass
- [ ] Documentation is current
- [ ] Dependencies are updated
- [ ] Changelog is updated
- [ ] Release notes are written
- [ ] GitHub release is created

## 📞 Getting Help

### **Community Support**
- GitHub Discussions
- GitHub Issues
- Stack Overflow (tag: movie-recommender)
- Discord/Slack channels

### **Developer Resources**
- [Python Documentation](https://docs.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Pandas Documentation](https://pandas.pydata.org/)

## 🏆 Recognition

### **Contributor Benefits**
- Name added to contributors list
- Recognition in release notes
- Invitation to core team (for major contributions)
- Featured in project showcases

### **Contributor Levels**
- **Contributor**: 1-5 contributions
- **Regular Contributor**: 6-20 contributions
- **Core Contributor**: 21+ contributions
- **Maintainer**: Core team member

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to the Hybrid Movie Recommender project! 🎬**

Your contributions help make this project better for everyone in the machine learning community.
