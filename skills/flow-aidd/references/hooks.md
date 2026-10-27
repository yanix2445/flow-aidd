# Hooks — réagir à leurs messages

Les hooks de flow-aidd ne concernent que les projets qui possèdent déjà `.flow/etat.json`. Ils rappellent le contexte, protègent les fichiers tenus par le helper et préviennent une fois quand un livrable change. Ils ne créent aucun produit, accord ou serveur et ne poursuivent jamais une conversation.

> **Contexte nécessaire :** le message reçu et la sortie de `status`. Les hooks ne tournent qu’après la revue de confiance native de Codex.

## Étape 1 : Reconnaître le message

| Message | Origine | Que faire |
| --- | --- | --- |
| Contexte `flow-aidd · … · Sxx …` à l’ouverture | SessionStart | Suivre les directives indiquées et lire seulement les fichiers cités ; traiter d’abord une attente ou un point de passage. |
| Écriture refusée sur `etat.json` ou `suivi.md` | PreToolUse | Passer par `record` ([record.md](record.md)). `suivi.md` se régénère seul. |
| « … a changé depuis le point de passage … » | PostToolUse | L’accord présenté ne peut plus s’appliquer : terminer les modifications, `record`, puis un nouveau `checkpoint` ([checkpoint.md](checkpoint.md)). Le dire au porteur. |
| « … a changé alors que Sxx l’ont validé … » | PostToolUse | `record` la nouvelle version, puis réexaminer les séquences citées avec le porteur. |
| « … a changé : l’enregistrer avec record … » | PostToolUse | Travail en cours : enregistrer avant le prochain `checkpoint`. |
| « le suivi a été modifié hors du helper » | PostToolUse | Lancer `check` et corriger avant de continuer. |
| « flow-aidd : suivi à vérifier (…) » | Tous | Le hook n’a pas pu lire l’état : lancer `status` et traiter son erreur. |

## Étape 2 : Ne pas forcer

- Un refus de PreToolUse n’est pas un obstacle à contourner par une autre commande shell : il indique le bon chemin.
- Un conseil n’est donné qu’une fois par livrable et par version enregistrée dans une séance ; son absence ensuite ne signifie pas que le problème est réglé.
- Une modification faite par une commande shell ne déclenche pas PostToolUse : elle sera prise en compte en fin de tour et à la reprise.

## Avant de terminer

- Chaque message de hook reçu a été traité ou signalé au porteur.
- Aucun fichier tenu par le helper n’a été modifié autrement que par `project_flow.py`.
