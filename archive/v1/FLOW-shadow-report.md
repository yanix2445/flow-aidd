---
source: /Users/yanis/Developer/flow-aidd/FLOW.md
generated_at: 2026-10-26
---

# Shadow Areas Report

Source: `/Users/yanis/Developer/flow-aidd/FLOW.md`
Generated: `2026-10-26`

Total gaps: 10 | Blocker: 0 | Major: 10 | Minor: 0

## Warnings

- Revue documentaire du flow et de ses représentations, pas validation de son exécution sur un projet réel.
- Sources complémentaires : `ORCHESTRATION.md`, `README.md`, `SCHEMA.md`, `MERMAID.md`, `workflow.json`, `schema.json`, les sources `.mmd` et les scripts de génération et vérification. Ces compléments comprennent des sources non Markdown ; les attributions sont précisées pour chaque constat.
- Les questions de diagnostic ci-dessous suivent les formes anglaises imposées par le skill shadow-areas. Les constats, conséquences et recommandations sont en français.
- Les niveaux concernent l’usage visé : un parcours compréhensible par un novice et fiable pour une IA. Aucun constat n’empêche un praticien de commencer une séance guidée ; les manques ne sont donc pas classés blocker.

## Lecture générale

Le découpage couvre les grands domaines d’un MVP numérique : besoin, positionnement, périmètre, expérience, faisabilité, socle, backlog, réalisation, recette, ouverture et apprentissage. Il distingue correctement produit livré, usage possible et valeur démontrée. Le rôle limité du SDLC et la distinction entre chemins natifs et proposés sont utiles.

La faiblesse principale est la conduite effective : plusieurs décisions restent interprétatives, les représentations ne constituent pas un protocole d’exécution, et la facilité d’emploi par un novice n’a pas été éprouvée. « Complet » peut décrire une couverture thématique ; cela ne démontre ni une procédure complète, ni une compréhension universelle, ni une optimisation pour l’IA.

## Gaps by Category

### unstated assumption

**[major]** How is the responsible skill activated before it helps produce the expected answer?
> entrée → sous-phase → question → réponse attendue → capacité responsable → résultat → décision de passage.

Preuves : `SCHEMA.md:7` ; `mermaid/02-phase.mmd:28-39`. Les liens placent la réponse avant le skill. Le principe opérationnel d’`ORCHESTRATION.md:7` place pourtant le choix de la capacité avant la production du résultat. Ce sont deux lectures différentes : une taxonomie des informations et un ordre de travail.

Conséquence : un novice peut croire qu’il doit fournir une réponse déjà aboutie avant d’utiliser brainstorm, recherche ou brief. Une IA doit interpréter quelle représentation décrit réellement l’exécution.

Correction attendue : distinguer le skill responsable de la chronologie, ou représenter explicitement contexte → activation du skill → dialogue/analyse → proposition → validation → persistance.

**[major]** How is semantic consistency maintained between the structured sources and the manually rewritten Mermaid labels?
> # Concise labels for the same questions and outputs in schema.json.

Preuves : `scripts/build_mermaid.py:8-47`, `schema.json`, `workflow.json`. Les libellés Mermaid sont réécrits dans `LABELS` ; les critères et suites sont aussi recopiés dans d’autres constantes. `scripts/verify_mermaid.cjs:19-48` contrôle la syntaxe, les nœuds et le rendu, pas l’équivalence du sens entre ces représentations.

Conséquence : une modification de règle peut ne pas atteindre toutes les vues. Ce constat établit un risque de divergence, pas que toutes les vues divergent déjà.

Correction attendue : choisir les champs propriétaires des décisions et dériver leurs représentations ; contrôler explicitement les différences lorsque des résumés sont conservés.

### ambiguous term

**[major]** What determines the minimum required depth for a specific project?
> Chaque niveau est un repère de réflexion. Adapter la profondeur au projet ; plusieurs éléments peuvent tenir dans une note courte. Ne pas créer tous les artefacts par défaut.

Preuves : `FLOW.md:7`, `ORCHESTRATION.md:102` et `scripts/build_flow.py:36-52`. Le texte permet d’alléger le parcours, mais le modèle et ses assertions imposent exactement 12 phases, 3 sous-phases par phase, 2 étapes par sous-phase et 2 actions par étape.

Conséquence : aucune règle pratique ne permet au novice ou à l’IA de choisir ce qui est obligatoire, condensable ou facultatif. La symétrie des comptes est une contrainte éditoriale, pas une preuve d’exhaustivité.

Correction attendue : définir un parcours de départ minimal et des approfondissements déclenchés par des besoins ou risques observés ; autoriser un nombre variable d’étapes.

### missing edge case

**[major]** How does a phase dependency become satisfied when the prerequisite is not applicable?
> "dependsOn": [5, 7, 8]

Preuves : `workflow.json:237`, `ORCHESTRATION.md:59` et `ORCHESTRATION.md:102`. Le modèle ne porte pas de règle de satisfaction pour un prérequis remplacé par une preuve existante ou déclaré non applicable. Exemple de limite : un produit sans interface graphique ne produit pas nécessairement les livrables de la phase UX/UI.

Conséquence : la règle générale d’adaptation et les dépendances doivent être réconciliées à la main. L’absence de fichier peut être confondue avec un prérequis non satisfait.

Correction attendue : consigner l’applicabilité et la preuve de satisfaction de chaque prérequis utile, sans imposer un moteur complexe.

**[major]** Which approved artifacts must be reconsidered after a scope decision changes?
> Ne pas rouvrir les choix approuvés sans un fait nouveau.

Preuves : `ORCHESTRATION.md:80` ; `FLOW.md:332` demande de revoir le PRD si l’apprentissage change le périmètre. Le droit de réexaminer existe, mais la conséquence sur design, architecture, stories, contrats, plans et validations acquises n’est pas décrite.

Conséquence : une IA peut continuer sur des documents approuvés devenus obsolètes, ou tout rouvrir inutilement.

Correction attendue : identifier la décision modifiée et ses sources, puis marquer les seuls livrables et validations affectés comme à réexaminer.

### missing actor

**[major]** Who owns the transition from a reviewed draft pull request to an integrated preproduction candidate?
> Ouvrir la PR en brouillon avec la validation ; suivre la politique du dépôt pour CI, promotion et fusion.

Preuves : `FLOW.md:584` puis `FLOW.md:601` ; `workflow.json:239` puis `workflow.json:266`. La sortie est une PR en brouillon et l’entrée suivante suppose des tranches intégrées en préproduction. La politique du dépôt est invoquée sans définir ici le responsable de cette transition et la preuve qu’elle a eu lieu.

Conséquence : un novice peut confondre revue du changement et intégration effective. Une IA doit résoudre une responsabilité non attribuée avant de passer à la recette globale.

Correction attendue : préciser qui vérifie la CI, autorise la fusion, constate l’intégration et fournit l’identité ou l’adresse du candidat à tester. Réutiliser la politique du dépôt lorsqu’elle existe.

**[major]** Who persists the project checkpoint after each meaningful session?
> Le modèle suivant est une convention proposée, à remplir pour un vrai projet.

Preuves : `ORCHESTRATION.md:61-80`. Un bon modèle de note de reprise est présent, mais son emplacement, son responsable d’écriture et son moment obligatoire de mise à jour ne sont pas fixés.

Conséquence : la reprise repose sur l’initiative du lecteur ou sur l’historique de conversation. Elle n’est pas reproductible entre sessions et agents.

Correction attendue : choisir une note d’état unique et confier explicitement sa mise à jour au coordinateur, avec l’étape courante, les preuves, les décisions, les inconnues et la prochaine action.

### missing failure mode

**[major]** How is the requested interactive mode encoded in the actual SDLC invocation?
> Utilise aidd-orchestrator:01-sdlc en mode interactif sur cette demande prête.

Preuves : `workflow.json:244`, `FLOW.md:589` et le fichier local `aidd-orchestrator/2.4.0/skills/01-sdlc/references/mode.md:5`. Le skill impose `interactive` comme premier mot entier de la requête ; son défaut est `auto`.

Conséquence : le prompt français exprime l’intention, mais sa reprise littérale ne respecte pas ce contrat. Un agent peut la traduire correctement ; cela n’est pas garanti par le flow. L’écart textuel est confirmé, le comportement d’un appel réel n’a pas été testé pendant cet audit.

Correction attendue : fournir une requête SDLC conforme commençant par `interactive`, avec une source concrète, et vérifier le mode retenu avant de laisser la livraison avancer.

**[major]** How is the next action selected from the actual cause of an unsuccessful phase?
> Non ou inconnu : reprendre le point manquant, retour possible en phase 8

Preuves : `mermaid/12-phase.mmd:26`, `workflow.json:241` et `workflow.json:325`. Les retours sont essentiellement une destination par phase. Les textes internes sont plus fins : `workflow.json:255` distingue problème produit et défaut de réalisation ; `ORCHESTRATION.md:112` autorise une conclusion encore indécidable faute d’observations.

Conséquence : le schéma ne représente pas clairement la différence entre corriger le code dans Deliver, clarifier le contrat, attendre des observations, réorienter ou arrêter. Les destinations sont des possibilités, pas un routeur suffisant.

Correction attendue : ajouter quelques issues explicites fondées sur la cause : clarification, réparation, attente de données ou d’accès, révision du périmètre, poursuite, arrêt.

### missing acceptance criterion

**[major]** What evidence must accompany a phase approval or an accepted risk?
> Des éléments réels éclairent le problème ; la poursuite repose sur des preuves identifiées ou sur un risque explicitement accepté.

Preuves : `FLOW.md:101`, `workflow.json:44`, `workflow.json:128`, `workflow.json:156`. Des critères existent et le PRD doit définir des mesures ; ils restent cependant des propositions en prose. Il manque un contrat minimal de validation reliant une décision à une preuve, une version de livrable et une éventuelle réserve.

Conséquence : des agents ou utilisateurs différents peuvent valider une phase à des niveaux de preuve très différents. Consigner les limites d’un test ne démontre pas à lui seul la compréhension ou la valeur.

Correction attendue : avant d’exécuter une étape, préciser le résultat vérifiable attendu, qui l’approuve et la preuve à conserver. En cas de risque accepté, consigner le manque, la raison et la prochaine vérification. Les seuils restent adaptés au projet ; aucun seuil numérique universel n’est nécessaire.

## Vérifications documentaires et lectures à blanc

Les contrôles Mermaid existants vérifient le parsing, les nœuds, les connexions et le rendu. Ils ne constituent ni une validation du processus, ni un test d’utilisabilité, ni un essai comparatif d’agents.

| Situation lue à blanc | Ce que les documents permettent de conclure | Limite constatée |
| --- | --- | --- |
| Un test de code échoue dans une tranche | Le texte détaillé renvoie à la réparation dans Deliver. | Le retour principal du schéma de phase 9 pointe vers le backlog ; il faut interpréter les deux niveaux. |
| Il manque encore des retours après l’ouverture | Le résultat peut rester indécidable selon ORCHESTRATION.md. | L’attente n’est pas une issue représentée dans le schéma détaillé de phase 12. |
| Le PRD change après approbation de l’UX | Le périmètre peut être révisé et les décisions réexaminées. | Les livrables et validations à invalider ne sont pas identifiés. |
| Une PR a été créée en brouillon | La tranche est proposée à la revue du dépôt. | La preuve de son intégration en préproduction manque pour démarrer la recette globale. |

Ces lectures sont des raisonnements à partir des sources, pas des exécutions d’un projet.

## Compréhension par un novice

La carte permet de voir les grandes activités. La conduite autonome reste insuffisamment étayée : absence de glossaire dédié, absence d’exemple complet de projet renseigné, critères de profondeur laissés au jugement et plusieurs présentations volumineuses du même contenu. Des termes comme PRD, SDLC, story, epic, scaffold ou tranche verticale demandent des connaissances que le lecteur novice ne possède pas nécessairement.

Cela n’établit pas qu’aucun novice ne peut comprendre. Cela établit que la compréhension et l’exécution sans accompagnement ne sont pas démontrées. Un novice accompagné par un agent compétent peut progresser, car les skills disposent de leurs propres échanges guidés.

## Compréhension et efficacité pour l’IA

Les identifiants de phases, les dépendances, les liens vers les skills, la distinction fait/hypothèse et la note de reprise proposée sont des fondations utiles. Un modèle de langage peut comprendre la vue globale.

La fiabilité d’exécution entre sessions demande encore un état réellement conservé, un contrat d’étape explicite, un routage par cause et la résolution des capacités présentes. La réécriture manuelle des mêmes intentions dans plusieurs sources augmente le risque de divergence et la charge de contexte. Les chemins de cache et versions figés dans les scripts réduisent aussi leur portabilité ; c’est une limite secondaire par rapport au routage et à l’état.

Il n’est pas nécessaire de construire un moteur d’orchestration, une nouvelle plateforme ou un système multi-agent général pour corriger ces limites. Une convention courte, des fichiers d’état et de décision simples, et le chargement de la seule étape courante peuvent suffire.

## Priorités proposées

1. Corriger le contrat d’appel SDLC, l’ordre représenté des opérations et le passage PR → candidat intégré.
2. Définir le contrat minimal d’une étape et une note de reprise tenue par le coordinateur.
3. Remplacer la décomposition symétrique obligatoire par un parcours essentiel avec approfondissements conditionnels.
4. Prévoir les issues de reprise, d’attente et de changement de périmètre ; garder les représentations cohérentes.
5. Fournir un exemple complet puis éprouver le parcours avec un novice et avec un agent sur un petit projet réel, notamment après interruption.

La sécurité, la confidentialité, les droits, la sauvegarde, le retour arrière, l’accessibilité, les coûts et le support sont déjà mentionnés dans le flow. Leur présence doit être conservée ; leur traitement concret dépend du produit et reste à vérifier lors d’un pilote.
