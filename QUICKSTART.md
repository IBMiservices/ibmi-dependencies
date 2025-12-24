# 🚀 Démarrage rapide - 5 minutes

Gérez vos dépendances IBM i comme avec npm ou Maven !

## ⚡ Installation express

```bash
# 1. Installer jsonschema (optionnel mais recommandé)
pip install jsonschema

# 2. C'est tout ! Les scripts sont prêts à l'emploi
```

## 📝 Votre premier projet

### Étape 1 : Créer `dependencies.json`

Créez un fichier à la racine de votre projet :

```json
{
  "name": "mon-premier-projet",
  "version": "1.0.0",
  "dependencies": {
    "ma-bibliotheque": {
      "repository": "https://github.com/user/ma-bibliotheque.git",
      "ref": "main"
    }
  }
}
```

### Étape 2 : Installer les dépendances

```bash
python .vscode-deps/install_deps_v2.py
```

Vous verrez :
```
══════════════════════════════════════════════════════════════════════
Démarrage de l'installation des dépendances IBM i
══════════════════════════════════════════════════════════════════════
✓ Fichier dependencies.json chargé
✓ Schéma JSON validé avec succès
✓ Aucune dépendance circulaire détectée

──────────────────────────────────────────────────────────────────────
Traitement de la dépendance: ma-bibliotheque
──────────────────────────────────────────────────────────────────────
Clonage de ma-bibliotheque depuis https://github.com/user/ma-bibliotheque.git...
✓ ma-bibliotheque cloné avec succès
✓ ma-bibliotheque est prêt

══════════════════════════════════════════════════════════════════════
Installation terminée
══════════════════════════════════════════════════════════════════════
✓ Dépendances installées avec succès: 1
Total de dépendances traitées: 1
══════════════════════════════════════════════════════════════════════
```

### Étape 3 : Compiler

```bash
makei build
```

**C'est tout !** Votre dépendance est intégrée et prête à l'emploi.

## 🎯 Exemples courants

### Exemple 1 : Plusieurs dépendances

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "utils": {
      "repository": "https://github.com/ibmi/utils.git",
      "version": "^1.0.0"
    },
    "logger": {
      "repository": "https://github.com/ibmi/logger.git",
      "version": "^2.0.0"
    },
    "db-wrapper": {
      "repository": "https://github.com/ibmi/db.git",
      "version": "~3.1.0"
    }
  }
}
```

### Exemple 2 : Avec versions spécifiques

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "version": "^2.1.0",
      "ref": "v2.1.5"
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
      "exclude": ["tests", "examples", "docs"]
    }
  }
}
```

## 🔍 Contraintes de versions

| Syntaxe | Signification |
|---------|---------------|
| `1.0.0` | Version exacte |
| `^1.0.0` | Compatible avec 1.x.x (≥1.0.0, <2.0.0) |
| `~1.0.0` | Compatible patch (≥1.0.0, <1.1.0) |
| `>=1.0.0` | Version minimum |
| `*` ou `latest` | Dernière version disponible |

## 🔄 Migrer un projet existant v1.0

Si vous avez déjà un fichier `dependencies.json` en format v1.0 :

```bash
# Migration automatique avec sauvegarde
python migrate_v1_to_v2.py

# Installer avec la nouvelle version
python install_deps_v2.py
```

## 🆘 Problèmes courants

### ❌ "jsonschema module not found"

```bash
pip install jsonschema
```

Le script fonctionne sans mais avec un avertissement.

### ❌ "Git command failed"

Vérifiez :
- Git est installé : `git --version`
- L'URL du dépôt est accessible
- Vous avez les droits d'accès (authentification)

### ❌ "Validation du schéma échouée"

Votre `dependencies.json` n'est pas au bon format. Exemple minimal :

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {}
}
```

## 📚 Pour aller plus loin

- **Documentation complète** : [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md)
- **Vue d'ensemble** : [README_V2.md](README_V2.md)
- **Format JSON** : [schema/README.md](schema/README.md)
- **Démonstration** : `python demo.py`
- **Tests** : `python tests.py`

## 💡 Astuces

1. **Utilisez le lockfile** : `dependencies-lock.json` garantit des installations identiques
2. **Versionnez votre config** : Commitez `dependencies.json` dans Git
3. **Excluez les dépendances** : Ajoutez `dep/` dans `.gitignore`
4. **Consultez les logs** : Fichier `install_deps.log` pour le débogage

## 🎯 Checklist pour nouveau projet

- [ ] Créer `dependencies.json` avec name, version, dependencies
- [ ] Ajouter `dep/` dans `.gitignore`
- [ ] Exécuter `python install_deps_v2.py`
- [ ] Vérifier que `dependencies-lock.json` est créé
- [ ] Compiler : `makei build`
- [ ] Commiter `dependencies.json` et `dependencies-lock.json`

## ✨ Et voilà !

Vous savez maintenant comment gérer les dépendances de vos projets IBM i de manière moderne et professionnelle !

**Besoin d'aide ?** Consultez le [Guide utilisateur](GUIDE_UTILISATEUR.md) complet.

---

*Version : 2.0.0 | Créé le 24 décembre 2025*
