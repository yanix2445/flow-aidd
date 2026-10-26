# Schéma : questions → réponses attendues → skills → résultats

Questions de conduite proposées et réponses attendues ; aucune réponse produit n’est acquise. Les sorties sont des résultats attendus, pas des fichiers déjà créés.

Les questions sont proposées pour conduire chaque sous-phase. Les réponses décrivent le niveau de précision à atteindre ; elles ne sont pas des faits sur un projet déjà choisi.

**Lecture :** entrée → sous-phase → question → réponse attendue → capacité responsable → résultat → décision de passage.

**Origine des sorties :** `natif` = chemin ou nom défini par le skill installé ; `proposé` = convention de rangement de ce guide ; `à résoudre` = emplacement choisi par le skill, la stack ou le service au moment de l’exécution. Les chemins avec `<...>` sont des gabarits.

Les fichiers indiqués ne sont pas créés par la consultation du schéma. Un même document peut être enrichi dans plusieurs sous-phases. Seuls les livrables utiles au projet seront produits.

Les fondations et le backlog peuvent commencer selon leurs dépendances, sans attendre toutes les autres phases. Les neuf plugins n’assurent pas à eux seuls le déploiement ou la mesure : les outils externes nécessaires sont nommés comme tels.

## 1. Clarifier l’idée

**Entrée :** Une intuition, une frustration, une envie ou une observation.

### 1.1. Faire émerger l’intention

**Question :** Qui rencontre quelle difficulté, dans quelle situation concrète ?

**Réponse attendue :** Une personne ou un groupe précis, une tâche difficile, un contexte et le résultat souhaité.

**Capacités :**

- `aidd-refine:01-brainstorm`

**Résultats attendus :**

- **Note d’intention** — document ; `docs/idee.md` — proposé.

Étapes et sous-étapes : voir la section 1.1 dans [FLOW.md](FLOW.md).

### 1.2. Ouvrir puis choisir une piste

**Question :** Quel problème et quelle piste veux-tu explorer en premier ?

**Réponse attendue :** Un problème et une cible provisoires ; une piste retenue et les autres explicitement reportées.

**Capacités :**

- `aidd-refine:01-brainstorm`

**Résultats attendus :**

- **Piste retenue et alternatives** — mise à jour ; `docs/idee.md` — proposé.

Étapes et sous-étapes : voir la section 1.2 dans [FLOW.md](FLOW.md).

### 1.3. Cadrer l’exploration

**Question :** Quelles sont tes limites et quelle hypothèse pourrait invalider le projet ?

**Réponse attendue :** Temps, budget, objectif personnel ou commercial, contraintes et première inconnue à tester.

**Capacités :**

- `aidd-refine:01-brainstorm`

**Résultats attendus :**

- **Contraintes et hypothèses** — mise à jour ; `docs/idee.md` — proposé.

Étapes et sous-étapes : voir la section 1.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Tu peux expliquer une situation concrète, une personne concernée et le résultat espéré ; les inconnues sont visibles.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant.

## 2. Comprendre le besoin et les alternatives

**Entrée :** La note d’intention et l’hypothèse à vérifier.

### 2.1. Préparer une recherche utile

**Question :** Qui veut-on comprendre et quelle observation ferait changer notre avis ?

**Réponse attendue :** Un segment provisoire, une question de recherche, les faits recherchés et une limite d’effort.

**Capacités :**

- `marketing-skills:product-marketing`
- `aidd-pm:06-product-brief`

**Résultats attendus :**

- **Contexte marketing provisoire** — document ; `.agents/product-marketing.md` — natif.
- **Plan de recherche** — document ; `docs/recherche.md` — proposé.

Étapes et sous-étapes : voir la section 2.1 dans [FLOW.md](FLOW.md).

### 2.2. Recueillir des faits

**Question :** Que font les personnes aujourd’hui, et quelles difficultés observe-t-on réellement ?

**Réponse attendue :** Des observations ou retours sourcés et datés, les alternatives employées et les limites de l’échantillon.

**Capacités :**

- `marketing-skills:customer-research`

**Résultats attendus :**

- **Observations, sources et verbatims** — mise à jour ; `docs/recherche.md` — proposé.

Étapes et sous-étapes : voir la section 2.2 dans [FLOW.md](FLOW.md).

### 2.3. Interpréter sans surconclure

**Question :** Les éléments recueillis justifient-ils de poursuivre sur cette cible et ce besoin ?

**Réponse attendue :** Une synthèse des signaux et contradictions, puis une décision de poursuite, de réorientation ou d’arrêt.

**Capacités :**

- `marketing-skills:customer-research`
- `aidd-pm:06-product-brief`

**Résultats attendus :**

- **Synthèse et décision de découverte** — mise à jour ; `docs/recherche.md` — proposé.

Étapes et sous-étapes : voir la section 2.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Des éléments réels éclairent le problème ; la poursuite repose sur des preuves identifiées ou sur un risque explicitement accepté.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 1.

## 3. Choisir le positionnement et la viabilité

**Entrée :** La synthèse de découverte et les contraintes du porteur de projet.

### 3.1. Définir une promesse crédible

**Question :** Pour qui apporte-t-on quel bénéfice, par rapport à quelle alternative ?

**Réponse attendue :** Une cible prioritaire, une promesse crédible et une différence utile ; les suppositions restent signalées.

**Capacités :**

- `marketing-skills:product-marketing`

**Résultats attendus :**

- **Positionnement et promesse** — mise à jour ; `.agents/product-marketing.md` — natif.

Étapes et sous-étapes : voir la section 3.1 dans [FLOW.md](FLOW.md).

### 3.2. Vérifier la soutenabilité

**Question :** Comment atteindre les premiers utilisateurs et soutenir le coût du produit ?

**Réponse attendue :** Un canal initial, un coût acceptable et une hypothèse de financement ou de prix si le projet est commercial.

**Capacités :**

- `aidd-pm:06-product-brief`
- `marketing-skills:product-marketing`

**Résultats attendus :**

- **Viabilité et accès aux utilisateurs** — contenu du Brief ; `aidd_docs/product/<product-slug>.md` — natif.

Étapes et sous-étapes : voir la section 3.2 dans [FLOW.md](FLOW.md).

### 3.3. Formaliser le choix produit

**Question :** Quelle opportunité choisit-on et comment décidera-t-on si elle mérite la suite ?

**Réponse attendue :** L’opportunité, les contraintes, les risques et les conditions de validation approuvés.

**Capacités :**

- `aidd-pm:06-product-brief`

**Résultats attendus :**

- **Product Brief approuvé** — document ; `aidd_docs/product/<product-slug>.md` — natif.

Étapes et sous-étapes : voir la section 3.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Une cible prioritaire, une promesse crédible, un premier accès aux utilisateurs et une hypothèse de viabilité sont décidés.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 2.

## 4. Délimiter le MVP

**Entrée :** Le Product Brief et les hypothèses encore ouvertes.

### 4.1. Définir la preuve de valeur

**Question :** Quelle tâche complète doit prouver la valeur, et comment l’observer ?

**Réponse attendue :** Un résultat principal, un moment de premier bénéfice, un indicateur et une fenêtre d’observation.

**Capacités :**

- `aidd-pm:03-prd`

**Résultats attendus :**

- **Résultat et mesure de réussite** — contenu du PRD ; `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` — natif.

Étapes et sous-étapes : voir la section 4.1 dans [FLOW.md](FLOW.md).

### 4.2. Réduire le périmètre

**Question :** Que faut-il absolument inclure pour réussir cette tâche, et que reporte-t-on ?

**Réponse attendue :** Le périmètre minimal complet, les exclusions, les acteurs, les données et les règles métier.

**Capacités :**

- `aidd-pm:03-prd`

**Résultats attendus :**

- **Périmètre du MVP** — contenu du PRD ; `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` — natif.

Étapes et sous-étapes : voir la section 4.2 dans [FLOW.md](FLOW.md).

### 4.3. Rendre le contrat vérifiable

**Question :** Quels états, contraintes ou angles morts empêchent encore de valider le MVP ?

**Réponse attendue :** Les états utiles et contraintes de qualité ; les lacunes bloquantes résolues ou un risque explicitement accepté.

**Capacités :**

- `aidd-refine:03-shadow-areas`
- `aidd-pm:03-prd`

**Résultats attendus :**

- **PRD validé et angles morts traités** — document ; `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` — natif.

Étapes et sous-étapes : voir la section 4.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Le parcours principal est complet à son échelle ; les inclusions, exclusions et critères de réussite sont explicites.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 3.

## 5. Concevoir et éprouver l’expérience

**Entrée :** Le PRD et les contenus ou données réels disponibles.

### 5.1. Structurer le parcours

**Question :** Quel chemin mène la personne du point d’entrée au résultat promis ?

**Réponse attendue :** Un parcours avec écrans, actions, décisions, contenus et états importants ; un brief UX confirmé.

**Capacités :**

- `impeccable:impeccable — init puis shape`

**Résultats attendus :**

- **Contexte produit** — document ; `PRODUCT.md` — natif.
- **Parcours et brief UX** — document ou croquis ; `docs/parcours.md` — proposé.

Étapes et sous-étapes : voir la section 5.1 dans [FLOW.md](FLOW.md).

### 5.2. Choisir une direction d’interface

**Question :** Quelle direction visuelle et quels comportements servent ce parcours ?

**Réponse attendue :** Une direction choisie et les règles utiles de composants, rédaction, typographie, couleurs et interaction.

**Capacités :**

- `impeccable:impeccable — direction après shape`

**Résultats attendus :**

- **Direction de design** — document ; `DESIGN.md` — natif.
- **Prototype du parcours** — prototype ; `Emplacement choisi dans le projet` — à résoudre.

Étapes et sous-étapes : voir la section 5.2 dans [FLOW.md](FLOW.md).

### 5.3. Tester avant de généraliser

**Question :** La personne comprend-elle le prototype et réussit-elle la tâche ?

**Réponse attendue :** Des observations sur la compréhension, les blocages et les corrections ; la nature réelle ou simulée du test est précisée.

**Capacités :**

- `interfaces:better-interface`
- `impeccable:impeccable — critique`

**Résultats attendus :**

- **Retours UX et prototype corrigé** — rapport + prototype ; `docs/retours-ux.md` — proposé.

Étapes et sous-étapes : voir la section 5.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Le parcours principal est compréhensible ; les états importants sont conçus et les tests réalisés ou leurs limites sont consignés.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 4.

## 6. Valider la faisabilité et l’architecture

**Entrée :** Le PRD, les contraintes et les interactions proposées.

### 6.1. Réduire les incertitudes

**Question :** Quelle inconnue technique pourrait empêcher de tenir la promesse ?

**Réponse attendue :** Une question bornée, une preuve recherchée, un temps maximal et une conclusion avec ses limites.

**Capacités :**

- `aidd-pm:05-spike`

**Résultats attendus :**

- **Résultat de spike et preuve** — rapport + essai borné ; `Chemin résolu par le skill` — à résoudre.

Étapes et sous-étapes : voir la section 6.1 dans [FLOW.md](FLOW.md).

### 6.2. Choisir une architecture proportionnée

**Question :** Quelle architecture satisfait les besoins avec le moins de complexité utile ?

**Réponse attendue :** Des options comparées puis un choix justifié : stack, données, accès, frontières et intégrations.

**Capacités :**

- `aidd-context:01-bootstrap — nouveau SaaS`

**Résultats attendus :**

- **Décisions d’architecture SaaS** — document ; `aidd_docs/INSTALL.md` — natif.

Étapes et sous-étapes : voir la section 6.2 dans [FLOW.md](FLOW.md).

### 6.3. Préparer la réalisation

**Question :** Comment installer et exploiter ce choix, et son coût reste-t-il acceptable ?

**Réponse attendue :** Des environnements, un chemin d’installation, les coûts et les conséquences sur le périmètre ou l’UX.

**Capacités :**

- `aidd-context:01-bootstrap — nouveau SaaS`

**Résultats attendus :**

- **Installation et exploitation prévues** — mise à jour ; aucun scaffold ; `aidd_docs/INSTALL.md` — natif.

Étapes et sous-étapes : voir la section 6.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Les risques techniques déterminants sont éprouvés ou bornés ; architecture, coût et plan d’installation correspondent au MVP.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 4.

## 7. Préparer les fondations du projet

**Entrée :** Les décisions techniques validées et le plan d’installation.

### 7.1. Mettre en place le socle

**Question :** Quel socle réel faut-il créer ou réutiliser pour commencer ?

**Réponse attendue :** Le dépôt, les conventions, les dépendances minimales et les environnements ; les secrets restent hors des fichiers suivis.

**Capacités :**

- `aidd-vcs:00-repo-init`
- `aidd-dev:01-plan`
- `aidd-dev:02-implement`

**Résultats attendus :**

- **Dépôt et scaffold réels** — code + configuration ; `Fichiers adaptés à la stack choisie` — à résoudre.

Étapes et sous-étapes : voir la section 7.1 dans [FLOW.md](FLOW.md).

### 7.2. Vérifier le chemin de livraison

**Question :** Une petite tranche fonctionne-t-elle localement et en préproduction ?

**Réponse attendue :** Un chemin réel de bout en bout, les commandes de vérification et les preuves sur la version testée.

**Capacités :**

- `aidd-dev:03-assert`
- `aidd-dev:06-test`

**Résultats attendus :**

- **Socle vérifié** — code + exécution ; `Code, configuration CI et URL de préproduction` — à résoudre.

Étapes et sous-étapes : voir la section 7.2 dans [FLOW.md](FLOW.md).

### 7.3. Transmettre le contexte aux agents

**Question :** Que doit lire un agent pour travailler et reprendre correctement le projet ?

**Réponse attendue :** L’architecture réellement présente, les règles, les commandes, les accès disponibles et la prochaine action.

**Capacités :**

- `aidd-context:02-project-memory`

**Résultats attendus :**

- **Contexte projet relié aux outils IA** — documents + configuration ; `Chemins résolus par project-memory` — à résoudre.

Étapes et sous-étapes : voir la section 7.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Une petite tranche de bout en bout peut tourner localement et en préproduction avec des vérifications reproductibles.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 6.

## 8. Organiser le backlog et la première tranche

**Entrée :** Le PRD, puis les décisions UX et techniques à mesure qu’elles arrivent.

### 8.1. Décomposer par résultat

**Question :** Quelles petites livraisons apportent chacune un résultat utile ?

**Réponse attendue :** Des tranches verticales reliées au PRD ; des epics seulement si le regroupement aide.

**Capacités :**

- `aidd-orchestrator:02-backlog`
- `aidd-pm:07-epic`
- `aidd-pm:02-user-stories`

**Résultats attendus :**

- **Stories du MVP** — documents ; `aidd_docs/backlog/stories/<slug>.md` — natif.

Étapes et sous-étapes : voir la section 8.1 dans [FLOW.md](FLOW.md).

### 8.2. Rendre la prochaine demande prête

**Question :** Que doit-on pouvoir observer pour dire que la prochaine demande est faite ?

**Réponse attendue :** Un acteur, un besoin, un résultat, des critères, les erreurs et dépendances pertinentes ; les inconnues sont levées.

**Capacités :**

- `aidd-pm:02-user-stories`
- `aidd-pm:04-spec — si nécessaire`

**Résultats attendus :**

- **Story prête** — mise à jour ; `aidd_docs/backlog/stories/<slug>.md` — natif.
- **Contrat si nécessaire** — document ; `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>_<slug>/spec.md` — natif.

Étapes et sous-étapes : voir la section 8.2 dans [FLOW.md](FLOW.md).

### 8.3. Ordonner sans tout figer

**Question :** Quelle tranche livre-t-on maintenant compte tenu de la valeur, du risque et des moyens ?

**Réponse attendue :** Une prochaine demande prête, ses dépendances et des demandes suivantes encore proportionnellement détaillées.

**Capacités :**

- `aidd-orchestrator:02-backlog`
- `aidd-pm:02-user-stories`

**Résultats attendus :**

- **Ordre et prochaine story** — état + documents ; `Backlog existant, sans copie concurrente` — à résoudre.

Étapes et sous-étapes : voir la section 8.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** La prochaine tranche est petite, utile, vérifiable et sans décision produit bloquante ; le reste peut rester moins détaillé.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 4.

## 9. Livrer par petites boucles SDLC

**Entrée :** Une demande prête et les contextes produit, UX et technique utiles.

### 9.1. Frame : établir le contrat

**Question :** Le contrat de cette tranche est-il suffisamment clair pour construire ?

**Réponse attendue :** L’artefact concerné, le résultat observable, les limites et les critères ; confirmation du contrat en mode interactif.

**Capacités :**

- `aidd-orchestrator:01-sdlc — Frame`
- `aidd-pm:04-spec — si le contrat manque`

**Résultats attendus :**

- **Contrat prêt** — document ; `Source existante ou spec.md dans le dossier de tâche` — à résoudre.

Étapes et sous-étapes : voir la section 9.1 dans [FLOW.md](FLOW.md).

### 9.2. Deliver : planifier, construire, vérifier

**Question :** Quel plan permet de livrer la tranche et quelles preuves vérifient sa réalisation ?

**Réponse attendue :** Un plan proportionné, puis un candidat implémenté avec assertions et tests pertinents ; les résultats sont consignés.

**Capacités :**

- `aidd-orchestrator:01-sdlc — Deliver`
- `aidd-dev:01-plan`
- `aidd-dev:02-implement`
- `aidd-dev:03-assert`
- `aidd-dev:06-test`
- `aidd-vcs:01-commit`

**Résultats attendus :**

- **Plan et phases techniques** — documents ; `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>_<feature-slug>/plan.md + phase-<n>.md` — natif.
- **Candidat vérifié** — code + exécution ; `Code, tests, commits et preuves du candidat` — à résoudre.

Étapes et sous-étapes : voir la section 9.2 dans [FLOW.md](FLOW.md).

### 9.3. Check : revoir et challenger

**Question :** Le candidat revu indépendamment tient-il le contrat et apporte-t-il le résultat ?

**Réponse attendue :** Une revue et un challenge avec écarts traités, puis le résultat présenté ; un changement de contrat retourne au cadrage.

**Capacités :**

- `aidd-orchestrator:01-sdlc — Check`
- `aidd-dev:05-review`
- `aidd-refine:02-challenge`
- `aidd-vcs:02-pull-request`

**Résultats attendus :**

- **Revue et livraison révisable** — rapports + PR ; `Rapports du candidat + URL de PR en brouillon` — à résoudre.

Étapes et sous-étapes : voir la section 9.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Le contrat est satisfait, les vérifications pertinentes passent et les conclusions de revue sont traitées.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 8.

## 10. Valider le MVP dans son ensemble

**Entrée :** Les tranches intégrées dans une préproduction représentative.

### 10.1. Vérifier le parcours intégré

**Question :** Le parcours intégré fonctionne-t-il réellement avec les droits et données prévus ?

**Réponse attendue :** Des résultats sur la version candidate : tâche complète, erreurs, persistance et contraintes de qualité pertinentes.

**Capacités :**

- `aidd-dev:03-assert`
- `aidd-dev:06-test`

**Résultats attendus :**

- **Vérification globale du candidat** — rapport + preuves ; `docs/recette-mvp.md` — proposé.

Étapes et sous-étapes : voir la section 10.1 dans [FLOW.md](FLOW.md).

### 10.2. Vérifier l’usage réel

**Question :** L’interface rendue permet-elle à la cible d’accomplir cette tâche ?

**Réponse attendue :** Les observations d’interface, d’accessibilité et d’usage, avec la preuve d’une recette externe ou sa limite explicite.

**Capacités :**

- `interfaces:better-interface`
- `impeccable:impeccable — audit puis polish si utile`

**Résultats attendus :**

- **Recette d’usage et corrections** — rapport + interface corrigée ; `docs/recette-mvp.md` — proposé.

Étapes et sous-étapes : voir la section 10.2 dans [FLOW.md](FLOW.md).

### 10.3. Décider de l’ouverture

**Question :** Peut-on ouvrir cette version, avec quelles limites et quel moyen de revenir en arrière ?

**Réponse attendue :** Les écarts bloquants traités, les autres limites acceptées, la première population et un retour arrière préparé.

**Capacités :**

- `aidd-refine:02-challenge`

**Résultats attendus :**

- **Décision d’ouverture et retour arrière** — décision + procédure ; `docs/lancement.md` — proposé.

Étapes et sous-étapes : voir la section 10.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Le parcours principal passe en environnement représentatif ; aucun problème bloquant connu ne reste sans résolution et les limites restantes sont acceptées.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 9.

## 11. Mettre le MVP entre les mains des utilisateurs

**Entrée :** Un candidat validé, un canal initial et une population de lancement définie.

### 11.1. Préparer l’accès et la présentation

**Question :** Comment la première population comprend-elle la promesse et commence-t-elle ?

**Réponse attendue :** Un message juste, un accès prévu, un premier usage compréhensible et un support facile à trouver.

**Capacités :**

- `marketing-skills:launch`
- `marketing-skills:product-marketing`

**Résultats attendus :**

- **Présentation et démarrage** — contenus + interface ; `Page, invitation ou démonstration selon le canal` — à résoudre.

Étapes et sous-étapes : voir la section 11.1 dans [FLOW.md](FLOW.md).

### 11.2. Livrer et ouvrir à la bonne population

**Question :** La version livrée est-elle accessible et fonctionnelle pour la population prévue ?

**Réponse attendue :** Une adresse vérifiée après déploiement, une ouverture dans le périmètre autorisé et une surveillance initiale.

**Capacités :**

- `Outil réel de l’hébergeur — hors de ces neuf plugins`
- `marketing-skills:launch`
- `aidd-vcs:03-release-tag — si utile`

**Résultats attendus :**

- **Version accessible** — déploiement + accès ; `URL de production ou accès privé vérifié` — à résoudre.
- **Version et notes si nécessaires** — version Git ; `Tag et notes de release` — à résoudre.

Étapes et sous-étapes : voir la section 11.2 dans [FLOW.md](FLOW.md).

### 11.3. Vérifier la boucle de retours

**Question :** Peut-on observer le premier bénéfice et recevoir les problèmes rencontrés ?

**Réponse attendue :** Une mesure testée sans doublon, un canal de retours fonctionnel et des premières observations datées.

**Capacités :**

- `marketing-skills:launch`
- `Outils de mesure et de support du projet`

**Résultats attendus :**

- **Mesure et retours opérationnels** — configuration + données ; `Événements vérifiés, retours et suivi d’erreurs` — à résoudre.

Étapes et sous-étapes : voir la section 11.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** Le produit fonctionne après livraison pour la population prévue et le résultat principal peut être observé.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 10.

## 12. Mesurer, apprendre et choisir la suite

**Entrée :** Les premières observations d’usage, les retours et la fenêtre de mesure prévue.

### 12.1. Observer l’utilisation

**Question :** Que font réellement les utilisateurs et qu’est-ce qui les aide ou les bloque ?

**Réponse attendue :** Des mesures et retours contextualisés sur la fenêtre prévue, avec les limites d’échantillon et de mesure.

**Capacités :**

- `marketing-skills:customer-research`
- `Outils de mesure du projet`

**Résultats attendus :**

- **Premiers usages et retours** — rapport + données ; `docs/bilan-mvp.md` — proposé.

Étapes et sous-étapes : voir la section 12.1 dans [FLOW.md](FLOW.md).

### 12.2. Réviser les hypothèses

**Question :** Quelles hypothèses sont étayées, contredites ou encore indécidables ?

**Réponse attendue :** Une comparaison des attentes et des faits, puis une décision de stabiliser, améliorer, réorienter ou arrêter.

**Capacités :**

- `marketing-skills:customer-research`
- `aidd-refine:02-challenge`

**Résultats attendus :**

- **Bilan de validation** — mise à jour + décision ; `docs/bilan-mvp.md` — proposé.

Étapes et sous-étapes : voir la section 12.2 dans [FLOW.md](FLOW.md).

### 12.3. Préparer la prochaine boucle

**Question :** Quelle est maintenant la seule prochaine priorité utile ?

**Réponse attendue :** Une prochaine demande ou une nouvelle recherche ; les contextes concernés reflètent les décisions approuvées.

**Capacités :**

- `aidd-orchestrator:02-backlog`
- `marketing-skills:product-marketing`

**Résultats attendus :**

- **Prochaine boucle et contexte à jour** — documents + état ; `Backlog + .agents/product-marketing.md` — à résoudre.

Étapes et sous-étapes : voir la section 12.3 dans [FLOW.md](FLOW.md).

**Décision de passage :** La décision s’appuie sur des faits datés et leurs limites ; le prochain changement ou l’arrêt est explicite.

**Si oui :** satisfaire les dépendances de la phase suivante ou livrer la tranche suivante. **Si non :** reprendre le point manquant ; retour possible vers la phase 8.
