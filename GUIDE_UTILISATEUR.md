# Guide d'utilisation - Gestionnaire de dépendances IBM i v2.0

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Cloner le dépôt
git clone https://github.com/IBMiservices/ibmi-dependencies.git
cd ibmi-dependencies

# Installer les dépendances Python (optionnel mais recommandé)
pip install jsonschema
```

### 2. Configuration de votre projet

Créez un fichier `dependencies.json` à la racine de votre projet :

```json
{
  "name": "mon-projet-ibmi",
  "version": "1.0.0",
  "description": "Mon projet IBM i",
  "dependencies": {
    "message-service": {
      "repository": "https://github.com/exemple/message-service.git",
      "version": "^1.0.0",
      "ref": "v1.0.0"
    }
  }
}
```

### 3. Installation des dépendances

```bash
# Utiliser la nouvelle version
python install_deps_v2.py

# Ou l'ancienne version (moins de fonctionnalités)
python install_deps.py
```

## 📋 Fonctionnalités

### Version 2.0 (install_deps_v2.py)

✅ **Validation automatique du schéma JSON**
- Vérifie la structure de `dependencies.json`
- Détecte les erreurs de configuration avant l'installation

✅ **Système de logging avancé**
- Messages détaillés dans le terminal
- Fichier de log `install_deps.log` pour le débogage
- Niveaux de log : INFO, WARNING, ERROR

✅ **Gestion d'erreurs robuste**
- Capture des erreurs de clonage Git
- Support des dépendances optionnelles
- Rollback automatique en cas d'échec

✅ **Détection de dépendances circulaires**
- Analyse les dépendances pour éviter les cycles
- Prévient les installations infinies

✅ **Fichier de verrouillage (lockfile)**
- `dependencies-lock.json` pour des installations reproductibles
- Enregistre les versions exactes installées
- Hashing d'intégrité

✅ **Configuration flexible**
- Options de nettoyage personnalisables
- Exclusion de fichiers/dossiers
- Support des dépendances transitives

## 📝 Format du fichier dependencies.json

### Structure complète

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
| `updateBuildFiles` | boolean | `true` | Mettre à jour `Rules.mk` et `iproj.json` |
| `recursiveDependencies` | boolean | `true` | Installer les dépendances transitives |

### Contraintes de versions

| Syntaxe | Signification | Exemple |
|---------|---------------|---------|
| `1.0.0` | Version exacte | Seulement `1.0.0` |
| `^1.0.0` | Compatible majeure | `1.0.0` à `1.x.x` |
| `~1.0.0` | Compatible patch | `1.0.0` à `1.0.x` |
| `>=1.0.0` | Minimum | `1.0.0` et supérieur |
| `*` ou `latest` | Dernière version | Version la plus récente |

## 🔧 Fichier de verrouillage

Le fichier `dependencies-lock.json` est créé automatiquement :

```json
{
  "version": "1.0.0",
  "lockfileVersion": 1,
  "created": "2025-12-24T10:00:00",
  "updated": "2025-12-24T10:05:00",
  "packages": {
    "message-service": {
      "repository": "https://github.com/exemple/message-service.git",
      "ref": "v1.0.0",
      "version": "1.0.0",
      "commitSha": "abc123def456...",
      "resolved": "2025-12-24T10:05:00",
      "integrity": "sha256-...",
      "dependencies": {}
    }
  }
}
```

**Avantages :**
- Installations reproductibles sur différentes machines
- Vérification de l'intégrité des packages
- Traçabilité des versions installées

## 🧪 Tests

Lancez les tests unitaires :

```bash
python tests.py
```

Les tests couvrent :
- Validation du schéma JSON
- Gestion du lockfile
- Détection de dépendances circulaires
- Résolution de contraintes de versions

## 📊 Logs

Les logs sont écrits dans :
- **Terminal** : Affichage en temps réel
- **install_deps.log** : Historique complet

Format des logs :
```
2025-12-24 10:00:00 - INFO - Démarrage de l'installation
2025-12-24 10:00:01 - INFO - ✓ Schéma JSON validé
2025-12-24 10:00:05 - INFO - ✓ message-service cloné avec succès
2025-12-24 10:00:10 - INFO - ✓ Installation terminée
```

## 🔍 Dépannage

### Erreur : "jsonschema module not found"

```bash
pip install jsonschema
```

Le script fonctionne sans jsonschema mais la validation sera désactivée.

### Erreur : "Git command failed"

Vérifiez que :
- Git est installé : `git --version`
- L'URL du dépôt est correcte
- Vous avez accès au dépôt (authentification)

### Dépendance circulaire détectée

Exemple : A dépend de B qui dépend de A

**Solution :** Refactorisez vos dépendances pour éliminer le cycle.

### Fichier lockfile corrompu

Supprimez le fichier et réinstallez :

```bash
rm dependencies-lock.json
python install_deps_v2.py
```

## 📦 Exemples d'utilisation

### Exemple 1 : Projet simple

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

### Exemple 2 : Avec dépendances de développement

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "version": "^2.0.0"
    }
  },
  "devDependencies": {
    "rpg-test": {
      "repository": "https://github.com/ibmi/rpg-test.git",
      "version": "latest"
    }
  }
}
```

### Exemple 3 : Avec exclusions

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "big-lib": {
      "repository": "https://github.com/ibmi/big-lib.git",
      "exclude": ["examples", "tests", "docs", "benchmarks"]
    }
  }
}
```

### Exemple 4 : Dépendance optionnelle

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "essential-lib": {
      "repository": "https://github.com/ibmi/essential.git"
    },
    "optional-lib": {
      "repository": "https://github.com/ibmi/optional.git",
      "optional": true
    }
  }
}
```

Si `optional-lib` échoue, l'installation continue.

## 🚧 Migration depuis v1

Pour migrer de `install_deps.py` vers `install_deps_v2.py` :

1. **Mettre à jour dependencies.json**

Ancien format :
```json
{
  "dependencies": {
    "lib-name": {
      "url": "https://github.com/user/lib.git",
      "ref": "v1.0.0"
    }
  }
}
```

Nouveau format :
```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
    "lib-name": {
      "repository": "https://github.com/user/lib.git",
      "version": "^1.0.0",
      "ref": "v1.0.0"
    }
  }
}
```

2. **Utiliser le nouveau script**

```bash
python install_deps_v2.py
```

3. **Vérifier le lockfile**

Un fichier `dependencies-lock.json` sera créé automatiquement.

## 📚 Ressources

- [Schéma JSON](schema/README.md)
- [README principal](README.md)
- [Exemples](examples/)

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le dépôt
2. Créez une branche feature
3. Ajoutez des tests
4. Soumettez une Pull Request

## 📄 Licence

GPL-3.0 - Voir [LICENSE](LICENSE)
