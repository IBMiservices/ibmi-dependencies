# Schéma dependencies.json

Structure du fichier de configuration.

## Structure minimale

```json
{
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
    "package": {
      "repository": "https://github.com/user/package.git",
      "ref": "v1.0.0"
    }
  }
}
```

## Structure complète

```json
{
  "$schema": "./schema/dependencies.schema.json",
  "name": "mon-projet",
  "version": "1.0.0",
  "dependencies": {
    "package": {
      "repository": "https://github.com/user/package.git",
      "version": "^1.0.0",
      "ref": "v1.0.0",
      "optional": false,
      "exclude": ["tests"]
    }
  },
  "config": {
    "targetDir": "dep",
    "cleanGit": true
  }
}
```

## Propriétés des dépendances

| Propriété | Requis | Description |
|-----------|--------|-------------|
| `repository` | ✅ | URL du dépôt Git |
| `version` | ❌ | Contrainte semver (`^1.0.0`, `~1.0.0`, `latest`) |
| `ref` | ❌ | Référence Git (branch, tag, commit) |
| `optional` | ❌ | Dépendance optionnelle |
| `exclude` | ❌ | Fichiers/dossiers à exclure |
