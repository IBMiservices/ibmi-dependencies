import os
import subprocess
import json

def clone_or_update(repo_name, repo_info, base_dir):
    repo_path = os.path.join(base_dir, repo_name)
    
    if not os.path.exists(repo_path):
        print(f"Clonage de {repo_name} depuis {repo_info['url']}...")
        subprocess.run(["git", "clone", repo_info["url"], repo_path], check=True)
    else:
        print(f"Mettre à jour {repo_name}...")
        os.chdir(repo_path)
        subprocess.run(["git", "pull"], check=True)
    
    os.chdir(repo_path)
    print(f"Basculer vers la référence {repo_info['ref']} pour {repo_name}...")
    subprocess.run(["git", "checkout", repo_info["ref"]], check=True)

    # Retourner au répertoire de base
    os.chdir("..")
    print(f"{repo_name} est prêt.\n")

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
    base_dir = "repos"  # Répertoire où cloner les dépôts
    install_dependencies(dependencies_file, base_dir)