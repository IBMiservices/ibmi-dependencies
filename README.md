# IBM i Dependency Management

Gestionnaire de dépendances Git pour projets IBM i avec [BOB](https://github.com/IBM/ibmi-bob).

## Structure

```
/
├── core/        # Votre code source (RPGLE, BND, etc.)
├── ref/         # Vos fichiers include (.rpgleinc)
├── dep/         # Dépendances installées (généré automatiquement)
├── .vscode-deps/            # Outils Python
├── dependencies.json        # Configuration des dépendances
└── iproj.json              # Configuration BOB
```

## Configuration `dependencies.json`

```json
{
  "dependencies": {
    "mon-package": {
      "url": "https://github.com/user/package.git",
      "ref": "v1.0.0"
    }
  }
}
```

## Utilisation

```sh
# Installer les dépendances
python .vscode-deps/install_deps_v2.py

# Ou via VS Code: Ctrl+Shift+P > Tasks: Run Task > Install dependencies
```

## Documentation

Voir [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md) pour plus de détails.

## Licence

GPL-3.0
