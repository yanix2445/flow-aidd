"""Project state, guided checkpoints and readable views for flow-aidd (stdlib only)."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

SKILL_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = SKILL_ROOT / 'references'
STATE_SCHEMA = 1


class FlowError(ValueError):
    pass


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def engine():
    spec = importlib.util.spec_from_file_location('flow_aidd_runtime', SKILL_ROOT / 'scripts' / 'flow.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def provenance():
    model = engine().load_model()
    return {
        'plugin': 'flow-aidd',
        'model_sha256': hashlib.sha256((MODEL_ROOT / 'workflow.json').read_bytes()).hexdigest(),
        'sequence_hashes': {seq['id']: digest(seq) for seq in model['sequences']},
        'policy_sha256': digest({key: model[key] for key in ['policies', 'context_fields', 'roles', 'contract']}),
    }


def state_path(project):
    root = Path(project).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise FlowError('Le dossier produit doit exister.')
    target = root / '.flow' / 'etat.json'
    if target.parent.is_symlink() or target.is_symlink() or not target.resolve().is_relative_to(root):
        raise FlowError('L’état doit rester dans le dossier réel du projet, sans lien symbolique.')
    return root, target


def read_state(target):
    state = json.loads(target.read_text(encoding='utf-8'))
    if not isinstance(state, dict):
        raise FlowError('Le fichier d’état doit être un objet JSON.')
    return state


def binding_errors(state, root, model):
    errors = []
    if state.get('mode') != 'reel':
        errors.append('Un cas illustratif ne pilote pas un projet réel.')
    if state.get('flow_version') != model['version']:
        errors.append('Version du modèle différente : examiner migration-plan avant migrate.')
    runtime = state.get('runtime') or {}
    if not runtime:
        errors.append('État non rattaché : examiner sa provenance avant adopt.')
    elif runtime.get('plugin') != 'flow-aidd' or runtime.get('model_sha256') != provenance()['model_sha256']:
        errors.append('Empreinte du modèle différente : examiner migration-plan.')
    if state.get('project_root') != str(root):
        errors.append('Dossier différent : vérifier l’instance avant relocate.')
    if state.get('state_schema') != STATE_SCHEMA or state.get('execution_mode') != 'guide':
        errors.append('État sans protocole guidé actuel : examiner adopt.')
    return errors


def local_artifact(root, artifact):
    raw = str(artifact.get('path', ''))
    if '://' in raw:
        if not raw.startswith('https://'):
            raise FlowError('Une référence distante doit utiliser HTTPS.')
        return None
    if not raw:
        raise FlowError('Emplacement de livrable manquant.')
    path = Path(raw).expanduser()
    path = path if path.is_absolute() else root / path
    path = path.resolve()
    if not path.is_relative_to(root):
        raise FlowError('Le fichier du livrable doit rester dans le projet.')
    return path


def content_hash(root, artifact):
    path = local_artifact(root, artifact)
    if path is None:
        return None
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if path.is_dir() and isinstance(artifact.get('files'), list) and artifact['files']:
        contents = {}
        for name in artifact['files']:
            file = (path / name).resolve()
            if not file.is_relative_to(path) or not file.is_file():
                raise FlowError('Un dossier nécessite une liste de fichiers existants contenus dans ce dossier.')
            contents[file.relative_to(path).as_posix()] = hashlib.sha256(file.read_bytes()).hexdigest()
        return digest(contents)
    raise FlowError('Fichier absent, ou dossier sans liste explicite de fichiers à vérifier.')


def freshness_errors(state, root):
    errors = []
    for key, artifact in state.get('artifacts', {}).items():
        try:
            path = local_artifact(root, artifact)
            if path is None:
                continue
            actual = content_hash(root, artifact)
            if not artifact.get('content_sha256'):
                errors.append(f'{key}: empreinte locale absente ; enregistrer le livrable avec record.')
            elif actual != artifact['content_sha256']:
                errors.append(f'{key}: contenu modifié depuis son enregistrement.')
        except (OSError, FlowError) as error:
            errors.append(f'{key}: {error}')
    return errors


def fingerprint(state):
    return digest({key: state.get(key) for key in [
        'runtime', 'context', 'actors', 'artifacts', 'evidence', 'sequences',
        'current_sequence', 'resume_sequence', 'execution_mode', 'project_id',
    ]})


def event(state, kind, **values):
    state.setdefault('history', []).append({'event': kind, 'at': now(), **values})


def snapshot(state):
    return {key: deepcopy(state.get(key)) for key in [
        'flow_version', 'runtime', 'current_sequence', 'context', 'actors',
        'artifacts', 'evidence', 'sequences', 'pending_transition', 'completed',
    ]}


def atomic_json(target, state):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


@contextmanager
def locked(target):
    lock = target.parent / '.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise FlowError('Une écriture est déjà en cours, ou son verrou doit être vérifié après un arrêt brutal.')
    try:
        with os.fdopen(descriptor, 'w') as stream:
            stream.write(json.dumps({'pid': os.getpid(), 'at': now()}))
        yield
    finally:
        lock.unlink(missing_ok=True)


def md(value):
    return str(value or '—').replace('\n', ' ').replace('|', r'\|')


def summary_text(state, root):
    model = engine().load_model()
    current = state.get('current_sequence')
    sequence = next((seq for seq in model['sequences'] if seq['id'] == current), {})
    pending = state.get('pending_transition')
    errors = binding_errors(state, root, model) + freshness_errors(state, root)
    errors += engine().state_errors(model, state)
    status = 'attente_validation' if pending else state.get('sequences', {}).get(current, {}).get('status', 'a_faire')
    lines = [
        '# Suivi du projet', '',
        '> Vue générée depuis etat.json. Le coordinateur conserve les décisions dans l’état.', '',
        f'**Projet :** {md(state.get("project"))}',
        f'**Séquence :** {current} — {md(sequence.get("title"))}',
        f'**État :** {status} · **Révision du suivi :** {state.get("revision", 0)}',
        '**Accompagnement :** guidé, une séquence à la fois.', '',
    ]
    if state.get('completed'):
        lines += ['La fin de boucle a été confirmée ; consulter ses preuves et ses limites.', '']
    if pending:
        lines += [
            '## Accord attendu', '', md(pending['summary']), '',
            f'Proposition : {current} → {pending["target"]}.',
            f'Référence du point de passage : {pending["id"]}.',
            'Un accord doit porter sur ces résultats et leurs versions.', '',
        ]
    waiting = state.get('sequences', {}).get(current, {}).get('waiting_for')
    if waiting:
        lines += ['## Attente', '', md(waiting), '']
    if errors:
        lines += ['## Points à examiner', ''] + [f'- {md(error)}' for error in dict.fromkeys(errors)] + ['']
    lines += ['## Livrables référencés', '', '| Livrable | Emplacement | Version |', '| --- | --- | --- |']
    for key, item in state.get('artifacts', {}).items():
        lines.append(f'| {md(key)} | {md(item.get("path"))} | {md(item.get("version"))} |')
    lines += ['', '## Parcours', '', '| Séquence | Intention | Statut déclaré |', '| --- | --- | --- |']
    for seq in model['sequences']:
        record = state.get('sequences', {}).get(seq['id'], {})
        lines.append(f'| {seq["id"]} | {md(seq["title"])} | {record.get("status", "a_faire")} |')
    lines += ['', 'Les données et preuves sont déclarées. Leur contenu doit être vérifié par les responsables compétents.', '']
    return '\n'.join(lines)


def write_summary(root, state):
    path = root / '.flow' / 'suivi.md'
    if path.is_symlink():
        raise FlowError('Le suivi généré ne doit pas être un lien symbolique.')
    text = summary_text(state, root)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(text)
            os.replace(temporary, path)
            temporary = None
        finally:
            if temporary:
                temporary.unlink(missing_ok=True)
    return path


def mutate(project, expected_revision, operation, check_binding=True):
    root, target = state_path(project)
    if expected_revision is None:
        raise FlowError('La révision lue est requise pour protéger les écritures concurrentes.')
    with locked(target):
        if (target.parent / 'suivi.md').is_symlink():
            raise FlowError('Le suivi généré ne doit pas être un lien symbolique.')
        state = read_state(target)
        if state.get('revision', 0) != expected_revision:
            raise FlowError('Le suivi a changé : relire la version courante avant cette action.')
        if check_binding:
            errors = binding_errors(state, root, engine().load_model())
            if errors:
                raise FlowError(' '.join(errors))
        result = operation(state, root)
        state['revision'] = expected_revision + 1
        atomic_json(target, state)
        try:
            write_summary(root, state)
        except (OSError, FlowError) as error:
            result['view_warning'] = f'État enregistré ; suivi à régénérer : {error}'
    return {**result, 'revision': state['revision'], 'errors': []}


def initialize(project, idea=None):
    root, target = state_path(project)
    model = engine().load_model()
    if target.exists():
        state = read_state(target)
        return {'created': False, 'preserved': True, 'state_path': str(target), 'errors': binding_errors(state, root, model)}
    state = json.loads((MODEL_ROOT / 'templates/etat.json').read_text(encoding='utf-8'))
    state.update(
        project=root.name, project_id=str(uuid.uuid4()), project_root=str(root),
        runtime=provenance(), state_schema=STATE_SCHEMA, execution_mode='guide',
        revision=0, pending_transition=None, completed=False,
    )
    if idea:
        state['initial_idea'] = idea
    event(state, 'instance_initialized', sequence='S00')
    target.parent.mkdir(exist_ok=True)
    with locked(target):
        if (target.parent / 'suivi.md').is_symlink():
            raise FlowError('Le suivi généré ne doit pas être un lien symbolique.')
        if target.exists():
            raise FlowError('Un état a été créé entre-temps ; relire le projet.')
        atomic_json(target, state)
        write_summary(root, state)
    return {'created': True, 'state_path': str(target), 'current_sequence': 'S00', 'mode': 'reel', 'revision': 0, 'errors': []}


def adopt(project, expected_revision=None, reference='adoption locale explicite'):
    root, target = state_path(project)
    state = read_state(target)
    runtime = engine()
    errors = runtime.state_errors(runtime.load_model(), state)
    if state.get('mode') != 'reel':
        errors.append('Une illustration ne peut pas être adoptée comme projet réel.')
    if state.get('runtime') and state['runtime'].get('model_sha256') != provenance()['model_sha256']:
        errors.append('Un modèle différent exige migrate, pas adopt.')
    if state.get('project_root') and state['project_root'] != str(root):
        errors.append('Dossier différent : examiner relocate.')
    if errors:
        return {'adopted': False, 'errors': errors}
    if not binding_errors(state, root, runtime.load_model()):
        return {'adopted': False, 'preserved': True, 'errors': []}
    def operation(current, root):
        current.update(runtime=provenance(), project_root=str(root), state_schema=STATE_SCHEMA, execution_mode='guide')
        current.setdefault('project_id', str(uuid.uuid4()))
        current.setdefault('pending_transition', None)
        event(current, 'runtime_adopted', reference=reference)
        return {'adopted': True, 'state_path': str(target)}
    return mutate(project, state.get('revision', 0) if expected_revision is None else expected_revision, operation, check_binding=False)


def descendants(model, seeds):
    affected = set(seeds)
    while True:
        expanded = affected | {seq['id'] for seq in model['sequences'] if affected.intersection(seq['requires'])}
        if expanded == affected:
            return affected
        affected = expanded


def invalidate(state, ids, reason):
    records = state.setdefault('sequences', {})
    for sid in ids:
        if sid in records and records[sid].get('status') in ['valide', 'non_applicable']:
            event(state, 'validation_to_review', sequence=sid, previous=deepcopy(records[sid]), reason=reason)
            records[sid] = {'status': 'a_reprendre', 'reason': reason}


def record(project, patch, expected_revision):
    if not isinstance(patch, dict) or not set(patch).issubset({'context', 'actors', 'artifacts', 'evidence', 'sequences'}):
        raise FlowError('record accepte seulement contexte, acteurs, livrables, preuves et contrats de séquences.')
    if any(not isinstance(value, dict) for value in patch.values()):
        raise FlowError('Chaque rubrique de record doit être un objet JSON.')
    def operation(state, root):
        runtime = engine()
        model = runtime.load_model()
        before = fingerprint(state)
        ids = {seq['id'] for seq in model['sequences']}
        for sid, value in patch.get('sequences', {}).items():
            if sid not in ids or not isinstance(value, dict):
                raise FlowError('Contrat de séquence inconnu ou invalide.')
            if sid != state['current_sequence'] and value.get('status') != 'non_applicable':
                raise FlowError('Enregistrer le travail courant ; utiliser focus pour une reprise proposée.')
        for field in ['context', 'actors']:
            allowed = model['context_fields'] if field == 'context' else model['roles']
            if any(key not in allowed for key in patch.get(field, {})):
                raise FlowError(f'{field}: champ inconnu.')
            for key, value in patch.get(field, {}).items():
                kind = 'string' if field == 'actors' else allowed[key]['type']
                if value is not None and ((kind == 'boolean' and type(value) is not bool) or (kind == 'string' and (not isinstance(value, str) or not value.strip()))):
                    raise FlowError(f'{field}: type incorrect pour {key}.')
            state[field].update(deepcopy(patch.get(field, {})))
        for key, value in patch.get('artifacts', {}).items():
            if key not in model['artifacts'] or not isinstance(value, dict):
                raise FlowError('Livrable inconnu ou invalide.')
            item = deepcopy(value)
            path = local_artifact(root, item)
            if path is not None:
                item['path'] = path.relative_to(root).as_posix()
                item['content_sha256'] = content_hash(root, item)
                item.setdefault('version', 'sha256:' + item['content_sha256'])
                previous = state['artifacts'].get(key)
                if previous and previous.get('content_sha256') != item['content_sha256'] and previous.get('version') == item['version']:
                    raise FlowError('Le contenu a changé : choisir une nouvelle version ou laisser record calculer son empreinte.')
            elif not item.get('version'):
                raise FlowError('Une référence distante nécessite une version explicite.')
            state['artifacts'][key] = item
        for key, proof in patch.get('evidence', {}).items():
            if not isinstance(proof, dict) or proof.get('simulated') is not False:
                raise FlowError('Une preuve réelle explicitement qualifiée est requise.')
            state['evidence'][key] = deepcopy(proof)
        for sid, value in patch.get('sequences', {}).items():
            state['sequences'][sid] = {**state['sequences'].get(sid, {}), **deepcopy(value)}
        for sid, value in patch.get('sequences', {}).items():
            problems = runtime.record_errors(model, state, sid)
            if problems:
                raise FlowError(f'{sid}: ' + ' '.join(problems))
        affected = {sid for sid, value in state['sequences'].items()
                    if value.get('status') in ['valide', 'non_applicable'] and runtime.record_errors(model, state, sid)}
        invalidate(state, affected, 'Une entrée, une sortie ou une condition a changé.')
        if state.get('pending_transition') and fingerprint(state) != before:
            event(state, 'checkpoint_superseded', checkpoint=state['pending_transition']['id'])
            state['pending_transition'] = None
        if fingerprint(state) != before:
            state['completed'] = False
        event(state, 'work_recorded', sequence=state['current_sequence'], changed=list(patch))
        return {'recorded': True, 'to_review': sorted(affected)}
    return mutate(project, expected_revision, operation)


def checkpoint(project, summary, expected_revision, target=None):
    if not summary or not summary.strip():
        raise FlowError('Décrire le résultat présenté et ses limites.')
    def operation(state, root):
        if state.get('completed'):
            raise FlowError('Cette boucle est terminée ; conserver une nouvelle décision avant de la rouvrir.')
        runtime = engine()
        model = runtime.load_model()
        errors = runtime.state_errors(model, state) + freshness_errors(state, root)
        if errors or not runtime.satisfied(model, state, state['current_sequence']):
            raise FlowError('La séquence nécessite des résultats et preuves valides avant passage. ' + ' '.join(errors))
        recommendation = runtime.recommend(model, state)
        candidates = [recommendation] + recommendation.get('alternatives', [])
        choices = {item.get('sequence'): item for item in candidates
                   if item.get('result') in ['sequence_a_realiser', 'reouverture_a_consigner', 'information_requise']}
        if recommendation.get('result') == 'END':
            choices['END'] = recommendation
        selected = target or ('END' if recommendation.get('result') == 'END' else recommendation.get('sequence'))
        if selected not in choices or selected == state['current_sequence']:
            raise FlowError('Aucune destination de passage prête : traiter la recommandation avant de créer cet accord.')
        pending = {
            'id': str(uuid.uuid4()), 'sequence': state['current_sequence'], 'target': selected,
            'summary': summary.strip(), 'fingerprint': fingerprint(state),
            'created_at': now(), 'reopen': choices[selected].get('result') == 'reouverture_a_consigner',
        }
        state['pending_transition'] = pending
        event(state, 'checkpoint_presented', checkpoint=pending['id'], sequence=pending['sequence'], target=selected)
        return {'checkpoint': pending, 'waiting_for': 'Accord du porteur sur le résultat et ses versions.'}
    return mutate(project, expected_revision, operation)


def decision(project, action, checkpoint_id, actor, reference, expected_revision, reason=None):
    if action not in ['approve', 'correct', 'pause']:
        raise FlowError('Décision inconnue.')
    if not actor or not reference or not reference.strip():
        raise FlowError('Conserver auteur et référence de la décision réellement donnée.')
    if action != 'approve' and not reason:
        raise FlowError('Préciser la correction ou l’attente demandée.')
    def operation(state, root):
        pending = state.get('pending_transition')
        if not pending or pending['id'] != checkpoint_id:
            raise FlowError('Ce point de passage n’est plus courant.')
        if actor != state.get('actors', {}).get('porteur'):
            raise FlowError('L’accord de passage appartient au porteur identifié.')
        if action == 'approve':
            runtime = engine()
            model = runtime.load_model()
            errors = runtime.state_errors(model, state) + freshness_errors(state, root)
            if pending['fingerprint'] != fingerprint(state) or errors:
                raise FlowError('Les résultats ont changé ; présenter un nouvel accord. ' + ' '.join(errors))
            if pending['reopen']:
                event(state, 'iteration_archived', snapshot=snapshot(state))
                affected = descendants(model, [pending['target']])
                invalidate(state, affected, 'Nouvelle tranche autorisée.')
            if pending['target'] == 'END':
                state['completed'] = True
            else:
                state['current_sequence'] = pending['target']
                state['sequences'].setdefault(pending['target'], {'status': 'a_faire'})
            state['pending_transition'] = None
        elif action == 'correct':
            state['sequences'][state['current_sequence']]['status'] = 'a_reprendre'
            state['sequences'][state['current_sequence']]['reason'] = reason
            state['pending_transition'] = None
        else:
            pending['waiting_for'] = reason
        event(state, 'passage_' + action, checkpoint=checkpoint_id, actor=actor, reference=reference,
              sequence=pending['sequence'], target=pending['target'], reason=reason)
        return {'decision': action, 'current_sequence': state['current_sequence'], 'completed': state.get('completed', False)}
    return mutate(project, expected_revision, operation)


def focus(project, sequence, actor, reference, expected_revision):
    if not actor or not reference:
        raise FlowError('Nommer la personne et la demande qui autorisent cette reprise.')
    def operation(state, root):
        if actor != state.get('actors', {}).get('porteur'):
            raise FlowError('La reprise doit être demandée par le porteur identifié.')
        recommendation = engine().recommend(engine().load_model(), state)
        if sequence != recommendation.get('sequence') or sequence == state['current_sequence']:
            raise FlowError('La reprise doit viser la séquence actuellement recommandée.')
        if state.get('pending_transition'):
            raise FlowError('Traiter le point de passage en attente avant une autre reprise.')
        if engine().satisfied(engine().load_model(), state, state['current_sequence']):
            raise FlowError('Une séquence terminée passe par checkpoint et approve.')
        if recommendation.get('remember_resume_sequence'):
            state['resume_sequence'] = recommendation['remember_resume_sequence']
        previous = state['current_sequence']
        state['current_sequence'] = sequence
        state['sequences'].setdefault(sequence, {'status': 'a_faire'})
        event(state, 'sequence_refocused', previous=previous, sequence=sequence, actor=actor, reference=reference)
        return {'current_sequence': sequence}
    return mutate(project, expected_revision, operation)


def relocate(project, reference, expected_revision):
    if not reference:
        raise FlowError('Le rattachement après déplacement nécessite une décision référencée.')
    def operation(state, root):
        old_root = Path(state.get('project_root', ''))
        if state.get('mode') != 'reel' or state.get('runtime', {}).get('model_sha256') != provenance()['model_sha256']:
            raise FlowError('Examiner d’abord la provenance et le modèle.')
        if str(old_root) == str(root):
            raise FlowError('Ce projet est déjà rattaché à ce dossier.')
        for artifact in state.get('artifacts', {}).values():
            path = Path(str(artifact.get('path', '')))
            if path.is_absolute():
                try:
                    artifact['path'] = path.relative_to(old_root).as_posix()
                except ValueError:
                    raise FlowError('Examiner les références absolues situées hors de l’ancien projet.')
        state['project_root'] = str(root)
        state['pending_transition'] = None
        event(state, 'project_relocated', previous=str(old_root), target=str(root), reference=reference)
        return {'relocated': True, 'project_id': state.get('project_id'), 'to_review': freshness_errors(state, root)}
    return mutate(project, expected_revision, operation, check_binding=False)


def migration_plan(project):
    root, target = state_path(project)
    state = read_state(target)
    current = provenance()
    previous = state.get('runtime', {})
    if state.get('mode') != 'reel':
        raise FlowError('Les exemples ne sont pas migrés en projets réels.')
    if previous.get('plugin') not in (None, 'flow-aidd') or state.get('state_schema', STATE_SCHEMA) > STATE_SCHEMA:
        raise FlowError('Provenance ou format de suivi inconnu : une migration dédiée est nécessaire.')
    if str(state.get('flow_version', '')).split('.')[0] != engine().load_model()['version'].split('.')[0]:
        raise FlowError('Changement majeur du format : une migration dédiée est nécessaire.')
    old = previous.get('sequence_hashes', {})
    new = current['sequence_hashes']
    changed = {sid for sid in new if old.get(sid) != new[sid]}
    if previous.get('policy_sha256') != current['policy_sha256']:
        changed.update(new)
    return {
        'required': previous.get('model_sha256') != current['model_sha256'],
        'revision': state.get('revision', 0),
        'changed_sequences': sorted(descendants(engine().load_model(), changed)),
        'retired_sequences': sorted(set(state.get('sequences', {})) - set(new)),
        'errors': [],
    }


def migrate(project, reference, expected_revision):
    if not reference:
        raise FlowError('Conserver la décision prise après lecture du plan de migration.')
    def operation(state, root):
        plan = migration_plan(root)
        if state.get('project_root') != str(root):
            raise FlowError('Rattacher le bon dossier avant la migration.')
        event(state, 'model_before_migration', reference=reference, snapshot=snapshot(state))
        invalidate(state, plan['changed_sequences'], 'Contrat ou règle du modèle modifié.')
        for sid in plan['retired_sequences']:
            state['sequences'].pop(sid, None)
        state.update(runtime=provenance(), flow_version=engine().load_model()['version'], state_schema=STATE_SCHEMA,
                     execution_mode='guide', pending_transition=None, completed=False)
        state.setdefault('project_id', str(uuid.uuid4()))
        if state['current_sequence'] not in provenance()['sequence_hashes']:
            state['current_sequence'] = 'S00'
        event(state, 'model_migrated', reference=reference, changes=plan['changed_sequences'])
        return {'migrated': True, 'to_review': plan['changed_sequences']}
    return mutate(project, expected_revision, operation, check_binding=False)


def guidance(state, working, pending, stale, binding, errors, capabilities, agents):
    """Name the only references to read now and the next actions, like a context loader."""
    sid = (working or {}).get('id')
    load, directives = [], []
    if binding:
        load.append('references/rattacher.md')
        directives.append('Rattacher l’état avant tout travail : ' + ' '.join(binding[:2]))
    if sid:
        load.append(f'references/sequences/{sid}.md')
    if pending:
        load.append('references/checkpoint.md')
        if stale:
            directives.append(f'Point de passage {pending["id"]} périmé : record puis nouveau checkpoint avant de le présenter.')
        else:
            directives.append(f'Accord attendu sur {pending["id"]} ({state.get("current_sequence")} → {pending["target"]}) : '
                              'présenter le résultat et attendre la réponse du porteur ; ne pas commencer la séquence suivante.')
    waiting = state.get('sequences', {}).get(sid, {}).get('waiting_for') if sid else None
    if waiting and not pending:
        directives.append(f'Attente : {waiting}')
    other = [error for error in errors if error not in binding]
    if other:
        directives.append('Examiner avant de continuer : ' + ' '.join(other[:2]))
    if capabilities and any(capabilities[key] for key in ['utiliser', 'selon_le_cas', 'a_confirmer']):
        load.append('references/capacites.md')
    for item in (capabilities or {}).get('a_confirmer', []):
        directives.append(f'Demander au porteur : {item["question"]} (`{item["field"]}`), puis record context.')
    if capabilities and capabilities['a_confirmer']:
        load += ['references/entretien.md', 'references/record.md']
    if sid and not pending and not binding and (working.get('validation', {}).get('by') == 'porteur' or working['action'].get('questions')):
        load.append('references/entretien.md')
    if sid and not pending and not binding:
        directives.append(f'Conduire {sid} selon sa fiche, record au fil du travail'
                          + (', puis lancer ' + ' et '.join(agent['codex'] for agent in agents) if agents else '')
                          + ' avant checkpoint (references/checkpoint.md).')
        load += ['references/record.md', 'references/socle.md']
    return list(dict.fromkeys(load)), directives


def inspect(project):
    root, target = state_path(project)
    if not target.exists():
        return {'initialized': False, 'project': str(root), 'next_action': 'Initialiser S00 à la demande du porteur.', 'errors': [],
                'skill_root': str(SKILL_ROOT), 'load': ['references/init.md'],
                'directives': ['Aucun suivi ici : expliquer, ou lancer init seulement si le porteur démarre ce projet.']}
    runtime = engine()
    model = runtime.load_model()
    state = read_state(target)
    binding = binding_errors(state, root, model)
    errors = list(binding)
    errors += freshness_errors(state, root)
    errors += runtime.state_errors(model, state)
    current = state.get('current_sequence')
    sequence = next((item for item in model['sequences'] if item['id'] == current), {})
    pending = state.get('pending_transition')
    stale = bool(pending and (pending.get('fingerprint') != fingerprint(state) or errors))
    recommendation = {'result': 'etat_a_corriger'} if errors else runtime.recommend(model, state)
    if pending and not errors:
        recommendation = {'result': 'attente_validation', 'sequence': current, 'proposed_target': pending['target']}
    working = next((item for item in model['sequences'] if item['id'] == (recommendation.get('sequence') or current)), sequence)
    capabilities = {'sequence': working.get('id'), **runtime.capability_plan(model, working, state)} if working else None
    agents = runtime.review_agents(model, working['id']) if working else []
    load, directives = guidance(state, working, pending, stale, binding, errors, capabilities, agents)
    return {
        'initialized': True, 'project': state.get('project'), 'project_id': state.get('project_id'),
        'state_path': str(target), 'mode': state.get('mode'), 'revision': state.get('revision', 0),
        'execution_mode': state.get('execution_mode'), 'current_sequence': current, 'title': sequence.get('title'),
        'status': 'attente_validation' if pending else state.get('sequences', {}).get(current, {}).get('status', 'a_faire'),
        'waiting_for': (pending or {}).get('waiting_for') or state.get('sequences', {}).get(current, {}).get('waiting_for'),
        'feedback': state.get('sequences', {}).get(current, {}).get('reason'),
        'pending_transition': pending, 'checkpoint_stale': stale, 'completed': state.get('completed', False),
        'recommendation': recommendation, 'errors': list(dict.fromkeys(errors)),
        'skill_root': str(SKILL_ROOT), 'load': load, 'directives': directives,
        'capabilities': capabilities, 'agents': agents,
        'artifacts': state.get('artifacts', {}), 'evidence': state.get('evidence', {}),
        'approver': state.get('actors', {}).get('porteur'),
        'sequences': [{'id': seq['id'], 'title': seq['title'], 'phase': seq['phase'],
                       'status': state.get('sequences', {}).get(seq['id'], {}).get('status', 'a_faire'),
                       'applicable': runtime.applicability(seq, state)} for seq in model['sequences']],
        'limit': 'Contrôles de cohérence et de fichiers locaux ; les preuves distantes et l’accord humain doivent être authentiques.',
    }


def render(project):
    root, target = state_path(project)
    with locked(target):
        return {'view': str(write_summary(root, read_state(target))), 'errors': []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['init', 'adopt', 'status', 'check', 'next', 'show', 'record', 'checkpoint',
                                          'approve', 'correct', 'pause', 'focus', 'relocate', 'migration-plan', 'migrate', 'render'])
    parser.add_argument('sequence', nargs='?')
    parser.add_argument('--project', type=Path)
    parser.add_argument('--idea')
    parser.add_argument('--input', type=Path)
    parser.add_argument('--expected-revision', type=int)
    parser.add_argument('--summary')
    parser.add_argument('--target')
    parser.add_argument('--checkpoint')
    parser.add_argument('--actor')
    parser.add_argument('--reference')
    parser.add_argument('--reason')
    args = parser.parse_args()
    if args.command != 'show' and args.project is None:
        parser.error('Choisir explicitement le dossier avec --project.')
    try:
        command = args.command
        if command == 'show':
            result = next((seq for seq in engine().load_model()['sequences'] if seq['id'] == args.sequence), None)
            if result is None:
                raise FlowError('Séquence inconnue.')
        elif command == 'init':
            result = initialize(args.project, args.idea)
        elif command == 'adopt':
            result = adopt(args.project, args.expected_revision, args.reference or 'adoption locale explicite')
        elif command == 'record':
            if args.input is None:
                raise FlowError('record nécessite --input, un fichier JSON préparé par le coordinateur.')
            result = record(args.project, json.loads(args.input.read_text()), args.expected_revision)
        elif command == 'checkpoint':
            result = checkpoint(args.project, args.summary, args.expected_revision, args.target)
        elif command in ['approve', 'correct', 'pause']:
            result = decision(args.project, command, args.checkpoint, args.actor, args.reference, args.expected_revision, args.reason)
        elif command == 'focus':
            result = focus(args.project, args.sequence, args.actor, args.reference, args.expected_revision)
        elif command == 'relocate':
            result = relocate(args.project, args.reference, args.expected_revision)
        elif command == 'migration-plan':
            result = migration_plan(args.project)
        elif command == 'migrate':
            result = migrate(args.project, args.reference, args.expected_revision)
        elif command == 'render':
            result = render(args.project)
        else:
            result = inspect(args.project)
            if command in ['check', 'next'] and not result['initialized']:
                result['errors'] = ['Le projet ne possède pas encore d’état.']
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('errors') else 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(json.dumps({'errors': [str(error)], 'limit': 'Aucun passage implicite ni écrasement silencieux.'}, ensure_ascii=False, indent=2))
        return 1


if __name__ == '__main__':
    sys.exit(main())
