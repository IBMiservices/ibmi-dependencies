# 📁 Réorganisation du projet - Documentation

## 🎯 Objectif

Séparer clairement les outils de gestion de dépendances VS Code du package IBM i lui-même pour :
- ✅ Éviter la confusion entre le code IBM i et les outils Python
- ✅ Faciliter la maintenance et la compréhension du projet
- ✅ Préserver la compatibilité avec BOB/gmake (fichiers à la racine)
- ✅ Améliorer l'organisation pour les développeurs

## 📦 Nouvelle structure

### Avant (mélangé)
```
/
├── core/                    # IBM i
├── ref/                     # IBM i
├── ibmi_deps.py            # Python (mélangé)
├── install_deps_v2.py      # Python (mélangé)
├── lockfile.py             # Python (mélangé)
├── dependencies.json       # Config IBM i
├── iproj.json             # Config IBM i
└── Rules.mk               # Makefile
```

### Après (organisé)
```
/
├── core/                    # IBM i package
├── ref/                     # IBM i package
├── .vscode-deps/            # Outils Python isolés ✨
│   ├── ibmi_deps.py
│   ├── install_deps_v2.py
│   ├── install_deps.py
│   ├── migrate_v1_to_v2.py
│   ├── lockfile.py
│   ├── tests.py
│   ├── demo.py
│   ├── requirements.txt
│   └── README.md
├── dependencies.json        # Config IBM i
├── iproj.json              # Config IBM i
├── Rules.mk                # Makefile
└── ibmi-dependencies.code-workspace  # Config VS Code ✨
```

## 📝 Fichiers déplacés

Tous les scripts Python ont été déplacés vers `.vscode-deps/` :

| Fichier | Ancien chemin | Nouveau chemin |
|---------|--------------|----------------|
| CLI principal | `ibmi_deps.py` | `.vscode-deps/ibmi_deps.py` |
| Installer v2 | `install_deps_v2.py` | `.vscode-deps/install_deps_v2.py` |
| Installer v1 | `install_deps.py` | `.vscode-deps/install_deps.py` |
| Migration | `migrate_v1_to_v2.py` | `.vscode-deps/migrate_v1_to_v2.py` |
| Lockfile | `lockfile.py` | `.vscode-deps/lockfile.py` |
| Tests | `tests.py` | `.vscode-deps/tests.py` |
| Demo | `demo.py` | `.vscode-deps/demo.py` |
| Requirements | `requirements.txt` | `.vscode-deps/requirements.txt` |
| Backup | `install_deps.py.backup` | `.vscode-deps/install_deps.py.backup` |

## 📚 Documentation mise à jour

Tous les fichiers de documentation ont été mis à jour avec les nouveaux chemins :

- ✅ [README.md](README.md) - Structure du projet et utilisation
- ✅ [README_V2.md](README_V2.md) - Documentation v2.0
- ✅ [QUICKSTART.md](QUICKSTART.md) - Guide de démarrage rapide
- ✅ [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md) - Guide utilisateur complet
- ✅ [examples/README.md](examples/README.md) - Exemples d'utilisation CLI
- ✅ [.vscode-deps/README.md](.vscode-deps/README.md) - Documentation des outils (nouveau)

## 🆕 Nouveaux fichiers

### `ibmi-dependencies.code-workspace`

Fichier workspace VS Code avec :
- **Settings** : Configuration Python et IBM i
- **Extensions** : Recommandations (Code for IBM i, Python, etc.)
- **Tasks** : Tâches prédéfinies pour la gestion des dépendances
- **File associations** : RPGLE, BND, BNDDIR, etc.

**Utilisation** :
```bash
# Ouvrir le workspace
code ibmi-dependencies.code-workspace
```

**Tâches disponibles** (Ctrl+Shift+P → Tasks: Run Task) :
- Install Dependencies (v2)
- Install Dependencies (v1 - legacy)
- Validate Dependencies
- List Dependencies
- Migrate v1 to v2
- Run Tests
- Clean Dependencies

### `.vscode-deps/README.md`

Documentation dédiée aux outils Python :
- Description de chaque script
- Instructions d'utilisation
- Liens vers la documentation complète

## 🔄 Migration des commandes

### Avant (à la racine)
```bash
python install_deps_v2.py
python ibmi_deps.py list
python tests.py
```

### Après (avec .vscode-deps/)
```bash
python .vscode-deps/install_deps_v2.py
python .vscode-deps/ibmi_deps.py list
python .vscode-deps/tests.py
```

### Avec le workspace VS Code
Utilisez les **tâches prédéfinies** (plus simple) :
- `Ctrl+Shift+P` → `Tasks: Run Task`
- Sélectionnez la tâche souhaitée

## ✅ Avantages

1. **Clarté** : Séparation nette entre package IBM i et outils VS Code
2. **Maintenabilité** : Plus facile de localiser et maintenir les outils
3. **Compatibilité** : Structure IBM i (core/, ref/, Rules.mk) reste à la racine
4. **Organisation** : Nom `.vscode-deps` indique clairement le rôle du dossier
5. **Workspace** : Configuration VS Code unifiée dans un seul fichier
6. **Tasks** : Accès rapide aux outils sans mémoriser les chemins

## 🔍 Vérification

```bash
# Structure du projet
tree -L 2 -I '__pycache__|.git' --dirsfirst

# Contenu de .vscode-deps
ls -la .vscode-deps/

# Statut Git
git status

# Test rapide
python .vscode-deps/ibmi_deps.py --help
```

## 📌 Notes importantes

- **Historique Git préservé** : Les fichiers ont été déplacés avec `git mv`
- **Pas de code cassé** : Toutes les références ont été mises à jour
- **Rétrocompatibilité** : `install_deps.py` (v1) reste disponible
- **Documentation** : Tous les exemples utilisent les nouveaux chemins
- **Workspace** : Facultatif mais fortement recommandé

## 🚀 Prochaines étapes

1. **Tester** : Vérifier que tout fonctionne avec les nouveaux chemins
2. **Workspace** : Ouvrir `ibmi-dependencies.code-workspace` dans VS Code
3. **Tasks** : Essayer les tâches prédéfinies
4. **Documentation** : Lire [.vscode-deps/README.md](.vscode-deps/README.md)

---

*Réorganisation effectuée le 24 décembre 2025*
