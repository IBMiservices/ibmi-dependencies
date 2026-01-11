# Dependencies Schema

This directory contains the JSON schema for validating `dependencies.json` files.

## Files

- **dependencies.schema.json**: JSON Schema (draft-07) defining the structure and constraints for dependency configuration files

## Usage

The schema is automatically referenced in `dependencies.json` via:

```json
{
  "$schema": "./schema/dependencies.schema.json",
  ...
}
```

This enables:
- **IDE autocomplete** in VS Code and other editors
- **Automatic validation** when editing the file
- **Runtime validation** via `install_deps_v2.py` (requires `jsonschema` package)

## Validation

Manual validation:
```bash
python .vscode-deps/ibmi_deps.py validate
```

Or programmatically:
```python
from jsonschema import validate
import json

with open('schema/dependencies.schema.json') as f:
    schema = json.load(f)

with open('dependencies.json') as f:
    data = json.load(f)

validate(instance=data, schema=schema)
```

## Schema Structure

### Required Fields
- `name`: Project name (alphanumeric with `-` and `_`)
- `version`: Semantic version (e.g., `1.0.0`)
- `dependencies`: Object of dependencies

### Optional Fields
- `description`: Project description
- `author`: Author name
- `license`: License (e.g., `Apache-2.0`, `MIT`)
- `repository`: Repository info (type + URL)
- `devDependencies`: Development dependencies
- `config`: Installation configuration

### Dependency Properties
- `repository` (required): Git repository URL
- `version`: Semver constraint (`^1.0.0`, `~1.0.0`, `>=1.0.0`, `latest`, etc.)
- `ref`: Git reference (branch, tag, commit SHA)
- `optional`: Boolean, dependency is optional
- `exclude`: Array of files/folders to exclude

## References

- JSON Schema specification: https://json-schema.org/
- Semantic Versioning: https://semver.org/
