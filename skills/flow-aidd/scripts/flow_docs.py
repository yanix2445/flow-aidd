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


def plugin_groups(model, seq):
    """Name the plugins a sequence relies on, grouped like the flow: AIDD first, then Impeccable, marketing, project tools."""
    groups = {'AIDD': [], 'Impeccable': [], 'Marketing': [], 'Outils du projet': []}
    for cap in seq['action']['capabilities']:
        mark = '*' if cap.get('if') or cap.get('if_text') else ''
        plugin, _, skill = cap['id'].partition(':')
        if cap.get('external'):
            groups['Outils du projet'].append(cap['id'].replace('_', ' '))
        elif plugin.startswith('aidd-'):
            groups['AIDD'].append(f'{plugin.removeprefix("aidd-")}/{skill}{mark}')
        elif plugin == 'impeccable':
            groups['Impeccable'].append((cap.get('command') or 'impeccable') + mark)
        elif plugin == 'marketing-skills':
            groups['Marketing'].append(skill + mark)
    return [(name, items) for name, items in groups.items() if items]


def sequence_mermaid(model, seq):
    sid = seq['id']
    title = json.dumps(f'{sid} — {seq["title"]}', ensure_ascii=False)
    success = seq['next'].get('valide', next(iter(seq['next'].values())))
    success_label = ', '.join(success) if isinstance(success, list) else success
    groups = plugin_groups(model, seq)
    agents = [name for name, agent in model.get('agents', {}).items() if sid in agent.get('sequences', [])]
    nodes = [
        ('Entree', 'Entrée : ' + (', '.join(seq['input']) or model['scope']['start'])),
        ('Responsable', 'Responsable : ' + seq['responsible']),
        ('Action', 'Action : ' + seq['title']),
    ]
    if groups:
        nodes.append(('Plugins', '<br/>'.join(f'{name} : {", ".join(items)}' for name, items in groups)))
    nodes += [
        ('Sortie', 'Sortie : ' + ', '.join(seq['output'])),
        ('Preuve', 'Preuves : ' + ', '.join(item['id'].replace('_', ' ') for item in seq['evidence'])),
    ]
    if agents:
        nodes.append(('Controle', 'Contrôle indépendant : ' + ', '.join(agents)))
    elif sid == 'S90':
        nodes.append(('Controle', 'Contrôle indépendant : relecteur natif du SDLC'))
    nodes += [
        ('Validation', 'Validation par ' + seq['validation']['by'] + ' : critères et preuves satisfaits ?'),
        ('Destination', 'Suite validée : ' + success_label),
        ('AutreIssue', 'Sinon : préciser, réparer ou attendre selon le tableau'),
    ]
    out = ['---', f'title: {title}', '---', 'flowchart TB']
    for name, label in nodes:
        quoted = json.dumps(label, ensure_ascii=False)
        out.append(f'  {name}{{{quoted}}}' if name == 'Validation' else f'  {name}[{quoted}]')
    chain = [name for name, _ in nodes if name not in ('Destination', 'AutreIssue')]
    out += [f'  {a} --> {b}' for a, b in zip(chain, chain[1:])]
    out += ['  Validation -- "Oui" --> Destination', '  Validation -- "Non ou inconnu" --> AutreIssue']
    if groups:
        out += ['  classDef plugins fill:#eef3fb,stroke:#7f9cc7', '  class Plugins plugins']
    if agents or sid == 'S90':
        out += ['  classDef controle fill:#f6f0e6,stroke:#b08a4f', '  class Controle controle']
    return '\n'.join(out) + '\n'


def overview_mermaid(model):
    out = ['---', 'title: "Prérequis des séquences — le routage est détaillé dans chaque fiche"', '---', 'flowchart TB']
    for seq in model['sequences']:
        out.append(f'  Sequence{seq["id"]}[{json.dumps(seq["id"] + " · " + seq["title"], ensure_ascii=False)}]')
    for seq in model['sequences']:
        for dep in seq['requires']:
            condition = seq.get('applicability')
            out.append(f'  Sequence{dep} -. "Si applicable" .-> Sequence{seq["id"]}' if condition else f'  Sequence{dep} --> Sequence{seq["id"]}')
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
    schemas = ['# Schémas des séquences', '', generated, 'Les flèches du premier schéma montrent les prérequis, pas une validation automatique. Pour une séquence conditionnelle, une non-applicabilité tracée peut satisfaire le prérequis. Les tables de chaque fiche portent les retours et attentes. Dans chaque contrat, le bloc bleu nomme les plugins mobilisés (AIDD, Impeccable, marketing-skills, outils du projet) et le bloc beige les agents de contrôle ; `*` signale une capacité activée seulement selon le contexte ou le cas.', '', '```mermaid', overview.rstrip(), '```', '', '## Contrats détaillés', '']
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
