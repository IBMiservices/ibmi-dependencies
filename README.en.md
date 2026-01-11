# IBM i Dependency Management

Git dependency manager for IBM i projects with [TOBI](https://github.com/IBM/ibmi-bob).

## Installation in Your Project

1. **Copy the tools** into your IBM i project:
   ```sh
   cd your-ibmi-project
   git clone https://github.com/IBMiservices/ibmi-dependencies.git .ibmi-deps-temp
   cp -r .ibmi-deps-temp/.vscode-deps .
   cp .ibmi-deps-temp/dependencies.json .
   rm -rf .ibmi-deps-temp
   ```

2. **Install jsonschema** (optional but recommended):
   ```sh
   pip install jsonschema
   ```

## Project Structure

```
your-project/
├── core/                 # Your source code (RPGLE, BND, etc.)
├── ref/                  # Your include files (.rpgleinc)
├── dep/                  # Installed dependencies (auto)
├── .vscode-deps/         # Management tools
├── dependencies.json     # Dependencies configuration
└── iproj.json            # IBM i project metadata (TOBI/Code for IBM i)
```

## `dependencies.json` Configuration

```json
{
  "dependencies": {
    "my-package": {
      "url": "https://github.com/user/package.git",
      "ref": "v1.0.0"
    }
  }
}
```

## Usage

```sh
# Install dependencies
python .vscode-deps/install_deps_v2.py

# Or via VS Code: Ctrl+Shift+P > Tasks: Run Task > Install dependencies
```

## `iproj.json` File

Metadata file for IBM i projects (compatible with TOBI, VS Code).

**Main parameters**:
- `objlib`: Target library (e.g., `"&BUILDLIB"`)
- `curlib`: Current library
- `preUsrlibl` / `postUsrlibl`: Library lists
- `setIBMiEnvCmd`: CL initialization commands
- `includePath`: Include paths
- `buildCommand`: Build command (e.g., `"gmake all"`)

Dynamic variables (`&VAR`) enable multi-environment builds (dev, CI/CD).

**Example**:
```json
{
  "description": "My IBM i project",
  "version": "1.0.0",
  "objlib": "&BUILDLIB",
  "curlib": "MYLIB",
  "preUsrlibl": ["QTEMP"],
  "buildCommand": "gmake all"
}
```

## Documentation

See [USER_GUIDE.md](USER_GUIDE.md) for more details.

## License

Apache-2.0
