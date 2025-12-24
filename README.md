# IBM i Dependency Management Project

This project allows you to clone and manage dependencies from various Git repositories specified in a JSON file. It also removes certain specific files and folders after cloning.

## Project Structure
Copy the structure of this project in your [BOB](https://github.com/IBM/ibmi-bob) project.

```
/
├── core/                    # IBM i package source code (RPGLE, BND, etc.)
├── ref/                     # Include files (.rpgleinc)
├── .vscode-deps/            # Python tools for VS Code dependency management
│   ├── ibmi_deps.py         # CLI tool (recommended)
│   ├── install_deps_v2.py   # Modern installer (v2.0)
│   ├── install_deps.py      # Legacy installer (v1.0)
│   ├── migrate_v1_to_v2.py  # Migration tool
│   └── README.md            # Tools documentation
├── dependencies.json        # Your project dependencies
├── iproj.json              # BOB build configuration
├── Rules.mk                # Makefile rules
└── ibmi-dependencies.code-workspace  # VS Code workspace config
```

**Key directories:**
- **Package sources** (core/, ref/) remain at the root for BOB/gmake compatibility
- **VS Code tools** (.vscode-deps/) are separated to avoid mixing with IBM i code
- **Configuration files** (dependencies.json, iproj.json) stay at the root

## Files

### `dependencies.json`

This file contains information about the dependencies to be cloned. 

**Note:** The current dependencies (APIIBMi and CommandsAPI) are examples to demonstrate the functionality. Replace them with your own project dependencies.

Example:

```json
{
  "dependencies": {
    "messageutils": {
      "url": "https://github.com/IBMiservices/messageutils.git",
      "ref": "1-classe-message"
    },
    "APIIBMi": {
      "url": "https://github.com/IBMiservices/API.git",
      "ref": "v0.0.1"
    }
  }
}
```

### `install_deps.py`

This Python script reads the `dependencies.json` file, clones the specified repositories, and removes certain specific files and folders after cloning. Here is an overview of the main functions:

- `clone_or_update(repo_name, repo_info, base_dir)`: Clones or updates a Git repository, then removes certain specific files and folders.
- `install_dependencies(dependencies_file, base_dir, processed_repos=None)`: Installs the dependencies specified in the JSON file, handling nested dependencies.

## Usage

To install the dependencies, run the `install_deps.py` script:

```sh
python .vscode-deps/install_deps.py
```
or use the ctrl+shift+p in vscode and Execute task Install dependencies.

## Using this Project as a Template

This project is configured as a VS Code workspace template for IBM i development. To use it as a template for your own projects:

### Method 1: Using the Workspace File
1. Copy the `ibmi-dependencies.code-workspace` file to your new project directory
2. Rename it to match your project name
3. Open it with VS Code (File > Open Workspace from File)
4. Customize the workspace settings as needed

### Method 2: Manual Setup
1. Copy the entire `.vscode/` directory to your new project
2. The directory includes:
   - `tasks.json`: Predefined tasks (like Install dependencies)
   - `extensions.json`: Recommended extensions for IBM i development
   - `settings.json`: Editor configuration optimized for RPGLE and IBM i files
3. Adjust the `dependencies.json` file for your specific dependencies
4. Modify `iproj.json` for your project's build configuration

### Recommended Extensions
The workspace automatically recommends these extensions:
- Code for IBM i
- IBM i Languages
- RPGLE Language Support

These will be suggested for installation when you open the workspace.

This will read the `dependencies.json` file, clone the specified repositories into the `dep` directory, and remove the specific files and folders.

## License

This project is licensed under the GNU General Public License v3.0.
