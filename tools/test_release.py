"""A distributable archive must run away from the development repository."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

from _paths import ROOT
import release


class ReleaseTests(unittest.TestCase):
    def test_packaged_plugin_is_complete_and_runs_after_extraction(self):
        with tempfile.TemporaryDirectory(prefix='flow-aidd-release-') as directory:
            root = Path(directory)
            output = root / 'flow-aidd.zip'
            result = release.package(output)
            self.assertFalse(result['installed'])
            with zipfile.ZipFile(output) as archive:
                self.assertIsNone(archive.testzip())
                self.assertIn('hooks/hooks.json', archive.namelist())
                self.assertIn('skills/flow-aidd/assets/icon.svg', archive.namelist())
                self.assertNotIn('tools/release.py', archive.namelist())
                self.assertEqual([name for name in archive.namelist() if Path(name).name == 'plugin.json'],
                                 ['.codex-plugin/plugin.json'])
                self.assertFalse(any(name.startswith(('.git/', 'tools/', '.impeccable/')) for name in archive.namelist()))
                archive.extractall(root / 'paquet extrait')
            project = root / 'produit synthétique'
            project.mkdir()
            script = root / 'paquet extrait/skills/flow-aidd/scripts/project_flow.py'
            process = subprocess.run([sys.executable, '-B', str(script), 'init', '--project', str(project)],
                                     text=True, capture_output=True, check=True)
            self.assertTrue(json.loads(process.stdout)['created'])
            self.assertTrue((project / '.flow/suivi.md').is_file())

    def test_packaging_cannot_create_an_internal_distribution_or_overwrite_an_archive(self):
        with self.assertRaises(ValueError):
            release.package(ROOT / 'dist/flow-aidd.zip')
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'existing.zip'
            output.write_bytes(b'archive conservee')
            with self.assertRaises(FileExistsError):
                release.package(output)
            self.assertEqual(output.read_bytes(), b'archive conservee')


if __name__ == '__main__':
    unittest.main()
