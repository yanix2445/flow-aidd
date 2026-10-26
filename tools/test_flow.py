"""Semantic checks for routing, evidence freshness, applicability and resumption."""
from copy import deepcopy
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
import re
import subprocess
import sys

from _paths import ROOT, MODEL_ROOT, SKILL_ROOT
import flow
from flow_docs import build, documents, example_state


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.model = flow.load_model()
        self.state = example_state(self.model)

    def test_model_contracts_are_complete(self):
        self.assertEqual(flow.model_errors(self.model), [])

    def test_unknown_route_is_rejected(self):
        self.model['sequences'][0]['next']['valide'] = 'S9999'
        self.assertTrue(any('destination' in message for message in flow.model_errors(self.model)))

    def test_generated_document_links_have_targets(self):
        generated = documents(self.model)
        for name, content in generated.items():
            if not name.endswith('.md'):
                continue
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
                if '://' in target or target.startswith('#'):
                    continue
                relative = os.path.normpath(str(Path(name).parent / target.split('#')[0]))
                self.assertTrue(relative in generated or (flow.ROOT / relative).exists(), f'{name}: {target}')

    def test_dependency_cycle_is_rejected(self):
        self.model['sequences'][0]['requires'] = ['S10']
        self.assertTrue(any('Cycle' in message for message in flow.model_errors(self.model)))

    def test_sdlc_prefix_is_explicit(self):
        invocation = next(seq for seq in self.model['sequences'] if seq['id'] == 'S90')['action']['invocation']
        self.assertEqual(invocation['template'].split()[0], 'interactive')
        invocation['template'] = 'Utilise le mode interactif'
        self.assertTrue(any('SDLC' in message for message in flow.model_errors(self.model)))

    def test_complete_example_is_coherent_but_only_illustrative(self):
        self.assertEqual(self.state['mode'], 'illustration')
        self.assertTrue(all(proof['simulated'] for proof in self.state['evidence'].values()))
        self.assertEqual(flow.state_errors(self.model, self.state), [])
        self.assertEqual(flow.recommend(self.model, self.state)['result'], 'END')

    def test_empty_instance_starts_at_scope(self):
        state = json.loads(documents(self.model)['templates/etat.json'])
        self.assertEqual(flow.state_errors(self.model, state), [])
        self.assertEqual(flow.recommend(self.model, state)['sequence'], 'S00')
        self.assertFalse(flow.satisfied(self.model, state, 'S00'))

    def test_code_failure_stays_in_delivery(self):
        self.state['current_sequence'] = 'S90'
        self.state['sequences']['S90'] = {'status':'a_reprendre','outcome':'reparer'}
        result = flow.recommend(self.model, self.state)
        self.assertEqual(result['sequence'], 'S90')
        self.assertNotEqual(result.get('sequence'), 'S80')

    def test_ideation_can_start_with_future_unknowns(self):
        for field in self.state['context']:
            self.state['context'][field] = None
        self.state['current_sequence'] = 'S00'
        self.state['sequences']['S10'] = {'status':'a_faire'}
        self.assertTrue(flow.satisfied(self.model, self.state, 'S00'))
        self.assertEqual(flow.recommend(self.model, self.state)['sequence'], 'S10')

    def test_a_late_required_context_is_not_silently_omitted(self):
        self.state['context']['integration_owner'] = None
        self.assertFalse(flow.satisfied(self.model, self.state, 'S91'))

    def test_incomplete_observation_window_waits(self):
        self.state['current_sequence'] = 'S120'
        self.state['sequences']['S120'] = {'status':'attente_info','outcome':'attendre_information','waiting_for':'Fin de la fenêtre prévue.'}
        self.assertEqual(flow.recommend(self.model, self.state)['result'], 'attente_info')

    def test_missing_access_waits_at_the_delivery_sequence(self):
        self.state['current_sequence'] = 'S111'
        self.state['sequences']['S111'] = {'status':'attente_acces','waiting_for':'Accès réel à l’hébergeur.'}
        result = flow.recommend(self.model, self.state)
        self.assertEqual(result['result'], 'attente_acces')
        self.assertEqual(result['sequence'], 'S111')

    def test_changed_scope_marks_dependents_not_earlier_intent(self):
        self.state['artifacts']['mvp']['version'] = 'illustration-v2'
        self.assertFalse(flow.satisfied(self.model, self.state, 'S50'))
        self.assertFalse(flow.satisfied(self.model, self.state, 'S90'))
        self.assertTrue(flow.satisfied(self.model, self.state, 'S10'))

    def test_no_gui_has_traceable_non_applicability(self):
        self.model['example']['context']['has_graphical_ui'] = False
        state = example_state(self.model)
        for sid in ['S50', 'S51']:
            self.assertEqual(state['sequences'][sid]['status'], 'non_applicable')
            self.assertTrue(flow.satisfied(self.model, state, sid))
        self.assertNotIn('prototype', state['artifacts'])

    def test_required_sequence_cannot_be_skipped(self):
        self.state['sequences']['S40'] = {'status':'non_applicable','reason':'Plus simple','context_ref':'S00:cadre_decide','context_version':'illustration-v1'}
        self.assertFalse(flow.satisfied(self.model, self.state, 'S40'))

    def test_unknown_condition_is_not_false(self):
        self.state['context']['critical_technical_risk'] = None
        self.assertFalse(flow.satisfied(self.model, self.state, 'S60'))

    def test_simulation_cannot_validate_a_real_instance_or_advance_it(self):
        self.state['mode'] = 'reel'
        self.assertTrue(flow.state_errors(self.model, self.state))
        self.assertFalse(flow.satisfied(self.model, self.state, 'S121'))
        self.assertNotEqual(flow.recommend(self.model, self.state)['result'], 'END')

    def test_evidence_revision_must_match_the_artifact(self):
        self.state['evidence']['S90:controles_candidat']['version'] = 'ancienne-revision'
        self.assertFalse(flow.satisfied(self.model, self.state, 'S90'))

    def test_draft_pr_is_not_an_integrated_candidate(self):
        self.state['current_sequence'] = 'S100'
        self.state['sequences']['S91'] = {'status':'a_faire'}
        self.state['sequences']['S100'] = {'status':'a_faire'}
        self.assertEqual(flow.recommend(self.model, self.state)['sequence'], 'S91')

    def test_another_slice_requires_a_recorded_new_iteration(self):
        self.state['current_sequence'] = 'S91'
        self.state['sequences']['S91']['outcome'] = 'autre_tranche'
        result = flow.recommend(self.model, self.state)
        self.assertEqual(result['result'], 'reouverture_a_consigner')
        self.assertEqual(result['sequence'], 'S80')

    def test_reviewer_must_differ_from_implementer(self):
        self.state['evidence']['S90:revue_independante']['actor'] = self.state['sequences']['S90']['performed_by']
        self.assertFalse(flow.satisfied(self.model, self.state, 'S90'))

    def test_undated_approval_is_not_valid(self):
        self.state['sequences']['S40']['validated_at'] = ''
        self.assertFalse(flow.satisfied(self.model, self.state, 'S40'))

    def test_spike_resumption_is_not_invented(self):
        self.model['example']['context']['critical_technical_risk'] = True
        state = example_state(self.model)
        state['current_sequence'] = 'S60'
        self.assertEqual(flow.recommend(self.model, state)['result'], 'destination_de_reprise_a_preciser')
        state['resume_sequence'] = 'S10'
        state['sequences']['S10'] = {'status':'a_faire'}
        self.assertEqual(flow.recommend(self.model, state)['sequence'], 'S10')

    def test_new_optional_source_is_not_a_silent_past_input(self):
        record = self.state['sequences']['S80']
        record['used_versions'].pop('prototype')
        self.assertTrue(flow.satisfied(self.model, self.state, 'S80'))

    def test_generated_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            root = Path(folder)
            self.assertEqual(build(self.model, root), 0)
            self.assertEqual(build(self.model, root, check=True), 0)
            (root / 'sequences/S40.md').write_text('Divergence manuelle')
            self.assertEqual(build(self.model, root, check=True), 1)

    def test_current_generated_tree_matches_the_single_source(self):
        for name, expected in documents(self.model).items():
            self.assertEqual((flow.ROOT / name).read_text(), expected, name)

    def test_read_only_cli_contracts(self):
        state = str(flow.ROOT / 'examples/minirevisions.etat.json')
        check = subprocess.run([sys.executable, str(SKILL_ROOT/'scripts/flow.py'), 'check', '--state', state], capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(check.stdout)['coherent'])
        next_result = subprocess.run([sys.executable, str(SKILL_ROOT/'scripts/flow.py'), 'next', '--state', state], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(next_result.stdout)['recommendation']['result'], 'END')

    def test_model_has_only_one_authoritative_copy(self):
        models = [path for path in ROOT.rglob('workflow.json') if '.git' not in path.parts]
        self.assertEqual(models, [MODEL_ROOT / 'workflow.json'])
        self.assertEqual(flow.ROOT, MODEL_ROOT)


if __name__ == '__main__':
    unittest.main(verbosity=2)
