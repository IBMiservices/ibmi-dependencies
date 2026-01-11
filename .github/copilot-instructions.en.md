# IBM i Dependencies - Instructions for AI Coding Agents

## Project Overview

Git dependency manager for IBM i (AS/400) projects, integrated with TOBI/Code for IBM i. Manages external dependencies (RPGLE, includes, etc.) via Git, similar to npm/pip but for the IBM i ecosystem.

## Architecture

```
.vscode-deps/          # Python dependency management tools
├── install_deps_v2.py # Main installation script
├── ibmi_deps.py       # CLI with commands (init, install, add, remove, etc.)
├── lockfile.py        # Lockfile management
└── tests.py           # Unit tests

schema/                # JSON schema for validation
dependencies.json      # Dependencies configuration (like package.json)
iproj.json            # IBM i project metadata (TOBI compatible)
Rules.mk              # Build with GNU Make (makei)
```

### Data Flow

1. **dependencies.json** → defines Git dependencies with semver versions
2. **install_deps_v2.py** → clones repositories into `dep/`, validates against schema
3. **lockfile.py** → generates `dependencies-lock.json` with exact commit SHAs
4. **Rules.mk + iproj.json** → automatically updated for compilation

## Specific Conventions

### dependencies.json Structure

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "project",
  "version": "1.0.0",
  "dependencies": {
    "package-name": {
      "repository": "https://github.com/user/repo.git",
      "version": "^1.0.0",  // Semver: ^, ~, >=, <=, *, latest
      "ref": "v1.0.0",       // Git ref: branch, tag, SHA
      "optional": false,
      "exclude": ["tests", "docs"]
    }
  },
  "config": {
    "targetDir": "dep",             // Where to install
    "cleanGit": true,               // Remove .git
    "recursiveDependencies": true   // Transitive dependencies
  }
}
```

### iproj.json File (IBM i)

- **Dynamic variables**: `&CURLIB`, `&BUILDLIB` for multi-environment builds
- **objlib/curlib**: IBM i target libraries
- **buildCommand**: uses `makei` (GNU Make wrapper for IBM i)
- **includePath**: automatically added during dependency installation

## Essential Commands

```bash
# Install dependencies
python .vscode-deps/install_deps_v2.py

# Full CLI
python .vscode-deps/ibmi_deps.py install
python .vscode-deps/ibmi_deps.py add <name> <url> --version "^1.0.0"
python .vscode-deps/ibmi_deps.py remove <name>
python .vscode-deps/ibmi_deps.py validate  # Validate against schema

# Unit tests
python .vscode-deps/tests.py                    # Run all tests
python -m unittest .vscode-deps.tests -v        # Verbose mode
python -m unittest .vscode-deps.tests.TestLockfile  # Specific test

# Tests with pytest (optional)
pytest .vscode-deps/tests.py -v
pytest .vscode-deps/tests.py --cov=.vscode-deps  # With coverage

# Build (on IBM i with Code for IBM i)
makei build        # Compile all
makei compile -f file.rpgle
```

## Code Patterns

### Schema Validation (install_deps_v2.py)

Uses `jsonschema` to validate `dependencies.json` against `schema/dependencies.schema.json`. If jsonschema is not installed, emits a warning but continues.

### Circular Dependency Detection

`check_circular_dependencies()` in [install_deps_v2.py](.vscode-deps/install_deps_v2.py) recursively traverses dependencies to detect cycles before installation.

### Lockfile with Commit SHA

[lockfile.py](.vscode-deps/lockfile.py) records exact commit SHAs to guarantee reproducibility, even if `dependencies.json` uses version constraints.

### Structured Logging

All operations log to `install_deps.log` with timestamps. Uses Python's standard `logging` module.

## Tests

### Unit Tests ([tests.py](.vscode-deps/tests.py))

**Structure**: Standard Python unittest with 4 test classes:

1. **TestDependencySchema**: validation of `dependencies.json` files
   - Minimal/complete configuration
   - Format and required fields

2. **TestLockfile**: lockfile management
   - Create/save lockfile
   - Detect package changes
   - Persist commit SHAs

3. **TestCircularDependencies**: circular dependency detection
   - Simple/complex dependency graphs

4. **TestVersionConstraints**: semver constraints
   - Exact versions, `^` (caret), `~` (tilde)
   - Version matching according to constraints

**Execution**:
```bash
python .vscode-deps/tests.py              # Run all
python -m unittest .vscode-deps.tests.TestLockfile -v  # Single test
```

### Integration Tests

**Manual tests** for end-to-end validation:

1. **Dependency installation**:
   ```bash
   # Create test project
   mkdir test-project && cd test-project
   cp -r /path/to/.vscode-deps .
   
   # Create dependencies.json with real Git repo
   python .vscode-deps/ibmi_deps.py init --name test-integration
   python .vscode-deps/ibmi_deps.py add test-lib https://github.com/user/lib.git
   
   # Install and verify
   python .vscode-deps/install_deps_v2.py
   ls -la dep/test-lib  # Check presence
   cat dependencies-lock.json  # Check commit SHA
   ```

2. **Cycle detection**:
   ```bash
   # Test with intentional circular dependencies
   # (pkg-a depends on pkg-b which depends on pkg-a)
   # Script must fail with explicit message
   ```

3. **Build files update**:
   ```bash
   python .vscode-deps/install_deps_v2.py
   cat iproj.json | grep includePath  # Check dep/*/ref added
   cat Rules.mk | grep SUBDIRS        # Check subdirs added
   ```

4. **IBM i Build** (requires IBM i connection):
   ```bash
   # Via Code for IBM i
   # Actions > Build all
   # Check compilation with dependency includes
   ```

**Test patterns**:
- `setUp()` / `tearDown()`: uses `tempfile` for isolation
- Temporary files automatically cleaned
- Isolated tests without side-effects

## Integrations

### TOBI/Code for IBM i

- **iproj.json**: recognized by VS Code "Code for IBM i" extension
- **.vscode/actions.json**: defines build/compile actions via extension
- Build with `makei` (GNU Make adapted for IBM i)

### Git

- Repository cloning with `subprocess` + `git clone`
- Ref support: branches, tags, commit SHAs
- Optional `.git/` cleanup after installation

## IBM i Specifics

- **RPGLE**: main language (RPG ILE - Integrated Language Environment)
- **.rpgleinc**: RPGLE include files (equivalent to .h in C)
- **Libraries**: IBM i concept for organizing objects (≈ SQL schemas)
- **makei**: GNU Make wrapper for compiling on IBM i via PASE (Unix environment)

## Common Errors

- **jsonschema missing**: `pip install jsonschema` (optional but recommended)
- **Git not found**: check that Git is in PATH
- **Circular dependency**: script detects it and stops installation
- **Invalid schema**: check with `ibmi_deps.py validate`

## Development

- Language: **Python 3** (3.6+)
- No external framework (except optional jsonschema)
- Tests: standard Python unittest
- Documentation: French (francophone project)
