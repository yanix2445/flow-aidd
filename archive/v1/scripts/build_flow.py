"""Build the readable guide from workflow.json; optionally populate its inline map."""

from pathlib import Path
import argparse
import json
import re


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('/Users/yanis/.codex/plugins/cache')
SKILL_ROOTS = {
    'aidd-context': PLUGIN / 'aidd-framework/aidd-context/2.9.0/skills',
    'aidd-dev': PLUGIN / 'aidd-framework/aidd-dev/2.7.0/skills',
    'aidd-orchestrator': PLUGIN / 'aidd-framework/aidd-orchestrator/2.4.0/skills',
    'aidd-pm': PLUGIN / 'aidd-framework/aidd-pm/2.6.0/skills',
    'aidd-refine': PLUGIN / 'aidd-framework/aidd-refine/3.1.1/skills',
    'aidd-vcs': PLUGIN / 'aidd-framework/aidd-vcs/2.5.0/skills',
    'marketing-skills': PLUGIN / 'marketingskills/marketing-skills/2.13.0/skills',
    'interfaces': PLUGIN / 'interfaces/interfaces/1.17.0/skills',
    'impeccable': PLUGIN / 'openai-curated-remote/impeccable/4.3.1/skills',
}


def source_path(skill):
    plugin, name = skill.split(':', 1)
    return SKILL_ROOTS[plugin] / name / 'SKILL.md'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visual', type=Path)
    args = parser.parse_args()
    data = json.loads((ROOT / 'workflow.json').read_text())
    phases = data['phases']
    ids = {p['id'] for p in phases}
    assert len(ids) == len(phases) == 12
    assert ids == set(range(1, 13))
    all_skills = sorted({s for p in phases for s in p['skills']})
    for skill in all_skills:
        assert source_path(skill).is_file(), f'Skill absent: {skill}'
    subs = steps = actions = 0
    for phase in phases:
        assert phase['group'] in data['groups']
        assert all(dep in ids and dep < phase['id'] for dep in phase['dependsOn'])
        assert phase['returnTo'] is None or phase['returnTo'] in ids
        assert len(phase['subphases']) == 3
        for sub in phase['subphases']:
            subs += 1
            assert len(sub['steps']) == 2
            for step in sub['steps']:
                steps += 1
                assert len(step['actions']) == 2
                actions += len(step['actions'])

    out = [
        '# De l’idée vague au premier MVP utilisable',
        '',
        f"Cadre proposé, version {data['version']} — capacités locales consultées le {data['verifiedAt']}.",
        '',
        f'{len(phases)} phases · {subs} sous-phases · {steps} étapes · {actions} sous-étapes.',
        '',
        'Chaque niveau est un repère de réflexion. Adapter la profondeur au projet ; plusieurs éléments peuvent tenir dans une note courte. Ne pas créer tous les artefacts par défaut.',
        '',
        'Les décisions de produit restent avec le porteur du projet. Une preuve manquante reste une inconnue ou un risque accepté, jamais une validation inventée. Le coordinateur choisit une prochaine étape utile ; il ne déroule pas douze phases automatiquement.',
        '',
        'Voir [README.md](README.md) pour la carte des dépendances et [ORCHESTRATION.md](ORCHESTRATION.md) pour les règles de conduite et de reprise.',
        '',
        '## Sommaire',
        '',
    ]
    for phase in phases:
        out.append(f"- [{phase['id']}. {phase['title']}](#phase-{phase['id']}) — {phase['group']}")

    for phase in phases:
        pid = phase['id']
        deps = ', '.join(str(x) for x in phase['dependsOn']) or 'aucune'
        out.extend([
            '', f'<a id="phase-{pid}"></a>', '',
            f"## {pid}. {phase['title']}", '',
            f"**Ensemble :** {phase['group']} · **Dépendances :** {deps}.", '',
            f"**Question :** {phase['question']}", '',
            f"**Entrée :** {phase['input']}", '',
            f"**Livrable :** {phase['output']}", '',
            f"**Critère de passage :** {phase['gate']}", '',
            f"**À adapter :** {phase['conditional']}", '',
            '**Skills mobilisables :** ' + ', '.join(f'`{s}`' for s in phase['skills']) + '.', '',
        ])
        if phase['returnTo']:
            out.extend([f"**Retour principal si le critère échoue :** phase {phase['returnTo']}. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.", ''])
        for sub_index, sub in enumerate(phase['subphases'], 1):
            prefix = f'{pid}.{sub_index}'
            out.extend([f"### {prefix} {sub['title']}", ''])
            for step_index, step in enumerate(sub['steps'], 1):
                out.extend([f"**{prefix}.{step_index} — {step['title']}**", ''])
                for action_index, action in enumerate(step['actions'], 1):
                    out.append(f'- {prefix}.{step_index}.{action_index} — {action}')
                out.append('')
        out.extend(['**Pour engager cette phase :**', '', '```text', phase['prompt'], '```', ''])

    out.extend([
        '## Sources locales et limites', '',
        'La carte assemble les responsabilités décrites par les plugins installés. Les étapes générales de recherche, de conception et d’exploitation sont des recommandations de ce guide, pas de nouvelles commandes natives. Les liens suivants pointent vers les sources locales ; les chemins versionnés peuvent changer après une mise à jour.', '',
    ])
    for skill in all_skills:
        out.append(f'- [{skill}]({source_path(skill)})')
    out.extend([
        '',
        'Pour les frontières du SDLC, les modes et les pauses : les références `mode.md`, `01-frame.md`, `02-deliver.md` et `03-check.md` sous le skill `aidd-orchestrator:01-sdlc` ont aussi été consultées. Pour Impeccable : `reference/routing.md` et `reference/shape.md`. Les chemins de persistance du PRD ont été vérifiés dans son action `02-finalize.md`.',
        '',
        'Ce guide ne démontre pas une connexion à un hébergeur, un outil de recherche terrain ou un dépôt distant. Leur disponibilité se vérifie au moment de la phase concernée. Aucun projet produit n’a parcouru ces phases dans ce dossier.',
        '',
    ])
    (ROOT / 'FLOW.md').write_text('\n'.join(out))
    if args.visual:
        fragment = args.visual.read_text()
        payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
        pattern = r'(<script type="application/json" id="flow-project-data">)[\s\S]*?(</script>)'
        fragment, replaced = re.subn(pattern, lambda m: m[1] + payload + m[2], fragment)
        assert replaced == 1, 'One data block expected in the inline map'
        args.visual.write_text(fragment)
    print(f'Guide généré : {len(phases)} phases, {subs} sous-phases, {steps} étapes, {actions} sous-étapes ; {len(all_skills)} sources de skills présentes.')


if __name__ == '__main__':
    main()
