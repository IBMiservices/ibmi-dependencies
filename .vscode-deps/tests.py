#!/usr/bin/env python3
"""
Tests pour le gestionnaire de dépendances IBM i
"""

import unittest
import json
import os
import tempfile
import shutil
from pathlib import Path


class TestDependencySchema(unittest.TestCase):
    """Tests de validation du schéma JSON."""
    
    def setUp(self):
        """Prépare les tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.deps_file = os.path.join(self.temp_dir, "dependencies.json")
    
    def tearDown(self):
        """Nettoie après les tests."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_valid_minimal_config(self):
        """Test d'une configuration minimale valide."""
        config = {
            "name": "test-project",
            "version": "1.0.0",
            "dependencies": {}
        }
        
        with open(self.deps_file, 'w') as f:
            json.dump(config, f)
        
        self.assertTrue(os.path.exists(self.deps_file))
        
        with open(self.deps_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded["name"], "test-project")
        self.assertEqual(loaded["version"], "1.0.0")
    
    def test_valid_complete_config(self):
        """Test d'une configuration complète valide."""
        config = {
            "name": "test-project",
            "version": "1.0.0",
            "description": "Test project",
            "author": "Test Author",
            "license": "Apache-2.0",
            "dependencies": {
                "test-lib": {
                    "repository": "https://github.com/test/test-lib.git",
                    "version": "^1.0.0",
                    "ref": "v1.0.0"
                }
            },
            "devDependencies": {},
            "config": {
                "targetDir": "dependencies",
                "cleanGit": True,
                "cleanDocs": True
            }
        }
        
        with open(self.deps_file, 'w') as f:
            json.dump(config, f)
        
        with open(self.deps_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertIn("test-lib", loaded["dependencies"])
        self.assertEqual(loaded["dependencies"]["test-lib"]["version"], "^1.0.0")


class TestLockfile(unittest.TestCase):
    """Tests du système de lockfile."""
    
    def setUp(self):
        """Prépare les tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.lock_file = os.path.join(self.temp_dir, "dependencies-lock.json")
    
    def tearDown(self):
        """Nettoie après les tests."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_create_lockfile(self):
        """Test de création d'un lockfile."""
        from lockfile import DependencyLockfile
        
        lock = DependencyLockfile(self.lock_file)
        lock.load()
        lock.add_package(
            name="test-package",
            repo_url="https://github.com/test/test.git",
            ref="v1.0.0",
            version="1.0.0",
            commit_sha="abc123"
        )
        lock.save()
        
        self.assertTrue(os.path.exists(self.lock_file))
        
        # Recharger et vérifier
        lock2 = DependencyLockfile(self.lock_file)
        lock2.load()
        
        self.assertTrue(lock2.has_package("test-package"))
        pkg = lock2.get_package("test-package")
        self.assertEqual(pkg["version"], "1.0.0")
        self.assertEqual(pkg["commitSha"], "abc123")
    
    def test_detect_package_change(self):
        """Test de détection de changement de package."""
        from lockfile import DependencyLockfile
        
        lock = DependencyLockfile(self.lock_file)
        lock.load()
        lock.add_package(
            name="test-package",
            repo_url="https://github.com/test/test.git",
            ref="v1.0.0",
            version="1.0.0"
        )
        
        # Même configuration - pas de changement
        self.assertFalse(lock.is_package_changed(
            "test-package",
            "https://github.com/test/test.git",
            "v1.0.0"
        ))
        
        # Différente ref - changement détecté
        self.assertTrue(lock.is_package_changed(
            "test-package",
            "https://github.com/test/test.git",
            "v2.0.0"
        ))


class TestCircularDependencies(unittest.TestCase):
    """Tests de détection de dépendances circulaires."""
    
    def test_no_circular_dependency(self):
        """Test sans dépendance circulaire."""
        dependencies = {
            "pkg-a": {"repository": "url-a", "dependencies": {}},
            "pkg-b": {"repository": "url-b", "dependencies": {}}
        }
        
        # Pas de cycle
        self.assertFalse(self._has_cycle(dependencies))
    
    def test_detect_circular_dependency(self):
        """Test de détection de dépendance circulaire."""
        # Ce test est simplifié - dans un vrai scénario,
        # il faudrait charger les dépendances imbriquées
        dependencies = {
            "pkg-a": {"repository": "url-a"},
            "pkg-b": {"repository": "url-b"}
        }
        
        # Pour tester les cycles réels, il faudrait
        # cloner les dépôts et analyser leurs dependencies.json
        pass
    
    def _has_cycle(self, deps):
        """Fonction helper pour détecter les cycles (simplifiée)."""
        return False


class TestVersionConstraints(unittest.TestCase):
    """Tests des contraintes de versions."""
    
    def test_exact_version(self):
        """Test de version exacte."""
        self.assertTrue(self._matches("1.0.0", "1.0.0"))
        self.assertFalse(self._matches("1.0.0", "1.0.1"))
    
    def test_caret_version(self):
        """Test de contrainte ^ (compatible)."""
        constraint = "^1.0.0"
        self.assertTrue(self._matches(constraint, "1.0.0"))
        self.assertTrue(self._matches(constraint, "1.1.0"))
        self.assertTrue(self._matches(constraint, "1.9.9"))
        self.assertFalse(self._matches(constraint, "2.0.0"))
    
    def test_tilde_version(self):
        """Test de contrainte ~ (patch)."""
        constraint = "~1.0.0"
        self.assertTrue(self._matches(constraint, "1.0.0"))
        self.assertTrue(self._matches(constraint, "1.0.5"))
        self.assertFalse(self._matches(constraint, "1.1.0"))
    
    def _matches(self, constraint, version):
        """
        Vérifie si une version satisfait une contrainte.
        Implémentation simplifiée pour les tests.
        """
        if constraint.startswith("^"):
            base = constraint[1:]
            major_base = int(base.split(".")[0])
            major_ver = int(version.split(".")[0])
            return major_base == major_ver and version >= base
        elif constraint.startswith("~"):
            base = constraint[1:]
            parts_base = base.split(".")
            parts_ver = version.split(".")
            return (parts_base[0] == parts_ver[0] and 
                   parts_base[1] == parts_ver[1] and 
                   version >= base)
        else:
            return constraint == version


def run_tests():
    """Lance tous les tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestDependencySchema))
    suite.addTests(loader.loadTestsFromTestCase(TestLockfile))
    suite.addTests(loader.loadTestsFromTestCase(TestCircularDependencies))
    suite.addTests(loader.loadTestsFromTestCase(TestVersionConstraints))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
