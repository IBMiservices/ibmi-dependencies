# 📚 Registre de packages IBM i

Un registre centralisé de packages réutilisables pour projets IBM i.

## 🎯 Objectif

Le registre permet de :
- **Découvrir** des packages disponibles pour IBM i
- **Rechercher** des bibliothèques par mots-clés
- **Vérifier** les versions disponibles
- **Simplifier** l'ajout de dépendances

## 📦 Packages disponibles

### 1. message-service
**Description**: Service de gestion de messages programmables  
**Auteur**: IBMiservices  
**Licence**: GPL-3.0  
**Dernière version**: 1.2.0  
**Repository**: https://github.com/IBMiservices/messageutils.git

```bash
python ibmi_deps.py add message-service \
  https://github.com/IBMiservices/messageutils.git \
  --version "^1.2.0"
```

### 2. db-utils
**Description**: Utilitaires pour bases de données IBM i  
**Auteur**: IBM i Community  
**Licence**: MIT  
**Dernière version**: 2.1.0  
**Repository**: https://github.com/example/db-utils.git

```bash
python ibmi_deps.py add db-utils \
  https://github.com/example/db-utils.git \
  --version "^2.1.0"
```

### 3. string-utils
**Description**: Manipulation de chaînes pour RPG  
**Auteur**: RPG Tools  
**Licence**: Apache-2.0  
**Dernière version**: 1.7.0 (stable: 1.6.0)  
**Repository**: https://github.com/example/string-utils.git

```bash
python ibmi_deps.py add string-utils \
  https://github.com/example/string-utils.git \
  --version "^1.6.0"
```

### 4. rpg-logger
**Description**: Système de logging pour RPG  
**Auteur**: Logging Solutions  
**Licence**: GPL-3.0  
**Dernière version**: 3.2.0  
**Repository**: https://github.com/example/rpg-logger.git

```bash
python ibmi_deps.py add rpg-logger \
  https://github.com/example/rpg-logger.git \
  --version "^3.2.0"
```

### 5. rpg-test-framework
**Description**: Tests unitaires pour RPG  
**Auteur**: Testing Tools  
**Licence**: MIT  
**Dernière version**: 2.2.0  
**Repository**: https://github.com/example/rpg-test.git

```bash
python ibmi_deps.py add rpg-test-framework \
  https://github.com/example/rpg-test.git \
  --version "^2.2.0" \
  --dev
```

### 6. json-parser
**Description**: Parser JSON pour RPG/COBOL  
**Auteur**: Data Tools  
**Licence**: BSD-3-Clause  
**Dernière version**: 1.1.0  
**Repository**: https://github.com/example/json-parser.git

```bash
python ibmi_deps.py add json-parser \
  https://github.com/example/json-parser.git \
  --version "^1.1.0"
```

### 7. http-client
**Description**: Client HTTP pour IBM i  
**Auteur**: Network Tools  
**Licence**: MIT  
**Dernière version**: 1.2.0  
**Repository**: https://github.com/example/http-client.git

```bash
python ibmi_deps.py add http-client \
  https://github.com/example/http-client.git \
  --version "^1.2.0"
```

### 8. date-utils
**Description**: Manipulation de dates  
**Auteur**: Time Tools  
**Licence**: Apache-2.0  
**Dernière version**: 2.1.0  
**Repository**: https://github.com/example/date-utils.git

```bash
python ibmi_deps.py add date-utils \
  https://github.com/example/date-utils.git \
  --version "^2.1.0"
```

## 🔍 Recherche par catégorie

### Utilitaires de base
- `string-utils` - Manipulation de chaînes
- `date-utils` - Gestion des dates
- `json-parser` - Parsing JSON

### Base de données
- `db-utils` - Utilitaires SQL/DB2

### Réseau & APIs
- `http-client` - Client HTTP/REST

### Développement
- `rpg-logger` - Logging
- `message-service` - Messages
- `rpg-test-framework` - Tests unitaires

## 📊 Statistiques

- **Total de packages**: 8
- **Total de versions**: 27
- **Dernière mise à jour**: 24 décembre 2025

## 🚀 Utilisation

### Recherche manuelle

Consultez [packages.json](packages.json) pour voir tous les packages disponibles.

### Installation depuis le registre

```bash
# 1. Trouver le package souhaité dans le registre
# 2. Copier la commande d'installation
# 3. L'exécuter dans votre projet
python ibmi_deps.py add <package> <repository> --version "<version>"

# 4. Installer
python ibmi_deps.py install
```

## 📝 Structure du registre

```json
{
  "packages": {
    "nom-du-package": {
      "name": "nom-du-package",
      "description": "Description du package",
      "author": "Auteur",
      "license": "Licence",
      "repository": "URL du dépôt Git",
      "homepage": "URL de la page d'accueil",
      "keywords": ["mot-clé1", "mot-clé2"],
      "versions": {
        "1.0.0": {
          "ref": "v1.0.0",
          "released": "2025-01-01",
          "stable": true
        }
      },
      "latest": "1.0.0"
    }
  }
}
```

## 🤝 Contribuer

### Ajouter votre package au registre

1. **Préparez votre package** :
   - Créez un dépôt Git
   - Ajoutez un fichier `dependencies.json` (optionnel pour dépendances transitives)
   - Taguez vos versions avec Git tags

2. **Soumettez une PR** :
   - Ajoutez votre package dans `packages.json`
   - Respectez le format du schéma
   - Incluez une description claire

3. **Maintenez** :
   - Ajoutez les nouvelles versions
   - Mettez à jour la documentation
   - Suivez le semantic versioning

### Format requis

```json
{
  "votre-package": {
    "name": "votre-package",
    "description": "Description courte et claire",
    "author": "Votre nom ou organisation",
    "license": "GPL-3.0 ou MIT ou Apache-2.0",
    "repository": "https://github.com/user/votre-package.git",
    "homepage": "https://votre-site.com",
    "keywords": ["rpg", "ibmi", "categorie"],
    "versions": {
      "1.0.0": {
        "ref": "v1.0.0",
        "released": "2025-12-24",
        "stable": true
      }
    },
    "latest": "1.0.0"
  }
}
```

## 🔮 Fonctionnalités futures

### Phase 1 (Actuelle)
- [x] Fichier JSON statique
- [x] Documentation manuelle
- [x] Recherche manuelle

### Phase 2 (Prévue)
- [ ] API REST pour recherche
- [ ] CLI intégré pour recherche (`ibmi-deps search`)
- [ ] Auto-complétion des noms de packages
- [ ] Statistiques de téléchargement

### Phase 3 (Future)
- [ ] Interface web de browsing
- [ ] Système de notation/reviews
- [ ] Vérification automatique de sécurité
- [ ] Miroirs pour performance
- [ ] Authentification pour packages privés

## 📚 Ressources

- [Guide d'utilisation du CLI](../examples/CLI_GUIDE.md)
- [Guide utilisateur](../GUIDE_UTILISATEUR.md)
- [Exemples de packages](../examples/README.md)

## ⚖️ Licences

Les packages du registre utilisent différentes licences :
- **GPL-3.0** : Copyleft fort
- **MIT** : Très permissive
- **Apache-2.0** : Permissive avec clause de brevets
- **BSD-3-Clause** : Permissive simple

⚠️ **Important** : Vérifiez toujours la compatibilité des licences avec votre projet.

## 📧 Contact

Pour ajouter un package ou signaler un problème :
- Ouvrez une issue sur GitHub
- Soumettez une Pull Request
- Contactez les mainteneurs

---

**Registre IBM i Dependencies v1.0**  
**Dernière mise à jour**: 24 décembre 2025
