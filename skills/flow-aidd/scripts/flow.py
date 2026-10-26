"""Read-only checks and navigation for the sequence model; build derived guides."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1] / 'references'


def load_model():
    return json.loads((ROOT / 'workflow.json').read_text())


def model_errors(model):
    errors = []
    sequences = model.get('sequences', [])
    ids = [item.get('id') for item in sequences]
    known = set(ids)
    if not sequences or len(ids) != len(known):
        errors.append('Séquences absentes ou identifiants dupliqués.')
    artifacts = model.get('artifacts', {})
    roles = model.get('roles', {})
    for item in sequences:
        sid = item.get('id', '?')
        if not re.fullmatch(r'S\d+', sid):
            errors.append(f'{sid}: identifiant non stable ou invalide.')
        for field in model.get('contract', {}):
            if field not in item:
                errors.append(f'{sid}: contrat sans {field}.')
        if item.get('responsible') not in roles or item.get('validation', {}).get('by') not in roles:
            errors.append(f'{sid}: rôle inconnu.')
        for field in ['input', 'input_optional', 'output']:
            if any(key not in artifacts for key in item.get(field, [])):
                errors.append(f'{sid}: artefact inconnu dans {field}.')
        if any(dep not in known for dep in item.get('requires', [])):
            errors.append(f'{sid}: dépendance inconnue.')
        applicability = item.get('applicability')
        if applicability and applicability.get('field') not in model.get('context_fields', {}):
            errors.append(f'{sid}: condition inconnue.')
        if not item.get('action', {}).get('steps') or not item.get('evidence') or not item.get('validation', {}).get('criteria'):
            errors.append(f'{sid}: action, preuve ou critères vides.')
        proof_ids = [proof['id'] for proof in item.get('evidence', [])]
        if len(proof_ids) != len(set(proof_ids)):
            errors.append(f'{sid}: critères de preuve dupliqués.')
        for outcome, targets in item.get('next', {}).items():
            for target in targets if isinstance(targets, list) else [targets]:
                if target not in known and target not in model.get('special_targets', {}):
                    errors.append(f'{sid}: destination {target} inconnue pour {outcome}.')
        invocation = item.get('action', {}).get('invocation')
        if invocation and (invocation.get('prefix') != 'interactive' or invocation.get('template', '').split()[0] != 'interactive'):
            errors.append(f'{sid}: requête SDLC interactive mal encodée.')
    graph = {item['id']: item.get('requires', []) for item in sequences}
    def walk(sid, trail):
        if sid in trail:
            errors.append(f'Cycle de prérequis : {trail + [sid]}')
            return
        for dep in graph.get(sid, []):
            walk(dep, trail + [sid])
    for sid in graph:
        walk(sid, [])
    return errors


def applicability(sequence, state):
    condition = sequence.get('applicability')
    if not condition:
        return True
    value = state.get('context', {}).get(condition['field'])
    if value is None:
        return None
    return value == condition['equals']


def record_errors(model, state, sid, trail=()):
    items = {item['id']: item for item in model['sequences']}
    sequence = items[sid]
    record = state.get('sequences', {}).get(sid, {})
    status = record.get('status', 'a_faire')
    if sid in trail:
        return ['Cycle de vérification.']
    errors = []
    if status not in model['statuses']:
        return ['Statut inconnu.']
    if status.startswith('attente_') and not record.get('waiting_for'):
        errors.append('Nommer précisément ce qui est attendu.')
    if status not in ['valide', 'non_applicable']:
        return errors
    app = applicability(sequence, state)
    artifacts = state.get('artifacts', {})
    proofs = state.get('evidence', {})
    if status == 'non_applicable':
        if app is not False:
            errors.append('Une séquence requise ou de condition inconnue ne peut pas être écartée.')
        if not record.get('reason') or not record.get('context_ref'):
            errors.append('Justification et référence au cadrage approuvé requises.')
        if record.get('context_version') != artifacts.get('cadre', {}).get('version'):
            errors.append('Le cadrage ayant justifié la non-applicabilité a changé.')
        if record.get('context_ref') not in proofs:
            errors.append('Preuve du cadrage introuvable.')
        else:
            context_proof = proofs[record['context_ref']]
            if context_proof.get('kind') != 'decision' or context_proof.get('artifact') != 'cadre' or context_proof.get('version') != artifacts.get('cadre', {}).get('version'):
                errors.append('La non-applicabilité doit citer la décision sur le cadrage actuel.')
        if sid != 'S00' and not satisfied(model, state, 'S00', trail + (sid,)):
            errors.append('Le cadrage doit être valide pour écarter une séquence.')
        return errors
    if app is not True:
        errors.append('Applicabilité fausse ou inconnue ; traiter ce cas explicitement.')
    for dep in sequence.get('requires', []):
        if not satisfied(model, state, dep, trail + (sid,)):
            errors.append(f'Prérequis {dep} non satisfait ou à réexaminer.')
    for field, definition in model['context_fields'].items():
        value = state.get('context', {}).get(field)
        required = sid in definition.get('required_at', [])
        expected = definition['type']
        if required and value is None:
            errors.append(f'Contexte : préciser {field} avant {sid}.')
        elif value is not None and ((expected == 'boolean' and type(value) is not bool) or (expected == 'string' and (not isinstance(value, str) or not value.strip()))):
            errors.append(f'Contexte : type incorrect pour {field}.')
    if not state.get('actors', {}).get(sequence['responsible']):
        errors.append('Le pilote effectif de la séquence doit être identifié.')
    if sid in ['S91', 'S110']:
        for role, field in [('integration', 'integration_owner')] if sid == 'S91' else [('exploitation', 'operations_owner')]:
            if state.get('actors', {}).get(role) != state.get('context', {}).get(field):
                errors.append(f'Le responsable {role} doit correspondre au cadrage.')
    expected_role = sequence['validation']['by']
    if record.get('validator_role') != expected_role:
        errors.append(f'Le rôle de validation attendu est {expected_role}.')
    actor = state.get('actors', {}).get(expected_role)
    if not actor or record.get('validated_by') != actor:
        errors.append('Le validateur effectif doit être identifié dans les rôles de l’instance.')
    try:
        datetime.fromisoformat(str(record.get('validated_at', '')).replace('Z', '+00:00'))
    except ValueError:
        errors.append('Date de validation ISO requise.')
    if record.get('outcome') not in sequence['next']:
        errors.append('Choisir une issue explicite parmi les destinations de la séquence.')
    for key in sequence['input']:
        if not artifacts.get(key, {}).get('version'):
            errors.append(f'Entrée {key} absente ou non versionnée.')
    used = sequence['input'] + [key for key in sequence.get('input_optional', []) if key in record.get('used_versions', {})]
    for key in used:
        if record.get('used_versions', {}).get(key) != artifacts.get(key, {}).get('version'):
            errors.append(f'Entrée {key} modifiée ou version utilisée non conservée.')
    for key in sequence['output']:
        artifact = artifacts.get(key, {})
        if not artifact.get('path') or not artifact.get('version'):
            errors.append(f'Sortie {key} sans emplacement et version concrets.')
        if record.get('produced_versions', {}).get(key) != artifact.get('version'):
            errors.append(f'Sortie {key} modifiée depuis cette validation.')
    linked = [proofs[key] for key in record.get('evidence_ids', []) if key in proofs]
    for criterion in sequence['evidence']:
        matches = [proof for proof in linked if proof.get('sequence') == sid and proof.get('criterion') == criterion['id']]
        if not matches:
            errors.append(f'Preuve manquante : {criterion["id"]}.')
            continue
        proof = matches[-1]
        if state.get('mode') == 'reel' and proof.get('simulated') is not False:
            errors.append(f'Une preuve simulée ou non qualifiée ne valide pas une instance réelle : {criterion["id"]}.')
        if proof.get('kind') != criterion['kind'] or proof.get('result') not in ['observed', 'passed', 'approved']:
            errors.append(f'Preuve non concluante : {criterion["id"]}.')
        if not proof.get('reference') or not proof.get('actor'):
            errors.append(f'Source et auteur de preuve requis : {criterion["id"]}.')
        artifact = artifacts.get(proof.get('artifact'), {})
        if not artifact or proof.get('version') != artifact.get('version'):
            errors.append(f'Preuve liée à une version absente ou obsolète : {criterion["id"]}.')
        if proof.get('artifact') not in sequence['input'] + sequence.get('input_optional', []) + sequence['output']:
            errors.append(f'Preuve sans rapport avec les entrées ou sorties : {criterion["id"]}.')
        if criterion.get('independent') and (not record.get('performed_by') or proof.get('actor') == record.get('performed_by')):
            errors.append('La revue indépendante ne peut pas être attribuée au réalisateur.')
    return errors


def satisfied(model, state, sid, trail=()):
    record = state.get('sequences', {}).get(sid, {})
    return record.get('status') in ['valide', 'non_applicable'] and not record_errors(model, state, sid, trail)


def state_errors(model, state):
    errors = []
    if state.get('flow_version') != model['version']:
        errors.append('Version du modèle différente de celle de l’instance.')
    if state.get('mode') not in ['reel', 'illustration']:
        errors.append('Mode reel ou illustration requis.')
    ids = {item['id'] for item in model['sequences']}
    if state.get('current_sequence') not in ids:
        errors.append('Séquence courante inconnue.')
    if any(sid not in ids for sid in state.get('sequences', {})):
        errors.append('L’instance cite une séquence inconnue.')
    if state.get('mode') == 'reel':
        for key, proof in state.get('evidence', {}).items():
            if proof.get('simulated') is not False:
                errors.append(f'{key}: une instance réelle exige une preuve explicitement non simulée.')
        for key, artifact in state.get('artifacts', {}).items():
            if str(artifact.get('path', '')).startswith('illustration:') or any(token in str(artifact.get('path', '')) for token in ['{projet}', '<slug>', '<yyyy_']):
                errors.append(f'{key}: résoudre l’emplacement illustratif ou générique avant une instance réelle.')
    for sid in state.get('sequences', {}):
        if sid in ids:
            errors += [f'{sid}: {message}' for message in record_errors(model, state, sid)]
    return errors


def recommend(model, state):
    if state.get('flow_version') != model['version'] or state.get('mode') not in ['reel', 'illustration']:
        return {'result': 'etat_a_corriger', 'reason': 'Vérifier version du flow et mode de l’instance.'}
    items = {item['id']: item for item in model['sequences']}
    current = state.get('current_sequence', 'S00')
    if current not in items:
        return {'result': 'etat_a_corriger', 'reason': 'Séquence courante inconnue.'}
    def task(sid, visited=()):
        if sid in visited:
            return {'result': 'etat_a_corriger', 'sequence': sid, 'reason': 'Boucle de navigation non résolue.'}
        item = items[sid]
        record = state.get('sequences', {}).get(sid, {})
        app = applicability(item, state)
        if app is False and record.get('status') != 'non_applicable':
            if not satisfied(model, state, 'S00'):
                return task('S00', visited + (sid,))
            return {'result': 'non_applicabilite_a_consigner', 'sequence': sid, 'reason': 'Réutiliser le cadrage approuvé, enregistrer raison, context_ref et context_version.'}
        for dep in item.get('requires', []):
            if not satisfied(model, state, dep):
                return task(dep, visited + (sid,))
        if app is None:
            return {'result': 'information_requise', 'sequence': sid, 'field': item['applicability']['field']}
        problems = record_errors(model, state, sid)
        if record.get('status') in ['valide', 'non_applicable']:
            return {'result': 'a_reexaminer' if problems else 'deja_satisfaite', 'sequence': sid, 'reasons': problems}
        if record.get('status', '').startswith('attente_'):
            return {'result': record['status'], 'sequence': sid, 'waiting_for': record.get('waiting_for', 'À préciser.')}
        return {'result': 'sequence_a_realiser', 'sequence': sid, 'title': item['title'], 'guide': f'sequences/{sid}.md'}
    record = state.get('sequences', {}).get(current, {})
    if record.get('status') == 'arrete':
        return {'result': 'STOP', 'sequence': current, 'reason': record.get('reason', 'Arrêt consigné.')}
    if not satisfied(model, state, current):
        # A failure does not implicitly advance to the success destination.
        outcome = record.get('outcome')
        target = items[current]['next'].get(outcome)
        if outcome in ['modifier_perimetre', 'reorienter', 'risque_technique', 'clarifier_contrat'] and isinstance(target, str) and target in items:
            if not record.get('decision_ref'):
                return {'result': 'decision_de_reprise_a_consigner', 'sequence': current, 'proposed_target': target}
            result = task(target)
            if outcome == 'risque_technique':
                result['remember_resume_sequence'] = current
            return result
        return task(current)
    if record['status'] == 'non_applicable':
        outcome = 'non_applicable'
    else:
        outcome = record.get('outcome')
    targets = items[current]['next'].get(outcome)
    if targets is None:
        return {'result': 'issue_a_preciser', 'sequence': current, 'choices': list(items[current]['next'])}
    if targets == 'RESUME':
        target = state.get('resume_sequence')
        return task(target) if target in items and target != current else {'result': 'destination_de_reprise_a_preciser', 'sequence': current}
    if isinstance(targets, str) and targets in model['special_targets']:
        return {'result': targets, 'sequence': current, 'reason': model['special_targets'][targets]}
    candidates = targets if isinstance(targets, list) else [targets]
    available = [task(target) for target in candidates]
    unfinished = [result for result in available if result['result'] != 'deja_satisfaite']
    if unfinished:
        result = unfinished[0]
        if len(candidates) > 1:
            result['alternatives'] = available
        return result
    if len(candidates) == 1:
        return {'result': 'reouverture_a_consigner', 'sequence': candidates[0], 'reason': 'Conserver l’historique, ouvrir la nouvelle itération et réexaminer les dépendances ; ne pas relivrer silencieusement l’ancienne demande.'}
    for item in model['sequences']:
        if not satisfied(model, state, item['id']):
            return task(item['id'])
    return {'result': 'decision_finale_requise', 'sequence': current}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'check', 'next', 'show'])
    parser.add_argument('sequence', nargs='?')
    parser.add_argument('--state', type=Path)
    parser.add_argument('--check', action='store_true', dest='check_generated')
    args = parser.parse_args()
    model = load_model()
    errors = model_errors(model)
    if errors:
        print(json.dumps({'errors': errors}, ensure_ascii=False, indent=2))
        return 1
    if args.command == 'build':
        from flow_docs import build
        return build(model, ROOT, check=args.check_generated)
    if args.command == 'show':
        sequence = next((item for item in model['sequences'] if item['id'] == args.sequence), None)
        if sequence is None:
            parser.error('Identifiant de séquence inconnu.')
        print(json.dumps(sequence, ensure_ascii=False, indent=2))
        return 0
    if args.command == 'next' and args.state is None:
        parser.error('next nécessite --state ; aucun état de projet n’est inventé.')
    state = json.loads(args.state.read_text()) if args.state else None
    if args.command == 'check':
        errors = state_errors(model, state) if state else []
        print(json.dumps({'mode': state.get('mode') if state else 'modele', 'coherent': not errors, 'errors': errors, 'limit': 'Contrôle de cohérence déclarée ; aucune exécution métier ni preuve réelle n’est créée.'}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    print(json.dumps({'mode': state.get('mode'), 'recommendation': recommend(model, state), 'limit': 'Suggestion en lecture seule ; le coordinateur conserve les décisions et ne lance que les actions autorisées.'}, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
