# IBM i Dependencies - Instructions pour agents IA

## Vue d'ensemble du projet

Gestionnaire de dépendances Git pour projets IBM i (AS/400), intégré avec TOBI/Code for IBM i. Permet de gérer des dépendances externes (RPGLE, includes, etc.) via Git, similaire à npm/pip mais pour l'écosystème IBM i.

## Architecture

```
.vscode-deps/          # Outils Python de gestion des dépendances
├── install_deps_v2.py # Script principal d'installation
├── ibmi_deps.py       # CLI avec commandes (init, install, add, remove, etc.)
├── lockfile.py        # Gestion du fichier de verrouillage
└── tests.py           # Tests unitaires

schema/                # Schéma JSON pour validation
dependencies.json      # Configuration des dépendances (comme package.json)
iproj.json            # Métadonnées projet IBM i (compatible TOBI)
Rules.mk              # Build avec GNU Make (makei)
```

### Flux de données

1. **dependencies.json** → définit les dépendances Git avec versions semver
2. **install_deps_v2.py** → clone les dépôts dans `dep/`, valide contre le schéma
3. **lockfile.py** → génère `dependencies-lock.json` avec commits SHA exacts
4. **Rules.mk + iproj.json** → mis à jour automatiquement pour la compilation

## Conventions spécifiques

### Structure dependencies.json

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "projet",
  "version": "1.0.0",
  "dependencies": {
    "package-name": {
      "repository": "https://github.com/user/repo.git",
      "version": "^1.0.0",  // Semver: ^, ~, >=, <=, *, latest
      "ref": "v1.0.0",       // Git ref: branch, tag, SHA
      "optional": false,
      "exclude": ["tests", "docs"]
    }
  },
  "config": {
    "targetDir": "dep",             // Où installer
    "cleanGit": true,               // Supprimer .git
    "recursiveDependencies": true   // Dépendances transitives
  }
}
```

### Fichier iproj.json (IBM i)

- **Variables dynamiques** : `&CURLIB`, `&BUILDLIB` pour builds multi-environnements
- **objlib/curlib** : bibliothèques cibles IBM i
- **buildCommand** : utilise `makei` (wrapper GNU Make pour IBM i)
- **includePath** : ajouté automatiquement lors de l'installation des dépendances

## Commandes essentielles

```bash
# Installer les dépendances
python .vscode-deps/install_deps_v2.py

# CLI complète
python .vscode-deps/ibmi_deps.py install
python .vscode-deps/ibmi_deps.py add <nom> <url> --version "^1.0.0"
python .vscode-deps/ibmi_deps.py remove <nom>
python .vscode-deps/ibmi_deps.py validate  # Valide contre le schéma

# Tests
python .vscode-deps/tests.py

# Build (sur IBM i avec Code for IBM i)
makei build        # Compile tout
makei compile -f fichier.rpgle
```

## Patterns de code

### Validation du schéma (install_deps_v2.py)

Utilise `jsonschema` pour valider `dependencies.json` contre `schema/dependencies.schema.json`. Si jsonschema n'est pas installé, émet un warning mais continue.

### Détection de dépendances circulaires

`check_circular_dependencies()` dans [install_deps_v2.py](.vscode-deps/install_deps_v2.py) traverse récursivement les dépendances pour détecter les cycles avant installation.

### Lockfile avec SHA de commit

[lockfile.py](.vscode-deps/lockfile.py) enregistre les commits SHA exacts pour garantir la reproductibilité, même si `dependencies.json` utilise des contraintes de version.

### Logging structuré

Toutes les opérations loggent dans `install_deps.log` avec timestamps. Utilise le module `logging` Python standard.

## Intégrations

### TOBI/Code for IBM i

- **iproj.json** : reconnu par l'extension VS Code "Code for IBM i"
- **.vscode/actions.json** : définit les actions de build/compile via l'extension
- Build avec `makei` (GNU Make adapté IBM i)

### Git

- Clone de dépôts avec `subprocess` + `git clone`
- Support des refs : branches, tags, SHA commits
- Nettoyage optionnel des `.git/` après installation

## Spécificités IBM i

- **RPGLE** : langage principal (RPG ILE - Integrated Language Environment)
- **.rpgleinc** : fichiers d'inclusion RPGLE (équivalent de .h en C)
- **Bibliothèques** : concept IBM i pour organiser objets (≈ schémas SQL)
- **makei** : wrapper de GNU Make pour compiler sur IBM i via PASE (environnement Unix)

## Erreurs fréquentes

- **jsonschema manquant** : `pip install jsonschema` (optionnel mais recommandé)
- **Git non trouvé** : vérifier que Git est dans le PATH
- **Dépendance circulaire** : le script la détecte et arrête l'installation
- **Schéma invalide** : vérifier avec `ibmi_deps.py validate`

## Développement

- Langage : **Python 3** (3.6+)
- Pas de framework externe (sauf jsonschema optionnel)
- Tests : unittest standard Python
- Documentation : français (projet francophone)
