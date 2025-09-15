# Contributing to AI Educational Assistant

Thank you for your interest in contributing to the AI Educational Assistant project! This document provides guidelines for contributing to this capstone project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a code of conduct that promotes a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bug fix

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-educational-assistant.git
cd ai-educational-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## Making Changes

### Branch Naming Convention
- Feature branches: `feature/description-of-feature`
- Bug fixes: `bugfix/description-of-bug`
- Documentation: `docs/description-of-change`
- Hotfixes: `hotfix/description-of-fix`

### Commit Message Guidelines
Follow the conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(assistant): add personalized learning path generation
fix(ui): resolve sidebar navigation issue
docs(readme): update installation instructions
```

## Submitting Changes

1. **Create a Pull Request**
   - Use a clear and descriptive title
   - Provide a detailed description of changes
   - Reference any related issues

2. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Other (please describe)

   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes (or clearly documented)
   ```

## Code Style

### Python Style Guidelines
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 88 characters (Black formatter)

### Code Formatting
We use the following tools:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

Run formatting before committing:
```bash
# Format code
black src/ tests/
isort src/ tests/

# Check linting
flake8 src/ tests/
```

### Documentation Style
- Use clear, concise language
- Include code examples where appropriate
- Update relevant documentation when making changes
- Use Markdown for documentation files

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src/

# Run specific test file
python -m pytest tests/test_educational_assistant.py
```

### Writing Tests
- Write unit tests for new functions and classes
- Include integration tests for complex features
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

Example test structure:
```python
def test_generate_personalized_content():
    # Arrange
    user_profile = UserProfile(learning_style="visual")
    assistant = EducationalAssistant()
    
    # Act
    content = assistant.generate_content(user_profile, "mathematics")
    
    # Assert
    assert content is not None
    assert "visual" in content.presentation_style
```

## Documentation

### Types of Documentation
1. **Code Documentation**: Docstrings and inline comments
2. **User Documentation**: README, user guides, tutorials
3. **Developer Documentation**: Architecture, API references
4. **Project Documentation**: Contributing guidelines, changelog

### Documentation Standards
- Keep documentation up-to-date with code changes
- Use clear examples and use cases
- Include screenshots for UI-related documentation
- Write for your target audience (users vs. developers)

## Project Structure

Understanding the project structure helps with contributions:

```
ai-educational-assistant/
├── src/                    # Main application code
│   ├── main.py            # Streamlit application entry point
│   ├── educational_assistant.py  # Core AI assistant logic
│   ├── user_profile.py    # User profiling and preferences
│   ├── learning_analytics.py     # Analytics and progress tracking
│   ├── config.py          # Configuration management
│   └── utils.py           # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── presentation/          # Project presentation materials
├── video/                 # Video demonstration materials
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup configuration
├── .env.example          # Environment variables template
└── README.md             # Project overview and setup
```

## Getting Help

If you need help or have questions:

1. Check existing documentation
2. Search through existing issues
3. Create a new issue with detailed information
4. Join our community discussions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

Thank you for contributing to the AI Educational Assistant project!