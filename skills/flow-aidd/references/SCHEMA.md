# Les sept rubriques d’une séquence

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


| Rubrique | Ce qu’elle doit préciser |
| --- | --- |
| **input** | Ce qui doit être connu ou disponible ; les identités et versions réelles sont enregistrées dans l’état. |
| **responsible** | Un pilote responsable de la conduite ; la personne qui valide est nommée séparément. |
| **action** | Capacité à activer d’abord, travail à mener ensuite, questions utiles et limites de l’action. |
| **output** | Livrable concret ou décision, dans une source propriétaire identifiée. |
| **evidence** | Ce qui prouve la réalisation ou justifie la décision ; un fichier créé ne suffit pas à lui seul. |
| **validation** | Qui vérifie quoi et sur quelle version, avec une issue explicite. |
| **next** | Destination selon le résultat : avancer, préciser, réparer, attendre, réorienter ou arrêter. |

Le skill intervient dans **action** avant le dialogue ou l’analyse. Les questions et réponses acceptables présentes dans les fiches aident à construire la réponse ; elles ne sont pas déjà acquises.

Une validation recevable rattache le résultat à ses entrées et sorties versionnées, aux preuves, à la personne qui valide et à une issue du tableau de destinations.

Voir une fiche complète : [S40](sequences/S40.md). Voir un appel SDLC encodé explicitement : [S90](sequences/S90.md). Voir le cas complet : [EXEMPLE.md](EXEMPLE.md).

Les emplacements `natif_conditionnel` s’appliquent si le skill natif est invoqué. `propose` est une convention du guide et `a_resoudre` demande une résolution lors du travail réel. Ces gabarits ne sont pas des fichiers déjà créés.
