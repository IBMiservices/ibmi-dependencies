# Schéma de configuration dependencies.json

Ce dossier contient le schéma JSON qui définit la structure du fichier `dependencies.json`.

## Structure du fichier dependencies.json

### Métadonnées du projet

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "description": "Description du projet",
  "author": "Nom de l'auteur",
  "license": "GPL-3.0"
}
```

### Configuration du dépôt

```json
{
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  }
}
```

### Dépendances

#### Dépendances de production

```json
{
  "dependencies": {
    "nom-du-package": {
      "repository": "https://github.com/user/package.git",
      "version": "^1.0.0",
      "ref": "v1.0.0"
    }
  }
}
```

#### Dépendances de développement

```json
{
  "devDependencies": {
    "package-dev": {
      "repository": "https://github.com/user/dev-package.git",
      "version": "^2.0.0"
    }
  }
}
```

### Options de dépendances

| Propriété | Type | Requis | Description |
|-----------|------|--------|-------------|
| `repository` | string | ✅ | URL du dépôt Git |
| `version` | string | ❌ | Contrainte de version (semver) |
| `ref` | string | ❌ | Référence Git (branch, tag, commit) |
| `optional` | boolean | ❌ | Dépendance optionnelle (défaut: false) |
| `exclude` | array | ❌ | Fichiers/dossiers à exclure |

### Contraintes de version (semver)

| Syntaxe | Signification | Exemple |
|---------|---------------|---------|
| `1.0.0` | Version exacte | `1.0.0` uniquement |
| `^1.0.0` | Compatible avec 1.x.x | `1.0.0` à `1.9.9` |
| `~1.0.0` | Patch compatible | `1.0.0` à `1.0.9` |
| `>=1.0.0` | Version minimum | `1.0.0` et plus |
| `*` ou `latest` | Dernière version | Version la plus récente |

### Configuration

```json
{
  "config": {
    "targetDir": "dep",
    "cleanGit": true,
    "cleanDocs": true,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `targetDir` | string | `"dep"` | Répertoire pour les dépendances |
| `cleanGit` | boolean | `true` | Supprimer les `.git` |
| `cleanDocs` | boolean | `true` | Supprimer README, LICENSE, etc. |
| `updateBuildFiles` | boolean | `true` | Mettre à jour Rules.mk et iproj.json |
| `recursiveDependencies` | boolean | `true` | Installer les dépendances transitives |

## Exemples complets

### Exemple minimal

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
    "ma-lib": {
      "repository": "https://github.com/user/ma-lib.git"
    }
  }
}
```

### Exemple complet

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "mon-projet-ibmi",
  "version": "2.1.0",
  "description": "Application de gestion pour IBM i",
  "author": "Mon Organisation",
  "license": "GPL-3.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/mon-org/mon-projet.git"
  },
  "dependencies": {
    "message-service": {
      "repository": "https://github.com/ibmi/message-service.git",
      "version": "^1.2.0",
      "ref": "v1.2.3"
    },
    "db-utils": {
      "repository": "https://github.com/ibmi/db-utils.git",
      "version": "~2.0.0"
    },
    "optional-lib": {
      "repository": "https://github.com/ibmi/optional.git",
      "optional": true,
      "exclude": ["tests", "examples"]
    }
  },
  "devDependencies": {
    "test-framework": {
      "repository": "https://github.com/ibmi/rpg-test.git",
      "version": "latest"
    }
  },
  "config": {
    "targetDir": "dependencies",
    "cleanGit": true,
    "cleanDocs": false,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

## Validation

Le schéma peut être utilisé pour valider votre fichier `dependencies.json` avec des outils comme :
- VS Code (auto-complétion et validation)
- `jsonschema` (Python)
- `ajv` (Node.js)
