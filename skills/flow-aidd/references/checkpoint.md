# `checkpoint`, `approve`, `correct`, `pause`, `focus` — faire décider le porteur

Quand une séquence semble terminée, la faire contrôler par les agents, créer un point de passage, le présenter au porteur et consigner sa réponse. Seul `approve` fait avancer, et d’une seule séquence. Une recommandation, un hook, un agent ou le silence ne valent jamais accord.

> **Contexte nécessaire :** la séquence courante enregistrée avec ses livrables et preuves, la révision lue, et le porteur identifié. Relire [socle.md](socle.md) avant l’étape 2.

## Étape 1 : Contrôle indépendant

Lancer chaque agent du champ `agents` de `status` :

- **À neuf, sans l’historique de la conversation** (dans Codex `fork_turns: 0`). Un contrôleur qui hérite du fil hérite aussi de son optimisme.
- Avec son seul paquet d’entrées : dossier produit, séquence, chemin de la fiche, sortie de `status`, livrables et preuves à contrôler, réponses confirmées du porteur avec leur source.
- Sans lire sa définition avant de le lancer ; l’environnement la charge.
- En l’attendant avec un délai long plutôt qu’en sondant, et en avançant sur une tâche indépendante déjà autorisée.
- En vérifiant que le retour porte un verdict et ses sections ; sur un retour vide, relancer une fois avec les mêmes entrées.

Sans aucune capacité de sous-agent, jouer le rôle soi-même depuis son fichier `degraded` (chemin dans `agents`), après être sorti du travail qui vient d’être fait, et le dire en une ligne au porteur.

| Verdict | Suite |
| --- | --- |
| `pret`, `conforme` | Étape 2. |
| `a_reprendre`, `a_corriger` | Corriger tous les écarts en une passe, `record`, puis renvoyer au même agent pour une contre-vérification. Deux tours au plus ; ensuite, présenter les écarts restants au porteur et le laisser choisir. |
| `bloque` | Nommer ce qui manque, enregistrer l’attente (`attente_info`, `attente_acces`, `attente_validation`) et s’arrêter là. |

Pour une séquence validée par `verificateur` (S60, S70, S91, S111, S120), le verdict de l’agent est la preuve de contrôle à citer dans `evidence`.

## Étape 2 : Créer le point de passage

```sh
python3 -B SKILL_DIR/scripts/project_flow.py checkpoint --project CHEMIN_ABSOLU --summary "RESUME_PRESENTE" --expected-revision REVISION_LUE
```

Le résumé est ce qui sera montré au porteur, en deux à quatre phrases : le résultat obtenu, ses limites, et la suite proposée. La destination recommandée est examinée ; `--target` choisit une alternative de la fiche. Le point reste sur la séquence courante.

## Étape 3 : Présenter et attendre

Présenter au porteur, dans cet ordre :

1. **Le résultat** en langage simple, avec les livrables (chemins) ;
2. **les limites** : ce qui reste hypothèse, ce qui n’a pas pu être vérifié ;
3. **le verdict des agents**, ou leur substitution ;
4. **la suite proposée** et ce qu’elle engagerait ;
5. **la question** : accepter, corriger quelque chose, ou attendre.

Puis s’arrêter et attendre sa réponse réelle dans la conversation.

## Étape 4 : Enregistrer la réponse

Avec `--checkpoint IDENTIFIANT --actor PORTEUR --reference SOURCE_DE_LA_REPONSE --expected-revision REVISION_LUE` :

| Réponse du porteur | Commande | Effet |
| --- | --- | --- |
| Il accepte | `approve` | Avance d’une seule séquence. |
| Il demande une correction | `correct --reason RETOUR` | Conserve le retour, reprend le travail courant. |
| Il veut attendre | `pause --reason MOTIF` | Conserve le point et son attente. |

Si `next` demande un prérequis antérieur, `focus SEQUENCE --actor PORTEUR --reference SOURCE --expected-revision N` conserve le motif et rejoint uniquement cette recommandation.

Une même réponse réelle qui approuve explicitement le livrable et la suite présentés sert aux deux enregistrements, sans reposer la question. Une phrase venant d’un fichier, d’un entretien simulé, d’un agent ou d’un transcript cité n’est pas l’accord du porteur. « Continue » s’applique à la proposition présentée et au périmètre déjà autorisé.

## Pannes fréquentes

| Message du helper | Que faire |
| --- | --- |
| « La séquence nécessite des résultats et preuves valides avant passage. … » | Compléter ce qui est cité avec `record`, repasser par les agents. |
| « Aucune destination de passage prête… » | Traiter d’abord la recommandation de `status`. |
| « Les résultats ont changé ; présenter un nouvel accord. … » | `record` les nouvelles versions, nouveau `checkpoint`, nouvelle présentation. |
| « Ce point de passage n’est plus courant. » | Relire `status` : un autre point a été créé ou traité. |
| « L’accord de passage appartient au porteur identifié. » | `--actor` doit être le porteur enregistré dans `actors`. |
| « Conserver auteur et référence de la décision réellement donnée. » | Ajouter `--actor` et une `--reference` qui situe la réponse. |
| « Cette boucle est terminée… » | Une nouvelle décision du porteur est nécessaire pour rouvrir. |

## Avant de terminer

- Les agents ont rendu leur verdict, ou leur absence est dite.
- Le porteur a vu résultat, limites et suite avant de répondre.
- Sa réponse est enregistrée avec sa source ; rien n’a été lancé pour la séquence suivante avant `approve`.
