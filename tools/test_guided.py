"""Guided passage invariants exercised in isolated, synthetic project fixtures."""
from concurrent.futures import ThreadPoolExecutor
import json
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_plugin


def ready_s00(case):
    case.initialize()
    cadre = case.project / '.flow/cadre.md'
    cadre.write_text('Cadrage synthétique de test, sans validation produit réelle.')
    patch = {
        'actors': {'porteur': 'TestOwner', 'coordinateur': 'TestCodex'},
        'artifacts': {'cadre': {'path': '.flow/cadre.md', 'version': 'test-v1'}},
        'evidence': {'decision-test': {'sequence': 'S00', 'criterion': 'cadre_decide', 'kind': 'decision',
            'actor': 'TestOwner', 'artifact': 'cadre', 'version': 'test-v1', 'reference': 'unit-test:decision',
            'result': 'approved', 'simulated': False}},
        'sequences': {'S00': {'status': 'valide', 'outcome': 'valide', 'used_versions': {},
            'produced_versions': {'cadre': 'test-v1'}, 'validator_role': 'porteur', 'validated_by': 'TestOwner',
            'validated_at': case.helper.now(), 'performed_by': 'TestCodex', 'evidence_ids': ['decision-test']}},
    }
    case.helper.record(case.project, patch, 0)
    return case.helper.inspect(case.project)


def awaiting_s00(case):
    ready_s00(case)
    return case.helper.checkpoint(case.project, 'Résultat de test présenté avant S10.', 1)['checkpoint']


class GuidedTests(unittest.TestCase):
    setUp = test_plugin.PluginTests.setUp
    state_path = test_plugin.PluginTests.state_path
    initialize = test_plugin.PluginTests.initialize
    write_state = test_plugin.PluginTests.write_state

    def test_initialization_is_guided_and_generates_a_readable_view(self):
        state = self.initialize()
        self.assertEqual(state['execution_mode'], 'guide')
        self.assertEqual(state['revision'], 0)
        self.assertIsNone(state['pending_transition'])
        view = (self.project / '.flow/suivi.md').read_text()
        self.assertIn('S00', view)
        self.assertIn('a_faire', view)
        self.assertEqual(state['evidence'], {})

    def test_finishing_a_contract_does_not_advance(self):
        report = ready_s00(self)
        self.assertEqual(report['current_sequence'], 'S00')
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['recommendation']['sequence'], 'S10')

    def test_checkpoint_survives_a_new_process_without_advancing(self):
        checkpoint = awaiting_s00(self)
        result = subprocess.run([sys.executable, str(self.script), 'next', '--project', str(self.project)], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report['pending_transition']['id'], checkpoint['id'])
        self.assertEqual(report['current_sequence'], 'S00')
        self.assertEqual(report['recommendation']['result'], 'attente_validation')

    def test_checkpoint_cannot_validate_missing_work(self):
        self.initialize()
        before = self.state_path().read_bytes()
        with self.assertRaises(ValueError):
            self.helper.checkpoint(self.project, 'Incomplet', 0)
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_approval_is_bound_to_the_checkpoint_owner_and_revision(self):
        checkpoint = awaiting_s00(self)
        before = self.state_path().read_bytes()
        for cid, actor, revision in [('inconnu', 'TestOwner', 2), (checkpoint['id'], 'TestCodex', 2), (checkpoint['id'], 'TestOwner', 1)]:
            with self.assertRaises(ValueError):
                self.helper.decision(self.project, 'approve', cid, actor, 'unit-test:accord', revision)
        self.assertEqual(self.state_path().read_bytes(), before)
        report = self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:accord', 2)
        self.assertEqual(report['current_sequence'], 'S10')
        state = self.helper.read_state(self.state_path())
        self.assertIsNone(state['pending_transition'])
        self.assertEqual(state['history'][-1]['reference'], 'unit-test:accord')

    def test_a_file_change_blocks_an_old_approval(self):
        checkpoint = awaiting_s00(self)
        (self.project / '.flow/cadre.md').write_text('Résultat changé après présentation.')
        before = self.state_path().read_bytes()
        with self.assertRaises(ValueError):
            self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:accord', 2)
        self.assertEqual(self.state_path().read_bytes(), before)
        self.assertTrue(self.helper.inspect(self.project)['checkpoint_stale'])

    def test_changed_content_cannot_reuse_a_version_label(self):
        ready_s00(self)
        (self.project / '.flow/cadre.md').write_text('Nouveau contenu.')
        with self.assertRaises(ValueError):
            self.helper.record(self.project, {'artifacts': {'cadre': {'path': '.flow/cadre.md', 'version': 'test-v1'}}}, 1)
        self.assertEqual(self.helper.read_state(self.state_path())['revision'], 1)

    def test_refreshing_a_source_invalidates_its_old_proof_and_checkpoint(self):
        checkpoint = awaiting_s00(self)
        (self.project / '.flow/cadre.md').write_text('Nouvelle version.')
        self.helper.record(self.project, {'artifacts': {'cadre': {'path': '.flow/cadre.md'}}}, 2)
        state = self.helper.read_state(self.state_path())
        self.assertIsNone(state['pending_transition'])
        self.assertEqual(state['sequences']['S00']['status'], 'a_reprendre')
        self.assertTrue(state['artifacts']['cadre']['version'].startswith('sha256:'))
        self.assertTrue(any(item.get('checkpoint') == checkpoint['id'] for item in state['history']))

    def test_correction_preserves_the_current_sequence_and_feedback(self):
        checkpoint = awaiting_s00(self)
        self.helper.decision(self.project, 'correct', checkpoint['id'], 'TestOwner', 'unit-test:correction', 2, 'Préciser les moyens.')
        state = self.helper.read_state(self.state_path())
        self.assertEqual(state['current_sequence'], 'S00')
        self.assertEqual(state['sequences']['S00']['status'], 'a_reprendre')
        self.assertEqual(state['history'][-1]['reason'], 'Préciser les moyens.')

    def test_waiting_preserves_the_checkpoint_and_can_resume(self):
        checkpoint = awaiting_s00(self)
        self.helper.decision(self.project, 'pause', checkpoint['id'], 'TestOwner', 'unit-test:pause', 2, 'Relecture demain.')
        self.assertEqual(self.helper.inspect(self.project)['waiting_for'], 'Relecture demain.')
        self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:reprise', 3)
        self.assertEqual(self.helper.inspect(self.project)['current_sequence'], 'S10')

    def test_record_cannot_change_navigation_or_unknown_types(self):
        self.initialize()
        for patch in [{'current_sequence': 'S90'}, {'execution_mode': 'auto'}, {'actors': {'porteur': 7}},
                      {'context': {'public_users': 'false'}}, {'sequences': {'S00': {'status': 'inconnu'}}}]:
            with self.assertRaises(ValueError):
                self.helper.record(self.project, patch, 0)
        self.assertEqual(self.helper.read_state(self.state_path())['revision'], 0)

    def test_record_cannot_skip_to_another_validated_sequence(self):
        self.initialize()
        with self.assertRaises(ValueError):
            self.helper.record(self.project, {'sequences': {'S90': {'status': 'valide'}}}, 0)

    def test_a_directory_can_track_a_declared_file_manifest(self):
        self.initialize()
        (self.project / 'package.json').write_text('{"name":"fixture"}')
        self.helper.record(self.project, {'artifacts': {'socle': {'path': '.', 'files': ['package.json']}}}, 0)
        self.assertEqual(self.helper.inspect(self.project)['errors'], [])
        (self.project / 'package.json').write_text('{"name":"modifie"}')
        self.assertTrue(self.helper.inspect(self.project)['errors'])

    def test_a_relocation_is_explicit_and_preserves_project_identity(self):
        ready_s00(self)
        state = self.helper.read_state(self.state_path())
        other = self.base / 'copie explicite'
        shutil.copytree(self.project, other)
        self.assertTrue(self.helper.inspect(other)['errors'])
        self.helper.relocate(other, 'unit-test:clone-confirme', 1)
        moved = self.helper.inspect(other)
        self.assertEqual(moved['errors'], [])
        self.assertEqual(moved['project_id'], state['project_id'])
        self.assertEqual(moved['current_sequence'], 'S00')

    def test_model_migration_invalidates_only_affected_contracts(self):
        awaiting_s00(self)
        path = self.skill / 'references/workflow.json'
        model = json.loads(path.read_text())
        model['sequences'][1]['title'] = 'Contrat S10 modifié pour le test'
        path.write_text(json.dumps(model))
        plan = self.helper.migration_plan(self.project)
        self.assertTrue(plan['required'])
        self.assertIn('S10', plan['changed_sequences'])
        self.assertNotIn('S00', plan['changed_sequences'])
        self.helper.migrate(self.project, 'unit-test:migration-examinee', 2)
        state = self.helper.read_state(self.state_path())
        self.assertIsNone(state['pending_transition'])
        self.assertEqual(state['sequences']['S00']['status'], 'valide')
        self.assertEqual(self.helper.inspect(self.project)['errors'], [])
        self.assertTrue(any(item['event'] == 'model_before_migration' for item in state['history']))

    def test_major_model_change_is_not_automatically_migrated(self):
        self.initialize()
        path = self.skill / 'references/workflow.json'
        model = json.loads(path.read_text())
        model['version'] = '3.0'
        path.write_text(json.dumps(model))
        before = self.state_path().read_bytes()
        with self.assertRaises(ValueError):
            self.helper.migrate(self.project, 'unit-test:major', 0)
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_two_tabs_cannot_approve_the_same_checkpoint_twice(self):
        checkpoint = awaiting_s00(self)
        def approve(_):
            try:
                self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:tab', 2)
                return True
            except ValueError:
                return False
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(approve, range(2)))
        self.assertEqual(results.count(True), 1)
        state = self.helper.read_state(self.state_path())
        self.assertEqual(sum(item['event'] == 'passage_approve' for item in state['history']), 1)

    def test_a_native_end_signal_finishes_once_without_losing_the_last_sequence(self):
        # The native END routing is checked in test_flow; isolate the guided bridge here.
        state = self.initialize()
        state.update(current_sequence='S121', actors={'porteur': 'TestOwner'},
                     sequences={'S121': {'status': 'valide'}})
        self.write_state(state)
        runtime = self.helper.engine()
        with patch.object(self.helper, 'engine', return_value=runtime), \
             patch.object(runtime, 'state_errors', return_value=[]), \
             patch.object(runtime, 'satisfied', return_value=True), \
             patch.object(runtime, 'recommend', return_value={'result': 'END', 'sequence': 'S121'}):
            checkpoint = self.helper.checkpoint(self.project, 'Fin synthétique de test.', 0)['checkpoint']
            self.assertEqual(checkpoint['target'], 'END')
            result = self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:fin', 1)
            self.assertTrue(result['completed'])
            self.assertEqual(result['current_sequence'], 'S121')
            with self.assertRaises(ValueError):
                self.helper.checkpoint(self.project, 'Fin déjà confirmée.', 2)

    def test_reopening_a_slice_preserves_its_previous_validation_in_history(self):
        state = self.initialize()
        state.update(current_sequence='S91', actors={'porteur': 'TestOwner'},
                     sequences={sid: {'status': 'valide', 'test_iteration': 'ancienne'}
                                for sid in ['S80', 'S90', 'S91']})
        self.write_state(state)
        runtime = self.helper.engine()
        with patch.object(self.helper, 'engine', return_value=runtime), \
             patch.object(runtime, 'state_errors', return_value=[]), \
             patch.object(runtime, 'satisfied', return_value=True), \
             patch.object(runtime, 'recommend', return_value={'result': 'reouverture_a_consigner', 'sequence': 'S80'}):
            checkpoint = self.helper.checkpoint(self.project, 'Autre tranche synthétique.', 0)['checkpoint']
            self.helper.decision(self.project, 'approve', checkpoint['id'], 'TestOwner', 'unit-test:iteration', 1)
        state = self.helper.read_state(self.state_path())
        self.assertEqual(state['current_sequence'], 'S80')
        self.assertEqual(state['sequences']['S80']['status'], 'a_reprendre')
        previous = next(item['snapshot'] for item in state['history'] if item['event'] == 'iteration_archived')
        self.assertEqual(previous['sequences']['S80']['test_iteration'], 'ancienne')

    def test_an_existing_lock_is_not_stolen_or_removed(self):
        self.initialize()
        lock = self.project / '.flow/.lock'
        lock.write_text('Autre écriture en cours.')
        with self.assertRaises(ValueError):
            self.helper.record(self.project, {'actors': {'porteur': 'TestOwner'}}, 0)
        self.assertTrue(lock.exists())

    def test_summary_regeneration_cannot_change_the_state(self):
        awaiting_s00(self)
        before = self.state_path().read_bytes()
        (self.project / '.flow/suivi.md').write_text('Ancienne vue.')
        self.helper.render(self.project)
        self.assertEqual(self.state_path().read_bytes(), before)
        self.assertIn('Accord attendu', (self.project / '.flow/suivi.md').read_text())


if __name__ == '__main__':
    unittest.main(verbosity=2)
