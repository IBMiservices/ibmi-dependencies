# 📦 Exemples de packages pour IBM i

Ce fichier contient des exemples de dépendances que vous pouvez utiliser dans vos projets IBM i.

## 🎯 Packages d'exemple

### 1. Service de messages

```json
{
  "message-service": {
    "repository": "https://github.com/IBMiservices/messageutils.git",
    "version": "^1.0.0",
    "ref": "main"
  }
}
```

**Description**: Service de gestion de messages programmables pour IBM i  
**Fonctionnalités**: Envoi de messages, formatage, gestion de files d'attente

### 2. Utilitaires de base de données

```json
{
  "db-utils": {
    "repository": "https://github.com/example/db-utils.git",
    "version": "~2.0.0",
    "ref": "v2.0.5"
  }
}
```

**Description**: Utilitaires pour manipuler les bases de données IBM i  
**Fonctionnalités**: Requêtes SQL, connexions, transactions

### 3. Logger RPG

```json
{
    "rpg-logger": {
    "repository": "https://github.com/example/rpg-logger.git",
    "version": "^3.1.0",
    "optional": true
  }
}
```

**Description**: Système de logging pour programmes RPG  
**Fonctionnalités**: Niveaux de log, rotation de fichiers, formatage

### 4. Framework de tests

```json
{
  "rpg-test-framework": {
    "repository": "https://github.com/example/rpg-test.git",
    "version": "latest"
  }
}
```

**Description**: Framework de tests unitaires pour RPG  
**Fonctionnalités**: Assertions, mocks, couverture de code

## 📝 Exemples complets de dependencies.json

### Projet simple

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "mon-application-simple",
  "version": "1.0.0",
  "description": "Application de gestion simple",
  "author": "Votre Nom",
  "license": "GPL-3.0",
  "dependencies": {
    "message-service": {
      "repository": "https://github.com/IBMiservices/messageutils.git",
      "version": "^1.0.0"
    }
  }
}
```

### Projet avec plusieurs dépendances

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "application-complete",
  "version": "2.1.0",
  "description": "Application complète de gestion",
  "author": "Équipe Dev",
  "license": "GPL-3.0",
  "repository": {
    "type": "git",
    "url": "https://github.com/votre-org/votre-projet.git"
  },
  "dependencies": {
    "message-service": {
      "repository": "https://github.com/IBMiservices/messageutils.git",
      "version": "^1.2.0",
      "ref": "v1.2.3"
    },
    "db-utils": {
      "repository": "https://github.com/example/db-utils.git",
      "version": "~2.0.0"
    },
    "string-utils": {
      "repository": "https://github.com/example/string-utils.git",
      "version": ">=1.5.0"
    }
  },
  "devDependencies": {
    "rpg-test-framework": {
      "repository": "https://github.com/example/rpg-test.git",
      "version": "latest"
    }
  },
  "config": {
    "targetDir": "dependencies",
    "cleanGit": true,
    "cleanDocs": true,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

### Projet avec dépendances optionnelles et exclusions

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "projet-avance",
  "version": "3.0.0",
  "description": "Projet avec configuration avancée",
  "dependencies": {
    "core-library": {
      "repository": "https://github.com/example/core.git",
      "version": "^4.0.0",
      "ref": "v4.2.1"
    },
    "big-library": {
      "repository": "https://github.com/example/big-lib.git",
      "version": "^2.0.0",
      "exclude": [
        "tests",
        "examples",
        "docs",
        "benchmarks",
        "*.md"
      ]
    },
    "optional-feature": {
      "repository": "https://github.com/example/optional.git",
      "version": "*",
      "optional": true
    }
  },
  "config": {
    "targetDir": "lib",
    "cleanGit": true,
    "cleanDocs": false,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

## 🚀 Utilisation avec le CLI

### Initialiser un projet

```bash
# Créer un nouveau dependencies.json
python ibmi_deps.py init --name mon-projet
```

### Ajouter des dépendances

```bash
# Ajouter une dépendance de production
python ibmi_deps.py add message-service \
  https://github.com/IBMiservices/messageutils.git \
  --version "^1.0.0" \
  --ref main

# Ajouter une dépendance de développement
python ibmi_deps.py add rpg-test \
  https://github.com/example/rpg-test.git \
  --dev
```

### Installer les dépendances

```bash
# Installation normale
python ibmi_deps.py install

# Simulation (dry-run)
python ibmi_deps.py install --dry-run

# Mode verbeux
python ibmi_deps.py install --verbose
```

### Lister les dépendances

```bash
# Lister depuis dependencies.json
python ibmi_deps.py list

# Lister depuis le lockfile
python ibmi_deps.py list --locked
```

### Obtenir des informations

```bash
# Info sur un package
python ibmi_deps.py info message-service

# Valider la configuration
python ibmi_deps.py validate
```

### Mettre à jour

```bash
# Mettre à jour toutes les dépendances
python ibmi_deps.py update

# Mettre à jour un package spécifique
python ibmi_deps.py update message-service
```

### Nettoyer

```bash
# Nettoyer les dépendances installées
python ibmi_deps.py clean

# Tout nettoyer (incluant lockfile)
python ibmi_deps.py clean --all
```

## 📚 Ressources

- [Guide utilisateur](../GUIDE_UTILISATEUR.md)
- [Démarrage rapide](../QUICKSTART.md)
- [Schéma JSON](../schema/README.md)
- [Documentation CLI](CLI_GUIDE.md)

## 💡 Conseils

1. **Versionnez dependencies.json** dans votre dépôt Git
2. **Versionnez dependencies-lock.json** pour garantir des builds reproductibles
3. **Utilisez .gitignore** pour exclure le répertoire des dépendances (dep/ ou lib/)
4. **Testez** vos mises à jour avec --dry-run avant de les appliquer
5. **Documentez** vos dépendances dans le README de votre projet

## ⚠️ Notes

- Les exemples utilisent des URLs fictives, adaptez-les à vos besoins
- Vérifiez toujours les licences des dépendances que vous utilisez
- Gardez vos dépendances à jour pour bénéficier des correctifs de sécurité
