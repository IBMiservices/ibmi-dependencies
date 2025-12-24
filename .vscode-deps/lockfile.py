#!/usr/bin/env python3
"""
Module de gestion du fichier de verrouillage (lockfile)
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, Optional


class DependencyLockfile:
    """Gère le fichier de verrouillage des dépendances."""
    
    def __init__(self, lockfile_path: str = "dependencies-lock.json"):
        self.lockfile_path = lockfile_path
        self.lock_data = {}
    
    def load(self) -> bool:
        """Charge le fichier de verrouillage existant."""
        try:
            with open(self.lockfile_path, 'r', encoding='utf-8') as f:
                self.lock_data = json.load(f)
            return True
        except FileNotFoundError:
            self.lock_data = {
                "version": "1.0.0",
                "lockfileVersion": 1,
                "created": datetime.now().isoformat(),
                "packages": {}
            }
            return False
        except Exception as e:
            print(f"Erreur lors du chargement du lockfile: {e}")
            return False
    
    def save(self) -> bool:
        """Sauvegarde le fichier de verrouillage."""
        try:
            self.lock_data["updated"] = datetime.now().isoformat()
            with open(self.lockfile_path, 'w', encoding='utf-8') as f:
                json.dump(self.lock_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du lockfile: {e}")
            return False
    
    def add_package(self, name: str, repo_url: str, ref: str, version: Optional[str] = None, 
                   commit_sha: Optional[str] = None, dependencies: Optional[Dict] = None):
        """
        Ajoute un package au lockfile.
        
        :param name: Nom du package
        :param repo_url: URL du dépôt
        :param ref: Référence Git (tag, branch)
        :param version: Version du package
        :param commit_sha: SHA du commit
        :param dependencies: Dépendances du package
        """
        if "packages" not in self.lock_data:
            self.lock_data["packages"] = {}
        
        self.lock_data["packages"][name] = {
            "repository": repo_url,
            "ref": ref,
            "version": version or "unknown",
            "commitSha": commit_sha,
            "resolved": datetime.now().isoformat(),
            "integrity": self._calculate_integrity(name, repo_url, ref),
            "dependencies": dependencies or {}
        }
    
    def get_package(self, name: str) -> Optional[Dict]:
        """Récupère les informations d'un package depuis le lockfile."""
        return self.lock_data.get("packages", {}).get(name)
    
    def has_package(self, name: str) -> bool:
        """Vérifie si un package est dans le lockfile."""
        return name in self.lock_data.get("packages", {})
    
    def is_package_changed(self, name: str, repo_url: str, ref: str) -> bool:
        """
        Vérifie si un package a changé depuis la dernière installation.
        
        :param name: Nom du package
        :param repo_url: URL du dépôt
        :param ref: Référence Git
        :return: True si changé, False sinon
        """
        if not self.has_package(name):
            return True
        
        package = self.get_package(name)
        return (package.get("repository") != repo_url or 
                package.get("ref") != ref)
    
    def _calculate_integrity(self, name: str, repo_url: str, ref: str) -> str:
        """Calcule un hash d'intégrité pour le package."""
        data = f"{name}:{repo_url}:{ref}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_all_packages(self) -> Dict:
        """Retourne tous les packages du lockfile."""
        return self.lock_data.get("packages", {})
    
    def remove_package(self, name: str):
        """Supprime un package du lockfile."""
        if "packages" in self.lock_data and name in self.lock_data["packages"]:
            del self.lock_data["packages"][name]
    
    def clear(self):
        """Vide le lockfile."""
        self.lock_data = {
            "version": "1.0.0",
            "lockfileVersion": 1,
            "created": datetime.now().isoformat(),
            "packages": {}
        }


def get_git_commit_sha(repo_path: str) -> Optional[str]:
    """
    Récupère le SHA du commit actuel d'un dépôt Git.
    
    :param repo_path: Chemin vers le dépôt
    :return: SHA du commit ou None
    """
    try:
        import subprocess
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return None
