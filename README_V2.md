# 📦 Gestionnaire de Dépendances pour IBM i

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

Un système moderne de gestion de dépendances pour projets IBM i, inspiré de Maven, npm et pip.

## 🎯 Objectif

Simplifier la gestion des dépendances dans les projets IBM i en permettant :
- ✅ Clonage automatique de bibliothèques depuis Git
- ✅ Gestion des versions avec semantic versioning
- ✅ Résolution automatique des dépendances transitives
- ✅ Intégration transparente avec [BOB](https://github.com/IBM/ibmi-bob) (Better Object Builder)
- ✅ Installations reproductibles via lockfile

## 🚀 Installation rapide

```bash
# 1. Cloner ce dépôt
git clone https://github.com/IBMiservices/ibmi-dependencies.git
cd ibmi-dependencies

# 2. Installer les dépendances Python (optionnel mais recommandé)
pip install jsonschema

# 3. Configurer vos dépendances dans dependencies.json
# Voir exemples ci-dessous

# 4. Installer les dépendances
python install_deps_v2.py
```

## 📋 Utilisation basique

### 1. Créer un fichier `dependencies.json`

```json
{
  "name": "mon-projet-ibmi",
  "version": "1.0.0",
  "description": "Mon application IBM i",
  "dependencies": {
    "message-service": {
      "repository": "https://github.com/IBMiservices/messageutils.git",
      "version": "^1.0.0",
      "ref": "v1.0.0"
    }
  }
}
```

### 2. Installer les dépendances

```bash
# Utiliser la version 2.0 (recommandée)
python install_deps_v2.py

# Ou la version 1.0 (héritée)
python install_deps.py
```

### 3. Compiler votre projet

```bash
# Avec BOB (Better Object Builder)
makei build
```

## 🆕 Nouveautés v2.0

La version 2.0 apporte des améliorations majeures :

### ✨ Fonctionnalités principales

| Fonctionnalité | v1.0 | v2.0 |
|----------------|------|------|
| Clonage de dépôts | ✅ | ✅ |
| Dépendances transitives | ✅ | ✅ |
| Validation schéma JSON | ❌ | ✅ |
| Logging détaillé | ❌ | ✅ |
| Gestion d'erreurs | Basique | Robuste |
| Fichier de verrouillage | ❌ | ✅ |
| Dépendances circulaires | ❌ | ✅ Détection |
| Dépendances optionnelles | ❌ | ✅ |
| Exclusion de fichiers | ❌ | ✅ |
| Configuration flexible | ❌ | ✅ |

### 📝 Fichier de verrouillage

Un fichier `dependencies-lock.json` est créé automatiquement pour garantir des installations reproductibles :

```json
{
  "packages": {
    "message-service": {
      "repository": "https://github.com/IBMiservices/messageutils.git",
      "commitSha": "abc123...",
      "version": "1.0.0",
      "resolved": "2025-12-24T10:00:00"
    }
  }
}
```

### 🔍 Validation automatique

Le schéma JSON est validé automatiquement avant installation :
- Structure du fichier
- Format des versions (semver)
- URLs des dépôts
- Configuration

### 📊 Logging amélioré

```
2025-12-24 10:00:00 - INFO - ══════════════════════════════════════
2025-12-24 10:00:00 - INFO - Démarrage de l'installation
2025-12-24 10:00:01 - INFO - ✓ Schéma JSON validé
2025-12-24 10:00:02 - INFO - Clonage de message-service...
2025-12-24 10:00:05 - INFO - ✓ message-service installé
2025-12-24 10:00:10 - INFO - ✓ Installation terminée (5 dépendances)
```

## 📖 Documentation complète

- **[Guide utilisateur détaillé](GUIDE_UTILISATEUR.md)** - Documentation complète
- **[Schéma JSON](schema/README.md)** - Format du fichier dependencies.json
- **[README original](README.old.md)** - Documentation v1.0

## 🏗️ Structure du projet

```
ibmi-dependencies/
├── install_deps_v2.py          # ⭐ Script principal v2.0
├── install_deps.py             # Script v1.0 (hérité)
├── lockfile.py                 # Module de gestion lockfile
├── tests.py                    # Tests unitaires
├── dependencies.json           # Configuration des dépendances
├── dependencies-lock.json      # Fichier de verrouillage (auto-généré)
├── schema/
│   ├── dependencies.schema.json # Schéma JSON
│   └── README.md               # Documentation du schéma
├── core/                       # Code source exemple
│   ├── MESSAGE.RPGLE           # Service de messages
│   ├── MESSAGESRV.BND          # Binding source
│   └── Rules.mk                # Règles de build
├── ref/                        # Headers/includes
│   └── message_h.rpgleinc      # Prototypes RPG
├── dep/                        # Dépendances installées (auto-généré)
├── GUIDE_UTILISATEUR.md        # ⭐ Guide complet
└── README.md                   # Ce fichier
```

## 🎓 Exemples

### Exemple 1 : Projet simple

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "utils": {
      "repository": "https://github.com/ibmi/utils.git"
    }
  }
}
```

### Exemple 2 : Avec contraintes de versions

```json
{
  "name": "mon-app",
  "version": "2.0.0",
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "version": "^2.0.0",
      "ref": "v2.1.0"
    },
    "db-utils": {
      "repository": "https://github.com/ibmi/db.git",
      "version": "~1.5.0"
    }
  }
}
```

### Exemple 3 : Configuration avancée

```json
{
  "name": "projet-avance",
  "version": "1.0.0",
  "dependencies": {
    "essential-lib": {
      "repository": "https://github.com/ibmi/essential.git",
      "version": "^3.0.0"
    },
    "optional-lib": {
      "repository": "https://github.com/ibmi/optional.git",
      "optional": true,
      "exclude": ["tests", "examples"]
    }
  },
  "config": {
    "targetDir": "dependencies",
    "cleanGit": true,
    "cleanDocs": false,
    "recursiveDependencies": true
  }
}
```

## 🧪 Tests

Lancer les tests unitaires :

```bash
python tests.py
```

Tests disponibles :
- ✅ Validation du schéma JSON
- ✅ Gestion du lockfile
- ✅ Détection de dépendances circulaires
- ✅ Résolution de contraintes de versions

## 🔧 Configuration

### Options du fichier `config`

| Option | Type | Défaut | Description |
|--------|------|--------|-------------|
| `targetDir` | string | `"dep"` | Répertoire des dépendances |
| `cleanGit` | boolean | `true` | Supprimer `.git` |
| `cleanDocs` | boolean | `true` | Supprimer docs |
| `updateBuildFiles` | boolean | `true` | Mettre à jour Rules.mk |
| `recursiveDependencies` | boolean | `true` | Dépendances transitives |

### Contraintes de versions

| Syntaxe | Description | Exemple |
|---------|-------------|---------|
| `1.0.0` | Version exacte | `1.0.0` uniquement |
| `^1.0.0` | Compatible majeure | `1.x.x` |
| `~1.0.0` | Compatible patch | `1.0.x` |
| `>=1.0.0` | Minimum | `≥ 1.0.0` |
| `*` | Dernière | Version la plus récente |

## 🛠️ Intégration avec BOB

Ce projet s'intègre parfaitement avec [BOB (Better Object Builder)](https://github.com/IBM/ibmi-bob) :

1. Les dépendances sont clonées dans le dossier `dep/`
2. Le fichier `Rules.mk` est mis à jour automatiquement
3. Le fichier `iproj.json` inclut les chemins des `.rpgleinc`
4. Compilez avec `makei build`

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence GPL-3.0 - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👥 Auteurs

- **IBMiservices** - [GitHub](https://github.com/IBMiservices)

## 🙏 Remerciements

- Inspiré par Maven, npm, et pip
- Intégration avec [BOB](https://github.com/IBM/ibmi-bob)
- Communauté IBM i

## 📞 Support

- 📖 [Guide utilisateur](GUIDE_UTILISATEUR.md)
- 🐛 [Signaler un bug](https://github.com/IBMiservices/ibmi-dependencies/issues)
- 💬 [Discussions](https://github.com/IBMiservices/ibmi-dependencies/discussions)

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !**
