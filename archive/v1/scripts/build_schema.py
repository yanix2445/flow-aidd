"""Join the existing workflow and its question/answer/output schematic."""

from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--visual', type=Path)
    args = parser.parse_args()
    flow = json.loads((ROOT / 'workflow.json').read_text())
    schema = json.loads((ROOT / 'schema.json').read_text())
    rows = {row['id']: row for row in schema['subphases']}
    assert len(rows) == len(schema['subphases']) == 36
    expected = {f"{phase['id']}.{index}" for phase in flow['phases'] for index in range(1, 4)}
    assert set(rows) == expected
    out = [
        '# Schéma : questions → réponses attendues → skills → résultats', '',
        schema['note'], '',
        'Les questions sont proposées pour conduire chaque sous-phase. Les réponses décrivent le niveau de précision à atteindre ; elles ne sont pas des faits sur un projet déjà choisi.', '',
        '**Lecture :** entrée → sous-phase → question → réponse attendue → capacité responsable → résultat → décision de passage.', '',
        '**Origine des sorties :** `natif` = chemin ou nom défini par le skill installé ; `proposé` = convention de rangement de ce guide ; `à résoudre` = emplacement choisi par le skill, la stack ou le service au moment de l’exécution. Les chemins avec `<...>` sont des gabarits.', '',
        'Les fichiers indiqués ne sont pas créés par la consultation du schéma. Un même document peut être enrichi dans plusieurs sous-phases. Seuls les livrables utiles au projet seront produits.', '',
        'Les fondations et le backlog peuvent commencer selon leurs dépendances, sans attendre toutes les autres phases. Les neuf plugins n’assurent pas à eux seuls le déploiement ou la mesure : les outils externes nécessaires sont nommés comme tels.', '',
    ]
    for phase in flow['phases']:
        pid = phase['id']
        out += [f"## {pid}. {phase['title']}", '', f"**Entrée :** {phase['input']}", '']
        for index, sub in enumerate(phase['subphases'], 1):
            key = f'{pid}.{index}'
            row = rows[key]
            assert all(row[field] for field in ['question', 'answer', 'skills', 'outputs'])
            for output in row['outputs']:
                assert output['origin'] in ['natif', 'proposé', 'à résoudre']
            sub['diagram'] = row
            out += [f"### {key}. {sub['title']}", '', f"**Question :** {row['question']}", '', f"**Réponse attendue :** {row['answer']}", '', '**Capacités :**', '']
            out += [f'- `{skill}`' for skill in row['skills']]
            out += ['', '**Résultats attendus :**', '']
            for output in row['outputs']:
                out.append(f"- **{output['name']}** — {output['type']} ; `{output['path']}` — {output['origin']}.")
            out += ['', f"Étapes et sous-étapes : voir la section {key} dans [FLOW.md](FLOW.md).", '']
        out += [f"**Décision de passage :** {phase['gate']}", '', f"**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant" + (f" ; retour possible vers la phase {phase['returnTo']}." if phase['returnTo'] else '.'), '']
    (ROOT / 'SCHEMA.md').write_text('\n'.join(out))
    if args.visual:
        fragment = args.visual.read_text()
        payload = json.dumps(flow, ensure_ascii=False).replace('<', '\\u003c')
        pattern = r'(<script type="application/json" id="qa-schema-data">)[\s\S]*?(</script>)'
        fragment, count = re.subn(pattern, lambda match: match[1] + payload + match[2], fragment)
        assert count == 1
        args.visual.write_text(fragment)
    print('Schéma construit : 12 phases, 36 sous-phases avec question, réponse attendue, capacités et sorties ; ordre et contenu initiaux conservés.')


if __name__ == '__main__':
    main()
