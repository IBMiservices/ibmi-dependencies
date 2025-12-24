# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [2.0.0] - 2025-12-24

### ✨ Ajouté

- **Validation automatique du schéma JSON** avec jsonschema
- **Système de logging avancé** avec sortie console et fichier
- **Fichier de verrouillage** (`dependencies-lock.json`) pour installations reproductibles
- **Détection de dépendances circulaires** avant installation
- **Support des dépendances optionnelles** avec `"optional": true`
- **Exclusion de fichiers/dossiers** via le champ `"exclude"`
- **Gestion d'erreurs robuste** avec messages détaillés
- **Configuration flexible** dans le champ `"config"`
- **Tests unitaires** complets (`tests.py`)
- **Documentation complète** :
  - `GUIDE_UTILISATEUR.md` - Guide détaillé
  - `schema/README.md` - Documentation du schéma
  - `README_V2.md` - README v2.0
- **Module lockfile** (`lockfile.py`) pour gestion du fichier de verrouillage
- **Script amélioré** (`install_deps_v2.py`) avec toutes les nouvelles fonctionnalités

### 🔧 Modifié

- Structure du fichier `dependencies.json` enrichie avec métadonnées
- Format des dépendances : `"url"` → `"repository"`, ajout de `"version"`
- Logging : `print()` → `logging` avec niveaux INFO/WARNING/ERROR
- Gestion Git : capture des sorties d'erreur pour meilleur débogage
- `.gitignore` étendu pour inclure logs, cache Python, dépendances

### 📚 Documentation

- Ajout de `requirements.txt` pour dépendances Python
- Ajout de `CHANGELOG.md` pour suivi des versions
- Enrichissement du README avec exemples et badges
- Documentation du schéma JSON avec tableaux de référence

### 🐛 Corrections

- Amélioration de la gestion des chemins Windows/Linux
- Meilleure gestion des erreurs Git
- Validation des URLs de dépôts

### 🔒 Sécurité

- Vérification d'intégrité via hashing SHA-256
- Validation des entrées utilisateur
- Capture d'exceptions pour éviter les crashs

---

## [1.0.0] - Date initiale

### Ajouté

- Script Python de base (`install_deps.py`)
- Clonage automatique de dépôts Git
- Gestion des dépendances transitives
- Nettoyage des fichiers `.git`, `.vscode`, etc.
- Mise à jour automatique de `Rules.mk` et `iproj.json`
- Création de fichiers `Rules.mk` vides dans sous-dossiers
- Support de références Git (branches, tags)
- Exemple de service de messages RPG
- Configuration `dependencies.json` basique
- Intégration avec BOB (Better Object Builder)

### Structure

- `install_deps.py` - Script principal
- `dependencies.json` - Configuration des dépendances
- `iproj.json` - Configuration IBM i
- `Rules.mk` - Fichier de build principal
- `core/` - Code source exemple
- `ref/` - Headers RPG

---

## [Non publié]

### Prévu pour v2.1.0

- Interface CLI avec commandes (`init`, `install`, `update`, `list`)
- Registre centralisé de packages IBM i
- Résolution intelligente de conflits de versions
- Support de multiples sources de packages
- Cache local pour éviter reclonages
- Commande `publish` pour partager des packages
- Intégration CI/CD avec exemples GitHub Actions
- Mode verbose et dry-run
- Rollback automatique en cas d'échec

### Prévu pour v3.0.0

- API REST pour registre de packages
- Interface web de gestion
- Authentification pour packages privés
- Métriques d'utilisation
- Recommandations de packages
- Migration automatique de projets existants

---

## Notes de version

### Migration v1.0 → v2.0

**Changements incompatibles :**

1. **Structure `dependencies.json`** :
   ```json
   // v1.0
   {
     "dependencies": {
       "lib": {
         "url": "...",
         "ref": "..."
       }
     }
   }
   
   // v2.0
   {
     "name": "projet",
     "version": "1.0.0",
     "dependencies": {
       "lib": {
         "repository": "...",
         "ref": "...",
         "version": "^1.0.0"
       }
     }
   }
   ```

2. **Script** : Utiliser `install_deps_v2.py` au lieu de `install_deps.py`

3. **Fichier lockfile** : Nouveau fichier `dependencies-lock.json` créé automatiquement

**Rétrocompatibilité :**
- `install_deps.py` (v1.0) reste disponible
- Le nouveau script accepte l'ancien format avec avertissement
- Migration progressive possible

### Dépendances

**Python ≥ 3.6 requis**

Modules optionnels :
- `jsonschema` (recommandé pour validation)
- `pytest` (pour exécuter les tests)

Installation :
```bash
pip install -r requirements.txt
```

---

## Liens

- [Changelog format](https://keepachangelog.com/fr/1.0.0/)
- [Semantic Versioning](https://semver.org/lang/fr/)
- [Dépôt GitHub](https://github.com/IBMiservices/ibmi-dependencies)
