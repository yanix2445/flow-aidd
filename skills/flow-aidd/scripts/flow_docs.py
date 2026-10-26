"""Derive every current guide and the labelled example from workflow.json."""
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


def sequence_mermaid(model, seq):
    sid = seq['id']
    title = json.dumps(f'{sid} — {seq["title"]}', ensure_ascii=False)
    success = seq['next'].get('valide', next(iter(seq['next'].values())))
    success_label = ', '.join(success) if isinstance(success, list) else success
    nodes = [
        ('Entree', 'Entrée : ' + (', '.join(seq['input']) or model['scope']['start'])),
        ('Responsable', 'Responsable : ' + seq['responsible']),
        ('Action', 'Activer la capacité puis : ' + seq['title']),
        ('Sortie', 'Sortie : ' + ', '.join(seq['output'])),
        ('Preuve', 'Preuves : ' + ', '.join(item['id'].replace('_', ' ') for item in seq['evidence'])),
        ('Validation', 'Validation par ' + seq['validation']['by'] + ' : critères et preuves satisfaits ?'),
        ('Destination', 'Suite validée : ' + success_label),
        ('AutreIssue', 'Sinon : préciser, réparer ou attendre selon le tableau'),
    ]
    out = ['---', f'title: {title}', '---', 'flowchart TB']
    for name, label in nodes:
        quoted = json.dumps(label, ensure_ascii=False)
        out.append(f'  {name}{{{quoted}}}' if name == 'Validation' else f'  {name}[{quoted}]')
    out += ['  Entree --> Responsable', '  Responsable --> Action', '  Action --> Sortie', '  Sortie --> Preuve', '  Preuve --> Validation', '  Validation -- "Oui" --> Destination', '  Validation -- "Non ou inconnu" --> AutreIssue']
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


def documents(model):
    files = {}
    ids = [seq['id'] for seq in model['sequences']]
    generated = '> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.\n\n'
    scope = ['# Périmètre du flow', '', generated, '**Objectif :** '+model['scope']['purpose'], '', '**Point de départ :** '+model['scope']['start'], '', '**MVP livré :** '+model['scope']['delivered'], '', '**Fin de la première boucle :** '+model['scope']['learning_end'], '', '## Projets concernés', '', paragraph_list(model['scope']['supported']), '', '## Profondeur et adaptation', '', paragraph_list(model['scope']['adaptation']), '', '## Limites', '', paragraph_list(model['scope']['boundaries']), '', '## Responsabilités', '', paragraph_list([actor_label(model, role) for role in model['roles']]), '']
    scope += ['## Informations à préciser progressivement', '', 'Une inconnue peut rester ouverte pendant l’idéation. Le coordinateur aide à la résoudre au plus tard avant la séquence qui l’utilise ; il ne transforme pas une inconnue en réponse négative.', '']
    scope += [f'- {definition["description"]} À résoudre avant : {", ".join(definition["required_at"])}.' for definition in model['context_fields'].values()]
    scope += ['']
    files['SCOPE.md'] = '\n'.join(scope)
    glossary = ['# Glossaire', '', generated, 'Définitions pour lire le flow ; chaque exemple illustre un terme et ne constitue pas une preuve sur un projet réel.', '']
    for term in model['glossary']:
        glossary += [f'<a id="{term["id"]}"></a>', '', f'## {term["term"]}', '', term['definition'], '', '**Exemple :** '+term['example'], '']
    files['GLOSSAIRE.md'] = '\n'.join(glossary)
    index = ['# Carte du parcours', '', generated, f'{len(model["phases"])} phases de référence et {len(ids)} séquences. Le nombre d’actions varie ; le contrat de chaque séquence est stable.', '', '| Séquence | Phase | Intention | Prérequis |', '| --- | --- | --- | --- |']
    for seq in model['sequences']:
        index.append(f'| [{seq["id"]}](sequences/{seq["id"]}.md) | {seq["phase"] or "Transversal"} | {seq["title"]} | {", ".join(seq["requires"]) or "Intention ou état existant"} |')
    index += ['', 'Les flèches de [MERMAID.md](MERMAID.md) montrent les prérequis. La table **Prochaine destination** de chaque fiche décide du routage selon le résultat. Une séquence ne se déduit pas terminée de l’existence d’un fichier.', '', 'Les séquences S50/S51 et S60 ont des conditions explicites. Une non-applicabilité est conservée avec sa raison et le cadrage approuvé ; un prérequis déjà satisfait peut être réutilisé avec une preuve actuelle.', '']
    files['FLOW.md'] = '\n'.join(index)
    orchestration = ['# Conduire et reprendre une séquence', '', generated, '## Règles de conduite', '']
    orchestration += [f'{index}. {rule}' for index, rule in enumerate(model['policies'], 1)]
    orchestration += ['', '## Statuts de l’instance', '', '| Statut | Sens |', '| --- | --- |']
    orchestration += [f'| `{status}` | {description} |' for status, description in model['statuses'].items()]
    orchestration += ['', '## Mise à jour de l’état', '', 'Le helper `project_flow.py init` prépare la nouvelle instance depuis le gabarit embarqué. Le coordinateur renseigne acteurs et cadrage à S00 avec `record` ; les autres éléments arrivent progressivement. Les utilisateurs n’éditent pas le JSON.', '', '- `artifacts` : emplacement réel et version du contenu propriétaire.', '- `evidence` : source, auteur, type, résultat, artefact et version ; une approbation est une preuve de décision, pas un simple oui sans référence.', '- `sequences` : statut, issue, versions utilisées et produites, preuves liées, validateur et date.', '- `current_sequence` : travail courant ; `resume_sequence` : travail à reprendre après un spike.', '- `history` : décisions et instantanés utiles avant une nouvelle itération. Ne pas écraser les preuves de l’itération précédente.', '', 'Une entrée modifiée rend ses validations dépendantes candidates à réexamen. Le coordinateur vérifie l’impact ; il peut réutiliser un livrable resté pertinent après revue, en conservant la nouvelle justification. Réexamen ne signifie pas reconstruction obligatoire.', '', '## Au début et à la fin d’une séance', '', 'Au début : lire l’état, contrôler les versions, puis la fiche courante et les seules sources nécessaires. S’il manque une information indispensable, la nommer et attendre ; les tâches indépendantes déjà autorisées peuvent continuer.', '', 'Avant interruption : conserver résultats et versions, les preuves disponibles, la décision ou l’attente précise, puis la prochaine action. Une nouvelle conversation peut ainsi reprendre à partir des fichiers plutôt que de l’historique du chat.', '', '## Boucles', '', 'Après S91, l’issue `autre_tranche` ouvre une nouvelle itération de S80 : conserver l’ancien état dans history, identifier la nouvelle demande et réexaminer les validations affectées. L’issue `mvp_integre` conduit à la recette S100.', '', 'À S120, une fenêtre incomplète conserve `attente_info`. Zéro usage mesuré sur une fenêtre complète est une observation possible ; une mesure absente ne vaut pas zéro usage.', '', 'Les contrôles locaux ne vérifient pas automatiquement les services distants ou la vérité d’un entretien. Le validateur compétent reste responsable de la preuve citée.', '']
    files['ORCHESTRATION.md'] = '\n'.join(orchestration)
    schema = ['# Les sept rubriques d’une séquence', '', generated, '| Rubrique | Ce qu’elle doit préciser |', '| --- | --- |']
    schema += [f'| **{field}** | {description} |' for field, description in model['contract'].items()]
    schema += ['', 'Le skill intervient dans **action** avant le dialogue ou l’analyse. Les questions et réponses acceptables présentes dans les fiches aident à construire la réponse ; elles ne sont pas déjà acquises.', '', 'Une validation recevable rattache le résultat à ses entrées et sorties versionnées, aux preuves, à la personne qui valide et à une issue du tableau de destinations.', '', 'Voir une fiche complète : [S40](sequences/S40.md). Voir un appel SDLC encodé explicitement : [S90](sequences/S90.md). Voir le cas complet : [EXEMPLE.md](EXEMPLE.md).', '', 'Les emplacements `natif_conditionnel` s’appliquent si le skill natif est invoqué. `propose` est une convention du guide et `a_resoudre` demande une résolution lors du travail réel. Ces gabarits ne sont pas des fichiers déjà créés.', '']
    files['SCHEMA.md'] = '\n'.join(schema)
    for seq in model['sequences']:
        sid = seq['id']
        text = [f'# {sid} — {seq["title"]}', '', '> Fiche générée depuis `workflow.json`. Les réponses et preuves du cas d’école restent illustratives.', '', f'**Phase :** {seq["phase"] or "Cadrage transversal"} · **Prérequis :** {", ".join(seq["requires"]) or "Aucun"}.', '']
        if seq.get('applicability'):
            condition = seq['applicability']
            text += [f'**Applicabilité :** `{condition["field"]} == {str(condition["equals"]).lower()}`. Une valeur inconnue exige une clarification ; une valeur fausse justifie une non-applicabilité tracée.', '']
        text += ['## 1. Entrée', '', artifact_lines(model, seq['input']) or model['scope']['start'], '']
        if seq.get('input_optional'):
            text += ['**À lire si disponible et pertinent :**', '', artifact_lines(model, seq['input_optional']), '']
        text += ['## 2. Responsable', '', actor_label(model, seq['responsible']), '', f'**Validation par :** {actor_label(model, seq["validation"]["by"])}', '', '## 3. Action', '', seq['action']['summary'], '', '**Capacités à activer selon le besoin :**', '']
        text += [f'- `{cap["id"]}` — {cap["when"]}' for cap in seq['action']['capabilities']] or ['- Le coordinateur cadre le travail ; aucun skill spécialisé n’est imposé.']
        text += ['', '**Étapes :**', '']+[f'{index}. {step}' for index, step in enumerate(seq['action']['steps'], 1)]+['']
        for question in seq['action']['questions']:
            text += ['**Question :** '+question['question'], '', '**Réponse acceptable, illustrative :** '+question['acceptable'], '', '**Réponse insuffisante :** '+question['insufficient'], '']
        if seq['action'].get('invocation'):
            text += ['**Requête à compléter avec une source réelle avant tout appel :**', '', '```text', seq['action']['invocation']['template'], '```', '', 'Le premier mot est exactement `interactive`. Vérifier le mode et la version du skill au moment de l’appel ; cette fiche n’exécute pas la requête.', '']
        text += ['## 4. Sortie', '', artifact_lines(model, seq['output']), '', '## 5. Preuve', '', paragraph_list([f'`{proof["id"]}` ({proof["kind"]}) — {proof["description"]}' for proof in seq['evidence']]), '', 'Chaque preuve indique sa source, son auteur et la version de l’artefact concerné. Un exemple ou une simulation ne valide pas une instance réelle.', '', '## 6. Validation', '', paragraph_list(seq['validation']['criteria']), '', 'Conserver le rôle et l’identité du validateur, la date, les versions et les preuves. Une réserve acceptée indique son manque, sa raison, son responsable et sa prochaine vérification.', '', '## 7. Prochaine destination', '', '| Issue observée ou décidée | Destination |', '| --- | --- |']
        for outcome, destinations in seq['next'].items():
            targets = destinations if isinstance(destinations, list) else [destinations]
            labels = [f'[{target}]({target}.md)' if target in ids else f'**{target}** — {model["special_targets"][target]}' for target in targets]
            text.append(f'| {outcome.replace("_", " ")} | {" ; ".join(labels)} |')
        text += ['', '## Cas d’école', '', '**Illustration fictive :** '+seq['example'], '', f'[Schéma Mermaid](../mermaid/{sid}.mmd) · [Glossaire](../GLOSSAIRE.md) · [Carte](../FLOW.md)', '']
        files[f'sequences/{sid}.md'] = '\n'.join(text)
        files[f'mermaid/{sid}.mmd'] = sequence_mermaid(model, seq)
    overview = overview_mermaid(model)
    files['mermaid/00-prerequis.mmd'] = overview
    mermaid = ['# Schémas des séquences', '', generated, 'Les flèches du premier schéma montrent les prérequis, pas une validation automatique. Pour une séquence conditionnelle, une non-applicabilité tracée peut satisfaire le prérequis. Les tables de chaque fiche portent les retours et attentes.', '', '```mermaid', overview.rstrip(), '```', '', '## Contrats détaillés', '']
    for seq in model['sequences']:
        mermaid += [f'### {seq["id"]} — {seq["title"]}', '', '```mermaid', files[f'mermaid/{seq["id"]}.mmd'].rstrip(), '```', '', f'Lire le [contrat complet](sequences/{seq["id"]}.md) pour les questions, capacités, critères de preuve et destinations.', '']
    files['MERMAID.md'] = '\n'.join(mermaid)
    template = {'flow_version':model['version'],'mode':'reel','project':None,'current_sequence':'S00','resume_sequence':None,'context':{field:None for field in model['context_fields']},'actors':{role:None for role in model['roles']},'artifacts':{},'evidence':{},'sequences':{'S00':{'status':'a_faire'}},'history':[]}
    files['templates/etat.json'] = dump(template)
    sample = example_state(model)
    files['examples/minirevisions.etat.json'] = dump(sample)
    example = ['# Exemple complet — MiniRévisions', '', generated, '**CAS FICTIF — AUCUNE PREUVE RÉELLE.** '+model['example']['premise'], '', '**Parcours critique :** '+model['example']['critical_task'], '', '**Exclusions :** '+', '.join(model['example']['exclusions'])+'.', '', '## Cadrage illustratif', '', '```json', dump(model['example']['context']).rstrip(), '```', '', 'Les emplacements `illustration://` du fichier d’état sont des identifiants de cas d’école. Ils ne représentent pas un service ou un fichier produit. Toutes ses preuves portent `simulated: true` et son mode est `illustration`.', '', '## Parcours de bout en bout', '']
    for seq in model['sequences']:
        record = sample['sequences'][seq['id']]
        example += [f'### {seq["id"]} — {seq["title"]}', '', seq['example'], '', '| Rubrique | Dans le cas d’école |', '| --- | --- |', f'| Entrée | {", ".join(seq["input"]) or "Intention de départ"} |', f'| Responsable | {sample["actors"][seq["responsible"]]} |', f'| Action | {seq["action"]["summary"]} |', f'| Sortie | {", ".join(seq["output"]) if record["status"] != "non_applicable" else "Aucun livrable de spike ; justification de non-applicabilité"} |', f'| Preuve | {", ".join(record.get("evidence_ids", [])) or record["context_ref"]} — illustration uniquement |', f'| Validation | {record["status"]} dans la simulation ; aucune validation réelle |', f'| Destination | {seq["next"].get(record.get("outcome", "non_applicable"))} |', '']
    example += ['## Variantes à comprendre', '', '- Si un test de code échoue à S90, conserver la séquence et réparer dans Deliver ; ne pas retourner arbitrairement au backlog.', '- Si la fenêtre d’observation n’est pas terminée, S120 reste en `attente_info` avec le manque nommé.', '- Si le MVP change de version, les séquences qui utilisaient l’ancienne version sont à réexaminer ; la note d’intention ne devient pas automatiquement fausse.', '- Si le projet n’a pas d’interface graphique, tracer les non-applicabilités S50 et S51 à partir du cadrage approuvé.', '- Si seule une PR en brouillon existe, S91 reste à faire et S100 ne peut pas être déclarée validée.', '', 'L’instance [examples/minirevisions.etat.json](examples/minirevisions.etat.json) illustre la structure de reprise. Un contrôle de cohérence de cet exemple ne prouve ni une livraison réelle ni la facilité du parcours pour un novice.', '']
    example += ['## Livrables remplis', '', 'Lire les [notes et contrats renseignés](examples/minirevisions/livrables.md) : intention, périmètre avec critères, demande prête, différence entre sortie et preuve, puis reprise en attente.', '']
    files['EXEMPLE.md'] = '\n'.join(example)
    filled = ['# MiniRévisions — livrables renseignés', '', '**Exemple fictif, aucune exécution ni observation réelle du produit.** Les notes ci-dessous montrent le niveau de précision recherché ; elles ne constituent pas un projet lancé.', '']
    for item in model['example']['deliverables']:
        filled += [f'<a id="{item["id"]}"></a>', '', f'## {item["title"]}', '', paragraph_list(item['content']), '']
    filled += ['[Revenir au parcours complet](../../EXEMPLE.md)', '']
    files['examples/minirevisions/livrables.md'] = '\n'.join(filled)
    return files


def build(model, root: Path, check=False):
    files = documents(model)
    changed = []
    for relative, expected in files.items():
        destination = root / relative
        if not destination.is_file() or destination.read_text() != expected:
            changed.append(relative)
            if not check:
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(expected)
    print(json.dumps({'mode':'verification' if check else 'generation','fichiers':len(files),'differences':changed,'source':'workflow.json'},ensure_ascii=False,indent=2))
    return 1 if check and changed else 0
