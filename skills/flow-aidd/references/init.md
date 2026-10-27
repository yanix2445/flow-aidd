# `init` — démarrer un projet

`init` crée le suivi d’un produit : `.flow/etat.json` et sa vue `.flow/suivi.md`, avec S00 à faire. Il ne cadre rien, ne remplit aucune réponse et n’accorde aucune validation : le cadrage se fait ensuite, avec le porteur, dans S00.

> **Contexte nécessaire :** le dossier réel du produit et l’idée du porteur, même floue.

## Étape 1 : Identifier le dossier et la situation

Déduire le dossier produit du contexte de travail et de la demande. Il peut être distinct du dossier du plugin. Lancer `status --project CHEMIN_ABSOLU` sur ce dossier.

- **`initialized: false` et le porteur veut démarrer :** passer à l’étape 2.
- **`initialized: false` et la demande est une question sur le flow :** expliquer avec [parcours.md](parcours.md) ; ne rien créer.
- **`initialized: false` juste après l’installation du plugin :** présenter les deux fichiers de suivi et proposer démarrer, reprendre ou explorer. L’installation seule n’autorise pas `init`.
- **`initialized: true` :** ne pas relancer `init`. Reprendre avec [status.md](status.md).
- **Plusieurs dossiers plausibles :** demander lequel en une question, avec les candidats.

## Étape 2 : Explorer avant de demander

Avant la première question, parcourir assez le dossier pour ne pas faire répéter ce qui est déjà écrit : README, notes, documents produit, `PRODUCT.md`, `.agents/product-marketing.md`, artefacts AIDD, code existant, consignes du projet (AGENTS.md). Traiter ce qui est trouvé comme une hypothèse à confirmer, jamais comme une décision du porteur.

## Étape 3 : Initialiser

```sh
python3 -B SKILL_DIR/scripts/project_flow.py init --project CHEMIN_ABSOLU --idea "IDEE DU PORTEUR"
```

`created: true` : l’état est créé, révision 0. `created: false` : un état existait déjà et n’a pas été touché. Le helper ne modifie ni AGENTS.md, ni `.gitignore`, ni la configuration de Codex, et ne crée aucun commit.

## Étape 4 : Ouvrir S00

Relancer `status` et suivre `directives` et `load` : la fiche [sequences/S00.md](sequences/S00.md), [entretien.md](entretien.md) pour conduire les questions, [record.md](record.md) pour consigner. Une idée imprécise suffit : S00 sert justement à construire les réponses manquantes.

## Pannes fréquentes

| Message du helper | Que faire |
| --- | --- |
| « Le dossier produit doit exister. » | Vérifier le chemin ; créer le dossier seulement si le porteur l’a demandé. |
| « L’état doit rester dans le dossier réel du projet, sans lien symbolique. » | `.flow` est un lien : choisir le dossier réel, ne pas contourner. |
| « Un état a été créé entre-temps ; relire le projet. » | Une autre session a initialisé : passer à `status`. |
| Erreur `--project` manquant | Toujours passer le chemin absolu du produit. |

## Avant de terminer

- Seuls `.flow/etat.json` et `.flow/suivi.md` ont été créés.
- Aucune réponse de cadrage n’a été inventée ; les inconnues restent `null`.
- Le porteur sait ce qui a été créé et quelle est la première question de S00.
