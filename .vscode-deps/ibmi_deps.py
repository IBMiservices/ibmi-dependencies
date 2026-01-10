#!/usr/bin/env python3
"""
Interface CLI pour le gestionnaire de dépendances IBM i
Usage: python ibmi_deps.py <command> [options]
"""

import sys
import os
import argparse
import json
import subprocess
from pathlib import Path


class IBMiDepsCLI:
    """Interface en ligne de commande pour ibmi-dependencies."""
    
    def __init__(self):
        self.version = "2.0.0"
        self.deps_file = "dependencies.json"
        self.lock_file = "dependencies-lock.json"
        
    def run(self, args=None):
        """Point d'entrée principal."""
        parser = self.create_parser()
        
        if args is None:
            args = sys.argv[1:]
        
        if not args:
            parser.print_help()
            return 0
        
        parsed = parser.parse_args(args)
        
        # Exécuter la commande
        if hasattr(parsed, 'func'):
            try:
                return parsed.func(parsed)
            except Exception as e:
                print(f"❌ Erreur: {e}", file=sys.stderr)
                return 1
        else:
            parser.print_help()
            return 0
    
    def create_parser(self):
        """Crée le parser d'arguments."""
        parser = argparse.ArgumentParser(
            prog='ibmi-deps',
            description='Gestionnaire de dépendances pour projets IBM i',
            epilog='Pour plus d\'aide sur une commande: ibmi-deps <command> --help'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version=f'ibmi-deps version {self.version}'
        )
        
        subparsers = parser.add_subparsers(
            title='Commandes disponibles',
            dest='command'
        )
        
        # Commande: init
        init_parser = subparsers.add_parser(
            'init',
            help='Initialiser un nouveau projet avec dependencies.json'
        )
        init_parser.add_argument(
            '--name',
            help='Nom du projet',
            required=False
        )
        init_parser.add_argument(
            '--force',
            action='store_true',
            help='Écraser le fichier existant'
        )
        init_parser.set_defaults(func=self.cmd_init)
        
        # Commande: install
        install_parser = subparsers.add_parser(
            'install',
            help='Installer les dépendances'
        )
        install_parser.add_argument(
            '--verbose',
            '-v',
            action='store_true',
            help='Mode verbeux'
        )
        install_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simuler sans installer'
        )
        install_parser.set_defaults(func=self.cmd_install)
        
        # Commande: add
        add_parser = subparsers.add_parser(
            'add',
            help='Ajouter une dépendance'
        )
        add_parser.add_argument(
            'package',
            help='Nom du package à ajouter'
        )
        add_parser.add_argument(
            'repository',
            help='URL du dépôt Git'
        )
        add_parser.add_argument(
            '--version',
            help='Contrainte de version (ex: ^1.0.0)',
            default='*'
        )
        add_parser.add_argument(
            '--ref',
            help='Référence Git (branch, tag, commit)',
            default=None
        )
        add_parser.add_argument(
            '--dev',
            action='store_true',
            help='Ajouter comme dépendance de développement'
        )
        add_parser.set_defaults(func=self.cmd_add)
        
        # Commande: remove
        remove_parser = subparsers.add_parser(
            'remove',
            help='Retirer une dépendance'
        )
        remove_parser.add_argument(
            'package',
            help='Nom du package à retirer'
        )
        remove_parser.set_defaults(func=self.cmd_remove)
        
        # Commande: list
        list_parser = subparsers.add_parser(
            'list',
            help='Lister les dépendances installées'
        )
        list_parser.add_argument(
            '--locked',
            action='store_true',
            help='Afficher depuis le lockfile'
        )
        list_parser.set_defaults(func=self.cmd_list)
        
        # Commande: update
        update_parser = subparsers.add_parser(
            'update',
            help='Mettre à jour les dépendances'
        )
        update_parser.add_argument(
            'package',
            nargs='?',
            help='Package spécifique à mettre à jour'
        )
        update_parser.set_defaults(func=self.cmd_update)
        
        # Commande: clean
        clean_parser = subparsers.add_parser(
            'clean',
            help='Nettoyer les dépendances installées'
        )
        clean_parser.add_argument(
            '--all',
            action='store_true',
            help='Supprimer aussi le lockfile'
        )
        clean_parser.set_defaults(func=self.cmd_clean)
        
        # Commande: info
        info_parser = subparsers.add_parser(
            'info',
            help='Afficher les informations d\'un package'
        )
        info_parser.add_argument(
            'package',
            help='Nom du package'
        )
        info_parser.set_defaults(func=self.cmd_info)
        
        # Commande: validate
        validate_parser = subparsers.add_parser(
            'validate',
            help='Valider dependencies.json'
        )
        validate_parser.set_defaults(func=self.cmd_validate)
        
        return parser
    
    def cmd_init(self, args):
        """Initialise un nouveau projet."""
        if os.path.exists(self.deps_file) and not args.force:
            print(f"❌ {self.deps_file} existe déjà. Utilisez --force pour écraser.")
            return 1
        
        # Déterminer le nom du projet
        project_name = args.name or os.path.basename(os.getcwd())
        
        # Créer la structure de base
        config = {
            "$schema": "./schema/dependencies.schema.json",
            "name": project_name,
            "version": "1.0.0",
            "description": f"Projet IBM i: {project_name}",
            "author": "",
            "license": "Apache-2.0",
            "repository": {
                "type": "git",
                "url": ""
            },
            "dependencies": {},
            "devDependencies": {},
            "config": {
                "targetDir": "dep",
                "cleanGit": True,
                "cleanDocs": True,
                "updateBuildFiles": True,
                "recursiveDependencies": True
            }
        }
        
        with open(self.deps_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ {self.deps_file} créé avec succès!")
        print(f"📝 Projet: {project_name}")
        print(f"\n💡 Prochaines étapes:")
        print(f"   1. Éditez {self.deps_file} pour ajouter vos dépendances")
        print(f"   2. Exécutez: ibmi-deps install")
        
        return 0
    
    def cmd_install(self, args):
        """Installe les dépendances."""
        if not os.path.exists(self.deps_file):
            print(f"❌ {self.deps_file} introuvable. Exécutez 'ibmi-deps init' d'abord.")
            return 1
        
        if args.dry_run:
            print("🔍 Mode simulation (dry-run)")
            with open(self.deps_file, 'r') as f:
                config = json.load(f)
            deps = config.get('dependencies', {})
            print(f"📦 {len(deps)} dépendance(s) à installer:")
            for name in deps:
                print(f"   • {name}")
            return 0
        
        print("📦 Installation des dépendances...")
        cmd = ['python3', 'install_deps_v2.py']
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("\n✅ Installation terminée avec succès!")
        else:
            print("\n❌ Échec de l'installation")
        
        return result.returncode
    
    def cmd_add(self, args):
        """Ajoute une dépendance."""
        if not os.path.exists(self.deps_file):
            print(f"❌ {self.deps_file} introuvable. Exécutez 'ibmi-deps init' d'abord.")
            return 1
        
        with open(self.deps_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Créer l'entrée de dépendance
        dep_entry = {
            "repository": args.repository,
            "version": args.version
        }
        if args.ref:
            dep_entry["ref"] = args.ref
        
        # Ajouter à la bonne section
        section = 'devDependencies' if args.dev else 'dependencies'
        if section not in config:
            config[section] = {}
        
        config[section][args.package] = dep_entry
        
        # Sauvegarder
        with open(self.deps_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        dep_type = "développement" if args.dev else "production"
        print(f"✅ Dépendance {args.package} ajoutée ({dep_type})")
        print(f"💡 Exécutez 'ibmi-deps install' pour installer")
        
        return 0
    
    def cmd_remove(self, args):
        """Retire une dépendance."""
        if not os.path.exists(self.deps_file):
            print(f"❌ {self.deps_file} introuvable.")
            return 1
        
        with open(self.deps_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Chercher et supprimer
        removed = False
        for section in ['dependencies', 'devDependencies']:
            if section in config and args.package in config[section]:
                del config[section][args.package]
                removed = True
                break
        
        if not removed:
            print(f"❌ Package {args.package} non trouvé")
            return 1
        
        # Sauvegarder
        with open(self.deps_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Dépendance {args.package} retirée")
        print(f"💡 Exécutez 'ibmi-deps clean' pour supprimer les fichiers")
        
        return 0
    
    def cmd_list(self, args):
        """Liste les dépendances."""
        if args.locked and os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                lock_data = json.load(f)
            packages = lock_data.get('packages', {})
            print(f"📦 Dépendances installées ({len(packages)}):\n")
            for name, info in packages.items():
                version = info.get('version', 'unknown')
                commit = info.get('commitSha', '')[:8]
                print(f"   • {name:25} v{version:10} [{commit}]")
        else:
            if not os.path.exists(self.deps_file):
                print(f"❌ {self.deps_file} introuvable.")
                return 1
            
            with open(self.deps_file, 'r') as f:
                config = json.load(f)
            
            deps = config.get('dependencies', {})
            dev_deps = config.get('devDependencies', {})
            
            if deps:
                print(f"📦 Dépendances de production ({len(deps)}):\n")
                for name, info in deps.items():
                    version = info.get('version', '*')
                    print(f"   • {name:25} {version}")
            
            if dev_deps:
                print(f"\n🔧 Dépendances de développement ({len(dev_deps)}):\n")
                for name, info in dev_deps.items():
                    version = info.get('version', '*')
                    print(f"   • {name:25} {version}")
            
            if not deps and not dev_deps:
                print("📦 Aucune dépendance déclarée")
        
        return 0
    
    def cmd_update(self, args):
        """Met à jour les dépendances."""
        print("🔄 Mise à jour des dépendances...")
        
        if args.package:
            print(f"   Package: {args.package}")
        else:
            print("   Toutes les dépendances")
        
        # Supprimer le lockfile pour forcer la mise à jour
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)
        
        # Réinstaller
        cmd = ['python3', 'install_deps_v2.py']
        result = subprocess.run(cmd)
        
        return result.returncode
    
    def cmd_clean(self, args):
        """Nettoie les dépendances."""
        print("🧹 Nettoyage...")
        
        # Lire la config pour trouver targetDir
        target_dir = "dep"
        if os.path.exists(self.deps_file):
            with open(self.deps_file, 'r') as f:
                config = json.load(f)
                target_dir = config.get('config', {}).get('targetDir', 'dep')
        
        # Supprimer le répertoire des dépendances
        if os.path.exists(target_dir):
            import shutil
            shutil.rmtree(target_dir)
            print(f"✅ Répertoire {target_dir}/ supprimé")
        
        # Supprimer le lockfile si demandé
        if args.all and os.path.exists(self.lock_file):
            os.remove(self.lock_file)
            print(f"✅ {self.lock_file} supprimé")
        
        # Supprimer le log
        if os.path.exists('install_deps.log'):
            os.remove('install_deps.log')
            print("✅ Logs supprimés")
        
        print("\n✅ Nettoyage terminé")
        return 0
    
    def cmd_info(self, args):
        """Affiche les infos d'un package."""
        if not os.path.exists(self.deps_file):
            print(f"❌ {self.deps_file} introuvable.")
            return 1
        
        with open(self.deps_file, 'r') as f:
            config = json.load(f)
        
        # Chercher le package
        package_info = None
        section_name = None
        
        for section in ['dependencies', 'devDependencies']:
            if section in config and args.package in config[section]:
                package_info = config[section][args.package]
                section_name = section
                break
        
        if not package_info:
            print(f"❌ Package {args.package} non trouvé")
            return 1
        
        print(f"\n📦 {args.package}")
        print("─" * 60)
        print(f"Type        : {'Développement' if section_name == 'devDependencies' else 'Production'}")
        print(f"Dépôt       : {package_info.get('repository', 'N/A')}")
        print(f"Version     : {package_info.get('version', '*')}")
        print(f"Référence   : {package_info.get('ref', 'N/A')}")
        print(f"Optionnel   : {'Oui' if package_info.get('optional', False) else 'Non'}")
        
        if 'exclude' in package_info:
            print(f"Exclusions  : {', '.join(package_info['exclude'])}")
        
        # Info depuis le lockfile si disponible
        if os.path.exists(self.lock_file):
            with open(self.lock_file, 'r') as f:
                lock_data = json.load(f)
            
            if args.package in lock_data.get('packages', {}):
                locked = lock_data['packages'][args.package]
                print("\n🔒 Informations verrouillées:")
                print(f"Version     : {locked.get('version', 'N/A')}")
                print(f"Commit SHA  : {locked.get('commitSha', 'N/A')[:16]}")
                print(f"Résolu le   : {locked.get('resolved', 'N/A')}")
        
        print("─" * 60)
        return 0
    
    def cmd_validate(self, args):
        """Valide le fichier dependencies.json."""
        if not os.path.exists(self.deps_file):
            print(f"❌ {self.deps_file} introuvable.")
            return 1
        
        print(f"🔍 Validation de {self.deps_file}...")
        
        try:
            with open(self.deps_file, 'r') as f:
                config = json.load(f)
            
            # Vérifications basiques
            errors = []
            warnings = []
            
            # Champs requis
            if 'name' not in config:
                errors.append("Champ 'name' manquant")
            if 'version' not in config:
                errors.append("Champ 'version' manquant")
            if 'dependencies' not in config:
                errors.append("Champ 'dependencies' manquant")
            
            # Validation des dépendances
            for section in ['dependencies', 'devDependencies']:
                if section in config:
                    for name, info in config[section].items():
                        if 'repository' not in info and 'url' not in info:
                            errors.append(f"Dépendance '{name}': repository manquant")
            
            # Affichage
            if errors:
                print("\n❌ Erreurs trouvées:")
                for err in errors:
                    print(f"   • {err}")
                return 1
            
            if warnings:
                print("\n⚠️  Avertissements:")
                for warn in warnings:
                    print(f"   • {warn}")
            
            print("\n✅ Validation réussie!")
            print(f"   Projet: {config.get('name', 'N/A')}")
            print(f"   Version: {config.get('version', 'N/A')}")
            print(f"   Dépendances: {len(config.get('dependencies', {}))}")
            
            return 0
            
        except json.JSONDecodeError as e:
            print(f"❌ Erreur JSON: {e}")
            return 1
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return 1


def main():
    """Point d'entrée."""
    cli = IBMiDepsCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
