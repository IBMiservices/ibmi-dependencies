#!/usr/bin/env python3
"""
Script de migration de dependencies.json v1.0 vers v2.0
"""

import json
import sys
import os
from pathlib import Path


def migrate_dependencies_file(input_file: str = "dependencies.json", 
                              output_file: str = "dependencies.json",
                              backup: bool = True) -> bool:
    """
    Migre un fichier dependencies.json de v1.0 vers v2.0.
    
    :param input_file: Fichier source
    :param output_file: Fichier de destination
    :param backup: Créer une sauvegarde
    :return: True si succès, False sinon
    """
    try:
        print("═" * 70)
        print("Migration dependencies.json v1.0 → v2.0")
        print("═" * 70)
        
        # Vérifier que le fichier existe
        if not os.path.exists(input_file):
            print(f"✗ Fichier {input_file} introuvable")
            return False
        
        # Créer une sauvegarde si demandé
        if backup and input_file == output_file:
            backup_file = f"{input_file}.v1.backup"
            print(f"\n📋 Création de la sauvegarde : {backup_file}")
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Sauvegarde créée")
        
        # Charger le fichier v1.0
        print(f"\n📖 Lecture de {input_file}...")
        with open(input_file, 'r', encoding='utf-8') as f:
            v1_config = json.load(f)
        
        print(f"✓ Fichier chargé")
        
        # Détecter le format
        is_v1 = ("url" in str(v1_config) and 
                 "name" not in v1_config and 
                 "version" not in v1_config)
        
        if not is_v1:
            print("\n⚠ Le fichier semble déjà être en format v2.0")
            response = input("Continuer quand même ? (o/N) : ")
            if response.lower() != 'o':
                print("Migration annulée")
                return False
        
        # Préparer la structure v2.0
        print("\n🔄 Migration en cours...")
        
        # Déterminer le nom du projet depuis le chemin
        project_name = Path.cwd().name.lower().replace(" ", "-")
        
        v2_config = {
            "$schema": "./schema/dependencies.schema.json",
            "name": project_name,
            "version": "1.0.0",
            "description": f"Projet IBM i - {project_name}",
            "author": "TODO: Ajouter votre nom",
            "license": "Apache-2.0"
        }
        
        # Ajouter le dépôt si disponible
        if "repository" in v1_config:
            v2_config["repository"] = v1_config["repository"]
        
        # Migrer les dépendances
        v2_dependencies = {}
        v1_dependencies = v1_config.get("dependencies", {})
        
        for dep_name, dep_info in v1_dependencies.items():
            new_dep = {}
            
            # Migrer url → repository
            if "url" in dep_info:
                new_dep["repository"] = dep_info["url"]
            elif "repository" in dep_info:
                new_dep["repository"] = dep_info["repository"]
            
            # Conserver ref
            if "ref" in dep_info:
                new_dep["ref"] = dep_info["ref"]
                # Essayer de déduire la version depuis le ref
                ref = dep_info["ref"]
                if ref.startswith("v") and ref[1:].replace(".", "").isdigit():
                    new_dep["version"] = f"^{ref[1:]}"
                else:
                    new_dep["version"] = "latest"
            else:
                new_dep["version"] = "latest"
            
            # Conserver les autres champs
            for key in ["optional", "exclude"]:
                if key in dep_info:
                    new_dep[key] = dep_info[key]
            
            v2_dependencies[dep_name] = new_dep
            print(f"  ✓ {dep_name} migré")
        
        v2_config["dependencies"] = v2_dependencies
        v2_config["devDependencies"] = v1_config.get("devDependencies", {})
        
        # Ajouter la configuration par défaut
        v2_config["config"] = {
            "targetDir": "dep",
            "cleanGit": True,
            "cleanDocs": True,
            "updateBuildFiles": True,
            "recursiveDependencies": True
        }
        
        # Sauvegarder le fichier v2.0
        print(f"\n💾 Écriture de {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(v2_config, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Fichier écrit")
        
        # Afficher un résumé
        print("\n" + "═" * 70)
        print("✅ Migration réussie !")
        print("═" * 70)
        print(f"\n📊 Résumé :")
        print(f"  • Dépendances migrées : {len(v2_dependencies)}")
        print(f"  • Nom du projet : {v2_config['name']}")
        print(f"  • Version : {v2_config['version']}")
        
        if backup and input_file == output_file:
            print(f"  • Sauvegarde : {backup_file}")
        
        print("\n📝 Actions recommandées :")
        print("  1. Vérifier et modifier les métadonnées (name, version, author)")
        print("  2. Vérifier les versions des dépendances")
        print("  3. Tester l'installation : python install_deps_v2.py")
        print("  4. Consulter le guide : GUIDE_UTILISATEUR.md")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"\n✗ Erreur JSON : {str(e)}")
        return False
    except Exception as e:
        print(f"\n✗ Erreur : {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Point d'entrée principal."""
    print("Script de migration dependencies.json v1.0 → v2.0\n")
    
    # Vérifier les arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else "dependencies.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file
    
    print(f"Fichier source : {input_file}")
    print(f"Fichier destination : {output_file}")
    
    if input_file == output_file:
        print("⚠ Le fichier sera modifié en place (une sauvegarde sera créée)")
    
    print("\nAppuyez sur Entrée pour continuer ou Ctrl+C pour annuler...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\nMigration annulée")
        sys.exit(0)
    
    print()
    success = migrate_dependencies_file(input_file, output_file, backup=True)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
