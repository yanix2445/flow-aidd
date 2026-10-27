"""Codex lifecycle adapter: existing flow projects only, no inferred decisions.

Each event does the least work that can change what the owner or the coordinator
needs to know. Only the helper-owned files are ever protected; everything else is
advice, given once per change instead of after every edit.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import time

PATCH_FILE = re.compile(r'^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$', re.MULTILINE)
OWNED = ('etat.json', 'suivi.md')
SHELL_WRITE = [
    re.compile(r'>>?\s*["\']?(?P<path>[^\s"\';&|]*\.flow/(?:etat\.json|suivi\.md))'),
    re.compile(r'\b(?:rm|mv|truncate|shred)\b[^;&|]*?(?P<path>[^\s"\';&|]*\.flow/(?:etat\.json|suivi\.md))'),
    re.compile(r'\b(?:sed|perl)\b[^;&|]*\s-i\S*[^;&|]*?(?P<path>[^\s"\';&|]*\.flow/(?:etat\.json|suivi\.md))'),
    re.compile(r'\b(?:cp|tee|install)\b[^;&|]*\s["\']?(?P<path>[^\s"\';&|]*\.flow/(?:etat\.json|suivi\.md))["\']?\s*(?:$|[;&|])'),
]
REMEMBER_SECONDS = 12 * 3600


def project_for(cwd):
    path = Path(cwd).resolve()
    for candidate in [path, *path.parents]:
        if (candidate / '.flow/etat.json').is_file():
            return candidate
        if (candidate / '.git').exists():
            break
    return None


def edited_paths(payload, cwd):
    tool_input = payload.get('tool_input')
    if not isinstance(tool_input, dict):
        return None
    raw = [tool_input.get(key) for key in ['file_path', 'path', 'notebook_path']]
    for key in ['patch', 'input', 'command']:
        text = tool_input.get(key)
        text = '\n'.join(map(str, text)) if isinstance(text, list) else text
        if isinstance(text, str):
            raw += [added or moved for added, moved in PATCH_FILE.findall(text)]
    paths = [Path(cwd, item.strip()).resolve() for item in raw if isinstance(item, str) and item.strip()]
    return paths or None


def owned_by_helper(project, path):
    return path.parent == project / '.flow' and path.name in OWNED


def read_state(project):
    return json.loads((project / '.flow/etat.json').read_text(encoding='utf-8'))


def tracked_artifacts(project, state):
    """Map each local deliverable key to the paths whose edition changes its version."""
    tracked = {}
    for key, item in (state.get('artifacts') or {}).items():
        raw = str(item.get('path', ''))
        if not raw or '://' in raw:
            continue
        base = Path(project, raw).resolve()
        files = item.get('files')
        tracked[key] = [(base / name).resolve() for name in files] if isinstance(files, list) and files else [base]
    return tracked


def memory(payload, project):
    """Per-session record of advice already given, kept outside the product."""
    session = str(payload.get('session_id') or 'session')
    name = hashlib.sha256(f'{project}\0{session}'.encode()).hexdigest()[:24]
    return Path(tempfile.gettempdir()) / 'flow-aidd-hooks' / f'{name}.json'


def first_time(payload, project, signature):
    path = memory(payload, project)
    try:
        seen = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        seen = {}
    now = time.time()
    seen = {key: at for key, at in seen.items() if now - at < REMEMBER_SECONDS}
    if signature in seen:
        return False
    seen[signature] = now
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(seen), encoding='utf-8')
    except OSError:
        pass
    return True


def deny(reason):
    return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'permissionDecision': 'deny', 'permissionDecisionReason': reason}}


def helper_command(project):
    script = Path(__file__).resolve().parent / 'project_flow.py'
    return f'python3 -B "{script}" record --project "{project}" --input FICHIER_JSON --expected-revision REVISION_LUE'


def pre_tool_use(payload, project, cwd):
    """Refuse only a direct write to the helper-owned files; every other call passes untouched."""
    if payload.get('tool_name') == 'Bash':
        command = str((payload.get('tool_input') or {}).get('command', ''))
        if 'project_flow.py' in command:
            return {}
        targets = [Path(cwd, match.group('path')).resolve() for pattern in SHELL_WRITE for match in pattern.finditer(command)]
    else:
        targets = edited_paths(payload, cwd) or []
    touched = sorted({path.name for path in targets if owned_by_helper(project, path)})
    if not touched:
        return {}
    return deny(
        f'flow-aidd : {", ".join(touched)} est tenu par le helper, pas par une édition directe. '
        f'Pour enregistrer un résultat : {helper_command(project)}. '
        'suivi.md se régénère seul ; check et status lisent l’état sans le modifier.')


def post_tool_use(payload, project, cwd):
    """Advise once per recorded version, with a weight that matches what the change puts at risk."""
    paths = edited_paths(payload, cwd)
    if paths is None:
        return {}
    if any(owned_by_helper(project, path) for path in paths):
        return {'systemMessage': 'flow-aidd : le suivi a été modifié hors du helper ; lancer check avant de continuer.'}
    try:
        state = read_state(project)
    except (OSError, ValueError):
        return {'systemMessage': 'flow-aidd : etat.json est illisible ; lancer check avant de continuer.'}
    keys = [key for key, files in tracked_artifacts(project, state).items()
            if any(path == item or path.is_relative_to(item) for path in paths for item in files)]
    if not keys:
        return {}
    import project_flow as flow
    root = project.resolve()
    changed = []
    for key in keys:
        artifact = state['artifacts'][key]
        try:
            actual = flow.content_hash(root, artifact)
        except (OSError, flow.FlowError):
            actual = 'absent'
        if actual != artifact.get('content_sha256'):
            changed.append((key, artifact.get('content_sha256')))
    if not changed:
        return {}
    pending = state.get('pending_transition')
    sequences = state.get('sequences') or {}
    user, model = [], []
    for key, baseline in changed:
        validated = sorted(sid for sid, record in sequences.items() if record.get('status') == 'valide'
                           and key in {**(record.get('used_versions') or {}), **(record.get('produced_versions') or {})})
        if pending:
            kind = 'checkpoint'
            text = (f'{key} a changé depuis le point de passage {pending.get("id")} '
                    f'({state.get("current_sequence")} → {pending.get("target")}) : l’accord présenté ne peut plus s’appliquer. '
                    'Après les modifications, enregistrer avec record puis présenter un nouveau checkpoint.')
            user.append(text)
        elif validated:
            kind = 'validation'
            text = (f'{key} a changé alors que {", ".join(validated)} l’ont validé : '
                    'enregistrer la nouvelle version avec record, puis réexaminer ces validations.')
            user.append(text)
        else:
            kind = 'travail'
            text = f'{key} a changé : l’enregistrer avec record avant le prochain checkpoint.'
        # One notice per deliverable and recorded version: iterative edits are not nagged again.
        if first_time(payload, project, f'{kind}:{key}:{baseline}'):
            model.append(text)
        elif text in user:
            user.remove(text)
    if not model:
        return {}
    result = {'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': 'flow-aidd · ' + ' '.join(model)}}
    if user:
        result['systemMessage'] = 'flow-aidd · ' + ' '.join(user)
    return result


def view_is_current(project):
    view = project / '.flow/suivi.md'
    try:
        built = view.stat().st_mtime
        state = read_state(project)
        sources = [project / '.flow/etat.json'] + [path for files in tracked_artifacts(project, state).values() for path in files]
        return all(not path.exists() or path.stat().st_mtime <= built for path in sources)
    except (OSError, ValueError):
        return False


def session_start(project):
    import project_flow as flow
    report = flow.inspect(project)
    current = report.get('current_sequence')
    parts = [f'flow-aidd · {report.get("project")} · {current} {report.get("title") or ""}'.rstrip() + f' · {report.get("status")}.']
    pending = report.get('pending_transition')
    if pending:
        parts.append(f'Accord de passage encore attendu sur {pending.get("id")} ({current} → {pending.get("target")}) ; '
                     'aucune nouvelle séquence autorisée par cette attente.')
        if report.get('checkpoint_stale'):
            parts.append('Ce point est périmé : refaire record puis checkpoint avant de le présenter.')
    elif report.get('waiting_for'):
        parts.append(f'Attente : {report["waiting_for"]}')
    if report.get('errors'):
        parts.append('À examiner avec check : ' + ' '.join(report['errors'][:2]))
    elif not pending and current:
        parts.append(f'Reprendre avec la fiche references/sequences/{current}.md.')
    return {'hookSpecificOutput': {'hookEventName': 'SessionStart', 'additionalContext': ' '.join(parts)[:600]}}


def handle(payload):
    event = payload.get('hook_event_name')
    cwd = payload.get('cwd') or '.'
    project = project_for(cwd)
    if project is None:
        return {}
    if event == 'SessionStart':
        return session_start(project)
    if event == 'PreToolUse':
        return pre_tool_use(payload, project, cwd)
    if event == 'PostToolUse':
        return post_tool_use(payload, project, cwd)
    if event in ['Stop', 'Interrupt'] and not view_is_current(project):
        import project_flow as flow
        flow.render(project)
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
