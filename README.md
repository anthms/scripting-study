# scripting-study

Intermediate scripting study repository focused on DevOps and CI/CD automation, covering both **Bash** and **Python**.

## Goals

- Learn and practice intermediate scripting patterns used in real DevOps workflows
- Run and test scripts both **locally** and through **GitHub Actions** automation
- Build reusable patterns for CI/CD pipelines, system management, and file operations

## Repository Structure

```
scripting-study/
├── bash/
│   ├── basics/          # Intermediate Bash concepts (variables, loops, functions)
│   ├── devops/          # DevOps-focused Bash scripts (files, env, processes)
│   └── tests/           # Bash test runner and unit tests
├── python/
│   ├── basics/          # Intermediate Python concepts (variables, loops, functions)
│   ├── devops/          # DevOps-focused Python scripts (files, env, processes)
│   ├── tests/           # pytest test suite
│   └── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml       # GitHub Actions CI for both Bash and Python
```

## Quick Start

### Bash

```bash
# Run a script directly
bash bash/basics/variables.sh

# Run the Bash test suite
bash bash/tests/run_tests.sh
```

### Python

```bash
# Install dependencies
pip install -r python/requirements.txt

# Run a script directly
python python/basics/variables.py

# Run the Python test suite
pytest python/tests/ -v
```

## Topics Covered

| Topic | Bash | Python |
|---|---|---|
| Variables & data types | ✅ | ✅ |
| Loops & iteration | ✅ | ✅ |
| Functions | ✅ | ✅ |
| File operations | ✅ | ✅ |
| Environment & system info | ✅ | ✅ |
| CI/CD automation | ✅ (GitHub Actions) | ✅ (GitHub Actions) |

## CI / CD

All scripts are validated automatically on every push and pull request via **GitHub Actions**.
See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for the workflow definition.
