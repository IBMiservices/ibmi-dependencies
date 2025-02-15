# IBM i Dependency Management Project

This project allows you to clone and manage dependencies from various Git repositories specified in a JSON file. It also removes certain specific files and folders after cloning.

## Project Structure

- `.vscode/`
  - `tasks.json`: Configuration tasks for Visual Studio Code.
- `dependencies.json`: JSON file containing information about the dependencies.
- `install_deps.py`: Python script to install the dependencies.
- `LICENSE`: Project license.

## Files

### `dependencies.json`

This file contains information about the dependencies to be cloned. Example:

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

install_deps.py
This Python script reads the dependencies.json file, clones the specified repositories, and removes certain specific files and folders after cloning. Here is an overview of the main functions:

clone_or_update(repo_name, repo_info, base_dir): Clones or updates a Git repository, then removes certain specific files and folders.
install_dependencies(dependencies_file, base_dir, processed_repos=None): Installs the dependencies specified in the JSON file, handling nested dependencies.
Usage
To install the dependencies, run the install_deps.py script:

This will read the dependencies.json file, clone the specified repositories into the dep directory, and remove the specific files and folders.

License
This project is licensed under the GNU General Public License v3.0.
