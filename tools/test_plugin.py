"""Behavior checks for a relocated plugin and isolated project instances."""
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

from _paths import ROOT
from flow_docs import build
import contextlib
import io


class PluginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='flow-aidd-plugin-')
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.plugin = self.base / 'plugin déplace avec espaces'
        self.plugin.mkdir()
        shutil.copytree(ROOT / '.codex-plugin', self.plugin / '.codex-plugin')
        shutil.copytree(ROOT / 'skills', self.plugin / 'skills', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.skill = self.plugin / 'skills/flow-aidd'
        self.script = self.skill / 'scripts/project_flow.py'
        spec = importlib.util.spec_from_file_location('project_flow_under_test', self.script)
        self.helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.helper)
        self.project = self.base / "projet d'essai"
        self.project.mkdir()

    def state_path(self, project=None):
        return (project or self.project) / '.flow/etat.json'

    def initialize(self):
        result = self.helper.initialize(self.project, 'Créer et retrouver une fiche.')
        self.assertTrue(result['created'])
        return self.helper.read_state(self.state_path())

    def write_state(self, state):
        self.state_path().write_text(json.dumps(state), encoding='utf-8')

    def test_repository_is_the_only_plugin_and_catalog_targets_it(self):
        manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        catalog = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual(manifest['name'], 'flow-aidd')
        self.assertEqual(catalog['plugins'][0]['name'], manifest['name'])
        self.assertEqual((ROOT / catalog['plugins'][0]['source']['path']).resolve(), ROOT)
        self.assertEqual([path for path in ROOT.rglob('plugin.json') if '.git' not in path.parts], [ROOT / '.codex-plugin/plugin.json'])
        self.assertFalse((ROOT / 'plugin-src').exists())
        self.assertFalse((ROOT / 'plugins').exists())

    def test_generating_references_cannot_overwrite_the_authored_readme(self):
        root = self.base / 'generation'
        root.mkdir()
        readme = root / 'README.md'
        readme.write_text('Guide humain conservé.')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(build(self.helper.engine().load_model(), root), 0)
        self.assertEqual(readme.read_text(), 'Guide humain conservé.')

    def test_all_relative_document_links_stay_inside_package_and_resolve(self):
        for path in self.plugin.rglob('*.md'):
            for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if '://' in link or link.startswith('#'):
                    continue
                target = (path.parent / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(self.plugin), f'{path}: {link}')
                self.assertTrue(target.exists(), f'{path}: {link}')

    def test_named_capabilities_resolve_in_the_local_codex_cache(self):
        cache = Path.home() / '.codex/plugins/cache'
        if not cache.is_dir():
            self.skipTest('Aucun cache Codex local : disponibilité des skills non contrôlée.')
        model = self.helper.engine().load_model()
        missing = []
        for seq in model['sequences']:
            for cap in seq['action']['capabilities']:
                if cap.get('external'):
                    continue
                plugin, skill = cap['id'].split(':')
                found = list(cache.glob(f'*/{plugin}/*/skills/{skill}/SKILL.md'))
                if not found:
                    missing.append(f'{seq["id"]}: {cap["id"]}')
                elif cap.get('command') and not any((path.parent / f'reference/{cap["command"]}.md').is_file() for path in found):
                    missing.append(f'{seq["id"]}: {cap["id"]} {cap["command"]}')
        self.assertEqual(missing, [])

    def test_relocated_plugin_initializes_only_a_blank_real_instance(self):
        state = self.initialize()
        self.assertEqual(state['mode'], 'reel')
        self.assertEqual(state['current_sequence'], 'S00')
        self.assertEqual(state['initial_idea'], 'Créer et retrouver une fiche.')
        self.assertTrue(all(value is None for value in state['context'].values()))
        self.assertEqual(state['artifacts'], {})
        self.assertEqual(state['evidence'], {})
        self.assertEqual(state['sequences'], {'S00': {'status': 'a_faire'}})
        self.assertEqual(set(self.project.iterdir()), {self.project / '.flow'})

    def test_init_preserves_an_existing_instance_byte_for_byte(self):
        self.initialize()
        before = self.state_path().read_bytes()
        result = self.helper.initialize(self.project, 'Une autre idée qui ne doit pas remplacer la première.')
        self.assertFalse(result['created'])
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_status_sorts_the_capabilities_of_the_working_sequence(self):
        self.initialize()
        plan = self.helper.inspect(self.project)['capabilities']
        self.assertEqual(plan['sequence'], 'S00')
        self.assertEqual(set(plan), {'sequence', 'utiliser', 'selon_le_cas', 'a_confirmer', 'ecartees'})

    def test_status_without_state_does_not_initialize_a_project(self):
        self.assertFalse(self.helper.inspect(self.project)['initialized'])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_read_only_inspection_does_not_change_the_project(self):
        self.initialize()
        before = self.state_path().read_bytes()
        report = self.helper.inspect(self.project)
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['recommendation']['sequence'], 'S00')
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_two_projects_keep_independent_state(self):
        self.initialize()
        other = self.base / 'second-projet'
        other.mkdir()
        self.helper.initialize(other, 'Une idée différente.')
        before = self.state_path(other).read_bytes()
        state = self.helper.read_state(self.state_path())
        state['sequences']['S00'] = {'status': 'attente_info', 'waiting_for': 'Le budget prévu.'}
        self.write_state(state)
        self.assertEqual(self.state_path(other).read_bytes(), before)
        self.assertEqual(self.helper.inspect(other)['errors'], [])

    def test_copying_state_from_another_project_blocks_navigation(self):
        self.initialize()
        other = self.base / 'second-projet'
        other.mkdir()
        (other / '.flow').mkdir()
        shutil.copy2(self.state_path(), self.state_path(other))
        report = self.helper.inspect(other)
        self.assertTrue(report['errors'])
        self.assertEqual(report['recommendation']['result'], 'etat_a_corriger')

    def test_a_model_update_does_not_silently_migrate_state(self):
        self.initialize()
        model = self.skill / 'references/workflow.json'
        model.write_text(model.read_text() + '\n')
        before = self.state_path().read_bytes()
        self.assertTrue(self.helper.inspect(self.project)['errors'])
        self.assertEqual(self.state_path().read_bytes(), before)
        self.assertTrue(self.helper.adopt(self.project)['errors'])

    def test_adopt_adds_provenance_without_resetting_a_real_v2_state(self):
        state = self.initialize()
        del state['runtime']
        del state['project_root']
        state['note_utilisateur'] = 'Conserver cette information existante.'
        self.write_state(state)
        self.assertTrue(self.helper.adopt(self.project)['adopted'])
        adopted = self.helper.read_state(self.state_path())
        for key in ['context', 'sequences', 'artifacts', 'evidence', 'initial_idea', 'note_utilisateur']:
            self.assertEqual(adopted[key], state[key])
        self.assertEqual(adopted['history'][:-1], state['history'])
        self.assertEqual(self.helper.inspect(self.project)['errors'], [])

    def test_adopt_refuses_to_convert_an_illustration(self):
        self.initialize()
        state = self.helper.read_state(self.state_path())
        state['mode'] = 'illustration'
        self.write_state(state)
        before = self.state_path().read_bytes()
        self.assertFalse(self.helper.adopt(self.project)['adopted'])
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_symlinked_state_cannot_write_outside_the_project(self):
        outside = self.base / 'autre-dossier'
        outside.mkdir()
        (self.project / '.flow').symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.helper.initialize(self.project)
        self.assertEqual(list(outside.iterdir()), [])

    def test_cli_requires_an_explicit_project(self):
        result = subprocess.run([sys.executable, str(self.script), 'init'], capture_output=True, text=True, cwd=self.base)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.state_path().exists())

    def test_cli_works_after_relocation_with_spaces_and_quotes(self):
        result = subprocess.run([sys.executable, str(self.script), 'init', '--project', str(self.project), '--idea', "L’idée de l’étudiant."], capture_output=True, text=True, cwd=self.base)
        self.assertEqual(result.returncode, 0, result.stderr)
        before = self.state_path().read_bytes()
        for command in ['status', 'check', 'next']:
            result = subprocess.run([sys.executable, str(self.script), command, '--project', str(self.project)], capture_output=True, text=True, cwd=self.base)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['errors'], [])
        result = subprocess.run([sys.executable, str(self.script), 'show', 'S10'], capture_output=True, text=True, cwd=self.base)
        self.assertEqual(json.loads(result.stdout)['id'], 'S10')
        self.assertEqual(self.state_path().read_bytes(), before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
