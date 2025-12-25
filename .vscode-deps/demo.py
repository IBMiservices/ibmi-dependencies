#!/usr/bin/env python3
"""
Script de démonstration du gestionnaire de dépendances IBM i
"""

import json
import os


def demo():
    """Affiche une démonstration du système."""
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "Gestionnaire de Dépendances IBM i" + " " * 20 + "║")
    print("║" + " " * 25 + "Démonstration" + " " * 30 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n📦 Ce système vous permet de gérer les dépendances de vos projets IBM i")
    print("   comme vous le feriez avec npm, Maven ou pip !\n")
    
    print("🎯 Fonctionnalités principales :\n")
    features = [
        ("Clonage automatique", "Clone vos dépendances depuis Git"),
        ("Gestion des versions", "Support de semantic versioning (^1.0.0, ~2.0.0)"),
        ("Dépendances transitives", "Résout automatiquement les dépendances des dépendances"),
        ("Fichier de verrouillage", "Garantit des installations reproductibles"),
        ("Validation du schéma", "Vérifie votre configuration avant installation"),
        ("Logging détaillé", "Suivez l'installation en temps réel"),
        ("Intégration TOBI", "Mise à jour automatique de Rules.mk et iproj.json")
    ]
    
    for i, (name, desc) in enumerate(features, 1):
        print(f"   {i}. {name:25} → {desc}")
    
    print("\n" + "─" * 70)
    print("📝 Exemple de fichier dependencies.json :\n")
    
    example = {
        "name": "mon-projet-ibmi",
        "version": "1.0.0",
        "description": "Application de gestion",
        "dependencies": {
            "message-service": {
                "repository": "https://github.com/ibmi/message-service.git",
                "version": "^1.0.0",
                "ref": "v1.0.0"
            },
            "db-utils": {
                "repository": "https://github.com/ibmi/db-utils.git",
                "version": "~2.0.0"
            }
        },
        "config": {
            "targetDir": "dep",
            "cleanGit": True,
            "updateBuildFiles": True
        }
    }
    
    print(json.dumps(example, indent=2, ensure_ascii=False))
    
    print("\n" + "─" * 70)
    print("🚀 Pour commencer :\n")
    
    steps = [
        "Créez votre fichier dependencies.json",
        "Exécutez : python install_deps_v2.py",
        "Compilez votre projet : makei build",
        "C'est tout ! Vos dépendances sont intégrées 🎉"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"   {i}. {step}")
    
    print("\n" + "─" * 70)
    print("📚 Documentation :\n")
    
    docs = [
        ("GUIDE_UTILISATEUR.md", "Guide complet d'utilisation"),
        ("README_V2.md", "Vue d'ensemble et exemples"),
        ("schema/README.md", "Documentation du schéma JSON"),
        ("CHANGELOG.md", "Historique des versions")
    ]
    
    for doc, desc in docs:
        exists = "✓" if os.path.exists(doc) else "✗"
        print(f"   {exists} {doc:25} - {desc}")
    
    print("\n" + "─" * 70)
    print("🔧 Scripts disponibles :\n")
    
    scripts = [
        ("install_deps_v2.py", "Installation des dépendances (v2.0)", True),
        ("install_deps.py", "Installation des dépendances (v1.0)", False),
        ("migrate_v1_to_v2.py", "Migration v1.0 → v2.0", True),
        ("tests.py", "Tests unitaires", True),
        ("lockfile.py", "Module de gestion du lockfile", False)
    ]
    
    for script, desc, is_main in scripts:
        marker = "⭐" if is_main else "  "
        exists = "✓" if os.path.exists(script) else "✗"
        print(f"   {marker} {exists} {script:25} - {desc}")
    
    print("\n" + "═" * 70)
    print("💡 Astuce : Commencez par lire GUIDE_UTILISATEUR.md !")
    print("═" * 70)
    
    print("\n✨ Bon développement sur IBM i ! ✨\n")


if __name__ == "__main__":
    demo()
