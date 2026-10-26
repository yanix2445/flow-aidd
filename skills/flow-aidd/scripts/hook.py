"""Codex lifecycle adapter: existing flow projects only, no inferred decisions."""
import json
from pathlib import Path
import sys

import project_flow as flow


def project_for(cwd):
    path = Path(cwd).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / '.flow/etat.json').is_file():
            return candidate
        if (candidate / '.git').exists():
            break
    return None


def handle(payload):
    event = payload.get('hook_event_name')
    project = project_for(payload.get('cwd') or '.')
    if project is None:
        return {}
    report = flow.inspect(project)
    message = f'flow-aidd · {report.get("project")} · {report.get("current_sequence")} · {report.get("status")}.'
    if report.get('pending_transition'):
        message += ' Accord de passage encore attendu ; aucune nouvelle séquence autorisée par cette attente.'
    if report.get('errors'):
        message += ' À examiner : ' + ' '.join(report['errors'][:2])
    if event == 'SessionStart':
        return {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': message}}
    if event in ['PostToolUse', 'Stop', 'Interrupt']:
        flow.render(project)
    if event == 'PostToolUse' and report.get('errors'):
        return {'systemMessage': message}
    return {}


def main():
    try:
        payload = json.load(sys.stdin)
        print(json.dumps(handle(payload), ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        # Advisory adapter only: no continuation, approval, or silent initialization.
        print(json.dumps({'systemMessage': f'flow-aidd : suivi à vérifier ({error}).'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
