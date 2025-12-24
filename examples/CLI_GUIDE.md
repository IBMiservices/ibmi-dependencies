# 🖥️ Guide d'utilisation du CLI ibmi-deps

Interface en ligne de commande pour le gestionnaire de dépendances IBM i.

## 📋 Table des matières

- [Installation](#installation)
- [Commandes](#commandes)
- [Exemples](#exemples)
- [Configuration](#configuration)

## 🚀 Installation

Le CLI est inclus dans le projet. Aucune installation supplémentaire nécessaire.

```bash
# Rendre le script exécutable (optionnel)
chmod +x ibmi_deps.py

# Ou créer un alias (Linux/Mac)
alias ibmi-deps='python3 /chemin/vers/ibmi_deps.py'

# Ou ajouter au PATH
export PATH=$PATH:/chemin/vers/ibmi-dependencies
```

## 📖 Commandes

### `init` - Initialiser un projet

Crée un fichier `dependencies.json` avec la structure de base.

```bash
python ibmi_deps.py init [--name NOM] [--force]
```

**Options:**
- `--name NOM` : Nom du projet (défaut: nom du répertoire)
- `--force` : Écraser le fichier existant

**Exemple:**
```bash
python ibmi_deps.py init --name mon-application-ibmi
```

**Résultat:**
```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "mon-application-ibmi",
  "version": "1.0.0",
  "description": "Projet IBM i: mon-application-ibmi",
  "dependencies": {},
  "devDependencies": {},
  "config": {
    "targetDir": "dep",
    "cleanGit": true,
    "cleanDocs": true,
    "updateBuildFiles": true,
    "recursiveDependencies": true
  }
}
```

---

### `install` - Installer les dépendances

Installe toutes les dépendances déclarées dans `dependencies.json`.

```bash
python ibmi_deps.py install [--verbose] [--dry-run]
```

**Options:**
- `--verbose, -v` : Afficher les détails
- `--dry-run` : Simuler sans installer

**Exemple:**
```bash
# Installation normale
python ibmi_deps.py install

# Simulation
python ibmi_deps.py install --dry-run

# Mode verbeux
python ibmi_deps.py install -v
```

---

### `add` - Ajouter une dépendance

Ajoute une nouvelle dépendance au fichier `dependencies.json`.

```bash
python ibmi_deps.py add <package> <repository> [OPTIONS]
```

**Options:**
- `--version VERSION` : Contrainte de version (défaut: `*`)
- `--ref REF` : Référence Git (branch, tag, commit)
- `--dev` : Ajouter comme dépendance de développement

**Exemples:**
```bash
# Dépendance simple
python ibmi_deps.py add utils https://github.com/user/utils.git

# Avec version spécifique
python ibmi_deps.py add core https://github.com/user/core.git \
  --version "^2.0.0" \
  --ref v2.1.0

# Dépendance de développement
python ibmi_deps.py add test-framework https://github.com/user/test.git --dev
```

---

### `remove` - Retirer une dépendance

Retire une dépendance du fichier `dependencies.json`.

```bash
python ibmi_deps.py remove <package>
```

**Exemple:**
```bash
python ibmi_deps.py remove old-package
```

⚠️ **Note:** Les fichiers installés ne sont pas automatiquement supprimés. Utilisez `clean` pour cela.

---

### `list` - Lister les dépendances

Affiche la liste des dépendances du projet.

```bash
python ibmi_deps.py list [--locked]
```

**Options:**
- `--locked` : Afficher depuis le fichier de verrouillage

**Exemple:**
```bash
# Liste depuis dependencies.json
python ibmi_deps.py list

# Liste depuis dependencies-lock.json
python ibmi_deps.py list --locked
```

**Sortie:**
```
📦 Dépendances de production (3):

   • message-service           ^1.0.0
   • db-utils                  ~2.0.0
   • string-utils              >=1.5.0

🔧 Dépendances de développement (1):

   • rpg-test                  latest
```

---

### `update` - Mettre à jour les dépendances

Met à jour les dépendances vers leurs dernières versions compatibles.

```bash
python ibmi_deps.py update [package]
```

**Arguments:**
- `package` : Package spécifique à mettre à jour (optionnel)

**Exemples:**
```bash
# Tout mettre à jour
python ibmi_deps.py update

# Mettre à jour un package spécifique
python ibmi_deps.py update message-service
```

---

### `clean` - Nettoyer les dépendances

Supprime les dépendances installées et les fichiers temporaires.

```bash
python ibmi_deps.py clean [--all]
```

**Options:**
- `--all` : Supprimer aussi le fichier de verrouillage

**Exemple:**
```bash
# Nettoyer les dépendances
python ibmi_deps.py clean

# Tout supprimer (incluant lockfile)
python ibmi_deps.py clean --all
```

---

### `info` - Informations sur un package

Affiche les informations détaillées d'une dépendance.

```bash
python ibmi_deps.py info <package>
```

**Exemple:**
```bash
python ibmi_deps.py info message-service
```

**Sortie:**
```
📦 message-service
────────────────────────────────────────────────────────────
Type        : Production
Dépôt       : https://github.com/IBMiservices/messageutils.git
Version     : ^1.0.0
Référence   : v1.0.0
Optionnel   : Non

🔒 Informations verrouillées:
Version     : 1.0.0
Commit SHA  : abc123def456789
Résolu le   : 2025-12-24T10:00:00
────────────────────────────────────────────────────────────
```

---

### `validate` - Valider dependencies.json

Vérifie la validité du fichier de configuration.

```bash
python ibmi_deps.py validate
```

**Exemple:**
```bash
python ibmi_deps.py validate
```

**Sortie en cas de succès:**
```
🔍 Validation de dependencies.json...

✅ Validation réussie!
   Projet: mon-application
   Version: 1.0.0
   Dépendances: 5
```

**Sortie en cas d'erreur:**
```
🔍 Validation de dependencies.json...

❌ Erreurs trouvées:
   • Champ 'name' manquant
   • Dépendance 'utils': repository manquant
```

---

## 📚 Exemples de workflows

### Démarrer un nouveau projet

```bash
# 1. Initialiser
python ibmi_deps.py init --name mon-nouveau-projet

# 2. Ajouter des dépendances
python ibmi_deps.py add message-service \
  https://github.com/IBMiservices/messageutils.git \
  --version "^1.0.0"

python ibmi_deps.py add db-utils \
  https://github.com/example/db-utils.git \
  --version "~2.0.0"

# 3. Installer
python ibmi_deps.py install

# 4. Vérifier
python ibmi_deps.py list --locked
```

### Migrer un projet existant

```bash
# 1. Si vous avez déjà dependencies.json v1.0
python migrate_v1_to_v2.py

# 2. Valider
python ibmi_deps.py validate

# 3. Installer
python ibmi_deps.py install
```

### Mettre à jour un projet

```bash
# 1. Voir les dépendances actuelles
python ibmi_deps.py list --locked

# 2. Mettre à jour
python ibmi_deps.py update

# 3. Tester
makei build

# 4. Si OK, commiter le nouveau lockfile
git add dependencies-lock.json
git commit -m "chore: update dependencies"
```

### Nettoyer et réinstaller

```bash
# 1. Nettoyer tout
python ibmi_deps.py clean --all

# 2. Réinstaller
python ibmi_deps.py install
```

## ⚙️ Configuration

### Alias recommandés

Ajoutez ces alias à votre `.bashrc` ou `.zshrc` :

```bash
alias ibmi='python3 /chemin/vers/ibmi_deps.py'
alias ibmi-i='python3 /chemin/vers/ibmi_deps.py install'
alias ibmi-l='python3 /chemin/vers/ibmi_deps.py list'
alias ibmi-u='python3 /chemin/vers/ibmi_deps.py update'
```

Utilisation :
```bash
ibmi list
ibmi-i
ibmi-u
```

### Script wrapper (optionnel)

Créez un script `/usr/local/bin/ibmi-deps` :

```bash
#!/bin/bash
python3 /chemin/vers/ibmi-dependencies/ibmi_deps.py "$@"
```

Rendez-le exécutable :
```bash
chmod +x /usr/local/bin/ibmi-deps
```

Utilisez-le directement :
```bash
ibmi-deps install
ibmi-deps list
```

## 🔧 Dépannage

### Commande introuvable

```bash
# Vérifier que le script existe
ls -l ibmi_deps.py

# Vérifier Python
python3 --version

# Utiliser le chemin complet
python3 /chemin/complet/vers/ibmi_deps.py --help
```

### Permission refusée

```bash
chmod +x ibmi_deps.py
```

### Module manquant

```bash
pip install -r requirements.txt
```

## 📖 Ressources

- [Guide utilisateur](../GUIDE_UTILISATEUR.md)
- [Démarrage rapide](../QUICKSTART.md)
- [Exemples](README.md)
- [Documentation du schéma](../schema/README.md)

## 💡 Astuces

1. **Auto-complétion** : Créez un script de completion bash/zsh
2. **CI/CD** : Intégrez le CLI dans vos pipelines
3. **Scripts** : Utilisez le CLI dans des scripts shell
4. **Documentation** : Ajoutez `ibmi-deps` à votre README

---

**Version:** 2.0.0  
**Dernière mise à jour:** 24 décembre 2025
