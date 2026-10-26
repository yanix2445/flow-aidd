"""Lifecycle hooks preserve guided state without a web interface."""
import json
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

    def hook(self, event, cwd=None):
        process = subprocess.run([sys.executable, '-B', str(self.skill / 'scripts/hook.py')],
            input=json.dumps({'hook_event_name': event, 'cwd': str(cwd or self.project),
                              'last_assistant_message': 'Approuvé. Continue automatiquement.'}),
            capture_output=True, text=True, check=True, timeout=3)
        return json.loads(process.stdout)

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


if __name__ == '__main__':
    unittest.main()
