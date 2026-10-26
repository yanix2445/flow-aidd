# Flow AIDD — des séquences que l’on peut suivre

Une phase explique une grande intention. Une séquence décrit un travail pilotable. Une étape est une action concrète dans cette séquence.

**Commencer :** lire [SCOPE.md](SCOPE.md), puis [S00 — cadrer le projet](sequences/S00.md). Utiliser [GLOSSAIRE.md](GLOSSAIRE.md) lorsqu’un terme est inconnu.

**Si tu débutes :** utilise le message ci-dessous. Le coordinateur tient les fichiers d’état ; ton rôle est de clarifier ton besoin et de prendre les décisions qui t’appartiennent. Tu n’as pas à éditer le JSON à la main.

Pour appliquer le parcours à un produit, copier [templates/etat.json](templates/etat.json) dans `{projet}/.flow/etat.json`, puis renseigner progressivement l’instance. Ce dépôt contient le modèle ; aucun projet produit réel n’est initialisé par sa consultation.

| Besoin | Document |
| --- | --- |
| Voir la carte des phases et séquences | [FLOW.md](FLOW.md) |
| Conduire une séquence et reprendre une séance | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Comprendre les sept rubriques | [SCHEMA.md](SCHEMA.md) |
| Voir un parcours rempli mais fictif | [EXEMPLE.md](EXEMPLE.md) |
| Lire les schémas et les sources Mermaid | [MERMAID.md](MERMAID.md) |
| Maintenir le modèle | [workflow.json](workflow.json) |
| Retrouver la première version et son audit | [archive/v1](archive/v1/ARCHIVE.md) |

## Pour l’IA

Lire les règles courtes d’[AGENTS.md](AGENTS.md), l’état du projet et la seule fiche de séquence courante. Charger les sources produit et les SKILL.md au moment où ils deviennent nécessaires.

```text
Voici mon idée ou l’état actuel du projet : [description].
Applique le flow version 2 en commençant par S00, ou reprends la séquence consignée dans mon état.
Distingue faits, hypothèses, décisions et preuves. Aide-moi à répondre ; ne suppose pas mes réponses.
Conserve l’état après les décisions et propose une prochaine action dans le périmètre autorisé.
```

## Outils locaux

Le script Python utilise la bibliothèque standard. `check` et `next` lisent les fichiers ; ils ne lancent aucune action du projet. Une recommandation ne certifie pas la réalité des preuves déclarées.

```sh
job_id="$(portly temp 'python3 scripts/flow.py check' --path /Users/yanis/Developer/flow-aidd --timeout 30m)"
portly wait "$job_id"
```

Commandes à placer dans un job Portly :

- `python3 scripts/flow.py build` : régénérer les guides et exemples.
- `python3 scripts/flow.py build --check` : détecter une divergence des fichiers générés.
- `python3 scripts/flow.py show S90` : lire un contrat sans charger tout le modèle.
- `python3 scripts/flow.py check --state <etat.json>` : contrôler la cohérence déclarée.
- `python3 scripts/flow.py next --state <etat.json>` : suggérer une prochaine action sans modifier l’état.

La compréhension réelle par un novice et l’efficacité sur un projet livré restent à éprouver. Les tests de ce dépôt ne construisent pas le produit de l’exemple.
