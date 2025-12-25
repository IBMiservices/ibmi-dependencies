# Guide d'utilisation - Gestionnaire de dépendances IBM i

## Installation dans votre projet

1. **Copier les outils** :
   ```bash
   cd votre-projet-ibmi
   git clone https://github.com/IBMiservices/ibmi-dependencies.git .temp
   cp -r .temp/.vscode-deps .
   cp .temp/dependencies.json .
   cp .temp/schema ./schema -r
   rm -rf .temp
   ```

2. **Installer jsonschema** (recommandé) :
   ```bash
   pip install jsonschema
   ```

## Utilisation

```bash
# Installer les dépendances
python .vscode-deps/install_deps_v2.py
```

## Configuration `dependencies.json`

### Structure de base

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "nom-du-projet",
  "version": "1.0.0",
  "description": "Description du projet",
  "author": "Votre nom",
  "license": "GPL-3.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/projet.git"
  },
  "dependencies": {
    "nom-package": {
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

### Options de configuration

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `targetDir` | string | `"dep"` | Répertoire où installer les dépendances |
| `cleanGit` | boolean | `true` | Supprimer les dossiers `.git` |
| `cleanDocs` | boolean | `true` | Supprimer README, LICENSE, etc. |
| `recursiveDependencies` | boolean | `true` | Installer les dépendances transitives |

### Contraintes de versions

| Syntaxe | Exemple |
|---------|---------|
| `1.0.0` | Version exacte |
| `^1.0.0` | Compatible `1.x.x` |
| `~1.0.0` | Compatible `1.0.x` |
| `>=1.0.0` | Minimum |
| `latest` | Dernière version |

## Exemples

### Projet simple

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "utils": {
      "repository": "https://github.com/ibmi/utils.git",
      "ref": "main"
    }
  }
}
```

### Avec versions et exclusions

```json
{
  "name": "mon-app",
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

## Dépannage

### Git non trouvé
```bash
git --version  # Vérifier l'installation
```

### Module jsonschema manquant
```bash
pip install jsonschema
```

### Accès dépôt privé
Configurez vos identifiants Git avant l'installation.

## Licence

Apache-2.0 - Voir [LICENSE](LICENSE)
