# Guide: How to Fill dependencies.json

Practical guide for IBM i developers discovering JSON.

## What is JSON?

JSON is a simple text file format for storing data. It's like a DDS file but more universal:
- Data is enclosed in **curly braces** `{ }`
- **Commas** `,` separate elements
- **Colons** `:` associate a name with a value
- **Quotation marks** `"` surround text

## Basic Structure

Here's the minimal skeleton of a `dependencies.json` file:

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "dependencies": {
  }
}
```

**⚠️ Important**: 
- Always put a **comma** after each line, except the last one in a block
- **Quotation marks** are mandatory around names and text
- No comma after the last element

## Complete Commented Example

```json
{
  "name": "my-rpg-project",
  "version": "1.0.0",
  "description": "Order management project",
  "author": "John Doe",
  "license": "Apache-2.0",
  
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  }
}
```

## Fill Required Fields

### 1. Project Information

```json
{
  "name": "my-project",
```
- **What it is**: Your project name
- **Rules**: Only lowercase letters, numbers, dashes `-` and underscores `_`
- **Example**: `"order-management"`, `"my_rpg_app"`

```json
  "version": "1.0.0",
```
- **What it is**: Your project version
- **Format**: Always 3 numbers separated by dots
- **Examples**: `"1.0.0"` (first version), `"2.1.5"` (version 2, update 1, fix 5)

```json
  "dependencies": {
```
- **What it is**: List of external libraries you need
- **Similar to**: The *LIBL list in your IBM i environment

## Add a Dependency

For each external library, add a block like this:

```json
"dependencies": {
  "library-name": {
    "repository": "https://github.com/user/library.git",
    "ref": "v1.0.0"
  }
}
```

### Example with a Real Library (logfori)

```json
"dependencies": {
  "logfori": {
    "repository": "https://github.com/IBMiservices/logfori.git",
    "ref": "main"
  }
}
```

**What this does**: 
- Automatically downloads logfori source code
- Places files in the `dep/logfori/` folder
- You can then use `/COPY` or `/INCLUDE` in your RPGLE programs

## Add Multiple Dependencies

Separate each library with a **comma**:

```json
"dependencies": {
  "logfori": {
    "repository": "https://github.com/IBMiservices/logfori.git",
    "ref": "main"
  },
  "http-client": {
    "repository": "https://github.com/user/http-client.git",
    "ref": "v2.1.0"
  },
  "json-parser": {
    "repository": "https://github.com/user/json-parser.git",
    "ref": "main"
  }
}
```

**⚠️ Warning**: No comma after the last library!

## Optional but Useful Fields

### Description and Author

```json
{
  "name": "order-management",
  "version": "1.0.0",
  "description": "Customer order management application",
  "author": "RPG Team - IT Department",
  "license": "Apache-2.0",
  
  "dependencies": {
    ...
  }
}
```

### Advanced Options for Dependencies

```json
"dependencies": {
  "my-library": {
    "repository": "https://github.com/user/lib.git",
    "ref": "v1.5.0",
    "version": "^1.5.0",
    "optional": false,
    "exclude": ["tests", "docs", "examples"]
  }
}
```

**Explanations**:

- **`version`**: Constrains the installed version
  - `"^1.5.0"` = accepts 1.5.0, 1.6.0, 1.9.0, but not 2.0.0
  - `"~1.5.0"` = accepts 1.5.0, 1.5.1, 1.5.9, but not 1.6.0
  - `"*"` or `"latest"` = always the latest version

- **`optional`**: If `true`, installation doesn't fail if the library is inaccessible

- **`exclude`**: List of folders not to download (saves space)

## Global Configuration

At the end of the file, you can add parameters:

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  },
  "config": {
    "targetDir": "dep",
    "cleanGit": true,
    "cleanDocs": true,
    "recursiveDependencies": true
  }
}
```

**Parameters**:

- **`targetDir`**: Folder where to install dependencies (default `"dep"`)
- **`cleanGit`**: Remove `.git` files (recommended: `true`)
- **`cleanDocs`**: Remove README, LICENSE, etc. (recommended: `true`)
- **`recursiveDependencies`**: Also install dependencies' dependencies (recommended: `true`)

## Practical Use Cases

### Case 1: Simple Project with logfori

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  }
}
```

### Case 2: Project with Multiple Libraries

```json
{
  "name": "web-application",
  "version": "2.0.0",
  "description": "Web application with REST API",
  "author": "IT Department",
  
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "v1.2.0"
    },
    "http-framework": {
      "repository": "https://github.com/ibmi/http-framework.git",
      "ref": "v3.0.0"
    },
    "json-tools": {
      "repository": "https://github.com/ibmi/json-tools.git",
      "ref": "main"
    }
  },
  
  "config": {
    "targetDir": "lib",
    "cleanGit": true,
    "cleanDocs": true
  }
}
```

### Case 3: Optional Dependencies

```json
{
  "name": "my-project",
  "version": "1.0.0",
  
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "ref": "v2.0.0"
    }
  },
  
  "devDependencies": {
    "test-framework": {
      "repository": "https://github.com/ibmi/tests.git",
      "ref": "main",
      "optional": true
    }
  }
}
```

## Common Errors and Solutions

### ❌ Error: Extra Comma

```json
{
  "name": "project",
  "dependencies": {
    "lib1": {...},
    "lib2": {...},  ← Extra comma!
  }
}
```

**✅ Fix**:
```json
{
  "name": "project",
  "dependencies": {
    "lib1": {...},
    "lib2": {...}  ← No comma on last line
  }
}
```

### ❌ Error: Missing Quotes

```json
{
  name: my-project,  ← Missing quotes!
  "dependencies": {}
}
```

**✅ Fix**:
```json
{
  "name": "my-project",  ← Quotes required
  "dependencies": {}
}
```

### ❌ Error: Mismatched Braces

```json
{
  "dependencies": {
    "lib": {
      "repository": "..."
    }
  ← Missing brace!
}
```

**✅ Fix**:
```json
{
  "dependencies": {
    "lib": {
      "repository": "..."
    }
  }  ← Properly closed
}
```

## File Validation

To check if your file is correct:

```bash
python .vscode-deps/ibmi_deps.py validate
```

The script will display:
- ✅ `Validation successful` if everything is correct
- ❌ A precise error message if something is wrong

## JSON Quick Reference

| Character | Meaning | Example |
|-----------|---------|---------|
| `{ }` | Start and end of a block | `{"name": "project"}` |
| `[ ]` | List of values | `["tests", "docs"]` |
| `:` | Associates name with value | `"name": "value"` |
| `,` | Separates elements | `"a": 1, "b": 2` |
| `"` | Delimits text | `"my text"` |
| `true/false` | Boolean values | `"optional": true` |

## Recommended Editors

These editors help you avoid errors:

1. **VS Code** (recommended)
   - Syntax highlighting
   - Automatic error detection
   - Auto-completion with schema

2. **Notepad++**
   - JSON Viewer plugin
   - Syntax validation

3. **Avoid Windows Notepad**
   - No highlighting
   - No validation
   - Risk of incorrect encoding

## Going Further

Once `dependencies.json` is created, run the installation:

```bash
python .vscode-deps/install_deps_v2.py
```

Libraries will be downloaded to the `dep/` folder.

You can then use them in your RPGLE programs:

```rpgle
**FREE

/COPY dep/logfori/qcpysrc/logger_h.rpgleinc

Dcl-Proc Main;
  Logger_Info('Application started');
End-Proc;
```

## Support

If you have problems:
1. Check syntax with `ibmi_deps.py validate`
2. Consult logs in `install_deps.log`
3. See user guide: [USER_GUIDE.md](USER_GUIDE.md)
