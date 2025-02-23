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
    
    # Vider le répertoire base_dir à l'intérieur du dépôt cloné
    inner_base_dir = os.path.join(repo_path, base_dir)
    if os.path.exists(inner_base_dir):
        print(f"Vidage du répertoire {inner_base_dir} pour {repo_name}...")
        empty_directory(inner_base_dir)
        print(f"Répertoire {inner_base_dir} vidé pour {repo_name}.\n")
    
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

def empty_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def update_rules_mk(project_root, base_dir):
    rules_mk_path = os.path.join(project_root, "Rules.mk")
    if not os.path.exists(rules_mk_path):
        with open(rules_mk_path, "w") as f:
            f.write("SUBDIRS = ")

    with open(rules_mk_path, "r") as f:
        content = f.read()

    subdirs = content.split("SUBDIRS = ")[1].strip().split() if "SUBDIRS = " in content else []

    for root, dirs, files in os.walk(base_dir):
        if any(file.lower().endswith((".rpgle", ".sqlrpgle", ".clle")) for file in files):
            relative_path = os.path.relpath(root, project_root).replace("\\", "/")
            if relative_path not in subdirs:
                subdirs.append(relative_path)

    with open(rules_mk_path, "w") as f:
        f.write("SUBDIRS = " + " ".join(subdirs))

def update_include_path(iproj_path, base_dir):
    with open(iproj_path, "r") as f:
        iproj_data = json.load(f)

    include_path = iproj_data.get("includePath", [])

    for root, dirs, files in os.walk(base_dir):
        if any(file.lower().endswith(".rpgleinc") for file in files):
            relative_path = os.path.relpath(root, os.path.dirname(iproj_path)).replace("\\", "/")
            if relative_path not in include_path:
                include_path.append(relative_path)

    iproj_data["includePath"] = include_path

    with open(iproj_path, "w") as f:
        json.dump(iproj_data, f, indent=2, ensure_ascii=False)

def install_dependencies(dependencies_file, base_dir, project_root, iproj_path, processed_repos=None):
    """
    Installe les dépendances spécifiées dans le fichier JSON.

    :param dependencies_file: Chemin vers le fichier JSON des dépendances
    :param base_dir: Répertoire racine où les dépôts seront stockés
    :param project_root: Répertoire racine du projet
    :param iproj_path: Chemin vers le fichier iproj.json
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
                install_dependencies(nested_dependencies_file, base_dir, project_root, iproj_path, processed_repos)

    # Mettre à jour le fichier Rules.mk à la racine du projet
    update_rules_mk(project_root, base_dir)

    # Mettre à jour le fichier iproj.json avec les chemins relatifs des fichiers *.rpgleinc ou *RPGLEINC
    update_include_path(iproj_path, base_dir)

# Exemple d'utilisation
if __name__ == "__main__":
    dependencies_file = "dependencies.json"  # Chemin vers le fichier des dépendances
    base_dir = "dep"  # Répertoire où cloner les dépôts
    project_root = os.path.dirname(os.path.abspath(__file__))  # Répertoire racine du projet
    iproj_path = os.path.join(project_root, "iproj.json")  # Chemin vers le fichier iproj.json
    install_dependencies(dependencies_file, base_dir, project_root, iproj_path)