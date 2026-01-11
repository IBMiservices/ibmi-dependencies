# User Guide - IBM i Dependency Manager

## Installation in Your Project

1. **Copy the tools**:
   ```bash
   cd your-ibmi-project
   git clone https://github.com/IBMiservices/ibmi-dependencies.git .temp
   cp -r .temp/.vscode-deps .
   cp .temp/dependencies.json .
   cp .temp/schema ./schema -r
   rm -rf .temp
   ```

2. **Install jsonschema** (recommended):
   ```bash
   pip install jsonschema
   ```

## Usage

```bash
# Install dependencies
python .vscode-deps/install_deps_v2.py
```

## `dependencies.json` Configuration

### Basic Structure

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "project-name",
  "version": "1.0.0",
  "description": "Project description",
  "author": "Your name",
  "license": "Apache-2.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/project.git"
  },
  "dependencies": {
    "package-name": {
      "repository": "https://github.com/user/package.git",
      "version": "^1.0.0",
      "ref": "v1.0.0",
      "optional": false,
      "exclude": ["tests", "docs"]
    }
  },
  "devDependencies": {
    "test-framework": {
      "repository": "https://github.com/user/test.git",
      "version": "latest"
    }
  },
  "config": {
    "targetDir": "dep",
    "cleanGit": true,
    "cleanDocs": true,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `targetDir` | string | `"dep"` | Directory where dependencies are installed |
| `cleanGit` | boolean | `true` | Remove `.git` folders |
| `cleanDocs` | boolean | `true` | Remove README, LICENSE, etc. |
| `recursiveDependencies` | boolean | `true` | Install transitive dependencies |

### Version Constraints

| Syntax | Example |
|---------|---------|
| `1.0.0` | Exact version |
| `^1.0.0` | Compatible `1.x.x` |
| `~1.0.0` | Compatible `1.0.x` |
| `>=1.0.0` | Minimum |
| `latest` | Latest version |

## Examples

### Simple Project

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "utils": {
      "repository": "https://github.com/ibmi/utils.git",
      "ref": "main"
    }
  }
}
```

### With Versions and Exclusions

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "version": "^2.0.0",
      "exclude": ["tests", "docs"]
    }
  }
}
```

## Troubleshooting

### Git Not Found
```bash
git --version  # Check installation
```

### Missing jsonschema Module
```bash
pip install jsonschema
```

### Private Repository Access
Configure your Git credentials before installation.

## License

Apache-2.0 - See [LICENSE](LICENSE)
