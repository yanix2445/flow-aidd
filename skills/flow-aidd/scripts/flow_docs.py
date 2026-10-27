"""Derive every current guide and the labelled example from workflow.json."""
from __future__ import annotations
from pathlib import Path
from copy import deepcopy
import json


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def paragraph_list(values):
    return '\n'.join(f'- {value}' for value in values)


def actor_label(model, role):
    return f'**{role}** — {model["roles"][role]}'


def artifact_lines(model, keys):
    return paragraph_list([f'**{key} — {model["artifacts"][key]["title"]}** : `{model["artifacts"][key]["path"]}` ({model["artifacts"][key]["origin"]}). {model["artifacts"][key]["description"]}' for key in keys])


AGENTS_ROOT = Path(__file__).resolve().parents[1] / 'agents'
DEGRADED_HEADER = ('<!-- Généré depuis agents/{codex}.toml par build.py. Ne pas modifier ; modifier la définition de l’agent. -->\n'
                   'Cet environnement ne peut pas lancer de sous-agent : tu joues ce rôle toi-même. Sors complètement du travail '
                   'qui vient d’être fait, n’applique que les consignes de ce fichier pour cette passe, et signale la substitution '
                   'en une ligne au porteur. Là où le texte s’adresse au coordinateur, tu es les deux : rends d’abord le retour '
                   'complet, puis applique-le.\n')


def degraded_agents(model):
    """Fallback instructions for harnesses without subagents, derived from the shipped agent definitions."""
    import tomllib
    files = {}
    for agent in model.get('agents', {}).values():
        definition = tomllib.loads((AGENTS_ROOT / f'{agent["codex"]}.toml').read_text(encoding='utf-8'))
        relative = agent['degraded'].removeprefix('references/')
        files[relative] = DEGRADED_HEADER.format(codex=agent['codex']) + definition['developer_instructions']
    return files


def capability_lines(model, capabilities):
    """Group a sheet's capabilities the way `next` sorts them for a real project."""
    def line(cap):
        text = f'- `{cap["id"]}`' + (f' · `{cap["command"]}`' if cap.get('command') else '')
        if cap.get('if_text'):
            text += f' — *seulement si {cap["if_text"]}* : {cap["when"][:1].lower()}{cap["when"][1:]}'
        else:
            text += f' — {cap["when"]}'
        return text
    unconditional = [cap for cap in capabilities if not cap.get('if')]
    if not capabilities:
        return ['**Capacités à activer :**', '', '- Le coordinateur cadre le travail ; aucun skill spécialisé n’est imposé.']
    lines = ['**Capacités à activer :**', ''] + [line(cap) for cap in unconditional] + [''] if unconditional else []
    fields = {}
    for cap in capabilities:
        if cap.get('if'):
            fields.setdefault((cap['if']['field'], cap['if']['equals']), []).append(cap)
    for (field, equals), caps in fields.items():
        question = model['context_fields'][field]['description']
        lines += [f'**Si `{field}` = `{str(equals).lower()}`** ({question}) :', ''] + [line(cap) for cap in caps] + ['']
    if fields:
        lines += ['`next` et `status` trient ces capacités selon le contexte du projet ; une réponse encore inconnue les laisse à confirmer, jamais écartées.']
    return lines[:-1] if lines and lines[-1] == '' else lines


CLASSES = {
    'entree': 'fill:#eef2f7,stroke:#8a9bb0,color:#1f2933',
    'responsable': 'fill:#f3f4f6,stroke:#9ca3af,color:#1f2933',
    'etape': 'fill:#e0ecff,stroke:#4a78c2,color:#10243f',
    'aidd': 'fill:#e4e1ff,stroke:#5b4fc7,color:#1d1554',
    'impeccable': 'fill:#ffe8cc,stroke:#d9822b,color:#3d2600',
    'marketing': 'fill:#dcf5e3,stroke:#3c9a5f,color:#0f3320',
    'outil': 'fill:#ececec,stroke:#8c8c8c,color:#262626',
    'sortie': 'fill:#e6f4ff,stroke:#3b82c4,color:#0b2a44',
    'preuve': 'fill:#f1e6ff,stroke:#8b5cc7,color:#2b1247',
    'controle': 'fill:#f6efe3,stroke:#b08a4f,color:#3a2a10',
    'validation': 'fill:#fff4c2,stroke:#c9a227,color:#3a2e00',
    'ok': 'fill:#d6f5d6,stroke:#2f8f46,color:#0d3318',
    'retour': 'fill:#eef2f7,stroke:#8a9bb0,color:#1f2933',
    'attente': 'fill:#fff0d6,stroke:#c98a2b,color:#3a2600',
    'stop': 'fill:#ffe0e0,stroke:#c24a4a,color:#3d0f0f',
}
FAMILIES = {
    'cadrage': ('Cadrage', 'fill:#f3f4f6,stroke:#9ca3af,color:#1f2933'),
    'decouvrir': ('Découvrir', 'fill:#dcf5e3,stroke:#3c9a5f,color:#0f3320'),
    'concevoir': ('Concevoir', 'fill:#ffe8cc,stroke:#d9822b,color:#3d2600'),
    'construire': ('Construire', 'fill:#e0ecff,stroke:#4a78c2,color:#10243f'),
    'ouvrir': ('Valider et ouvrir', 'fill:#f1e6ff,stroke:#8b5cc7,color:#2b1247'),
    'observer': ('Observer', 'fill:#d5f2f2,stroke:#2f8f8f,color:#0b3030'),
}
OUTCOME_LABELS = {'valide': 'valide', 'non_applicable': 'non applicable', 'a_preciser': 'à préciser', 'reparer': 'réparer',
                  'modifier_perimetre': 'modifier le périmètre', 'reorienter': 'réorienter', 'risque_technique': 'risque technique',
                  'clarifier_contrat': 'clarifier le contrat', 'mvp_integre': 'MVP intégré', 'autre_tranche': 'autre tranche',
                  'stabiliser': 'stabiliser', 'ameliorer': 'améliorer', 'attendre_information': 'attendre une information',
                  'attendre_acces': 'attendre un accès', 'attendre_validation': 'attendre une décision', 'arreter': 'arrêter'}
SPECIAL_LABELS = {'WAIT_INFO': 'Attendre une information', 'WAIT_ACCESS': 'Attendre un accès',
                  'WAIT_APPROVAL': 'Attendre une décision', 'STOP': 'Arrêter la branche',
                  'END': 'Fin de la boucle', 'RESUME': 'Reprendre la séquence mémorisée'}


def family(seq):
    phase = seq['phase']
    if phase is None:
        return 'cadrage'
    return 'decouvrir' if phase <= 4 else 'concevoir' if phase == 5 else 'construire' if phase <= 9 else 'ouvrir' if phase <= 11 else 'observer'


def quote(text):
    return json.dumps(text, ensure_ascii=False)


def short(text, limit=72):
    """Keep the first meaningful clause; fall back to a word boundary. The sheet keeps the full text."""
    text = text.rstrip('.')
    if len(text) <= limit:
        return text
    for separator in [' ; ', ' : ', ', puis ', ', ']:
        index = text.find(separator)
        if 24 <= index <= limit + 10:
            return text[:index] + ' …'
    return text[:limit].rsplit(' ', 1)[0] + ' …'


def plugin_groups(model, seq):
    """Plugins a sequence relies on: AIDD first, then Impeccable, marketing, project tools; always-on and case-by-case apart."""
    order = [('aidd', 'AIDD'), ('impeccable', 'Impeccable'), ('marketing', 'Marketing'), ('outil', 'Outils du projet')]
    groups = {}
    for cap in seq['action']['capabilities']:
        plugin, _, skill = cap['id'].partition(':')
        kind = 'outil' if cap.get('external') else 'aidd' if plugin.startswith('aidd-') else 'impeccable' if plugin == 'impeccable' else 'marketing' if plugin == 'marketing-skills' else 'outil'
        name = (cap['id'].replace('_', ' ') if kind == 'outil' else f'{plugin.removeprefix("aidd-")}/{skill}' if kind == 'aidd'
                else cap.get('command') or '$impeccable' if kind == 'impeccable' else skill)
        conditional = bool(cap.get('if') or cap.get('if_text'))
        groups.setdefault((kind, conditional), []).append(name)
    return [(kind, label, conditional, groups[(kind, conditional)]) for kind, label in order for conditional in (False, True) if (kind, conditional) in groups]


def sequence_mermaid(model, seq):
    """One sequence contract, top to bottom, in the seven numbered rubrics."""
    sid = seq['id']
    titles = {item['id']: item['title'] for item in model['sequences']}
    out = ['---', f'title: {quote(f"{sid} — {seq["title"]}")}', '---', 'flowchart TB']
    classes = {}
    def node(name, label, cls, shape='[]'):
        open_, close = shape[0], shape[1]
        out.append(f'    {name}{open_}{quote(label)}{close}')
        classes.setdefault(cls, []).append(name)
    out.append(f'  subgraph Entrees[{quote("1 · Entrées")}]')
    inputs = seq['input'] or ['intention']
    for key in inputs:
        node(f'Entree{key.capitalize()}', model['artifacts'][key]['title'] if key in model['artifacts'] else model['scope']['start'], 'entree')
    out.append('  end')
    out.append(f'  Responsable[{quote("2 · Responsable : " + seq["responsible"])}]')
    classes.setdefault('responsable', []).append('Responsable')
    out.append(f'  subgraph Action[{quote("3 · Action : " + seq["title"])}]')
    out.append('    direction TB')
    steps = seq['action']['steps']
    for index, step in enumerate(steps, 1):
        node(f'Etape{index}', f'{index}. {short(step)}', 'etape')
    out.append('  end')
    groups = plugin_groups(model, seq)
    plugin_blocks = []
    for conditional, title in [(False, 'Plugins mobilisés'), (True, 'Plugins selon le cas')]:
        members = [(kind, label, items) for kind, label, cond, items in groups if cond == conditional]
        if not members:
            continue
        block = 'PluginsCas' if conditional else 'Plugins'
        out.append(f'  subgraph {block}[{quote(title)}]')
        out.append('    direction TB')
        block_nodes = []
        for kind, label, items in members:
            chunks = [items[index:index + 4] for index in range(0, len(items), 4)]
            for part, chunk in enumerate(chunks, 1):
                suffix = f' ({part}/{len(chunks)})' if len(chunks) > 1 else ''
                block_nodes.append(f'{block}{kind.capitalize()}{part if len(chunks) > 1 else ""}')
                node(block_nodes[-1], f'{label}{suffix} : {", ".join(chunk)}', kind)
        out.append('  end')
        plugin_blocks.append((block, block_nodes, conditional))
    out.append(f'  subgraph Sortie[{quote("4 · Sortie")}]')
    for key in seq['output']:
        node(f'Sortie{key.capitalize()}', model['artifacts'][key]['title'], 'sortie')
    out.append('  end')
    out.append(f'  subgraph Preuves[{quote("5 · Preuves")}]')
    for proof in seq['evidence']:
        node(f'Preuve{"".join(part.capitalize() for part in proof["id"].split("_"))}', short(proof['description'], 110), 'preuve')
    out.append('  end')
    agents = [(name, agent['codex']) for name, agent in model.get('agents', {}).items() if sid in agent.get('sequences', [])]
    if agents or sid == 'S90':
        out.append(f'  subgraph Controle[{quote("6 · Contrôle indépendant")}]')
        for name, codex in agents or [('sdlc', 'relecteur natif du SDLC')]:
            node(f'Agent{name.capitalize()}', codex, 'controle')
        out.append('  end')
    out.append(f'  Validation{{{quote("7 · Validation par " + seq["validation"]["by"])}}}')
    classes.setdefault('validation', []).append('Validation')
    targets = {}
    for outcome, destinations in seq['next'].items():
        for target in destinations if isinstance(destinations, list) else [destinations]:
            targets.setdefault(target, []).append(OUTCOME_LABELS.get(outcome, outcome.replace('_', ' ')))
    for target, outcomes in targets.items():
        name = f'Vers{target}'
        label = (f'{sid} · reprendre cette séquence' if target == sid else f'{target} · {titles[target]}' if target in titles
                 else SPECIAL_LABELS[target])
        cls = ('ok' if 'valide' in outcomes or 'MVP intégré' in outcomes else 'stop' if target == 'STOP'
               else 'attente' if target.startswith('WAIT') else 'retour')
        out.append(f'  {name}[{quote(label)}]')
        classes.setdefault(cls, []).append(name)
    out += ['  Entrees --> Responsable', '  Responsable -- "conduit" --> Action']
    out += [f'  Etape{index} --> Etape{index + 1}' for index in range(1, len(steps))]
    for block, block_nodes, conditional in plugin_blocks:
        out.append(f'  Action -. "selon le cas" .-> {block}' if conditional else f'  Action -- "mobilise" --> {block}')
        out += [f'  {upper} ~~~ {lower}' for upper, lower in zip(block_nodes, block_nodes[1:])]
    out += ['  Action --> Sortie', '  Sortie --> Preuves']
    out += ['  Preuves --> Controle', '  Controle --> Validation'] if agents or sid == 'S90' else ['  Preuves --> Validation']
    ordered = sorted(targets, key=lambda target: 0 if ('valide' in targets[target] or 'MVP intégré' in targets[target]) else 2 if target in SPECIAL_LABELS else 1)
    out += [f'  Vers{upper} ~~~ Vers{lower}' for upper, lower in zip(ordered, ordered[1:])]
    for target, outcomes in targets.items():
        arrow = '==>' if 'valide' in outcomes or 'MVP intégré' in outcomes else '-->'
        out.append(f'  Validation {arrow[:2]} {quote(" / ".join(outcomes))} {arrow} Vers{target}' if arrow == '==>' else f'  Validation -- {quote(" / ".join(outcomes))} --> Vers{target}')
    out += [f'  classDef {name} {CLASSES[name]}' for name in classes]
    out += [f'  class {",".join(names)} {name}' for name, names in classes.items()]
    for group in ['Entrees', 'Action', 'Plugins', 'PluginsCas', 'Sortie', 'Preuves', 'Controle']:
        if f'subgraph {group}[' in '\n'.join(out):
            out.append(f'  style {group} fill:#fbfcfe,stroke:#cbd5e1')
    return '\n'.join(out) + '\n'


def overview_mermaid(model):
    """All sequences grouped by phase, colored by stage, with the plugin families they mobilise."""
    out = ['---', 'title: "Parcours flow-aidd — phases, séquences et plugins mobilisés"', '---', 'flowchart TB']
    phases = [(None, 'Cadrage transversal')] + [(phase['id'], f'Phase {phase["id"]} · {phase["title"]}') for phase in model['phases']]
    members = {}
    for phase_id, label in phases:
        sequences = [seq for seq in model['sequences'] if seq['phase'] == phase_id]
        group = f'Phase{phase_id if phase_id is not None else "Cadrage"}'
        out.append(f'  subgraph {group}[{quote(label)}]')
        for seq in sequences:
            plugins = ', '.join(dict.fromkeys(label for _, label, _, _ in plugin_groups(model, seq) if label != 'Outils du projet'))
            out.append(f'    Sequence{seq["id"]}[{quote(seq["id"] + " · " + seq["title"] + (" · " + plugins if plugins else ""))}]')
            members.setdefault(family(seq), []).append(f'Sequence{seq["id"]}')
        out.append('  end')
    groups = [f'Phase{phase_id if phase_id is not None else "Cadrage"}' for phase_id, _ in phases]
    out += [f'  {upper} ~~~ {lower}' for upper, lower in zip(groups, groups[1:])]
    phase_of = {seq['id']: seq['phase'] or 0 for seq in model['sequences']}
    for seq in model['sequences']:
        for dep in seq['requires']:
            if seq.get('applicability'):
                out.append(f'  Sequence{dep} -. "si applicable" .-> Sequence{seq["id"]}')
            elif phase_of[seq['id']] - phase_of[dep] > 1:
                out.append(f'  Sequence{dep} -.-> Sequence{seq["id"]}')
            else:
                out.append(f'  Sequence{dep} --> Sequence{seq["id"]}')
    out += [f'  classDef {name} {FAMILIES[name][1]}' for name in members]
    out += [f'  class {",".join(names)} {name}' for name, names in members.items()]
    out += [f'  style Phase{phase_id if phase_id is not None else "Cadrage"} fill:#fbfcfe,stroke:#cbd5e1' for phase_id, _ in phases]
    return '\n'.join(out) + '\n'


def example_state(model):
    context = deepcopy(model['example']['context'])
    actors = {'porteur':'porteur_fictif','coordinateur':'coordinateur_fictif','verificateur':'verificateur_fictif','relecteur':'relecteur_fictif','integration':context['integration_owner'],'exploitation':context['operations_owner']}
    active = [seq for seq in model['sequences'] if not seq.get('applicability') or context[seq['applicability']['field']] == seq['applicability']['equals']]
    artifacts = {key:{'path':f'illustration://{key}','version':'illustration-v1'} for seq in active for key in seq['output']}
    state = {'flow_version':model['version'],'mode':'illustration','project':'MiniRévisions — cas fictif','current_sequence':'S121','resume_sequence':None,'context':context,'actors':actors,'artifacts':artifacts,'evidence':{},'sequences':{},'history':[]}
    for seq in model['sequences']:
        sid = seq['id']
        condition = seq.get('applicability')
        if condition and context[condition['field']] != condition['equals']:
            state['sequences'][sid] = {'status':'non_applicable','reason':f'Le cadrage illustratif indique {condition["field"]} = {context[condition["field"]]}, contrairement à la condition d’application.','context_ref':'S00:cadre_decide','context_version':artifacts['cadre']['version'],'marked_by':actors['coordinateur']}
            continue
        inputs = seq['input'] + [key for key in seq.get('input_optional', []) if key in artifacts]
        record = {'status':'valide','outcome':'mvp_integre' if sid == 'S91' else 'stabiliser' if sid == 'S121' else 'valide','used_versions':{key:artifacts[key]['version'] for key in inputs},'produced_versions':{key:artifacts[key]['version'] for key in seq['output']},'validator_role':seq['validation']['by'],'validated_by':actors[seq['validation']['by']],'validated_at':model['updated']+'T00:00:00+01:00','performed_by':'executeur_fictif' if sid == 'S90' else actors[seq['responsible']],'evidence_ids':[]}
        for criterion in seq['evidence']:
            eid = f'{sid}:{criterion["id"]}'
            kind = criterion['kind']
            actor = actors['relecteur'] if criterion.get('independent') else actors['porteur'] if kind == 'decision' else actors['verificateur']
            state['evidence'][eid] = {'sequence':sid,'criterion':criterion['id'],'kind':kind,'actor':actor,'artifact':seq['output'][0],'version':artifacts[seq['output'][0]]['version'],'reference':f'illustration://{sid}/{criterion["id"]}','result':'approved' if kind == 'decision' else 'observed' if kind in ['observation','access'] else 'passed','simulated':True}
            record['evidence_ids'].append(eid)
        state['sequences'][sid] = record
    return state


def phase_label(model, seq):
    title = next((phase['title'] for phase in model['phases'] if phase['id'] == seq['phase']), None)
    return f'{seq["phase"]} — {title}' if title else 'Cadrage transversal'


def scope_lines(model):
    """Depth and adaptation guidance, read while framing the project at S00."""
    scope = model['scope']
    lines = ['## Adapter la profondeur au projet', '',
             '**Objectif du flow :** ' + scope['purpose'], '', '**Point de départ :** ' + scope['start'], '',
             '**MVP livré :** ' + scope['delivered'], '', '**Fin de la première boucle :** ' + scope['learning_end'], '',
             '**Projets concernés :**', '', paragraph_list(scope['supported']), '',
             '**Profondeur et adaptation :**', '', paragraph_list(scope['adaptation']), '',
             '**Limites :**', '', paragraph_list(scope['boundaries']), '',
             '**Informations à préciser progressivement.** Une inconnue peut rester ouverte pendant l’idéation ; l’aider à se résoudre au plus tard avant la séquence qui l’utilise, sans la transformer en réponse négative.', '']
    lines += [f'- `{field}` — {definition["description"]} À résoudre avant : {", ".join(definition["required_at"])}.' for field, definition in model['context_fields'].items()]
    return lines + ['']


def documents(model):
    """Views the skill loads at run time, relative to references/."""
    files = {}
    ids = [seq['id'] for seq in model['sequences']]
    generated = '> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.\n\n'
    glossary = ['# Glossaire', '', generated, 'Définitions pour lire le flow ; chaque exemple illustre un terme et ne constitue pas une preuve sur un projet réel.', '']
    for term in model['glossary']:
        glossary += [f'<a id="{term["id"]}"></a>', '', f'## {term["term"]}', '', term['definition'], '', '**Exemple :** '+term['example'], '']
    glossary += ['<a id="roles"></a>', '', '## Rôles', '', paragraph_list([actor_label(model, role) for role in model['roles']]), '']
    files['glossaire.md'] = '\n'.join(glossary)
    index = ['# Parcours', '', generated, f'{len(model["phases"])} phases de référence et {len(ids)} séquences. Le nombre d’actions varie ; le contrat de chaque séquence est stable.', '', '| Séquence | Phase | Intention | Prérequis |', '| --- | --- | --- | --- |']
    for seq in model['sequences']:
        index.append(f'| [{seq["id"]}](sequences/{seq["id"]}.md) | {phase_label(model, seq)} | {seq["title"]} | {", ".join(seq["requires"]) or "Intention ou état existant"} |')
    index += ['', 'Les prérequis indiquent l’ordre possible ; la table **Prochaine destination** de chaque fiche décide du routage selon le résultat. Une séquence ne se déduit pas terminée de l’existence d’un fichier.', '', 'Les séquences S50/S51 et S60 ont des conditions explicites. Une non-applicabilité est conservée avec sa raison et le cadrage approuvé ; un prérequis déjà satisfait peut être réutilisé avec une preuve actuelle.', '']
    files['parcours.md'] = '\n'.join(index)
    rules = ['# Règles complètes', '', generated, 'La liste exhaustive, pour le vérificateur et les cas de doute. En conduite courante, [socle.md](socle.md) et la référence de la commande suffisent.', '',
             '<a id="rubriques"></a>', '', '## Les sept rubriques d’une séquence', '', '| Rubrique | Ce qu’elle doit préciser |', '| --- | --- |']
    rules += [f'| **{field}** | {description} |' for field, description in model['contract'].items()]
    rules += ['', 'Les emplacements `natif_conditionnel` s’appliquent si le skill natif est invoqué. `propose` est une convention du guide et `a_resoudre` demande une résolution lors du travail réel. Ces gabarits ne sont pas des fichiers déjà créés.', '',
              '<a id="regles"></a>', '', '## Règles de conduite', '']
    rules += [f'{number}. {rule}' for number, rule in enumerate(model['policies'], 1)]
    rules += ['', '<a id="statuts"></a>', '', '## Statuts d’une séquence', '', '| Statut | Sens |', '| --- | --- |']
    rules += [f'| `{status}` | {description} |' for status, description in model['statuses'].items()]
    rules += ['', '<a id="boucles"></a>', '', '## Boucles', '', 'Après S91, l’issue `autre_tranche` ouvre une nouvelle itération de S80 : conserver l’ancien état dans history, identifier la nouvelle demande et réexaminer les validations affectées. L’issue `mvp_integre` conduit à la recette S100.', '', 'À S120, une fenêtre incomplète conserve `attente_info`. Zéro usage mesuré sur une fenêtre complète est une observation possible ; une mesure absente ne vaut pas zéro usage.', '', 'Une entrée modifiée rend ses validations dépendantes candidates à réexamen ; réexamen ne signifie pas reconstruction obligatoire. Les contrôles locaux ne vérifient pas les services distants ni la vérité d’un entretien.', '']
    files['regles.md'] = '\n'.join(rules)
    for seq in model['sequences']:
        sid = seq['id']
        text = [f'# {sid} — {seq["title"]}', '', '> Fiche générée depuis `workflow.json`. Les réponses et preuves du cas d’école restent illustratives.', '', f'**Phase :** {phase_label(model, seq)} · **Prérequis :** {", ".join(seq["requires"]) or "Aucun"}.', '']
        if seq.get('applicability'):
            condition = seq['applicability']
            text += [f'**Applicabilité :** `{condition["field"]} == {str(condition["equals"]).lower()}`. Une valeur inconnue exige une clarification ; une valeur fausse justifie une non-applicabilité tracée.', '']
        text += ['## 1. Entrée', '', artifact_lines(model, seq['input']) or model['scope']['start'], '']
        if seq.get('input_optional'):
            text += ['**À lire si disponible et pertinent :**', '', artifact_lines(model, seq['input_optional']), '']
        text += ['## 2. Responsable', '', actor_label(model, seq['responsible']), '', f'**Validation par :** {actor_label(model, seq["validation"]["by"])}', '', '## 3. Action', '', seq['action']['summary'], '']
        text += capability_lines(model, seq['action']['capabilities'])
        text += ['', '**Étapes :**', '']+[f'{index}. {step}' for index, step in enumerate(seq['action']['steps'], 1)]+['']
        for question in seq['action']['questions']:
            text += ['**Question :** '+question['question'], '', '**Réponse acceptable, illustrative :** '+question['acceptable'], '', '**Réponse insuffisante :** '+question['insufficient'], '']
        if seq['validation']['by'] == 'porteur' or seq['action']['questions']:
            text += ['**Cadence :** deux ou trois questions liées par tour, puis attendre la réponse. Partir de ce que le projet sait déjà, proposer la lecture la plus probable et la faire corriger ; la réponse illustrative montre le niveau de précision visé, jamais la réponse du porteur. Détail : [entretien.md](../entretien.md).', '']
        if seq['action'].get('invocation'):
            text += ['**Requête à compléter avec une source réelle avant tout appel :**', '', '```text', seq['action']['invocation']['template'], '```', '', 'Le premier mot est exactement `interactive`. Vérifier le mode et la version du skill au moment de l’appel ; cette fiche n’exécute pas la requête.', '']
        if sid == 'S00':
            text += scope_lines(model)
        text += ['## 4. Sortie', '', artifact_lines(model, seq['output']), '', '## 5. Preuve', '', paragraph_list([f'`{proof["id"]}` ({proof["kind"]}) — {proof["description"]}' for proof in seq['evidence']]), '', 'Chaque preuve indique sa source, son auteur et la version de l’artefact concerné. Un exemple ou une simulation ne valide pas une instance réelle.', '', '## 6. Validation', '', paragraph_list(seq['validation']['criteria']), '', 'Conserver le rôle et l’identité du validateur, la date, les versions et les preuves. Une réserve acceptée indique son manque, sa raison, son responsable et sa prochaine vérification.', '', '## 7. Prochaine destination', '', '| Issue observée ou décidée | Destination |', '| --- | --- |']
        for outcome, destinations in seq['next'].items():
            targets = destinations if isinstance(destinations, list) else [destinations]
            labels = [f'[{target}]({target}.md)' if target in ids else f'**{target}** — {model["special_targets"][target]}' for target in targets]
            text.append(f'| {outcome.replace("_", " ")} | {" ; ".join(labels)} |')
        text += ['', '## Avant de terminer', '']
        count = len(seq['validation']['criteria'])
        text += ['- Le critère de la rubrique 6 est satisfait par une preuve nommée, pas seulement affirmé.' if count == 1
                 else f'- Les {count} critères de la rubrique 6 sont satisfaits par une preuve nommée, pas seulement affirmés.']
        text += ['- Preuves enregistrées avec leur source et la version exacte de l’artefact : ' + ', '.join(f'`{proof["id"]}`' for proof in seq['evidence']) + '.']
        agents = [agent['codex'] for agent in model.get('agents', {}).values() if sid in agent.get('sequences', [])]
        if agents:
            text += ['- Verdict rendu par ' + ' et '.join(f'`{name}`' for name in agents) + ', ou leur absence dite au porteur.']
        text += ['- Résultat, limites et suite présentés avec `checkpoint` ; rien n’est lancé pour la suite avant `approve` ([checkpoint.md](../checkpoint.md)).']
        text += ['', '## Cas d’école', '', '**Illustration fictive :** '+seq['example'], '', '[Parcours](../parcours.md) · [Glossaire](../glossaire.md) · [Règles](../regles.md)', '']
        files[f'sequences/{sid}.md'] = '\n'.join(text)
    template = {'flow_version':model['version'],'mode':'reel','project':None,'current_sequence':'S00','resume_sequence':None,'context':{field:None for field in model['context_fields']},'actors':{role:None for role in model['roles']},'artifacts':{},'evidence':{},'sequences':{'S00':{'status':'a_faire'}},'history':[]}
    files['templates/etat.json'] = dump(template)
    files.update(degraded_agents(model))
    return files


def doc_pages(model):
    """Human-oriented pages kept in the repository docs/, outside the installed skill."""
    files = {}
    generated = '> Généré depuis `skills/flow-aidd/references/workflow.json` par `tools/build.py`. Ne pas modifier à la main.\n\n'
    overview = overview_mermaid(model)
    files['schemas/00-prerequis.mmd'] = overview
    schemas = ['# Schémas des séquences', '', generated, 'Le premier schéma montre tout le parcours de haut en bas : un bloc par phase, dans l’ordre, chaque séquence avec les plugins qu’elle mobilise. Les flèches pleines suivent la ligne principale ; un pointillé simple relie un prérequis éloigné de plusieurs phases, un pointillé « si applicable » une séquence conditionnelle. Couleurs des séquences : gris cadrage, vert découvrir (phases 1 à 4), orange concevoir (5), bleu construire (6 à 9), violet valider et ouvrir (10 et 11), turquoise observer (12).', '', 'Chaque contrat se lit de haut en bas, dans l’ordre des sept rubriques : 1 entrées, 2 responsable, 3 action et ses étapes, avec à côté les plugins mobilisés (indigo AIDD, orange Impeccable, vert marketing-skills, gris outils du projet), dans un bloc « Plugins mobilisés » relié par une flèche pleine et un bloc « Plugins selon le cas » relié en pointillés, 4 sortie, 5 preuves, 6 contrôle indépendant, 7 validation. Les flèches qui partent de la validation montrent toutes les suites possibles : en vert et en trait épais la suite validée, en gris un retour, en orange une attente, en rouge un arrêt. La fiche de chaque séquence reste la référence complète.', '', '```mermaid', overview.rstrip(), '```', '', '## Contrats détaillés', '']
    for seq in model['sequences']:
        diagram = sequence_mermaid(model, seq)
        files[f'schemas/{seq["id"]}.mmd'] = diagram
        schemas += [f'### {seq["id"]} — {seq["title"]}', '', '```mermaid', diagram.rstrip(), '```', '', f'Lire le [contrat complet](../../skills/flow-aidd/references/sequences/{seq["id"]}.md) pour les questions, capacités, critères de preuve et destinations.', '']
    files['schemas/schemas.md'] = '\n'.join(schemas)
    sample = example_state(model)
    files['exemple/minirevisions.etat.json'] = dump(sample)
    example = ['# Exemple complet — MiniRévisions', '', generated, '**CAS FICTIF — AUCUNE PREUVE RÉELLE.** '+model['example']['premise'], '', '**Parcours critique :** '+model['example']['critical_task'], '', '**Exclusions :** '+', '.join(model['example']['exclusions'])+'.', '', '## Cadrage illustratif', '', '```json', dump(model['example']['context']).rstrip(), '```', '', 'Les emplacements `illustration://` du fichier d’état sont des identifiants de cas d’école. Ils ne représentent pas un service ou un fichier produit. Toutes ses preuves portent `simulated: true` et son mode est `illustration`.', '', '## Parcours de bout en bout', '']
    from flow import capability_plan
    for seq in model['sequences']:
        record = sample['sequences'][seq['id']]
        plan = capability_plan(model, seq, sample)
        named = lambda entries: ', '.join(f'`{entry["id"]}`' + (f' · `{entry["command"]}`' if entry.get('command') else '') for entry in entries if not entry.get('external')) or '—'
        controls = [agent['codex'] for agent in model.get('agents', {}).values() if seq['id'] in agent.get('sequences', [])]
        example += [f'### {seq["id"]} — {seq["title"]}', '', seq['example'], '', '| Rubrique | Dans le cas d’école |', '| --- | --- |', f'| Entrée | {", ".join(seq["input"]) or "Intention de départ"} |', f'| Responsable | {sample["actors"][seq["responsible"]]} |', f'| Action | {seq["action"]["summary"]} |',
                    f'| Capacités pour ce cas | {named(plan["utiliser"])} ; selon le cas : {named(plan["selon_le_cas"])} ; écartées : {named(plan["ecartees"])} |',
                    f'| Contrôle indépendant | {", ".join(f"`{name}`" for name in controls) or "Relecteur natif du SDLC"} |', f'| Sortie | {", ".join(seq["output"]) if record["status"] != "non_applicable" else "Aucun livrable de spike ; justification de non-applicabilité"} |', f'| Preuve | {", ".join(record.get("evidence_ids", [])) or record["context_ref"]} — illustration uniquement |', f'| Validation | {record["status"]} dans la simulation ; aucune validation réelle |', f'| Destination | {seq["next"].get(record.get("outcome", "non_applicable"))} |', '']
    example += ['## Variantes à comprendre', '', '- Si un test de code échoue à S90, conserver la séquence et réparer dans Deliver ; ne pas retourner arbitrairement au backlog.', '- Si la fenêtre d’observation n’est pas terminée, S120 reste en `attente_info` avec le manque nommé.', '- Si le MVP change de version, les séquences qui utilisaient l’ancienne version sont à réexaminer ; la note d’intention ne devient pas automatiquement fausse.', '- Si le projet n’a pas d’interface graphique, tracer les non-applicabilités S50 et S51 à partir du cadrage approuvé.', '- Si seule une PR en brouillon existe, S91 reste à faire et S100 ne peut pas être déclarée validée.', '', 'L’instance [minirevisions.etat.json](minirevisions.etat.json) illustre la structure de reprise. Un contrôle de cohérence de cet exemple ne prouve ni une livraison réelle ni la facilité du parcours pour un novice.', '']
    example += ['## Livrables remplis', '', 'Lire les [notes et contrats renseignés](livrables.md) : intention, périmètre avec critères, demande prête, différence entre sortie et preuve, puis reprise en attente.', '']
    files['exemple/exemple.md'] = '\n'.join(example)
    filled = ['# MiniRévisions — livrables renseignés', '', '**Exemple fictif, aucune exécution ni observation réelle du produit.** Les notes ci-dessous montrent le niveau de précision recherché ; elles ne constituent pas un projet lancé.', '']
    for item in model['example']['deliverables']:
        filled += [f'<a id="{item["id"]}"></a>', '', f'## {item["title"]}', '', paragraph_list(item['content']), '']
    filled += ['[Revenir au parcours complet](exemple.md)', '']
    files['exemple/livrables.md'] = '\n'.join(filled)
    return files


def build(model, root: Path, check=False, docs_root: Path | None = None):
    """Write or verify the skill views under root, and the human pages under docs_root when given."""
    targets = [(root, documents(model))] + ([(docs_root, doc_pages(model))] if docs_root else [])
    changed, count = [], 0
    for base, files in targets:
        count += len(files)
        for relative, expected in files.items():
            destination = base / relative
            if not destination.is_file() or destination.read_text() != expected:
                changed.append(str(destination.relative_to(base.parent)) if base is docs_root else relative)
                if not check:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(expected)
    print(json.dumps({'mode':'verification' if check else 'generation','fichiers':count,'differences':changed,'source':'workflow.json'},ensure_ascii=False,indent=2))
    return 1 if check and changed else 0
