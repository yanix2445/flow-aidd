---
name: flow-aidd
description: "Piloter un produit de l’idée vague au premier MVP puis à la décision sur ses premiers usages, une séquence à la fois, avec décisions, livrables et preuves conservés dans les fichiers .flow/ du projet. Utiliser lorsque l’utilisateur veut démarrer un projet avec Flow AIDD, le reprendre, savoir où il en est ou quelle est la suite, comprendre le parcours ou une séquence, enregistrer un résultat ou faire valider un résultat. Orchestre les plugins aidd-* comme chaîne principale, Impeccable pour le design et marketing-skills pour le public, l’offre, la mesure et le lancement. Pas pour un travail de code sans lien avec un projet qui suit le flow."
---

Ce skill conduit un produit de l’idée au premier MVP avec son porteur, une séquence à la fois. Le modèle embarqué fixe le parcours ; les faits, décisions et preuves du produit restent dans le projet ciblé.

Principes :
- **Une séquence, puis l’accord.** Conduire la séquence utile, la faire contrôler, présenter résultat, limites, preuves et destination, puis attendre la réponse réelle du porteur. Une recommandation, un hook, un agent ou le silence ne valent jamais accord.
- **Le helper écrit, le porteur décide.** `scripts/project_flow.py` est le seul à écrire `.flow/etat.json` et `.flow/suivi.md`. Les décisions produit nouvelles restent au porteur ; les actes externes restent dans le périmètre déjà autorisé.
- **Une preuve réelle ou rien.** Faits, hypothèses, décisions et simulations restent distincts. Une inconnue reste inconnue ; un exemple ou une simulation ne valident jamais le projet réel.

## Mise en route

1. `SKILL_DIR` est le dossier qui contient ce SKILL.md, y compris dans le cache d’installation ; tous les chemins ci-dessous en partent. Ne pas dépendre du dépôt où le plugin a été développé.
2. Lancer une fois par séance `python3 -B SKILL_DIR/scripts/project_flow.py status --project CHEMIN_ABSOLU` sur le dossier du produit (demander lequel s’il y en a plusieurs). Suivre ses `directives` et lire **seulement** les fichiers de `load`. Pour une simple explication, ne rien initialiser.
3. Relire [socle.md](references/socle.md) juste avant chaque `record` et chaque `checkpoint`. Ne pas le charger pour une explication.

## Commandes

| Commande du helper | Usage | Référence |
| --- | --- | --- |
| `init` | Démarrer un projet avec une idée | [init.md](references/init.md) |
| `status`, `next`, `check` | Où en est le projet, quoi lire, quoi faire | [status.md](references/status.md) |
| `record` | Enregistrer un résultat, une preuve, une réponse de contexte | [record.md](references/record.md) |
| `checkpoint`, `approve`, `correct`, `pause`, `focus` | Faire contrôler, présenter et recueillir la décision | [checkpoint.md](references/checkpoint.md) |
| `adopt`, `relocate`, `migration-plan`, `migrate` | Rattacher un ancien état, un projet déplacé, un modèle mis à jour | [rattacher.md](references/rattacher.md) |

| Besoin transversal | Référence |
| --- | --- |
| La fiche de la séquence de travail | `references/sequences/Sxx.md`, donnée par `load` |
| Poser les questions de la séquence au porteur | [entretien.md](references/entretien.md) |
| Activer les bons skills (AIDD, Impeccable, marketing-skills) | [capacites.md](references/capacites.md) |
| Réagir à un message de hook | [hooks.md](references/hooks.md) |
| Expliquer le parcours, une séquence ou un terme | [parcours.md](references/parcours.md), la fiche concernée, [glossaire.md](references/glossaire.md) |
| Adapter la profondeur au projet | Section « Adapter la profondeur » de [sequences/S00.md](references/sequences/S00.md) |
| Règles complètes, rubriques, statuts et boucles (vérificateur, cas de doute) | [regles.md](references/regles.md) |

## Agents de contrôle

Avant chaque `checkpoint`, lancer les agents du champ `agents` de `status`. Ils ne modifient rien et rendent un verdict.

| Agent | Rôle | Sans sous-agent |
| --- | --- | --- |
| `flow_aidd_verificateur` | Critères couverts par des preuves réelles, aux bonnes versions | [degraded/verificateur.md](references/degraded/verificateur.md) |
| `flow_aidd_relecteur` | Livrable fidèle à la promesse, au contrat du MVP et aux réponses du porteur | [degraded/relecteur.md](references/degraded/relecteur.md) |

Les lancer à neuf, sans l’historique de la conversation (`fork_turns: 0`), avec leur seul paquet d’entrées, sans lire leur définition avant. La version `degraded` ne sert que si aucun sous-agent n’est possible, et la substitution est dite au porteur. Le détail est dans [checkpoint.md](references/checkpoint.md).

## Aiguillage

- **Question sur le fonctionnement :** expliquer à partir des références, sans initialiser de produit.
- **Accueil après installation :** présenter les deux fichiers de suivi et proposer démarrer, reprendre ou explorer. L’installation seule n’autorise pas `init`.
- **Demande d’avancement :** réponse courte depuis `status` ; elle n’autorise pas à exécuter la suite.
- **« Continue » :** s’applique à la proposition déjà présentée et à son périmètre, pas à une séquence non présentée.
- **Sinon :** suivre `directives`, conduire la séquence, `record` au fil du travail, faire contrôler, puis `checkpoint`.

Répondre au porteur en langage simple : séquence courante, résultat visé, informations ou décisions manquantes, prochaine action concrète, sans annoncer de résultat que le helper n’a pas produit.
