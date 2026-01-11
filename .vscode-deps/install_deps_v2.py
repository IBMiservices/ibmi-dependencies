#!/usr/bin/env python3
"""
Gestionnaire de dépendances pour projets IBM i
Version 2.0 - Avec validation de schéma, logging et gestion d'erreurs
"""

import os
import subprocess
import json
import shutil
import stat
import logging
import sys
from typing import Dict, Set, Optional
from pathlib import Path
from lockfile import DependencyLockfile

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('install_deps.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


def validate_dependencies_schema(dependencies_data: dict, schema_path: str = "schema/dependencies.schema.json") -> bool:
    """
    Valide le fichier dependencies.json contre le schéma JSON.
    
    :param dependencies_data: Données du fichier dependencies.json
    :param schema_path: Chemin vers le fichier de schéma
    :return: True si valide, False sinon
    """
    try:
        import jsonschema
        from jsonschema import validate
        
        if not os.path.exists(schema_path):
            logger.warning(f"Schéma non trouvé à {schema_path}, validation ignorée")
            return True
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        validate(instance=dependencies_data, schema=schema)
        logger.info("✓ Schéma JSON validé avec succès")
        return True
        
    except ImportError:
        logger.warning("Module jsonschema non installé. Installation recommandée: pip install jsonschema")
        return True
    except Exception as e:
        try:
            from jsonschema.exceptions import ValidationError
            if isinstance(e, ValidationError):
                logger.error(f"✗ Erreur de validation du schéma: {e.message}")
                logger.error(f"  Chemin: {' -> '.join(str(p) for p in e.path)}")
            else:
                raise
        except:
            logger.error(f"✗ Erreur lors de la validation: {str(e)}")
        return False


def check_circular_dependencies(current_repo: str, dependencies: Dict, visited: Set[str], path: list) -> bool:
    """
    Détecte les dépendances circulaires.
    
    :param current_repo: Dépôt actuel
    :param dependencies: Dictionnaire de toutes les dépendances
    :param visited: Ensemble des dépôts visités
    :param path: Chemin actuel de la traversée
    :return: True si dépendance circulaire détectée, False sinon
    """
    if current_repo in path:
        cycle = ' -> '.join(path + [current_repo])
        logger.error(f"✗ Dépendance circulaire détectée: {cycle}")
        return True
    
    if current_repo in visited:
        return False
    
    visited.add(current_repo)
    path.append(current_repo)
    path.pop()
    return False


def load_dependencies_config(dependencies_file: str) -> Optional[dict]:
    """
    Charge et valide le fichier de configuration des dépendances.
    
    :param dependencies_file: Chemin vers le fichier dependencies.json
    :return: Configuration chargée ou None en cas d'erreur
    """
    try:
        if not os.path.exists(dependencies_file):
            logger.error(f"✗ Fichier {dependencies_file} introuvable")
            return None
        
        with open(dependencies_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        logger.info(f"✓ Fichier {dependencies_file} chargé")
        
        # Validation du schéma
        if not validate_dependencies_schema(config):
            logger.error("✗ Validation du schéma échouée")
            return None
        
        return config
        
    except json.JSONDecodeError as e:
        logger.error(f"✗ Erreur JSON dans {dependencies_file}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"✗ Erreur lors du chargement de {dependencies_file}: {str(e)}")
        return None


def remove_readonly(func, path, excinfo):
    """Change les permissions d'un fichier en lecture seule avant de le supprimer."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clean_git_files(repo_path: str, repo_name: str):
    """Supprime les fichiers Git d'un dépôt."""
    # Supprimer .git
    git_path = os.path.join(repo_path, ".git")
    if os.path.exists(git_path):
        logger.info(f"Suppression du dossier .git pour {repo_name}...")
        shutil.rmtree(git_path, onerror=remove_readonly)
        logger.debug(f"✓ Dossier .git supprimé")
    
    # Supprimer .gitignore
    gitignore_path = os.path.join(repo_path, ".gitignore")
    if os.path.exists(gitignore_path):
        os.remove(gitignore_path)
        logger.debug(f"✓ Fichier .gitignore supprimé")


def clean_doc_files(repo_path: str, repo_name: str):
    """Supprime les fichiers de documentation."""
    doc_files = ['README.md', 'README', 'LICENSE', 'LICENSE.txt', 'CHANGELOG.md']
    for doc_file in doc_files:
        doc_path = os.path.join(repo_path, doc_file)
        if os.path.exists(doc_path):
            os.remove(doc_path)
            logger.debug(f"✓ Fichier {doc_file} supprimé")
    
    # Supprimer .vscode
    vscode_path = os.path.join(repo_path, ".vscode")
    if os.path.exists(vscode_path):
        shutil.rmtree(vscode_path)
        logger.debug(f"✓ Dossier .vscode supprimé")
    
    # Supprimer iproj.json et Rules.mk dupliqués
    for file in ['iproj.json', 'Rules.mk']:
        file_path = os.path.join(repo_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"✓ Fichier {file} supprimé")


def clone_or_update(repo_name: str, repo_info: dict, base_dir: str, config: dict) -> Optional[str]:
    """
    Clone ou met à jour un dépôt Git.
    
    :param repo_name: Nom du dépôt
    :param repo_info: Informations du dépôt (url, ref, version, etc.)
    :param base_dir: Répertoire de base
    :param config: Configuration globale
    :return: Commit SHA si succès, None sinon
    """
    try:
        repo_path = os.path.join(base_dir, repo_name)
        
        # Extraire l'URL du dépôt (nouveau format ou ancien)
        repo_url = repo_info.get('repository', repo_info.get('url'))
        if not repo_url:
            logger.error(f"✗ URL du dépôt manquante pour {repo_name}")
            return False
        
        # Vérifier si c'est une dépendance optionnelle
        is_optional = repo_info.get('optional', False)
        
        # Supprimer le dossier du projet s'il existe déjà
        if os.path.exists(repo_path):
            logger.info(f"Suppression du dossier existant pour {repo_name}...")
            shutil.rmtree(repo_path)
            logger.info(f"✓ Dossier existant supprimé pour {repo_name}")
        
        # Cloner le dépôt
        logger.info(f"Clonage de {repo_name} depuis {repo_url}...")
        result = subprocess.run(
            ["git", "clone", repo_url, repo_path],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            if is_optional:
                logger.warning(f"⚠ Échec du clonage de la dépendance optionnelle {repo_name}")
                return None  # Ne pas échouer pour une dépendance optionnelle
            else:
                logger.error(f"✗ Échec du clonage de {repo_name}: {result.stderr}")
                return None
        
        logger.info(f"✓ {repo_name} cloné avec succès")
        
        # Basculer vers une référence spécifique si fournie
        ref = repo_info.get('ref')
        if ref:
            logger.info(f"Basculer vers la référence {ref} pour {repo_name}...")
            result = subprocess.run(
                ["git", "-C", repo_path, "checkout", ref.strip()],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"✗ Échec du checkout de {ref} pour {repo_name}: {result.stderr}")
                return None
            
            logger.info(f"✓ Référence {ref} appliquée")
        
        # Récupérer le SHA du commit actuel
        commit_sha_result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True,
            text=True
        )
        commit_sha = commit_sha_result.stdout.strip() if commit_sha_result.returncode == 0 else None
        
        logger.info(f"✓ {repo_name} est prêt\n")
        
        # Nettoyage selon la configuration
        if config.get('cleanGit', True):
            clean_git_files(repo_path, repo_name)
        
        if config.get('cleanDocs', True):
            clean_doc_files(repo_path, repo_name)
        
        # Supprimer le répertoire base_dir à l'intérieur du dépôt cloné s'il existe
        inner_base_dir = os.path.join(repo_path, base_dir)
        if os.path.exists(inner_base_dir):
            logger.info(f"Suppression du répertoire {inner_base_dir} pour {repo_name}...")
            shutil.rmtree(inner_base_dir)
            logger.info(f"✓ Répertoire {inner_base_dir} supprimé")
        
        # Supprimer les fichiers/dossiers exclus
        excluded = repo_info.get('exclude', [])
        for exclude_pattern in excluded:
            exclude_path = os.path.join(repo_path, exclude_pattern)
            if os.path.exists(exclude_path):
                if os.path.isdir(exclude_path):
                    shutil.rmtree(exclude_path)
                else:
                    os.remove(exclude_path)
                logger.info(f"✓ Exclusion appliquée: {exclude_pattern}")
        
        return commit_sha
        
    except Exception as e:
        logger.error(f"✗ Erreur lors du traitement de {repo_name}: {str(e)}")
        if repo_info.get('optional', False):
            logger.warning(f"⚠ Dépendance optionnelle {repo_name} ignorée")
            return None
        return None


def remove_unnecessary_files(base_dir):
    """Supprime les fichiers inutiles dans les dépendances."""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file in ["install_deps.py", "dependencies.json"]:
                file_path = os.path.join(root, file)
                logger.info(f"Suppression du fichier {file_path}...")
                os.remove(file_path)
                logger.debug(f"✓ Fichier {file_path} supprimé")


def update_rules_mk(project_root, base_dir):
    """Met à jour le fichier Rules.mk à la racine du projet."""
    rules_mk_path = os.path.join(project_root, "Rules.mk")
    if not os.path.exists(rules_mk_path):
        with open(rules_mk_path, "w") as f:
            f.write("SUBDIRS = ")

    with open(rules_mk_path, "r") as f:
        content = f.read()

    subdirs = content.split("SUBDIRS = ")[1].strip().split() if "SUBDIRS = " in content else []

    for root, dirs, files in os.walk(base_dir):
        if any(file.lower().endswith((".rpgle", ".sqlrpgle", ".clle")) for file in files):
            # Gérer le cas des chemins cross-drive sur Windows
            try:
                relative_path = os.path.relpath(root, project_root).replace("\\", "/")
            except ValueError:
                # Si les chemins sont sur des lecteurs différents, utiliser le chemin absolu
                logger.warning(f"Impossible de calculer le chemin relatif pour {root} (cross-drive)")
                relative_path = os.path.abspath(root).replace("\\", "/")
            
            if relative_path not in subdirs:
                subdirs.append(relative_path)

    with open(rules_mk_path, "w") as f:
        f.write("SUBDIRS = " + " ".join(subdirs))
    
    logger.info(f"✓ Fichier Rules.mk mis à jour avec {len(subdirs)} sous-répertoires")


def update_include_path(iproj_path, base_dir):
    """Met à jour les chemins d'inclusion dans iproj.json."""
    # Vérifier si le fichier existe
    if not os.path.exists(iproj_path):
        logger.warning(f"Fichier {iproj_path} non trouvé, création ignorée")
        return
    
    with open(iproj_path, "r") as f:
        iproj_data = json.load(f)

    include_path = iproj_data.get("includePath", [])
    original_count = len(include_path)

    for root, dirs, files in os.walk(base_dir):
        if any(file.lower().endswith(".rpgleinc") for file in files):
            # Gérer le cas des chemins cross-drive
            try:
                relative_path = os.path.relpath(root, os.path.dirname(iproj_path)).replace("\\", "/")
            except ValueError:
                logger.warning(f"Impossible de calculer le chemin relatif pour {root} (cross-drive)")
                relative_path = os.path.abspath(root).replace("\\", "/")
            
            if relative_path not in include_path:
                include_path.append(relative_path)

    iproj_data["includePath"] = include_path

    with open(iproj_path, "w") as f:
        json.dump(iproj_data, f, indent=2, ensure_ascii=False)
    
    new_paths = len(include_path) - original_count
    if new_paths > 0:
        logger.info(f"✓ Fichier iproj.json mis à jour avec {new_paths} nouveaux chemins d'inclusion")


def create_empty_rules_mk(base_dir):
    """Crée des fichiers Rules.mk vides dans chaque sous-répertoire."""
    count = 0
    for root, dirs, files in os.walk(base_dir):
        rules_mk_path = os.path.join(root, "Rules.mk")
        if not os.path.exists(rules_mk_path):
            with open(rules_mk_path, "w") as f:
                f.write("")
            count += 1
    
    if count > 0:
        logger.info(f"✓ {count} fichiers Rules.mk créés")


def install_dependencies(dependencies_file: str, base_dir: str, project_root: str, 
                        iproj_path: str, processed_repos: Optional[Set[str]] = None) -> bool:
    """
    Installe les dépendances spécifiées dans le fichier JSON.

    :param dependencies_file: Chemin vers le fichier JSON des dépendances
    :param base_dir: Répertoire racine où les dépôts seront stockés
    :param project_root: Répertoire racine du projet
    :param iproj_path: Chemin vers le fichier iproj.json
    :param processed_repos: Ensemble des dépôts déjà traités pour éviter les redondances
    :return: True si succès, False si échec
    """
    if processed_repos is None:
        processed_repos = set()
        logger.info("=" * 70)
        logger.info("Démarrage de l'installation des dépendances IBM i")
        logger.info("=" * 70)
        
        # Charger ou créer le lockfile
        lockfile = DependencyLockfile(os.path.join(project_root, "dependencies-lock.json"))
        lockfile.load()
    else:
        lockfile = None

    # Charger et valider la configuration
    config_data = load_dependencies_config(dependencies_file)
    if config_data is None:
        return False
    
    dependencies = config_data.get("dependencies", {})
    dev_dependencies = config_data.get("devDependencies", {})
    config = config_data.get("config", {})
    
    # Utiliser le targetDir de la config si spécifié
    if processed_repos == set():  # Première itération
        base_dir = config.get("targetDir", base_dir)
        logger.info(f"Répertoire cible: {base_dir}")
    
    # Vérifier les dépendances circulaires
    logger.info("Vérification des dépendances circulaires...")
    all_deps = {**dependencies, **dev_dependencies}
    for repo_name in all_deps.keys():
        if check_circular_dependencies(repo_name, all_deps, set(), []):
            logger.error("✗ Installation annulée en raison de dépendances circulaires")
            return False
    logger.info("✓ Aucune dépendance circulaire détectée")
    
    # Assurer que le répertoire de base existe
    os.makedirs(base_dir, exist_ok=True)
    
    # Traiter chaque dépendance
    success_count = 0
    fail_count = 0
    
    for repo_name, repo_info in dependencies.items():
        if repo_name not in processed_repos:
            logger.info(f"\n{'─' * 70}")
            logger.info(f"Traitement de la dépendance: {repo_name}")
            logger.info(f"{'─' * 70}")
            
            commit_sha = clone_or_update(repo_name, repo_info, base_dir, config)
            if commit_sha:
                processed_repos.add(repo_name)
                success_count += 1
                
                # Ajouter au lockfile
                if lockfile:
                    lockfile.add_package(
                        name=repo_name,
                        repo_url=repo_info.get('repository', ''),
                        ref=repo_info.get('ref', ''),
                        version=repo_info.get('version'),
                        commit_sha=commit_sha
                    )
                
                # Traiter les dépendances imbriquées si activé
                if config.get("recursiveDependencies", True):
                    nested_dependencies_file = os.path.join(base_dir, repo_name, "dependencies.json")
                    if os.path.exists(nested_dependencies_file):
                        logger.info(f"Traitement des dépendances imbriquées de {repo_name}...")
                        install_dependencies(nested_dependencies_file, base_dir, project_root, iproj_path, processed_repos)
            else:
                fail_count += 1
                if not repo_info.get('optional', False):
                    logger.error(f"✗ Échec de l'installation de {repo_name}")
                    return False

    # Mettre à jour les fichiers de build si activé
    if config.get("updateBuildFiles", True) and processed_repos:
        logger.info(f"\n{'─' * 70}")
        logger.info("Mise à jour des fichiers de build")
        logger.info(f"{'─' * 70}")
        
        create_empty_rules_mk(base_dir)
        update_rules_mk(project_root, base_dir)
        update_include_path(iproj_path, base_dir)
        remove_unnecessary_files(base_dir)
    
    # Résumé final (seulement pour l'appel initial)
    if len(processed_repos) == success_count + fail_count:
        # Sauvegarder le lockfile
        if lockfile:
            lockfile.save()
            logger.info("✓ Fichier dependencies-lock.json sauvegardé")
        
        logger.info(f"\n{'=' * 70}")
        logger.info("Installation terminée")
        logger.info(f"{'=' * 70}")
        logger.info(f"✓ Dépendances installées avec succès: {success_count}")
        if fail_count > 0:
            logger.info(f"✗ Dépendances échouées: {fail_count}")
        logger.info(f"Total de dépendances traitées: {len(processed_repos)}")
        logger.info(f"{'=' * 70}")
    
    return True


def main():
    """Point d'entrée principal du script."""
    dependencies_file = "dependencies.json"
    project_root = os.getcwd()  # Utiliser le répertoire courant, pas celui du script
    iproj_path = os.path.join(project_root, "iproj.json")
    base_dir = "dep"  # Valeur par défaut, sera remplacée par config si spécifié
    
    try:
        success = install_dependencies(dependencies_file, base_dir, project_root, iproj_path)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("\n⚠ Installation interrompue par l'utilisateur")
        sys.exit(130)
    except Exception as e:
        logger.error(f"\n✗ Erreur fatale: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
