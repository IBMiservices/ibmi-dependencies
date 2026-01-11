# Guide : Comment remplir dependencies.json

Guide pratique pour développeurs IBM i qui découvrent JSON.

## Qu'est-ce que JSON ?

JSON est un format de fichier texte simple pour stocker des données. C'est comme un fichier DDS mais plus universel :
- Les données sont entre **accolades** `{ }`
- Les **virgules** `,` séparent les éléments
- Les **deux-points** `:` associent un nom à une valeur
- Les **guillemets** `"` entourent le texte

## Structure de base

Voici le squelette minimal d'un fichier `dependencies.json` :

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
  }
}
```

**⚠️ Important** : 
- Toujours mettre une **virgule** après chaque ligne, sauf la dernière d'un bloc
- Les **guillemets** sont obligatoires autour des noms et des textes
- Pas de virgule après le dernier élément

## Exemple complet commenté

```json
{
  "name": "mon-projet-rpg",
  "version": "1.0.0",
  "description": "Projet de gestion des commandes",
  "author": "Jean Dupont",
  "license": "Apache-2.0",
  
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  }
}
```

## Remplir les champs obligatoires

### 1. Informations du projet

```json
{
  "name": "mon-projet",
```
- **Ce que c'est** : Le nom de votre projet
- **Règles** : Seulement lettres minuscules, chiffres, tirets `-` et underscores `_`
- **Exemple** : `"gestion-commandes"`, `"mon_app_rpg"`

```json
  "version": "1.0.0",
```
- **Ce que c'est** : La version de votre projet
- **Format** : Toujours 3 chiffres séparés par des points
- **Exemples** : `"1.0.0"` (première version), `"2.1.5"` (version 2, mise à jour 1, correction 5)

```json
  "dependencies": {
```
- **Ce que c'est** : La liste des bibliothèques externes dont vous avez besoin
- **C'est comme** : La liste des *LIBL dans votre environnement IBM i

## Ajouter une dépendance

Pour chaque bibliothèque externe, ajoutez un bloc comme celui-ci :

```json
"dependencies": {
  "nom-de-la-bibliotheque": {
    "repository": "https://github.com/utilisateur/bibliotheque.git",
    "ref": "v1.0.0"
  }
}
```

### Exemple avec une vraie bibliothèque (logfori)

```json
"dependencies": {
  "logfori": {
    "repository": "https://github.com/IBMiservices/logfori.git",
    "ref": "main"
  }
}
```

**Ce que cela fait** : 
- Télécharge automatiquement le code source de logfori
- Place les fichiers dans le dossier `dep/logfori/`
- Vous pouvez ensuite utiliser `/COPY` ou `/INCLUDE` dans vos programmes RPGLE

## Ajouter plusieurs dépendances

Séparez chaque bibliothèque par une **virgule** :

```json
"dependencies": {
  "logfori": {
    "repository": "https://github.com/IBMiservices/logfori.git",
    "ref": "main"
  },
  "http-client": {
    "repository": "https://github.com/user/http-client.git",
    "ref": "v2.1.0"
  },
  "json-parser": {
    "repository": "https://github.com/user/json-parser.git",
    "ref": "main"
  }
}
```

**⚠️ Attention** : Pas de virgule après la dernière bibliothèque !

## Champs optionnels mais utiles

### Description et auteur

```json
{
  "name": "gestion-commandes",
  "version": "1.0.0",
  "description": "Application de gestion des commandes clients",
  "author": "Équipe RPG - Service Informatique",
  "license": "Apache-2.0",
  
  "dependencies": {
    ...
  }
}
```

### Options avancées pour les dépendances

```json
"dependencies": {
  "ma-bibliotheque": {
    "repository": "https://github.com/user/lib.git",
    "ref": "v1.5.0",
    "version": "^1.5.0",
    "optional": false,
    "exclude": ["tests", "docs", "exemples"]
  }
}
```

**Explications** :

- **`version`** : Contraint la version installée
  - `"^1.5.0"` = accepte 1.5.0, 1.6.0, 1.9.0, mais pas 2.0.0
  - `"~1.5.0"` = accepte 1.5.0, 1.5.1, 1.5.9, mais pas 1.6.0
  - `"*"` ou `"latest"` = toujours la dernière version

- **`optional`** : Si `true`, l'installation ne plante pas si la bibliothèque est inaccessible

- **`exclude`** : Liste des dossiers à ne pas télécharger (économise de l'espace)

## Configuration globale

À la fin du fichier, vous pouvez ajouter des paramètres :

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  },
  "config": {
    "targetDir": "dep",
    "cleanGit": true,
    "cleanDocs": true,
    "recursiveDependencies": true
  }
}
```

**Paramètres** :

- **`targetDir`** : Dossier où installer les dépendances (par défaut `"dep"`)
- **`cleanGit`** : Supprimer les fichiers `.git` (recommandé : `true`)
- **`cleanDocs`** : Supprimer README, LICENSE, etc. (recommandé : `true`)
- **`recursiveDependencies`** : Installer aussi les dépendances des dépendances (recommandé : `true`)

## Cas d'usage pratiques

### Cas 1 : Projet simple avec logfori

```json
{
  "name": "mon-app",
  "version": "1.0.0",
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "main"
    }
  }
}
```

### Cas 2 : Projet avec plusieurs bibliothèques

```json
{
  "name": "application-web",
  "version": "2.0.0",
  "description": "Application web avec API REST",
  "author": "Service IT",
  
  "dependencies": {
    "logfori": {
      "repository": "https://github.com/IBMiservices/logfori.git",
      "ref": "v1.2.0"
    },
    "http-framework": {
      "repository": "https://github.com/ibmi/http-framework.git",
      "ref": "v3.0.0"
    },
    "json-tools": {
      "repository": "https://github.com/ibmi/json-tools.git",
      "ref": "main"
    }
  },
  
  "config": {
    "targetDir": "lib",
    "cleanGit": true,
    "cleanDocs": true
  }
}
```

### Cas 3 : Dépendances optionnelles

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  
  "dependencies": {
    "core-lib": {
      "repository": "https://github.com/ibmi/core.git",
      "ref": "v2.0.0"
    }
  },
  
  "devDependencies": {
    "test-framework": {
      "repository": "https://github.com/ibmi/tests.git",
      "ref": "main",
      "optional": true
    }
  }
}
```

## Erreurs courantes et solutions

### ❌ Erreur : Virgule en trop

```json
{
  "name": "projet",
  "dependencies": {
    "lib1": {...},
    "lib2": {...},  ← Virgule en trop !
  }
}
```

**✅ Correction** :
```json
{
  "name": "projet",
  "dependencies": {
    "lib1": {...},
    "lib2": {...}  ← Pas de virgule sur la dernière ligne
  }
}
```

### ❌ Erreur : Guillemets manquants

```json
{
  name: mon-projet,  ← Guillemets manquants !
  "dependencies": {}
}
```

**✅ Correction** :
```json
{
  "name": "mon-projet",  ← Guillemets obligatoires
  "dependencies": {}
}
```

### ❌ Erreur : Accolades mal fermées

```json
{
  "dependencies": {
    "lib": {
      "repository": "..."
    }
  ← Accolade manquante !
}
```

**✅ Correction** :
```json
{
  "dependencies": {
    "lib": {
      "repository": "..."
    }
  }  ← Bien fermé
}
```

## Validation du fichier

Pour vérifier que votre fichier est correct :

```bash
python .vscode-deps/ibmi_deps.py validate
```

Le script affichera :
- ✅ `Validation réussie` si tout est correct
- ❌ Un message d'erreur précis si quelque chose ne va pas

## Aide-mémoire JSON

| Caractère | Signification | Exemple |
|-----------|---------------|---------|
| `{ }` | Début et fin d'un bloc | `{"name": "projet"}` |
| `[ ]` | Liste de valeurs | `["tests", "docs"]` |
| `:` | Associe un nom à une valeur | `"name": "valeur"` |
| `,` | Sépare les éléments | `"a": 1, "b": 2` |
| `"` | Délimite le texte | `"mon texte"` |
| `true/false` | Valeurs booléennes | `"optional": true` |

## Éditeurs recommandés

Ces éditeurs vous aident à éviter les erreurs :

1. **VS Code** (recommandé)
   - Coloration syntaxique
   - Détection automatique des erreurs
   - Auto-complétion avec le schéma

2. **Notepad++**
   - Plugin JSON Viewer
   - Validation de la syntaxe

3. **Éviter Notepad Windows**
   - Pas de coloration
   - Pas de validation
   - Risque d'encodage incorrect

## Aller plus loin

Une fois `dependencies.json` créé, lancez l'installation :

```bash
python .vscode-deps/install_deps_v2.py
```

Les bibliothèques seront téléchargées dans le dossier `dep/`.

Vous pouvez ensuite les utiliser dans vos programmes RPGLE :

```rpgle
**FREE

/COPY dep/logfori/qcpysrc/logger_h.rpgleinc

Dcl-Proc Main;
  Logger_Info('Application démarrée');
End-Proc;
```

## Support

En cas de problème :
1. Vérifiez la syntaxe avec `ibmi_deps.py validate`
2. Consultez les logs dans `install_deps.log`
3. Voir le guide utilisateur : [GUIDE_UTILISATEUR.md](GUIDE_UTILISATEUR.md)
