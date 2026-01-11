#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test d'intégration manuel pour l'installation de logfori
Lance ce script pour tester l'installation réelle de logfori
"""

import os
import sys
import json
import tempfile
import shutil
import subprocess

# Forcer l'encodage UTF-8 pour éviter les erreurs Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def test_logfori_installation():
    """Test manuel d'installation de logfori."""
    print("=" * 70)
    print("Test d'intégration : Installation de logfori")
    print("=" * 70)
    
    # Créer un dossier temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"\nDossier temporaire créé : {temp_dir}")
        
        # Créer dependencies.json
        deps_config = {
            "name": "test-integration-logfori",
            "version": "1.0.0",
            "description": "Test d'intégration logfori",
            "dependencies": {
                "logfori": {
                    "repository": "https://github.com/IBMiservices/logfori.git",
                    "version": "*",
                    "ref": "main"
                }
            },
            "config": {
                "targetDir": "dep",
                "cleanGit": True,
                "recursiveDependencies": False
            }
        }
        
        deps_file = os.path.join(temp_dir, "dependencies.json")
        with open(deps_file, 'w', encoding='utf-8') as f:
            json.dump(deps_config, f, indent=2)
        print(f"✓ Fichier dependencies.json créé")
        
        # Chemin vers le script d'installation
        script_dir = os.path.dirname(__file__)
        install_script = os.path.join(script_dir, "install_deps_v2.py")
        
        print(f"\nLancement de l'installation...")
        print(f"Script : {install_script}")
        print(f"Répertoire : {temp_dir}")
        
        # Lancer l'installation
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, install_script],
            cwd=temp_dir,
            env=env,
            capture_output=False  # Afficher la sortie en temps réel
        )
        
        print("\n" + "=" * 70)
        print("Vérification des résultats")
        print("=" * 70)
        
        # Vérifier les résultats
        success = True
        
        # 1. Code de retour
        if result.returncode == 0:
            print("✓ Installation terminée avec succès (code 0)")
        else:
            print(f"✗ Installation échouée (code {result.returncode})")
            success = False
        
        # 2. Dossier dep/logfori
        logfori_dir = os.path.join(temp_dir, "dep", "logfori")
        if os.path.exists(logfori_dir) and os.path.isdir(logfori_dir):
            files = os.listdir(logfori_dir)
            print(f"✓ Dossier dep/logfori créé ({len(files)} fichiers)")
            if files:
                print(f"  Exemples de fichiers : {', '.join(files[:5])}")
        else:
            print("✗ Dossier dep/logfori non créé")
            success = False
        
        # 3. Lockfile
        lockfile_path = os.path.join(temp_dir, "dependencies-lock.json")
        if os.path.exists(lockfile_path):
            with open(lockfile_path, 'r', encoding='utf-8') as f:
                lockfile = json.load(f)
            
            if "logfori" in lockfile.get("packages", {}):
                commit_sha = lockfile["packages"]["logfori"].get("commitSha", "")
                print(f"✓ Lockfile créé avec commit SHA: {commit_sha[:8]}...")
            else:
                print("✗ Lockfile créé mais logfori manquant")
                success = False
        else:
            print("✗ Lockfile non créé")
            success = False
        
        print("\n" + "=" * 70)
        if success:
            print("✓ TOUS LES TESTS SONT PASSÉS")
            return 0
        else:
            print("✗ CERTAINS TESTS ONT ÉCHOUÉ")
            return 1


if __name__ == "__main__":
    sys.exit(test_logfori_installation())
