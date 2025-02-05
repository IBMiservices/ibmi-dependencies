import os
import subprocess
import json
import shutil

def clone_or_update(repo_name, repo_info, base_dir):
    repo_path = os.path.join(base_dir, repo_name)
    
    if not os.path.exists(repo_path):
        print(f"Clonage de {repo_name} depuis {repo_info['url']}...")
        subprocess.run(["git", "clone", repo_info["url"], repo_path], check=True)
    else:
        print(f"Mettre à jour {repo_name}...")
        subprocess.run(["git", "-C", repo_path, "pull"], check=True)
    
    print(f"Basculer vers la référence {repo_info['ref']} pour {repo_name}...")
    subprocess.run(["git", "-C", repo_path, "checkout", repo_info["ref"].strip()], check=True)

    print(f"{repo_name} est prêt.\n")
    
    # Supprimer le dossier .vscode s'il existe
    vscode_path = os.path.join(repo_path, ".vscode")
    if (os.path.exists(vscode_path)):
        print(f"Suppression du dossier .vscode pour {repo_name}...")
        shutil.rmtree(vscode_path)
        print(f"Dossier .vscode supprimé pour {repo_name}.\n")
    
    # Supprimer le fichier iproj.json s'il existe
    iproj_path = os.path.join(repo_path, "iproj.json")
    if (os.path.exists(iproj_path)):
        print(f"Suppression du fichier iproj.json pour {repo_name}...")
        os.remove(iproj_path)
        print(f"Fichier iproj.json supprimé pour {repo_name}.\n")
    
    # Supprimer le fichier Rules.mk s'il existe
    rules_mk_path = os.path.join(repo_path, "Rules.mk")
    if (os.path.exists(rules_mk_path)):
        print(f"Suppression du fichier Rules.mk pour {repo_name}...")
        os.remove(rules_mk_path)
        print(f"Fichier Rules.mk supprimé pour {repo_name}.\n")

def install_dependencies(dependencies_file, base_dir):
    """
    Installe les dépendances spécifiées dans le fichier JSON.

    :param dependencies_file: Chemin vers le fichier JSON des dépendances
    :param base_dir: Répertoire racine où les dépôts seront stockés
    """
    with open(dependencies_file, "r") as f:
        dependencies = json.load(f)["dependencies"]

    # Assure-toi que le répertoire de base existe
    os.makedirs(base_dir, exist_ok=True)

    # Traiter chaque dépendance
    for repo_name, repo_info in dependencies.items():
        clone_or_update(repo_name, repo_info, base_dir)

# Exemple d'utilisation
if __name__ == "__main__":
    dependencies_file = "dependencies.json"  # Chemin vers le fichier des dépendances
    base_dir = "dep"  # Répertoire où cloner les dépôts
    install_dependencies(dependencies_file, base_dir)