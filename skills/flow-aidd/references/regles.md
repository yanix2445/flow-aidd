# Règles complètes

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


La liste exhaustive, pour le vérificateur et les cas de doute. En conduite courante, [socle.md](socle.md) et la référence de la commande suffisent.

<a id="rubriques"></a>

## Les sept rubriques d’une séquence

| Rubrique | Ce qu’elle doit préciser |
| --- | --- |
| **input** | Ce qui doit être connu ou disponible ; les identités et versions réelles sont enregistrées dans l’état. |
| **responsible** | Un pilote responsable de la conduite ; la personne qui valide est nommée séparément. |
| **action** | Capacité à activer d’abord, travail à mener ensuite, questions utiles et limites de l’action. |
| **output** | Livrable concret ou décision, dans une source propriétaire identifiée. |
| **evidence** | Ce qui prouve la réalisation ou justifie la décision ; un fichier créé ne suffit pas à lui seul. |
| **validation** | Qui vérifie quoi et sur quelle version, avec une issue explicite. |
| **next** | Destination selon le résultat : avancer, préciser, réparer, attendre, réorienter ou arrêter. |

Les emplacements `natif_conditionnel` s’appliquent si le skill natif est invoqué. `propose` est une convention du guide et `a_resoudre` demande une résolution lors du travail réel. Ces gabarits ne sont pas des fichiers déjà créés.

<a id="regles"></a>

## Règles de conduite

1. Le coordinateur lit les consignes du projet, socle.md, l’état du projet et la seule fiche de séquence utile. Les autres sources sont chargées lorsqu’elles sont nécessaires.
2. Avant de travailler : vérifier l’applicabilité, les entrées, leurs versions et les dépendances. Une donnée inconnue ne devient jamais fausse par défaut.
3. Une inconnue prévue n’empêche pas l’idéation. Les champs de contexte sont résolus progressivement, au plus tard aux séquences required_at ; le coordinateur aide à les préciser sans inventer de réponse.
4. Activer la capacité responsable avant le dialogue, la recherche ou la production. Poser quelques questions utiles à la fois et attendre les réponses nécessaires.
5. Les questions et réponses attendues sont des guides, pas des réponses déjà obtenues. Une observation, une hypothèse, une décision et une simulation restent distinctes.
6. Les sept rubriques du contrat sont renseignées dans chaque séquence. Les livrables concrets et les preuves réelles sont liés à leur version.
7. Une autorisation déjà donnée pour un périmètre précis reste valable. Les décisions produit nouvelles restent avec le porteur ; les actes externes restent dans l’autorisation existante.
8. La validation précise le validateur, la date, les références de preuve et les versions d’entrée et de sortie. Un risque accepté précise le manque, la raison, son responsable et la prochaine vérification.
9. Le coordinateur utilise project_flow.py record pour conserver une décision, un livrable versionné, un contrôle significatif et la prochaine action dans {projet}/.flow/etat.json. Il fournit la révision lue ; le helper protège l’écriture et génère suivi.md.
10. Pour un prérequis non applicable, enregistrer la raison et la référence au cadrage approuvé. L’absence d’un fichier ne prouve pas la non-applicabilité.
11. Après un changement, versionner la source propriétaire et comparer les versions utilisées par les séquences déjà validées. Réexaminer les livrables affectés, sans réécrire une spec verrouillée.
12. Un risque technique bloquant peut déclencher S60 dès son apparition. Conserver resume_sequence pour revenir au bon travail si le périmètre ne change pas.
13. SDLC pilote sa boucle interne. Ne pas exécuter une seconde chaîne plan/implémentation/revue à côté. Sa requête interactive commence par le mot exact interactive, suivi d’une source concrète.
14. Une PR en brouillon n’est pas un candidat intégré. S91 vérifie explicitement contrôles, autorisation de fusion, intégration et révision de préproduction avant S100.
15. Les sorties WAIT_INFO et WAIT_ACCESS conservent la séquence courante ; STOP arrête la branche ; RESUME revient à la séquence mémorisée ; END termine la boucle choisie.
16. Les scripts vérifient la cohérence déclarée et la fraîcheur des versions enregistrées. Ils ne prouvent pas à eux seuls la véracité d’une observation, d’un résultat de commande ou d’une approbation.
17. Une preuve simulée n’est jamais recevable pour valider une instance réelle. Les exemples restent au mode illustration.
18. Les statuts du flow ne remplacent pas les statuts natifs des plans, stories et autres artefacts AIDD.
19. Pour les serveurs et les tâches bornées, respecter le gestionnaire et les règles du projet ; utiliser Portly lorsqu’il est prévu. Les vérifications des livrables doivent se faire sur la version réellement destinée à l’étape suivante.
20. Le mode d’exécution guide est conservé séparément du mode reel ou illustration. Un contrat satisfait ne change pas seul current_sequence : checkpoint conserve le résultat présenté, sa destination et l’empreinte des versions.
21. L’accord réel du porteur est conservé avec approve, correct ou pause sur le point de passage et la révision lus. Seul approve avance d’une séquence. Une recommandation, un hook ou le silence ne fournit jamais cet accord.
22. Une même réponse réelle peut approuver le livrable et le passage explicitement présentés ; conserver cette source dans les deux enregistrements sans reposer la question. Une décision native manquante reste en attente, sans preuve inventée.
23. Pour un fichier local, enregistrer son empreinte réelle ; pour un dossier, déclarer les fichiers de code suivis. Un contenu changé prend une nouvelle version et conduit au réexamen de ses validations dépendantes.
24. Le déplacement d’un projet passe par relocate ; une évolution du modèle passe par migration-plan puis migrate après examen. Conserver l’identité stable, les anciens enregistrements et les références de ces reprises.
25. AIDD reste la chaîne principale : ses artefacts (brief, PRD, epic, stories, spec, plan, mémoire) portent le besoin, le périmètre et le code, et le SDLC conduit la livraison. Chaque contexte a une seule source qui fait foi : le brief et le PRD pour le besoin et le périmètre, .agents/product-marketing.md (marketing-skills) pour le public, le positionnement et le ton, PRODUCT.md (Impeccable init) pour le contexte de design, rédigé à partir des deux premiers et y renvoyant, DESIGN.md (Impeccable document) pour le langage visuel réellement construit. Une source cite les autres sans les recopier ; une capacité conditionnelle ne s’active que si sa condition est vraie.

<a id="statuts"></a>

## Statuts d’une séquence

| Statut | Sens |
| --- | --- |
| `a_faire` | Séquence non commencée. |
| `en_cours` | Travail en cours, aucune validation finale acquise. |
| `attente_info` | Une réponse ou une observation manque ; consigner précisément laquelle. |
| `attente_acces` | Un outil, service ou droit requis manque. |
| `attente_validation` | Un livrable concret attend la décision compétente. |
| `a_reprendre` | Une preuve manque, un contrôle échoue ou une version d’entrée a changé. |
| `valide` | Critères contrôlés, preuves rattachées aux bonnes versions et décision conservée. |
| `non_applicable` | Condition explicitement fausse, justification et référence au cadrage approuvé conservées. |
| `arrete` | Arrêt explicite du travail sur cette branche. |

<a id="boucles"></a>

## Boucles

Après S91, l’issue `autre_tranche` ouvre une nouvelle itération de S80 : conserver l’ancien état dans history, identifier la nouvelle demande et réexaminer les validations affectées. L’issue `mvp_integre` conduit à la recette S100.

À S120, une fenêtre incomplète conserve `attente_info`. Zéro usage mesuré sur une fenêtre complète est une observation possible ; une mesure absente ne vaut pas zéro usage.

Une entrée modifiée rend ses validations dépendantes candidates à réexamen ; réexamen ne signifie pas reconstruction obligatoire. Les contrôles locaux ne vérifient pas les services distants ni la vérité d’un entretien.
