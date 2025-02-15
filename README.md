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

