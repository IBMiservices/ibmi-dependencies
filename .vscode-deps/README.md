# Outils de gestion de dépendances VS Code

Ce dossier contient les scripts Python pour la gestion des dépendances IBM i dans VS Code.

## 📦 Scripts disponibles

### `ibmi_deps.py` - CLI principal (recommandé)
Interface en ligne de commande complète pour gérer les dépendances.

```bash
python .vscode-deps/ibmi_deps.py --help
```

### `install_deps_v2.py` - Installation v2.0
Script d'installation moderne avec toutes les fonctionnalités v2.0 :
- Validation de schéma
- Lockfile
- Dépendances transitives
- Logging détaillé

```bash
python .vscode-deps/install_deps_v2.py
```

### `install_deps.py` - Installation v1.0 (legacy)
Version originale, maintenue pour compatibilité.

```bash
python .vscode-deps/install_deps.py
```

### `migrate_v1_to_v2.py` - Migration
Outil de migration de dependencies.json v1.0 vers v2.0.

```bash
python .vscode-deps/migrate_v1_to_v2.py
```

### `lockfile.py` - Gestion du lockfile
Module pour la gestion du fichier de verrouillage.

### `tests.py` - Suite de tests
Tests unitaires pour tous les modules.

```bash
python .vscode-deps/tests.py
```

### `demo.py` - Démonstration
Exemples d'utilisation des différentes fonctionnalités.

```bash
python .vscode-deps/demo.py
```

## 🔧 Installation

```bash
pip install -r .vscode-deps/requirements.txt
```

## 📚 Documentation

Consultez les fichiers à la racine du projet :
- [README_V2.md](../README_V2.md) - Documentation complète v2.0
- [QUICKSTART.md](../QUICKSTART.md) - Guide de démarrage rapide
- [GUIDE_UTILISATEUR.md](../GUIDE_UTILISATEUR.md) - Guide utilisateur détaillé
- [CHANGELOG.md](../CHANGELOG.md) - Historique des versions
