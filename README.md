# IBM i Dependency Management

Gestionnaire de dépendances Git pour projets IBM i avec [TOBI](https://github.com/IBM/ibmi-bob).

## Installation dans votre projet

1. **Copier les outils** dans votre projet IBM i :
   ```sh
   cd votre-projet-ibmi
   git clone https://github.com/IBMiservices/ibmi-dependencies.git .ibmi-deps-temp
   cp -r .ibmi-deps-temp/.vscode-deps .
   cp .ibmi-deps-temp/dependencies.json .
   rm -rf .ibmi-deps-temp
   ```

2. **Installer jsonschema** (optionnel mais recommandé) :
   ```sh
   pip install jsonschema
   ```

## Structure de votre projet

```
votre-projet/
├── core/                 # Votre code source (RPGLE, BND, etc.)
├── ref/                  # Vos fichiers include (.rpgleinc)
├── dep/                  # Dépendances installées (auto)
├── .vscode-deps/         # Outils de gestion
├── dependencies.json     # Configuration des dépendances
└── iproj.json            # Métadonnées du projet IBM i (TOBI/Code for IBM i)
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

## Fichier `iproj.json`

Fichier de métadonnées pour les projets IBM i (compatible TOBI, VS Code).

**Paramètres principaux** :
- `objlib` : Bibliothèque cible (ex: `"&BUILDLIB"`)
- `curlib` : Bibliothèque courante
- `preUsrlibl` / `postUsrlibl` : Listes de bibliothèques
- `setIBMiEnvCmd` : Commandes CL d'initialisation
- `includePath` : Chemins d'inclusion
- `buildCommand` : Commande de build (ex: `"gmake all"`)

Variables dynamiques (`&VAR`) permettent des builds multi-environnements (dev, CI/CD).

**Exemple** :
```json
{
  "description": "Mon projet IBM i",
  "version": "1.0.0",
  "objlib": "&BUILDLIB",
  "curlib": "MYLIB",
  "preUsrlibl": ["QTEMP"],
  "buildCommand": "gmake all"
}
```

## Documentation

Voir [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md) pour plus de détails.

## Licence

Apache-2.0
