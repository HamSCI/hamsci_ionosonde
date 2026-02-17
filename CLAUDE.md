# CLAUDE.md -- Project Context for AI Assistants

This file provides context for Claude Code and other AI assistants working on this project.

## Project Overview

This is the **HamSCI Ionosonde** project -- software for processing, analyzing, and validating data from a low-cost chirp ionosonde system built with software-defined radio (SDR) technology. The system transmits chirp signals (2-10 MHz), receives ionospheric echoes, and cross-correlates them to calculate virtual layer heights.

See [docs/Piccini HamSCI 2025 Poster.pdf](docs/Piccini%20HamSCI%202025%20Poster.pdf) for the full technical description.

## Repository Structure

```
hamsci_ionosonde/
├── data/               # Ionosonde data files (starter data; will eventually move out of repo)
├── docs/               # Documentation and reference materials
├── CONTRIBUTING.md     # Contribution guidelines
├── LICENSE             # GPLv3
├── CLAUDE.md           # This file
└── README.md           # Project README
```

## Project Management

- GitHub project board: https://github.com/orgs/HamSCI/projects/11
- Repository: https://github.com/HamSCI/hamsci_ionosonde

## Development Guidelines

### Language and Tools

- **Python 3.8+** for data processing and analysis
- **GNU Radio** for SDR control and signal generation
- **NumPy, SciPy, Matplotlib** for scientific computing and visualization

### Code Style

- Follow **PEP 8** for Python code
- Use **Google-style docstrings**
- Use `snake_case` for functions and variables, `UPPER_SNAKE_CASE` for constants, `PascalCase` for classes
- Order imports: standard library, third-party, local

### Git Workflow

Follow the **Git Flow** branching model:

| Branch      | Branches from | Merges back to       | Naming      | Purpose                              |
|-------------|---------------|----------------------|-------------|--------------------------------------|
| `main`      | --            | --                   | `main`      | Production-ready code                |
| `develop`   | `main`        | --                   | `develop`   | Integration branch for next release  |
| **Feature** | `develop`     | `develop`            | `feature/*` | New features                         |
| **Bugfix**  | `develop`     | `develop`            | `bugfix/*`  | Non-urgent bug fixes                 |
| **Release** | `develop`     | `main` and `develop` | `release/*` | Release preparation                  |
| **Hotfix**  | `main`        | `main` and `develop` | `hotfix/*`  | Urgent production fixes              |

- Use `--no-ff` when merging branches to preserve branch history.
- Delete supporting branches after merging.

### Commit Messages

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### Pull Requests

- Create PRs from feature/bugfix branches to `develop`
- Include description, type of change, changes made, and testing done
- Small PRs are preferred -- break large features into multiple PRs

## Domain Context

### Key Concepts

- **Ionosphere:** Region of the atmosphere with ions and electrons; electron density varies with solar energy absorption.
- **Ionosonde:** Radar system that transmits signals toward the ionosphere and measures the refracted return to determine layer heights.
- **Chirp:** A signal whose frequency increases linearly over time; used as the transmitted waveform.
- **Virtual height:** The apparent height of an ionospheric layer calculated from the round-trip time delay assuming straight-line propagation at the speed of light.
- **Cross-correlation:** Signal processing technique used to find the time delay between the transmitted chirp and the received echo.
- **SDR (Software Defined Radio):** Radio where signal processing is done in software rather than dedicated hardware (Ettus N200 USRP, Red Pitaya SDRlab 122-16).

### Frequency Range

The system operates under an FCC experimental license: **2-10 MHz at up to 300 watts**.

### Validation Reference

The **Wallops Island ionosonde** (professional Digisonde) is used as the reference for validating measurements. Data from the Lowell GIRO Data Center (LGDC) at https://giro.uml.edu/.

## Testing

- Use **pytest** for Python unit tests
- Test data processing functions with known inputs/outputs
- Validate against reference data (e.g., Wallops Island ionosonde) where available
