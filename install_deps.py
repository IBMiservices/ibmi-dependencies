import os
import subprocess
import json
import shutil
import stat

def clone_or_update(repo_name, repo_info, base_dir):
    repo_path = os.path.join(base_dir, repo_name)
    
    # Supprimer le dossier du projet s'il existe déjà
    if os.path.exists(repo_path):
        print(f"Suppression du dossier existant pour {repo_name}...")
        shutil.rmtree(repo_path)
        print(f"Dossier existant supprimé pour {repo_name}.\n")
    
    # Cloner ou mettre à jour le dépôt
    print(f"Clonage de {repo_name} depuis {repo_info['url']}...")
    subprocess.run(["git", "clone", repo_info["url"], repo_path], check=True)
    
    print(f"Basculer vers la référence {repo_info['ref']} pour {repo_name}...")
    subprocess.run(["git", "-C", repo_path, "checkout", repo_info["ref"].strip()], check=True)

    print(f"{repo_name} est prêt.\n")
    
    # Supprimer le dossier .vscode s'il existe
    vscode_path = os.path.join(repo_path, ".vscode")
    if os.path.exists(vscode_path):
        print(f"Suppression du dossier .vscode pour {repo_name}...")
        shutil.rmtree(vscode_path)
        print(f"Dossier .vscode supprimé pour {repo_name}.\n")
    
    # Supprimer le fichier iproj.json s'il existe
    iproj_path = os.path.join(repo_path, "iproj.json")
    if os.path.exists(iproj_path):
        print(f"Suppression du fichier iproj.json pour {repo_name}...")
        os.remove(iproj_path)
        print(f"Fichier iproj.json supprimé pour {repo_name}.\n")
    
    # Supprimer le fichier Rules.mk s'il existe
    rules_mk_path = os.path.join(repo_path, "Rules.mk")
    if os.path.exists(rules_mk_path):
        print(f"Suppression du fichier Rules.mk pour {repo_name}...")
        os.remove(rules_mk_path)
        print(f"Fichier Rules.mk supprimé pour {repo_name}.\n")
    
    # Supprimer le dossier .git s'il existe
    git_path = os.path.join(repo_path, ".git")
    if os.path.exists(git_path):
        print(f"Suppression du dossier .git pour {repo_name}...")
        shutil.rmtree(git_path, onerror=remove_readonly)
        print(f"Dossier .git supprimé pour {repo_name}.\n")

def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def install_dependencies(dependencies_file, base_dir, processed_repos=None):
    """
    Installe les dépendances spécifiées dans le fichier JSON.

    :param dependencies_file: Chemin vers le fichier JSON des dépendances
    :param base_dir: Répertoire racine où les dépôts seront stockés
    :param processed_repos: Ensemble des dépôts déjà traités pour éviter les redondances
    """
    if processed_repos is None:
        processed_repos = set()

    with open(dependencies_file, "r") as f:
        dependencies = json.load(f)["dependencies"]

    # Assure-toi que le répertoire de base existe
    os.makedirs(base_dir, exist_ok=True)

    # Traiter chaque dépendance
    for repo_name, repo_info in dependencies.items():
        if repo_name not in processed_repos:
            clone_or_update(repo_name, repo_info, base_dir)
            processed_repos.add(repo_name)
            
            # Traiter les dépendances imbriquées
            nested_dependencies_file = os.path.join(base_dir, repo_name, "dependencies.json")
            if os.path.exists(nested_dependencies_file):
                install_dependencies(nested_dependencies_file, base_dir, processed_repos)

# Exemple d'utilisation
if __name__ == "__main__":
    dependencies_file = "dependencies.json"  # Chemin vers le fichier des dépendances
    base_dir = "dep"  # Répertoire où cloner les dépôts
    install_dependencies(dependencies_file, base_dir)