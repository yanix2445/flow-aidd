"""Translate the established workflow and Q&A schema into readable Mermaid sources."""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

# Concise labels for the same questions and outputs in schema.json.
# Full questions, skill identifiers and paths remain in SCHEMA.md and the tables.
LABELS = {
    '1.1': ('Qui rencontre quelle difficulté ?', 'Une cible, une situation et un résultat souhaité', 'AIDD Refine : 01-brainstorm', 'Note d’intention : docs/idee.md, nom proposé'),
    '1.2': ('Quelle piste explorer en premier ?', 'Une piste retenue et les autres reportées', 'AIDD Refine : 01-brainstorm', 'Piste et alternatives dans idee.md, proposé'),
    '1.3': ('Quelles limites et quelle inconnue prioritaire ?', 'Temps, budget, objectif et hypothèse à tester', 'AIDD Refine : 01-brainstorm', 'Contraintes et hypothèses dans idee.md, proposé'),
    '2.1': ('Qui étudier et quelle observation rechercher ?', 'Un segment, une question et une limite d’effort', 'Marketing : product-marketing ; AIDD PM : 06-product-brief', 'Contexte marketing natif + recherche.md proposé'),
    '2.2': ('Que font les personnes et où peinent-elles ?', 'Des faits datés, des sources et les alternatives', 'Marketing : customer-research', 'Sources et observations dans recherche.md, proposé'),
    '2.3': ('Les faits justifient-ils de poursuivre ?', 'Signaux, contradictions, limites et décision', 'Marketing : customer-research ; AIDD PM : 06-product-brief', 'Synthèse et décision dans recherche.md, proposé'),
    '3.1': ('Quel bénéfice pour quelle cible ?', 'Une promesse crédible face à une alternative', 'Marketing : product-marketing', 'Positionnement dans le contexte marketing natif'),
    '3.2': ('Comment atteindre la cible et financer l’usage ?', 'Un premier canal et une hypothèse de viabilité', 'AIDD PM : 06-product-brief ; Marketing : product-marketing', 'Viabilité et canal dans le Product Brief natif'),
    '3.3': ('Quelle opportunité et comment la valider ?', 'Objectif, risques et critères de poursuite approuvés', 'AIDD PM : 06-product-brief', 'Product Brief approuvé, chemin du skill'),
    '4.1': ('Quelle tâche complète prouve la valeur ?', 'Un résultat, un indicateur et une fenêtre de mesure', 'AIDD PM : 03-prd', 'Résultat et mesure dans le PRD natif'),
    '4.2': ('Que garder et que reporter ?', 'Le nécessaire, les exclusions et les règles métier', 'AIDD PM : 03-prd', 'Périmètre du MVP dans le PRD natif'),
    '4.3': ('Quels états ou angles morts restent ouverts ?', 'Qualité attendue et lacunes bloquantes traitées', 'AIDD Refine : 03-shadow-areas ; AIDD PM : 03-prd', 'PRD validé et angles morts traités'),
    '5.1': ('Quel parcours mène au résultat ?', 'Entrée, actions, écrans, décisions et états utiles', 'Impeccable : init puis shape', 'PRODUCT.md natif + parcours.md proposé'),
    '5.2': ('Quelle direction sert ce parcours ?', 'Une direction et des règles d’interface choisies', 'Impeccable : direction après shape', 'DESIGN.md natif + prototype au chemin choisi'),
    '5.3': ('La personne comprend-elle et réussit-elle ?', 'Des observations, des corrections et les limites du test', 'Interfaces : better-interface ; Impeccable : critique', 'Prototype corrigé + retours-ux.md proposé'),
    '6.1': ('Quel risque technique peut invalider la promesse ?', 'Une question bornée et une preuve de faisabilité', 'AIDD PM : 05-spike', 'Résultat de spike, preuve et limites'),
    '6.2': ('Quelle architecture répond aux besoins ?', 'Des options comparées et un choix proportionné', 'AIDD Context : 01-bootstrap, pour un nouveau SaaS', 'Décisions dans aidd_docs/INSTALL.md, natif'),
    '6.3': ('Comment installer et exploiter à coût acceptable ?', 'Environnements, installation, coûts et impacts', 'AIDD Context : 01-bootstrap, pour un nouveau SaaS', 'INSTALL.md complété ; le scaffold reste à créer'),
    '7.1': ('Quel socle créer ou réutiliser ?', 'Dépôt, conventions, dépendances et environnements', 'AIDD VCS : 00-repo-init ; AIDD Dev : plan et implement', 'Dépôt, code et configuration adaptés à la stack'),
    '7.2': ('Une petite tranche fonctionne-t-elle réellement ?', 'Un parcours local et de préproduction vérifié', 'AIDD Dev : 03-assert et 06-test', 'Socle vérifié, configuration et URL de préproduction'),
    '7.3': ('Que doit lire un agent pour reprendre le projet ?', 'Architecture réelle, règles, commandes et accès', 'AIDD Context : 02-project-memory', 'Contexte projet et configuration des outils IA'),
    '8.1': ('Quelles petites livraisons apportent de la valeur ?', 'Des tranches verticales, regroupées si nécessaire', 'AIDD Orchestrator : backlog ; AIDD PM : epic et user-stories', 'Stories Markdown ; epics seulement si utiles'),
    '8.2': ('Comment saura-t-on que la demande est faite ?', 'Acteur, résultat, critères et dépendances levées', 'AIDD PM : 02-user-stories et 04-spec si nécessaire', 'Story prête + spec.md si le contrat manque'),
    '8.3': ('Quelle tranche livrer maintenant ?', 'Une demande prête, ordonnée selon valeur et risque', 'AIDD Orchestrator : 02-backlog ; AIDD PM : 02-user-stories', 'Backlog ordonné et prochaine story identifiée'),
    '9.1': ('Le contrat permet-il de construire ?', 'Résultat, limites et critères suffisamment clairs', 'AIDD Orchestrator : SDLC Frame ; PM : spec si nécessaire', 'Contrat existant ou spec.md dans le dossier de tâche'),
    '9.2': ('Quel plan et quelles preuves de réalisation ?', 'Un plan confirmé puis un candidat construit et vérifié', 'SDLC Deliver : Dev plan, implement, assert, test ; VCS commit', 'plan.md, phase-N.md, code, tests, commits et preuves'),
    '9.3': ('La revue indépendante confirme-t-elle le résultat ?', 'Écarts traités et résultat conforme au contrat', 'SDLC Check : Dev review ; Refine challenge ; VCS pull-request', 'Rapports du candidat et PR en brouillon'),
    '10.1': ('Le parcours intégré fonctionne-t-il ?', 'Tâche, erreurs, données, droits et qualité vérifiés', 'AIDD Dev : 03-assert et 06-test', 'Rapport et preuves dans recette-mvp.md, proposé'),
    '10.2': ('La cible peut-elle accomplir la tâche ?', 'Observations d’usage et d’accessibilité contextualisées', 'Interfaces : better-interface ; Impeccable : audit et polish', 'Recette d’usage et interface corrigée'),
    '10.3': ('Peut-on ouvrir et revenir en arrière si besoin ?', 'Écarts bloquants traités et limites acceptées', 'AIDD Refine : 02-challenge', 'Décision et retour arrière dans lancement.md, proposé'),
    '11.1': ('Comment la cible comprend-elle et démarre-t-elle ?', 'Message, accès, premier usage et support prêts', 'Marketing : launch et product-marketing', 'Page, invitation ou démonstration selon le canal'),
    '11.2': ('La version livrée est-elle accessible et fonctionnelle ?', 'Adresse et parcours vérifiés pour la population prévue', 'Hébergeur réel ; Marketing launch ; VCS release-tag si utile', 'URL livrée ; tag et notes de version si nécessaires'),
    '11.3': ('Peut-on mesurer la valeur et recevoir les problèmes ?', 'Mesure sans doublon et canal de retours fonctionnel', 'Marketing : launch ; outils de mesure et de support', 'Événements vérifiés et premiers retours datés'),
    '12.1': ('Que font réellement les utilisateurs ?', 'Mesures et retours avec leur contexte et leurs limites', 'Marketing : customer-research ; mesure du projet', 'Premiers usages dans bilan-mvp.md, proposé'),
    '12.2': ('Quelles hypothèses sont étayées ou contredites ?', 'Un bilan et une décision justifiés par les faits', 'Marketing : customer-research ; AIDD Refine : 02-challenge', 'Bilan de validation et décision dans bilan-mvp.md'),
    '12.3': ('Quelle est la prochaine priorité utile ?', 'Une demande, une recherche ou un arrêt explicite', 'AIDD Orchestrator : 02-backlog ; Marketing : product-marketing', 'Backlog et contexte marketing mis à jour'),
}
INPUTS = [
    'Une idée encore vague', 'La note d’intention et une hypothèse à tester',
    'Les observations et contraintes connues', 'Le Product Brief approuvé',
    'Le PRD et les contenus disponibles', 'Le PRD et les contraintes techniques',
    'Les décisions techniques et le plan d’installation', 'Le PRD et les décisions UX et techniques utiles',
    'Une demande prête et les contextes du projet', 'Les tranches intégrées en préproduction',
    'Le candidat validé et la population de lancement', 'Les usages et retours sur la fenêtre prévue',
]
GATES = [
    'Cible, problème et résultat assez clairs ?', 'Besoin étayé ou risque accepté ?',
    'Promesse, accès aux utilisateurs et viabilité décidés ?', 'Parcours complet, périmètre et critères approuvés ?',
    'Parcours compréhensible et limites des tests connues ?', 'Faisabilité et architecture suffisamment éprouvées ?',
    'Une tranche tourne et se vérifie de façon reproductible ?', 'Prochaine demande petite, utile et prête ?',
    'Contrat satisfait et conclusions de revue traitées ?', 'Parcours du MVP validé et écarts bloquants traités ?',
    'Produit accessible et action de valeur observable ?', 'Décision justifiée et prochaine action explicite ?',
]
NEXT = [
    'Phase 2 : comprendre le besoin', 'Phase 3 : choisir le positionnement',
    'Phase 4 : délimiter le MVP', 'Phases 5, 6 et 8 selon leurs dépendances',
    'Phase 9 quand socle et demande sont aussi prêts', 'Phase 7 : préparer les fondations',
    'Phase 9 quand UX et demande sont aussi prêtes', 'Phase 9 quand UX et socle sont aussi prêts',
    'Phase 8 : prochaine tranche ; phase 10 : MVP intégré', 'Phase 11 : ouvrir à la première population',
    'Phase 12 : observer et choisir la suite', 'Stabiliser, reprendre le backlog, réorienter ou arrêter',
]
GLOBAL_LABELS = [
    'Clarifier l’idée', 'Comprendre le besoin', 'Positionner le produit',
    'Délimiter le MVP', 'Concevoir l’UX et l’UI', 'Valider la technique',
    'Préparer le socle', 'Préparer le backlog', 'Livrer une tranche avec SDLC',
    'Faire la recette du MVP', 'Ouvrir le MVP', 'Mesurer et décider',
]


def node(identifier, label, decision=False):
    label = json.dumps(label, ensure_ascii=False)
    return f'  {identifier}{{{label}}}' if decision else f'  {identifier}[{label}]'


def header(title):
    return ['---', f'title: {json.dumps(title, ensure_ascii=False)}', '---', 'flowchart TB']


def overview(flow):
    lines = header('Vue d’ensemble : de l’idée au premier MVP')
    for index, group in enumerate(flow['groups'], 1):
        lines.append(f'  subgraph Groupe{index}["{group}"]')
        for phase in flow['phases']:
            if phase['group'] == group:
                lines.append(node(f"Phase{phase['id']}", f"{phase['id']:02d} · {GLOBAL_LABELS[phase['id']-1]}"))
                if phase['id'] == 2:
                    lines.append(node('DecisionBesoin', GATES[1], True))
                if phase['id'] == 10:
                    lines.append(node('DecisionRecette', 'Parcours du MVP validé ?', True))
        lines.append('  end')
    lines += [
        node('RetourIdee', 'Reprendre 01 : cible ou problème'),
        node('RetourMVP', 'Reprendre 04 : périmètre ou parcours'),
        node('RetourTranche', 'Reprendre 08 : prochaine tranche'),
        node('RetourCorrections', 'Reprendre 09 : corrections'),
        node('RetourDecouverte', 'Reprendre 02 : valeur incertaine'),
        node('RetourPriorite', 'Reprendre 08 : amélioration comprise'),
        '',
    ]
    lines += [
        '  Phase1 --> Phase2',
        '  Phase2 --> DecisionBesoin',
        '  DecisionBesoin -- "Oui" --> Phase3',
        '  DecisionBesoin -- "Non" --> RetourIdee',
        '  Phase3 --> Phase4',
        '  Phase4 -- "UX et UI" --> Phase5',
        '  Phase4 -- "Technique" --> Phase6',
        '  Phase4 -- "Backlog" --> Phase8',
        '  Phase6 --> Phase7',
        '  Phase5 --> Phase9',
        '  Phase7 --> Phase9',
        '  Phase8 --> Phase9',
        '  Phase9 --> Phase10',
        '  Phase10 --> DecisionRecette',
        '  DecisionRecette -- "Oui" --> Phase11',
        '  DecisionRecette -- "Non" --> RetourCorrections',
        '  Phase11 --> Phase12',
        '  Phase9 -. "Si une autre tranche est nécessaire" .-> RetourTranche',
        '  Phase5 -. "Si le parcours change" .-> RetourMVP',
        '  Phase6 -. "Si le périmètre change" .-> RetourMVP',
        '  Phase12 -. "Si la valeur reste incertaine" .-> RetourDecouverte',
        '  Phase12 -. "Si la prochaine amélioration est comprise" .-> RetourPriorite',
    ]
    return '\n'.join(lines) + '\n'


def phase_diagram(phase):
    pid = phase['id']
    lines = header(f"Phase {pid:02d} : {phase['title']}")
    lines.append(node(f'Entree{pid}', f'Entrée : {INPUTS[pid-1]}'))
    for index, sub in enumerate(phase['subphases'], 1):
        key = f'{pid}.{index}'
        question, answer, skills, output = LABELS[key]
        prefix = f'Phase{pid}SousPhase{index}'
        lines.append(f'  subgraph {prefix}["{key} · {sub["title"]}"]')
        lines += [
            node(f'Question{pid}Partie{index}', f'Question : {question}'),
            node(f'Reponse{pid}Partie{index}', f'Réponse attendue : {answer}'),
            node(f'Skills{pid}Partie{index}', skills),
            node(f'Resultat{pid}Partie{index}', f'Résultat : {output}'),
            '  end',
        ]
    lines += [
        node(f'Decision{pid}', GATES[pid-1], True),
        node(f'Suite{pid}', f'Oui : {NEXT[pid-1]}'),
        node(f'Reprise{pid}', f"Non ou inconnu : reprendre le point manquant, retour possible en phase {phase['returnTo'] or 1}"),
        '',
        f'  Entree{pid} --> Question{pid}Partie1',
    ]
    for index in range(1, 4):
        lines += [
            f'  Question{pid}Partie{index} --> Reponse{pid}Partie{index}',
            f'  Reponse{pid}Partie{index} --> Skills{pid}Partie{index}',
            f'  Skills{pid}Partie{index} --> Resultat{pid}Partie{index}',
        ]
        if index < 3:
            lines.append(f'  Resultat{pid}Partie{index} --> Question{pid}Partie{index+1}')
    lines += [
        f'  Resultat{pid}Partie3 --> Decision{pid}',
        f'  Decision{pid} -- "Oui" --> Suite{pid}',
        f'  Decision{pid} -- "Non ou inconnu" --> Reprise{pid}',
    ]
    return '\n'.join(lines) + '\n'


def main():
    flow = json.loads((ROOT / 'workflow.json').read_text())
    rows = {row['id']: row for row in json.loads((ROOT / 'schema.json').read_text())['subphases']}
    assert set(LABELS) == set(rows)
    folder = ROOT / 'mermaid'
    folder.mkdir(exist_ok=True)
    diagrams = [('00-ensemble.mmd', overview(flow))]
    diagrams += [(f"{phase['id']:02d}-phase.mmd", phase_diagram(phase)) for phase in flow['phases']]
    document = [
        '# Du concept au MVP — schémas Mermaid', '',
        'Le contenu reprend les 12 phases et 36 sous-phases du parcours existant. La vue globale montre les dépendances ; chaque phase détaille questions, réponses attendues, capacités et résultats.', '',
        '**Lecture :** entrée → sous-phase → question → réponse attendue → skill → résultat → décision de passage.', '',
        '**Les réponses sont attendues, pas acquises.** Les sorties décrivent des livrables à produire ; leur présence ici ne signifie pas que les fichiers existent. `Proposé` indique une convention de ce guide ; `natif` indique un emplacement défini par le skill. Les valeurs entre chevrons sont des gabarits.', '',
        'Les libellés des schémas sont abrégés pour rester lisibles. Les identifiants exacts et les chemins complets figurent sous chaque phase ; les questions complètes sont dans [SCHEMA.md](SCHEMA.md). Les 72 étapes et 144 sous-étapes restent dans [FLOW.md](FLOW.md).', '',
        'Une liste de capacités ne prescrit pas plusieurs appels simultanés. Le coordinateur choisit le skill responsable ; SDLC pilote déjà ses sous-étapes de développement. Les variantes conditionnelles restent décrites sous les phases.', '',
        'Les nœuds « Reprendre » sont des renvois vers les phases numérotées. Ils évitent de tirer des flèches de retour à travers tout le schéma.', '',
        '## Vue globale', '', '```mermaid', diagrams[0][1].rstrip(), '```', '',
        '**Pour la construction :** la phase 9 attend une conception suffisante, un socle opérationnel et une demande prête. UX, technique et backlog peuvent avancer après le cadrage du MVP selon ces dépendances. Un risque majeur se teste dès son apparition.', '',
        '## Phases détaillées', '',
    ]
    for phase, (filename, source) in zip(flow['phases'], diagrams[1:]):
        pid = phase['id']
        document += [f"### {pid:02d}. {phase['title']}", '', f"**À adapter :** {phase['conditional']}", '', '```mermaid', source.rstrip(), '```', '', '| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |', '| --- | --- | --- |']
        for index in range(1, 4):
            row = rows[f'{pid}.{index}']
            skills = '; '.join(f'`{skill}`' for skill in row['skills'])
            outputs = '; '.join(f"**{item['name']}** : `{item['path']}` ({item['origin']})" for item in row['outputs'])
            document.append(f"| {row['id']} | {skills} | {outputs} |")
        document += ['', f"**Critère complet :** {phase['gate']}", '', f'[Source Mermaid de la phase](mermaid/{filename}).', '']
    document += [
        '## Sources', '',
        '[workflow.json](workflow.json) et [schema.json](schema.json) portent le contenu ; les sources des skills sont répertoriées dans [FLOW.md](FLOW.md). Les conventions Mermaid appliquées viennent du skill local AIDD Context 09-mermaid : titres en frontmatter, identifiants descriptifs, libellés sur une ligne, déclarations avant les liens et aucune personnalisation de style.', '',
    ]
    for filename, source in diagrams:
        assert '\\n' not in source
        assert '<br' not in source
        (folder / filename).write_text(source)
    (ROOT / 'MERMAID.md').write_text('\n'.join(document))
    print('Créés : MERMAID.md et 13 sources .mmd ; 12 phases, 36 sous-phases, questions, réponses attendues, capacités, sorties et décisions.')


if __name__ == '__main__':
    main()
