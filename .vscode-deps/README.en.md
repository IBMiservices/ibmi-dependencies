# .vscode-deps - IBM i Dependency Management Tools

Python tools for managing Git dependencies in IBM i projects.

## Files

- **install_deps_v2.py**: Main installation script
- **ibmi_deps.py**: Command-line interface (CLI)
- **lockfile.py**: Lockfile management
- **tests.py**: Unit tests
- **test_integration_logfori.py**: Integration test for logfori installation
- **requirements.txt**: Python dependencies

## Installation

```bash
pip install -r requirements.txt
```

**Required**:
- Python 3.6+
- Git

**Optional**:
- `jsonschema` for schema validation
- `pytest` for running tests with coverage

## Usage

### Basic Installation

```bash
# From project root
python .vscode-deps/install_deps_v2.py
```

### CLI Commands

```bash
# Initialize new project
python .vscode-deps/ibmi_deps.py init --name my-project

# Install dependencies
python .vscode-deps/ibmi_deps.py install

# Add dependency
python .vscode-deps/ibmi_deps.py add mylib https://github.com/user/mylib.git --version "^1.0.0"

# Remove dependency
python .vscode-deps/ibmi_deps.py remove mylib

# List dependencies
python .vscode-deps/ibmi_deps.py list

# Validate dependencies.json
python .vscode-deps/ibmi_deps.py validate

# Show dependency info
python .vscode-deps/ibmi_deps.py info mylib

# Update dependencies
python .vscode-deps/ibmi_deps.py update [name]

# Clean dep/ directory
python .vscode-deps/ibmi_deps.py clean
```

## Testing

### Unit Tests

```bash
# Run all tests
python .vscode-deps/tests.py

# Run with unittest
python -m unittest .vscode-deps.tests -v

# Run specific test class
python -m unittest .vscode-deps.tests.TestLockfile -v

# With pytest
pytest .vscode-deps/tests.py -v
pytest .vscode-deps/tests.py --cov=.vscode-deps
```

### Integration Test

```bash
# Test real installation of logfori
python .vscode-deps/test_integration_logfori.py
```

## Architecture

### install_deps_v2.py

Main features:
- JSON schema validation
- Circular dependency detection
- Git clone/checkout with specific refs
- Lockfile generation with commit SHAs
- Automatic update of `Rules.mk` and `iproj.json`
- Structured logging

### lockfile.py

Manages `dependencies-lock.json`:
- Records exact commit SHAs
- Detects dependency changes
- Ensures reproducibility

### ibmi_deps.py

CLI providing:
- Project initialization
- Dependency addition/removal
- Installation and updates
- Validation and information display

## Logging

All operations are logged to `install_deps.log` with:
- Timestamps
- Log levels (INFO, WARNING, ERROR)
- Detailed error traces

## Error Handling

The scripts handle:
- Missing Git
- Missing jsonschema (warning only)
- Git clone failures
- Circular dependencies
- Cross-drive paths (Windows)
- Missing files (iproj.json, schema)

## Integration

Designed to work with:
- **Code for IBM i** VS Code extension
- **TOBI** (IBM i Build tools)
- **makei** (GNU Make for IBM i)
- **Git** for version control
