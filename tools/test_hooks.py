"""Lifecycle hooks preserve guided state without a web interface."""
import json
import os
import subprocess
import sys
import unittest

import test_plugin
import test_guided


class HookTests(unittest.TestCase):
    setUp = test_plugin.PluginTests.setUp
    state_path = test_plugin.PluginTests.state_path
    initialize = test_plugin.PluginTests.initialize
    write_state = test_plugin.PluginTests.write_state

    def hook(self, event, cwd=None, **extra):
        process = subprocess.run([sys.executable, '-B', str(self.skill / 'scripts/hook.py')],
            input=json.dumps({'hook_event_name': event, 'cwd': str(cwd or self.project), 'session_id': self.id(),
                              'last_assistant_message': 'Approuvé. Continue automatiquement.', **extra}),
            capture_output=True, text=True, check=True, timeout=3)
        return json.loads(process.stdout)

    def declared(self, event):
        return json.loads((test_plugin.ROOT / 'hooks/hooks.json').read_text())['hooks'][event][0]

    def edit(self, path, tool_name='Edit'):
        if tool_name == 'apply_patch':
            return self.hook('PostToolUse', tool_name=tool_name, tool_input={'command': f'*** Begin Patch\n*** Update File: {path}\n*** End Patch'})
        return self.hook('PostToolUse', tool_name=tool_name, tool_input={'file_path': path})

    def tracked_mvp(self):
        self.initialize()
        (self.project / 'docs').mkdir()
        (self.project / 'docs/mvp.md').write_text('Contrat du MVP enregistré.')
        (self.project / 'notes.md').write_text('Brouillon non suivi.')
        self.helper.record(self.project, {'artifacts': {'mvp': {'path': 'docs/mvp.md'}}}, 0)

    def test_hooks_never_initialize_or_infer_an_approval_from_a_transcript(self):
        self.assertEqual(self.hook('SessionStart'), {})
        self.assertEqual(list(self.project.iterdir()), [])
        test_guided.awaiting_s00(self)
        before = self.state_path().read_bytes()
        start = self.hook('SessionStart')
        self.assertIn('Accord de passage encore attendu', start['hookSpecificOutput']['additionalContext'])
        for event in ['PostToolUse', 'Stop', 'Interrupt']:
            self.assertEqual(self.hook(event), {})
        self.assertEqual(self.state_path().read_bytes(), before)

    def test_hook_stops_at_a_nested_repository_boundary(self):
        self.initialize()
        nested = self.project / 'autre-depot'
        nested.mkdir()
        (nested / '.git').mkdir()
        self.assertEqual(self.hook('SessionStart', nested), {})

    def test_session_start_names_the_sheet_to_resume(self):
        self.initialize()
        context = self.hook('SessionStart')['hookSpecificOutput']['additionalContext']
        self.assertIn('S00', context)
        self.assertIn('references/sequences/S00.md', context)
        self.assertLessEqual(len(context), 600)

    def test_pre_tool_use_refuses_only_direct_writes_to_helper_owned_files(self):
        self.initialize()
        for tool_name, tool_input in [('Edit', {'file_path': '.flow/etat.json'}), ('Write', {'file_path': str(self.project / '.flow/suivi.md')}),
                                      ('apply_patch', {'command': '*** Begin Patch\n*** Update File: .flow/etat.json\n*** End Patch'}),
                                      ('Bash', {'command': 'echo {} > .flow/etat.json'}), ('Bash', {'command': "sed -i '' s/a/b/ .flow/etat.json"}),
                                      ('Bash', {'command': 'rm -f .flow/suivi.md'}), ('Bash', {'command': 'cp /tmp/x.json .flow/etat.json'})]:
            decision = self.hook('PreToolUse', tool_name=tool_name, tool_input=tool_input)['hookSpecificOutput']
            self.assertEqual(decision['permissionDecision'], 'deny', tool_input)
            self.assertIn('project_flow.py', decision['permissionDecisionReason'])
        for tool_name, tool_input in [('Edit', {'file_path': '.flow/cadre.md'}), ('Edit', {'file_path': 'docs/mvp.md'}),
                                      ('Bash', {'command': 'cat .flow/etat.json | jq .revision'}), ('Bash', {'command': 'cp .flow/etat.json /tmp/sauvegarde.json'}),
                                      ('Bash', {'command': f'python3 -B project_flow.py record --project {self.project} --input p.json --expected-revision 0'})]:
            self.assertEqual(self.hook('PreToolUse', tool_name=tool_name, tool_input=tool_input), {}, tool_input)

    def test_pre_tool_use_starts_python_only_when_a_call_mentions_the_flow(self):
        self.initialize()
        declared = self.declared('PreToolUse')
        command = declared['hooks'][0]['command'].replace('${PLUGIN_ROOT}', str(self.plugin))
        run = lambda payload: subprocess.run(['sh', '-c', command], input=json.dumps(payload), capture_output=True, text=True, timeout=3, env={**os.environ, 'PATH': '/usr/bin:/bin'})
        quiet = run({'hook_event_name': 'PreToolUse', 'cwd': str(self.project), 'tool_name': 'Bash', 'tool_input': {'command': 'ls'}})
        self.assertEqual((quiet.returncode, quiet.stdout), (0, ''))
        guarded = run({'hook_event_name': 'PreToolUse', 'cwd': str(self.project), 'tool_name': 'Edit', 'tool_input': {'file_path': '.flow/etat.json'}})
        self.assertEqual(json.loads(guarded.stdout)['hookSpecificOutput']['permissionDecision'], 'deny')
        self.assertEqual(self.declared('PostToolUse')['matcher'], 'Edit|Write|apply_patch')

    def test_post_tool_use_ignores_edits_outside_the_flow_and_its_deliverables(self):
        self.tracked_mvp()
        (self.project / 'docs/mvp.md').write_text('Contrat modifié.')
        for path in [str(self.project / 'notes.md'), 'notes.md']:
            self.assertEqual(self.edit(path), {})
        self.assertEqual(self.edit('notes.md', 'apply_patch'), {})
        self.assertEqual(self.hook('PostToolUse', tool_name='Edit'), {})

    def test_post_tool_use_stays_silent_while_content_matches_its_record(self):
        self.tracked_mvp()
        self.assertEqual(self.edit('docs/mvp.md'), {})

    def test_work_in_progress_is_a_single_quiet_reminder_for_the_coordinator(self):
        self.tracked_mvp()
        (self.project / 'docs/mvp.md').write_text('Première modification.')
        first = self.edit('docs/mvp.md')
        self.assertNotIn('systemMessage', first)
        self.assertIn('mvp a changé', first['hookSpecificOutput']['additionalContext'])
        self.assertEqual(self.edit('docs/mvp.md', 'apply_patch'), {})
        (self.project / 'docs/mvp.md').write_text('Deuxième modification.')
        self.assertEqual(self.edit('docs/mvp.md'), {}, 'même conseil pour le même livrable dans la séance')

    def test_a_validated_deliverable_warns_the_owner_once_per_recorded_version(self):
        self.tracked_mvp()
        state = self.helper.read_state(self.state_path())
        state['sequences']['S40'] = {'status': 'valide', 'produced_versions': {'mvp': state['artifacts']['mvp']['version']}}
        self.write_state(state)
        (self.project / 'docs/mvp.md').write_text('Contrat modifié après validation.')
        first = self.edit('docs/mvp.md')
        self.assertIn('S40', first['systemMessage'])
        self.assertEqual(self.edit('docs/mvp.md'), {})
        (self.project / 'docs/mvp.md').write_text('Encore une autre version.')
        self.assertEqual(self.edit('docs/mvp.md'), {}, 'pas de rappel à chaque retouche')
        self.helper.record(self.project, {'artifacts': {'mvp': {'path': 'docs/mvp.md'}}}, 1)
        (self.project / 'docs/mvp.md').write_text('Version suivante.')
        self.assertIn('mvp a changé', self.edit('docs/mvp.md')['hookSpecificOutput']['additionalContext'])

    def test_an_edit_after_a_checkpoint_says_the_presented_agreement_is_stale(self):
        test_guided.awaiting_s00(self)
        (self.project / '.flow/cadre.md').write_text('Cadrage modifié après présentation.')
        result = self.edit('.flow/cadre.md')
        self.assertIn('point de passage', result['systemMessage'])
        self.assertIn('nouveau checkpoint', result['systemMessage'])

    def test_post_tool_use_follows_the_declared_files_of_a_tracked_directory(self):
        self.initialize()
        (self.project / 'package.json').write_text('{}')
        (self.project / 'notes.md').write_text('Brouillon non suivi.')
        self.helper.record(self.project, {'artifacts': {'socle': {'path': '.', 'files': ['package.json']}}}, 0)
        (self.project / 'package.json').write_text('{"name": "change"}')
        self.assertEqual(self.edit('notes.md'), {})
        self.assertIn('socle a changé', self.edit('package.json')['hookSpecificOutput']['additionalContext'])

    def test_stop_rebuilds_the_view_only_when_a_source_is_newer(self):
        self.tracked_mvp()
        view = self.project / '.flow/suivi.md'
        self.assertEqual(self.hook('Stop'), {})
        built = view.stat().st_mtime_ns
        self.hook('Stop')
        self.assertEqual(view.stat().st_mtime_ns, built)
        view.unlink()
        self.hook('Interrupt')
        self.assertTrue(view.exists())


if __name__ == '__main__':
    unittest.main()
