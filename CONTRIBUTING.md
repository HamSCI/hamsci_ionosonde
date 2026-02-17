# Contributing to HamSCI Ionosonde

Thank you for your interest in contributing to the HamSCI Ionosonde project! This document provides guidelines for contributing code, reporting issues, and collaborating on this open-source project.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation Standards](#documentation-standards)
7. [Submitting Changes](#submitting-changes)
8. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

### Our Pledge

This project follows amateur radio traditions of courtesy, cooperation, and mutual assistance. We welcome contributions from operators and scientists of all experience levels.

### Expected Behavior

- Be respectful and constructive in all communications
- Provide helpful feedback and accept feedback graciously
- Focus on what is best for the project and the amateur radio community
- Use welcoming and inclusive language
- Follow the amateur radio principles of service, experimentation, and skill-building

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.8+ installed
- Familiarity with NumPy, SciPy, and Matplotlib
- Basic understanding of signal processing concepts (cross-correlation, FFT)
- Familiarity with ionospheric science concepts (see [CLAUDE.md](CLAUDE.md) for key terms)

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone git@github.com:HamSCI/hamsci_ionosonde.git
   cd hamsci_ionosonde
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt  # when available
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

---

## Development Workflow

### Branch Strategy

We follow the **Git Flow** branching model ([Vincent Driessen, 2010](https://nvie.com/posts/a-successful-git-branching-model/)), adapted to use `main` instead of `master`.

#### Main Branches

These two branches exist permanently and should always be in a stable state:

| Branch    | Purpose                                                                       |
|-----------|-------------------------------------------------------------------------------|
| `main`    | Production-ready code. Every merge into `main` represents a new release.      |
| `develop` | Integration branch containing the latest delivered changes for the next release. |

#### Supporting Branches

Supporting branches have a limited lifetime and are removed after merging.

| Branch      | Branches from | Merges back to       | Naming      | Purpose                                                  |
|-------------|---------------|----------------------|-------------|----------------------------------------------------------|
| **Feature** | `develop`     | `develop`            | `feature/*` | New features (e.g., `feature/add-chirp-generator`)       |
| **Bugfix**  | `develop`     | `develop`            | `bugfix/*`  | Non-urgent bug fixes (e.g., `bugfix/fix-correlation`)    |
| **Release** | `develop`     | `main` and `develop` | `release/*` | Prepare a release: version bumps, last-minute fixes      |
| **Hotfix**  | `main`        | `main` and `develop` | `hotfix/*`  | Urgent production fixes that can't wait for next release |

#### Merge Rules

- Use `--no-ff` (no fast-forward) when merging branches so that the branch history is preserved as a distinct group of commits:
  ```bash
  git merge --no-ff feature/my-new-feature
  ```
- Delete the supporting branch after it has been merged.

### Workflow Steps

1. **Create feature branch:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-new-feature
   ```

2. **Make changes:**
   - Write code following style guidelines (see below)
   - Add comments and docstrings
   - Test locally

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

4. **Push to remote:**
   ```bash
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request:**
   - Go to GitHub and create PR from your feature branch to `develop`
   - Fill out PR template with description of changes
   - Request review from maintainers

6. **Address review feedback:**
   - Make requested changes
   - Push updates to same branch
   - PR will update automatically

7. **Merge:**
   - Once approved, maintainer will merge to `develop` using `--no-ff`
   - When ready for a release, create a `release/*` branch from `develop` for final prep, then merge to `main` and back to `develop`
   - Hotfixes branch directly from `main` and merge back to both `main` and `develop`

---

## Code Style Guidelines

### Python

**Follow PEP 8 with these specifics:**

#### Naming Conventions
```python
# Functions: lowercase with underscores
def compute_virtual_height(time_delay):
    pass

# Variables: lowercase with underscores
sample_rate = 0
chirp_duration = 1.0

# Constants: UPPERCASE with underscores
SPEED_OF_LIGHT = 299792458  # m/s
FREQ_RANGE = (2e6, 10e6)    # Hz

# Classes: PascalCase
class IonogramProcessor:
    pass
```

#### Docstrings
Use Google-style docstrings:

```python
def cross_correlate_chirp(tx_signal, rx_signal, sample_rate):
    """
    Cross-correlate transmitted chirp with received signal to find echo delay.

    Computes the normalized cross-correlation between the transmitted chirp
    and the received signal, then identifies peaks corresponding to the
    direct path and ionospheric echo.

    Args:
        tx_signal (np.ndarray): Transmitted chirp waveform.
        rx_signal (np.ndarray): Received signal containing direct path and echo.
        sample_rate (float): Sample rate in Hz.

    Returns:
        float: Time delay in seconds between direct path and echo.

    Example:
        >>> delay = cross_correlate_chirp(chirp, recording, 250e3)
        >>> height = delay * SPEED_OF_LIGHT / 2
    """
```

#### Comments
```python
# Good: Explain WHY, not WHAT
# Use Hamming window to reduce spectral leakage from finite chirp duration
windowed_signal = signal * np.hamming(len(signal))

# Bad: States the obvious
# Multiply signal by Hamming window
windowed_signal = signal * np.hamming(len(signal))
```

#### Imports
```python
# Standard library imports first
from datetime import datetime, timedelta
import os

# Third-party imports second
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Local imports last
from processing import chirp_correlator
```

---

## Testing Guidelines

### Automated Testing

We use **pytest** for automated testing.

#### Data Processing Tests

- [ ] Chirp generation produces expected waveform
- [ ] Cross-correlation correctly identifies known time delays
- [ ] Virtual height calculation is accurate for known inputs
- [ ] Data loading handles expected file formats
- [ ] Edge cases handled (e.g., no echo detected, clipped signals)

#### Validation Tests

- [ ] Results are consistent with reference data (e.g., Wallops Island ionosonde)
- [ ] Output formats match expected specifications

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_correlation.py
```

---

## Documentation Standards

### Code Documentation Requirements

**Every new function must have:**

1. Google-style docstring explaining purpose
2. Parameter descriptions with types
3. Return value description
4. Example usage (if not obvious)

**Complex algorithms must have:**

1. Inline comments explaining logic
2. References to sources (if using published algorithms or formulas)

**New features must include:**

1. Update to README.md if applicable

**When using AI assistance (Claude, etc.):**

1. Review [CLAUDE.md](CLAUDE.md) for project context before starting
2. Log every AI session in the Session Log table in [CLAUDE.md](CLAUDE.md) (date, LLM name/version, summary of work done)
3. Include `Co-Authored-By: Claude <noreply@anthropic.com>` in git commit messages for AI-assisted changes
4. Review all AI-generated output before committing — treat AI suggestions as drafts requiring human approval

### Writing Style

- Be concise but complete
- Use active voice ("The function returns..." not "The value is returned...")
- Include code examples
- Link to relevant external resources
- Define domain-specific terms (ionospheric science, signal processing) on first use

---

## Submitting Changes

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes (1-2 sentences)

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Changes Made
- List specific changes
- Use bullet points
- Be specific

## Testing Done
- [ ] Tested locally with sample data
- [ ] All existing tests pass
- [ ] Added new tests for new functionality
- [ ] Updated documentation

## Related Issues
Closes #123
Related to #456
```

### Commit Message Format

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(processing): add chirp cross-correlation function

Implement normalized cross-correlation between transmitted chirp and
received signal. Identifies direct path and echo peaks to compute
time delay.

Closes #12
```

```
fix(correlation): handle case where no echo is detected

Return None instead of raising an exception when cross-correlation
finds no peak above the noise floor threshold.

Fixes #25
```

```
docs: add signal processing overview to README

Add section explaining the chirp generation, transmission, and
cross-correlation pipeline.
```

---

## Reporting Issues

### Bug Reports

**Use this template:**

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Run '...'
2. With input data '...'
3. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- Python version: [e.g., 3.11]
- OS: [e.g., Ubuntu 22.04]
- NumPy/SciPy version: [e.g., 1.26/1.12]

## Sample Data
If applicable, attach or describe the input data that triggers the bug

## Additional Context
Any other relevant information (error traceback, plots, etc.)
```

### Feature Requests

**Use this template:**

```markdown
## Feature Description
Clear description of the feature

## Use Case
Explain why this feature would be useful:
- Who would use it?
- What problem does it solve?
- How does it improve ionosonde data processing or analysis?

## Proposed Solution
Describe how you envision this working

## Alternatives Considered
Other approaches you've thought about

## Additional Context
References to papers, algorithms, or similar implementations
```

### Questions

For technical questions, feel free to open a discussion or contact the maintainers directly.

---

## Code Review Process

### What Reviewers Look For

1. **Correctness:** Does it produce scientifically valid results?
2. **Code Quality:** Follows style guidelines?
3. **Documentation:** Well-commented and documented?
4. **Testing:** Adequately tested with known inputs/outputs?
5. **Performance:** Efficient for large datasets?

### Review Timeline

- Small PRs (<100 lines): 1-2 days
- Medium PRs (100-500 lines): 3-5 days
- Large PRs (>500 lines): 1 week+

**Tip:** Smaller PRs get reviewed faster! Break large features into multiple PRs if possible.

---

## Project Priorities

### High Priority

1. **Correctness:** Data processing must produce scientifically valid results
2. **Reproducibility:** Results must be reproducible from raw data
3. **Validation:** Outputs should be validated against reference ionosonde data

### Medium Priority

1. **Multi-frequency support:** Process echoes across multiple bands for true height calculation
2. **Visualization:** Clear, publication-quality plots of ionograms and layer heights
3. **Data formats:** Support for standard ionosonde data formats

### Low Priority

1. **Real-time processing:** Live processing during data collection
2. **Automation:** Automated data collection and processing pipelines

---

## Resources for Contributors

### Project Documentation

- [README.md](README.md) - Project overview and setup
- [CLAUDE.md](CLAUDE.md) - AI assistant context and guidelines
- [docs/](docs/) - Reference materials including the HamSCI 2025 poster

### Scientific Resources

- [HamSCI Project](https://hamsci.org/) - Parent project
- [Lowell GIRO Data Center](https://giro.uml.edu/) - Digisonde data for validation
- Lloyd, W. C. (2019). *Ionospheric Sounding During a Total Solar Eclipse.* Master's Thesis, Virginia Tech.

### Technical Resources

- [NumPy Documentation](https://numpy.org/doc/)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
- [GNU Radio Documentation](https://wiki.gnuradio.org/)

### Development Tools

- [Visual Studio Code](https://code.visualstudio.com/) - Code editor
- [pytest Documentation](https://docs.pytest.org/) - Testing framework

---

## Recognition

Contributors will be recognized in:
- Repository README.md
- Documentation acknowledgments
- Conference presentations (HamSCI Workshop, Dayton Hamvention)
- Academic publications resulting from this work

---

## License

By contributing to this project, you agree that your contributions will be licensed under the GNU General Public License v3.0, the same license as the project.

---

## Questions?

**Project Lead:**
Gerard Piccini
Email: <gerard.piccini@scranton.edu>

**Faculty Advisor:**
Dr. Nathaniel Frissell, W2NAF
Email: <nathaniel.frissell@scranton.edu>

**Institutions:**
University of Scranton / MIT Haystack Observatory

---

**Thank you for contributing to HamSCI and advancing amateur radio science!**
