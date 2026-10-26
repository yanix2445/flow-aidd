# De l’idée vague au premier MVP utilisable

Cadre proposé, version 1.0 — capacités locales consultées le 2026-10-26.

12 phases · 36 sous-phases · 72 étapes · 144 sous-étapes.

Chaque niveau est un repère de réflexion. Adapter la profondeur au projet ; plusieurs éléments peuvent tenir dans une note courte. Ne pas créer tous les artefacts par défaut.

Les décisions de produit restent avec le porteur du projet. Une preuve manquante reste une inconnue ou un risque accepté, jamais une validation inventée. Le coordinateur choisit une prochaine étape utile ; il ne déroule pas douze phases automatiquement.

Voir [README.md](README.md) pour la carte des dépendances et [ORCHESTRATION.md](ORCHESTRATION.md) pour les règles de conduite et de reprise.

## Sommaire

- [1. Clarifier l’idée](#phase-1) — Explorer
- [2. Comprendre le besoin et les alternatives](#phase-2) — Explorer
- [3. Choisir le positionnement et la viabilité](#phase-3) — Explorer
- [4. Délimiter le MVP](#phase-4) — Concevoir
- [5. Concevoir et éprouver l’expérience](#phase-5) — Concevoir
- [6. Valider la faisabilité et l’architecture](#phase-6) — Concevoir
- [7. Préparer les fondations du projet](#phase-7) — Construire
- [8. Organiser le backlog et la première tranche](#phase-8) — Construire
- [9. Livrer par petites boucles SDLC](#phase-9) — Construire
- [10. Valider le MVP dans son ensemble](#phase-10) — Lancer et apprendre
- [11. Mettre le MVP entre les mains des utilisateurs](#phase-11) — Lancer et apprendre
- [12. Mesurer, apprendre et choisir la suite](#phase-12) — Lancer et apprendre

<a id="phase-1"></a>

## 1. Clarifier l’idée

**Ensemble :** Explorer · **Dépendances :** aucune.

**Question :** Quel changement veux-tu apporter, et à qui ?

**Entrée :** Une intuition, une frustration, une envie ou une observation.

**Livrable :** Une note d’intention : cible provisoire, problème, résultat, contraintes et inconnues.

**Critère de passage :** Tu peux expliquer une situation concrète, une personne concernée et le résultat espéré ; les inconnues sont visibles.

**À adapter :** Explorer plusieurs pistes seulement si le problème ou la cible restent ouverts.

**Skills mobilisables :** `aidd-refine:01-brainstorm`.

### 1.1 Faire émerger l’intention

**1.1.1 — Raconter la situation de départ**

- 1.1.1.1 — Décrire un exemple récent et concret de la difficulté.
- 1.1.1.2 — Nommer la personne qui la rencontre et ce qu’elle tente de faire.

**1.1.2 — Formuler le changement souhaité**

- 1.1.2.1 — Décrire le résultat utile sans imposer une fonctionnalité.
- 1.1.2.2 — Expliquer pourquoi tu veux travailler sur ce sujet maintenant.

### 1.2 Ouvrir puis choisir une piste

**1.2.1 — Séparer problème et solution imaginée**

- 1.2.1.1 — Lister ce qui a été observé et ce qui est supposé.
- 1.2.1.2 — Comparer quelques réponses possibles, y compris une solution manuelle.

**1.2.2 — Retenir un angle de départ**

- 1.2.2.1 — Choisir une cible et un problème provisoires.
- 1.2.2.2 — Mettre les autres pistes de côté avec leur raison de report.

### 1.3 Cadrer l’exploration

**1.3.1 — Poser les limites réelles**

- 1.3.1.1 — Préciser le temps disponible, le budget, les compétences et les contraintes.
- 1.3.1.2 — Distinguer objectif d’apprentissage, usage personnel et ambition commerciale.

**1.3.2 — Choisir l’inconnue prioritaire**

- 1.3.2.1 — Repérer l’hypothèse dont l’échec rendrait le projet inutile.
- 1.3.2.2 — Décider quelle observation permettrait de la remettre en cause.

**Pour engager cette phase :**

```text
Utilise aidd-refine:01-brainstorm pour clarifier mon idée. Distingue mes décisions, les preuves disponibles et les hypothèses. Aide-moi à choisir le prochain point à éclaircir, sans choisir une stack ni construire le produit.
```


<a id="phase-2"></a>

## 2. Comprendre le besoin et les alternatives

**Ensemble :** Explorer · **Dépendances :** 1.

**Question :** Le problème existe-t-il réellement pour la cible retenue ?

**Entrée :** La note d’intention et l’hypothèse à vérifier.

**Livrable :** Une synthèse de découverte avec sources, situations, alternatives, contradictions et limites.

**Critère de passage :** Des éléments réels éclairent le problème ; la poursuite repose sur des preuves identifiées ou sur un risque explicitement accepté.

**À adapter :** Étude de marché large et personas détaillés seulement si la décision le nécessite ; une hypothèse de segment ne devient pas un persona prouvé.

**Skills mobilisables :** `marketing-skills:product-marketing`, `marketing-skills:customer-research`, `aidd-pm:06-product-brief`.

**Retour principal si le critère échoue :** phase 1. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 2.1 Préparer une recherche utile

**2.1.1 — Définir la cible provisoire**

- 2.1.1.1 — Décrire le contexte d’usage et le déclencheur du besoin.
- 2.1.1.2 — Créer le contexte marketing minimal avec les inconnues signalées.

**2.1.2 — Préparer la vérification**

- 2.1.2.1 — Choisir une question et les observations attendues.
- 2.1.2.2 — Fixer une limite d’effort et une règle de poursuite, de réduction ou d’arrêt.

### 2.2 Recueillir des faits

**2.2.1 — Étudier les pratiques actuelles**

- 2.2.1.1 — Lire les retours, documents ou données déjà disponibles avec leur date et leur source.
- 2.2.1.2 — Observer les alternatives : concurrent, tableur, bricolage, délégation ou absence d’action.

**2.2.2 — Parler aux personnes concernées si possible**

- 2.2.2.1 — Préparer des questions sur les comportements passés et les difficultés réelles.
- 2.2.2.2 — Recueillir des retours autorisés et attribuer précisément citations et observations.

### 2.3 Interpréter sans surconclure

**2.3.1 — Regrouper les observations**

- 2.3.1.1 — Identifier les situations répétées, les écarts entre segments et les contradictions.
- 2.3.1.2 — Distinguer douleur observée, intérêt déclaré et engagement concret.

**2.3.2 — Décider de la suite**

- 2.3.2.1 — Évaluer les biais, la fraîcheur et les limites de l’échantillon.
- 2.3.2.2 — Poursuivre, réorienter la cible ou revenir à l’idée selon les faits recueillis.

**Pour engager cette phase :**

```text
À partir de la note d’intention, utilise marketing-skills:product-marketing puis marketing-skills:customer-research pour explorer le besoin. Propose un contexte provisoire avant les autres travaux marketing. Analyse les éléments existants, les alternatives et les contradictions ; n’invente ni entretiens ni personas.
```


<a id="phase-3"></a>

## 3. Choisir le positionnement et la viabilité

**Ensemble :** Explorer · **Dépendances :** 2.

**Question :** Pourquoi cette solution serait-elle choisie et soutenable ?

**Entrée :** La synthèse de découverte et les contraintes du porteur de projet.

**Livrable :** Un Product Brief et un contexte marketing cohérents, avec promesse, différenciation et stratégie de validation.

**Critère de passage :** Une cible prioritaire, une promesse crédible, un premier accès aux utilisateurs et une hypothèse de viabilité sont décidés.

**À adapter :** Prix, payeur et modèle économique si le projet est commercial ; sinon coût d’usage, maintenance et bénéfice attendu.

**Skills mobilisables :** `aidd-pm:06-product-brief`, `marketing-skills:product-marketing`, `marketing-skills:launch`.

**Retour principal si le critère échoue :** phase 2. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 3.1 Définir une promesse crédible

**3.1.1 — Choisir le cas d’usage prioritaire**

- 3.1.1.1 — Sélectionner le segment et la situation les mieux étayés.
- 3.1.1.2 — Décrire le résultat promis dans les mots de la cible.

**3.1.2 — Préciser la différence utile**

- 3.1.2.1 — Comparer cette promesse à l’alternative réellement employée.
- 3.1.2.2 — Relier chaque différence annoncée à un bénéfice ou la marquer comme hypothèse.

### 3.2 Vérifier la soutenabilité

**3.2.1 — Évaluer valeur et coût**

- 3.2.1.1 — Identifier utilisateur, bénéficiaire et payeur lorsqu’ils diffèrent.
- 3.2.1.2 — Estimer les principaux coûts, la maintenance et les limites du budget.

**3.2.2 — Préparer l’accès au terrain**

- 3.2.2.1 — Repérer où trouver les premiers utilisateurs et avec quel message.
- 3.2.2.2 — Choisir un premier canal réaliste et une manière de recueillir leurs retours.

### 3.3 Formaliser le choix produit

**3.3.1 — Rédiger le Product Brief**

- 3.3.1.1 — Rassembler opportunité, cible, valeur, contraintes et risques majeurs.
- 3.3.1.2 — Définir ce qui ferait poursuivre, changer de direction ou arrêter.

**3.3.2 — Aligner les documents de contexte**

- 3.3.2.1 — Faire valider les décisions produit et les hypothèses acceptées.
- 3.3.2.2 — Reporter le positionnement approuvé dans le contexte marketing sans créer deux vérités divergentes.

**Pour engager cette phase :**

```text
Utilise aidd-pm:06-product-brief pour cadrer l’opportunité et sa validation, puis aligne marketing-skills:product-marketing. Aide-moi à choisir la promesse, l’alternative de référence, le premier canal d’accès aux utilisateurs et les hypothèses de viabilité. Reste au niveau produit, sans exigences détaillées ni plan technique.
```


<a id="phase-4"></a>

## 4. Délimiter le MVP

**Ensemble :** Concevoir · **Dépendances :** 3.

**Question :** Quel est le plus petit parcours complet qui prouve la valeur ?

**Entrée :** Le Product Brief et les hypothèses encore ouvertes.

**Livrable :** Un PRD proportionné : résultat, périmètre, exclusions, règles, états, contraintes de qualité et mesure.

**Critère de passage :** Le parcours principal est complet à son échelle ; les inclusions, exclusions et critères de réussite sont explicites.

**À adapter :** Paiement, comptes, rôles complexes et intégrations seulement s’ils sont nécessaires à la promesse du MVP.

**Skills mobilisables :** `aidd-pm:03-prd`, `aidd-refine:03-shadow-areas`.

**Retour principal si le critère échoue :** phase 3. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 4.1 Définir la preuve de valeur

**4.1.1 — Choisir le résultat principal**

- 4.1.1.1 — Décrire l’action que l’utilisateur doit réussir de bout en bout.
- 4.1.1.2 — Définir le moment où il obtient un premier bénéfice concret.

**4.1.2 — Définir l’observation du succès**

- 4.1.2.1 — Choisir un indicateur principal, sa méthode de mesure et sa fenêtre d’observation.
- 4.1.2.2 — Fixer les critères de poursuite et les limites de cette première mesure.

### 4.2 Réduire le périmètre

**4.2.1 — Conserver le nécessaire**

- 4.2.1.1 — Relier chaque capacité envisagée au résultat principal.
- 4.2.1.2 — Retirer ou rendre manuelles les capacités qui ne sont pas indispensables à sa preuve.

**4.2.2 — Écrire les frontières**

- 4.2.2.1 — Lister clairement ce qui entre dans le MVP et ce qui attendra.
- 4.2.2.2 — Préciser les profils concernés, les données nécessaires et les règles métier.

### 4.3 Rendre le contrat vérifiable

**4.3.1 — Couvrir les états et la qualité**

- 4.3.1.1 — Décrire démarrage, vide, chargement, erreur, succès et permissions lorsqu’ils existent.
- 4.3.1.2 — Définir les besoins pertinents d’accessibilité, de fiabilité, de confidentialité et de performance.

**4.3.2 — Traiter les angles morts**

- 4.3.2.1 — Examiner le PRD avec shadow-areas et résoudre les lacunes qui changent le produit.
- 4.3.2.2 — Valider le périmètre avant d’investir dans la conception détaillée et la construction.

**Pour engager cette phase :**

```text
Utilise aidd-pm:03-prd à partir du Product Brief pour définir un MVP complet sur un périmètre réduit. Décris ce qu’il doit permettre et pourquoi, les exclusions, les états importants et la mesure de réussite. Utilise aidd-refine:03-shadow-areas pour relever les angles morts avant validation.
```


<a id="phase-5"></a>

## 5. Concevoir et éprouver l’expérience

**Ensemble :** Concevoir · **Dépendances :** 4.

**Question :** Une personne comprend-elle comment obtenir le résultat promis ?

**Entrée :** Le PRD et les contenus ou données réels disponibles.

**Livrable :** Le parcours, un prototype adapté au risque, PRODUCT.md, DESIGN.md et les décisions d’interface utiles.

**Critère de passage :** Le parcours principal est compréhensible ; les états importants sont conçus et les tests réalisés ou leurs limites sont consignés.

**À adapter :** Prototype cliquable et tests terrain approfondis pour une interaction incertaine ; croquis et vérification ciblée pour un parcours simple connu.

**Skills mobilisables :** `impeccable:impeccable`, `interfaces:better-interface`.

**Retour principal si le critère échoue :** phase 4. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 5.1 Structurer le parcours

**5.1.1 — Cartographier les tâches**

- 5.1.1.1 — Relier point d’entrée, actions, décisions et résultat obtenu.
- 5.1.1.2 — Retirer les étapes qui n’apportent ni valeur ni information nécessaire.

**5.1.2 — Organiser les écrans et contenus**

- 5.1.2.1 — Poser l’architecture de l’information et les premiers croquis.
- 5.1.2.2 — Décrire chaque état utile avec des contenus plausibles et explicitement sourcés.

### 5.2 Choisir une direction d’interface

**5.2.1 — Établir le contexte de design**

- 5.2.1.1 — Dériver PRODUCT.md des décisions approuvées en liant le Brief et le PRD.
- 5.2.1.2 — Faire confirmer le brief shape puis la direction visuelle avant l’implémentation.

**5.2.2 — Définir les éléments réutilisables**

- 5.2.2.1 — Formaliser la direction dans DESIGN.md et les briefs de surfaces nécessaires.
- 5.2.2.2 — Définir typographie, couleurs, composants, rédaction et comportements accessibles au bon niveau de détail.

### 5.3 Tester avant de généraliser

**5.3.1 — Éprouver une tâche représentative**

- 5.3.1.1 — Faire réaliser le parcours sur le prototype et noter les hésitations observées.
- 5.3.1.2 — Distinguer retour d’un utilisateur réel, auto-évaluation et simulation.

**5.3.2 — Revoir les points qui bloquent**

- 5.3.2.1 — Corriger compréhension, navigation, erreurs et adaptation aux petits écrans.
- 5.3.2.2 — Revoir le PRD si l’apprentissage change la promesse ou le périmètre.

**Pour engager cette phase :**

```text
À partir du PRD, utilise Impeccable init puis shape pour établir le contexte produit et concevoir le parcours sans code produit. Fais préciser la hiérarchie, les contenus et les états. Après confirmation, prépare un prototype proportionné ; utilise Interfaces pour vérifier la compréhension, l’accessibilité et l’adaptation aux écrans.
```


<a id="phase-6"></a>

## 6. Valider la faisabilité et l’architecture

**Ensemble :** Concevoir · **Dépendances :** 4.

**Question :** Peut-on délivrer cette promesse avec les moyens disponibles ?

**Entrée :** Le PRD, les contraintes et les interactions proposées.

**Livrable :** Les décisions techniques et les preuves de faisabilité ; aidd_docs/INSTALL.md si bootstrap est adapté.

**Critère de passage :** Les risques techniques déterminants sont éprouvés ou bornés ; architecture, coût et plan d’installation correspondent au MVP.

**À adapter :** Un spike dès qu’un risque peut invalider le projet, même plus tôt ; bootstrap est conçu pour un nouveau SaaS et produit de la documentation, jamais le scaffold.

**Skills mobilisables :** `aidd-pm:05-spike`, `aidd-context:01-bootstrap`.

**Retour principal si le critère échoue :** phase 4. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 6.1 Réduire les incertitudes

**6.1.1 — Identifier les risques structurants**

- 6.1.1.1 — Repérer API indispensable, accès aux données, performance, coût ou contrainte de plateforme.
- 6.1.1.2 — Séparer ce qui est connu, testé, supposé et inaccessible.

**6.1.2 — Conduire un spike borné si nécessaire**

- 6.1.2.1 — Définir une question, une durée maximale et une preuve de sortie.
- 6.1.2.2 — Conclure avec résultat, limites et conséquence sur le MVP plutôt qu’un prototype qui devient production par défaut.

### 6.2 Choisir une architecture proportionnée

**6.2.1 — Comparer les options pertinentes**

- 6.2.1.1 — Comparer quelques solutions selon contraintes, compétences et exploitation.
- 6.2.1.2 — Choisir l’option la plus simple qui satisfait les besoins constatés.

**6.2.2 — Concevoir les frontières techniques**

- 6.2.2.1 — Définir données, accès, intégrations et responsabilités des composants.
- 6.2.2.2 — Prévoir erreurs, sauvegarde, restauration et gestion des secrets selon le risque.

### 6.3 Préparer la réalisation

**6.3.1 — Décrire installation et exploitation**

- 6.3.1.1 — Documenter environnements, dépendances, hébergement et commandes nécessaires.
- 6.3.1.2 — Estimer les coûts initiaux et récurrents ainsi que les plafonds acceptables.

**6.3.2 — Réconcilier produit et technique**

- 6.3.2.1 — Vérifier que l’architecture permet le parcours et sa mesure.
- 6.3.2.2 — Revenir au périmètre ou au design si une contrainte impose un changement visible.

**Pour engager cette phase :**

```text
Évalue la faisabilité du PRD et traite les inconnues bloquantes avec aidd-pm:05-spike. Pour un nouveau SaaS, utilise aidd-context:01-bootstrap afin de comparer des stacks proportionnées et produire INSTALL.md. Pour un autre type de projet, adapte le cadrage technique sans imposer le questionnaire SaaS. Ne confonds pas cette documentation avec l’installation réelle.
```


<a id="phase-7"></a>

## 7. Préparer les fondations du projet

**Ensemble :** Construire · **Dépendances :** 6.

**Question :** Peut-on développer, vérifier et livrer une première tranche de façon reproductible ?

**Entrée :** Les décisions techniques validées et le plan d’installation.

**Livrable :** Un dépôt fonctionnel, un environnement reproductible, les premières vérifications et le contexte projet.

**Critère de passage :** Une petite tranche de bout en bout peut tourner localement et en préproduction avec des vérifications reproductibles.

**À adapter :** Réutiliser dépôt, stack et conventions existants ; repo-init est expérimental. Créer les accès externes uniquement dans le périmètre autorisé.

**Skills mobilisables :** `aidd-vcs:00-repo-init`, `aidd-dev:01-plan`, `aidd-dev:02-implement`, `aidd-context:02-project-memory`.

**Retour principal si le critère échoue :** phase 6. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 7.1 Mettre en place le socle

**7.1.1 — Préparer le dépôt et les conventions**

- 7.1.1.1 — Réutiliser ou initialiser le dépôt et décider le fonctionnement des branches et revues.
- 7.1.1.2 — Poser les règles de contribution, les fichiers ignorés et les exemples de configuration sans secrets.

**7.1.2 — Créer le scaffold réel**

- 7.1.2.1 — Installer le minimum nécessaire dans le cadre d’un plan technique borné.
- 7.1.2.2 — Configurer les environnements et les premiers services effectivement requis.

### 7.2 Vérifier le chemin de livraison

**7.2.1 — Exécuter les premières vérifications**

- 7.2.1.1 — Rendre reproductibles build, typage et vérifications adaptées à la stack.
- 7.2.1.2 — Ajouter une intégration continue proportionnée lorsque le mode de livraison la nécessite.

**7.2.2 — Faire fonctionner une tranche minimale**

- 7.2.2.1 — Vérifier un chemin interface, logique, données et retour lorsqu’ils existent.
- 7.2.2.2 — Tester un déploiement en préproduction et la configuration qui l’accompagne.

### 7.3 Transmettre le contexte aux agents

**7.3.1 — Documenter l’existant vérifié**

- 7.3.1.1 — Écrire architecture, conventions, commandes et accès réellement disponibles.
- 7.3.1.2 — Lier Brief, PRD, design et décisions techniques au lieu d’en dupliquer le contenu.

**7.3.2 — Établir le point de reprise**

- 7.3.2.1 — Relier les outils d’IA utilisés au contexte projet approprié.
- 7.3.2.2 — Consigner les limites connues et la prochaine action de construction.

**Pour engager cette phase :**

```text
Prépare les fondations à partir des décisions techniques. Réutilise ce qui existe ; utilise aidd-vcs:00-repo-init si un dépôt doit être initialisé, puis un plan et une implémentation bornés pour le scaffold réel. Vérifie une tranche de bout en bout avant de formaliser le contexte avec aidd-context:02-project-memory. Utilise Portly pour les serveurs et les tâches bornées.
```


<a id="phase-8"></a>

## 8. Organiser le backlog et la première tranche

**Ensemble :** Construire · **Dépendances :** 4.

**Question :** Que livre-t-on en premier et comment saura-t-on que c’est fait ?

**Entrée :** Le PRD, puis les décisions UX et techniques à mesure qu’elles arrivent.

**Livrable :** Un backlog ordonné et une première demande prête, avec résultat observable, critères et dépendances.

**Critère de passage :** La prochaine tranche est petite, utile, vérifiable et sans décision produit bloquante ; le reste peut rester moins détaillé.

**À adapter :** Epics si plusieurs résultats doivent être regroupés ; spec séparée si le contrat manque de précision. Ne pas dupliquer une demande déjà prête.

**Skills mobilisables :** `aidd-orchestrator:02-backlog`, `aidd-pm:07-epic`, `aidd-pm:02-user-stories`, `aidd-pm:04-spec`.

**Retour principal si le critère échoue :** phase 4. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 8.1 Décomposer par résultat

**8.1.1 — Repérer les capacités nécessaires**

- 8.1.1.1 — Relier chaque demande au parcours et au résultat du MVP.
- 8.1.1.2 — Regrouper par epic uniquement si cela aide à comprendre plusieurs résultats.

**8.1.2 — Découper des tranches verticales**

- 8.1.2.1 — Définir de petites livraisons qui traversent les couches nécessaires.
- 8.1.2.2 — Éviter un découpage uniquement frontend, backend puis intégration finale.

### 8.2 Rendre la prochaine demande prête

**8.2.1 — Décrire un comportement observable**

- 8.2.1.1 — Préciser acteur, besoin, résultat et critères d’acceptation.
- 8.2.1.2 — Inclure les erreurs et droits pertinents ainsi que la preuve attendue.

**8.2.2 — Lever les dépendances bloquantes**

- 8.2.2.1 — Identifier données, contenus, services et décisions encore manquants.
- 8.2.2.2 — Créer un spike ou revoir le contrat si une incertitude empêche une estimation utile.

### 8.3 Ordonner sans tout figer

**8.3.1 — Choisir l’ordre de livraison**

- 8.3.1.1 — Faire passer tôt les preuves de valeur et les risques structurants.
- 8.3.1.2 — Ajuster au temps et à la capacité disponibles sans promettre une date inventée.

**8.3.2 — Confirmer la prochaine tranche**

- 8.3.2.1 — Vérifier ses critères d’entrée et les exclusions.
- 8.3.2.2 — Laisser les demandes suivantes au niveau de détail nécessaire à la décision suivante.

**Pour engager cette phase :**

```text
Utilise aidd-orchestrator:02-backlog pour organiser les demandes issues du PRD. Fais produire les user stories par aidd-pm:02-user-stories et les epics seulement si utiles. Découpe en tranches de valeur, explicite les dépendances et prépare surtout la prochaine tranche. Produis une spec uniquement si le contrat reste insuffisant.
```


<a id="phase-9"></a>

## 9. Livrer par petites boucles SDLC

**Ensemble :** Construire · **Dépendances :** 5, 7, 8.

**Question :** Cette tranche apporte-t-elle le résultat prévu, avec des preuves ?

**Entrée :** Une demande prête et les contextes produit, UX et technique utiles.

**Livrable :** Un candidat vérifié et revu, puis une PR en brouillon lorsque le dépôt distant le permet.

**Critère de passage :** Le contrat est satisfait, les vérifications pertinentes passent et les conclusions de revue sont traitées.

**À adapter :** Une boucle par changement cohérent. SDLC inclut déjà le cadrage, le plan, l’exécution, la validation, la revue et la PR ; ne pas les relancer en double.

**Skills mobilisables :** `aidd-orchestrator:01-sdlc`, `aidd-dev:01-plan`, `aidd-dev:02-implement`, `aidd-dev:03-assert`, `aidd-dev:06-test`, `aidd-dev:05-review`, `aidd-refine:02-challenge`, `aidd-vcs:01-commit`, `aidd-vcs:02-pull-request`.

**Retour principal si le critère échoue :** phase 8. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 9.1 Frame : établir le contrat

**9.1.1 — Reprendre la source existante**

- 9.1.1.1 — Utiliser directement une demande déjà prête ou clarifier seulement ce qui change le résultat.
- 9.1.1.2 — Formaliser les exigences manquantes sans réécrire une spec verrouillée.

**9.1.2 — Fixer le résultat et la vérification**

- 9.1.2.1 — Relier le contrat aux critères de la story et au PRD.
- 9.1.2.2 — En mode interactif, faire valider le contrat avant la réalisation.

### 9.2 Deliver : planifier, construire, vérifier

**9.2.1 — Préparer puis exécuter le plan**

- 9.2.1.1 — Explorer le code, proposer le plan proportionné et le faire valider en mode interactif.
- 9.2.1.2 — Implémenter chaque tâche avec ses vérifications et des commits locaux cohérents.

**9.2.2 — Valider le candidat**

- 9.2.2.1 — Exécuter les assertions, les vérifications frontend et les tests pertinents ; corriger les échecs.
- 9.2.2.2 — Exécuter le parcours de bout en bout lorsqu’il est prévu, puis préparer le candidat commité pour la revue.

### 9.3 Check : revoir et challenger

**9.3.1 — Obtenir un regard indépendant**

- 9.3.1.1 — Faire revoir le candidat contre le contrat, le plan et les preuves par un checker distinct de l’implémentation.
- 9.3.1.2 — Challenger le résultat réel ; renvoyer un problème produit au cadrage et un défaut de réalisation à la livraison.

**9.3.2 — Présenter une livraison révisable**

- 9.3.2.1 — Présenter le résultat et ses limites au point de validation interactif.
- 9.3.2.2 — Ouvrir la PR en brouillon avec la validation ; suivre la politique du dépôt pour CI, promotion et fusion.

**Pour engager cette phase :**

```text
Utilise aidd-orchestrator:01-sdlc en mode interactif sur cette demande prête. Appuie-toi sur le contrat et les contextes existants ; présente le contrat, le plan puis le résultat aux points de validation prévus. Garde une revue indépendante et fournis les preuves de validation. Termine par une PR en brouillon si le dépôt distant et les accès le permettent.
```


<a id="phase-10"></a>

## 10. Valider le MVP dans son ensemble

**Ensemble :** Lancer et apprendre · **Dépendances :** 9.

**Question :** Le parcours complet fonctionne-t-il dans les conditions de livraison ?

**Entrée :** Les tranches intégrées dans une préproduction représentative.

**Livrable :** Une recette globale avec preuves, problèmes résiduels, décision de lancement et procédure de retour arrière.

**Critère de passage :** Le parcours principal passe en environnement représentatif ; aucun problème bloquant connu ne reste sans résolution et les limites restantes sont acceptées.

**À adapter :** Paiement, rôles, charge, restauration ou intégrations à vérifier lorsqu’ils existent ; la profondeur suit le risque réel.

**Skills mobilisables :** `aidd-dev:03-assert`, `aidd-dev:06-test`, `interfaces:better-interface`, `impeccable:impeccable`, `aidd-refine:02-challenge`.

**Retour principal si le critère échoue :** phase 9. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 10.1 Vérifier le parcours intégré

**10.1.1 — Tester la tâche de bout en bout**

- 10.1.1.1 — Partir du point d’entrée réel et atteindre le résultat promis sur la version candidate.
- 10.1.1.2 — Vérifier persistance, retours d’erreur et intégrations pertinentes au-delà d’une démo heureuse.

**10.1.2 — Vérifier droits et qualité**

- 10.1.2.1 — Tester les profils autorisés, les refus d’accès et les cas de données pertinents.
- 10.1.2.2 — Contrôler les objectifs de fiabilité, de confidentialité et de performance définis au PRD.

### 10.2 Vérifier l’usage réel

**10.2.1 — Examiner l’interface rendue**

- 10.2.1.1 — Observer clavier, focus, petits écrans, zoom, contenus et états importants.
- 10.2.1.2 — Corriger les problèmes concrets avant la finition visuelle ciblée.

**10.2.2 — Faire une recette du résultat**

- 10.2.2.1 — Faire réaliser une tâche représentative à une personne de la cible lorsque possible.
- 10.2.2.2 — Comparer le résultat aux critères prévus et signaler si aucune recette externe n’a eu lieu.

### 10.3 Décider de l’ouverture

**10.3.1 — Trier les écarts**

- 10.3.1.1 — Corriger les problèmes qui bloquent la promesse ou exposent un risque inacceptable.
- 10.3.1.2 — Consigner les autres écarts et leur effet sur l’usage sans gonfler le périmètre.

**10.3.2 — Préparer l’exploitation initiale**

- 10.3.2.1 — Vérifier logs, suivi d’erreurs, support, sauvegarde et retour arrière selon le projet.
- 10.3.2.2 — Valider le candidat et la population de lancement avec les preuves disponibles.

**Pour engager cette phase :**

```text
Vérifie le MVP intégré contre le PRD et le parcours principal. Utilise aidd-dev:03-assert et aidd-dev:06-test pour les vérifications de réalisation, Interfaces pour l’interface, puis Impeccable audit et polish selon les besoins constatés. Distingue ces vérifications développeur d’une recette utilisateur. Documente ce qui a été testé, les limites et les corrections nécessaires avant lancement.
```


<a id="phase-11"></a>

## 11. Mettre le MVP entre les mains des utilisateurs

**Ensemble :** Lancer et apprendre · **Dépendances :** 10.

**Question :** La cible peut-elle accéder au produit, comprendre sa promesse et démarrer ?

**Entrée :** Un candidat validé, un canal initial et une population de lancement définie.

**Livrable :** Un MVP accessible à la population prévue, un démarrage compréhensible, une mesure fonctionnelle et un canal de retours.

**Critère de passage :** Le produit fonctionne après livraison pour la population prévue et le résultat principal peut être observé.

**À adapter :** Pilote fermé, accès privé ou lancement public selon l’objectif ; une grande campagne et un tag de release ne sont pas indispensables à tout MVP.

**Skills mobilisables :** `marketing-skills:launch`, `marketing-skills:product-marketing`, `aidd-vcs:03-release-tag`.

**Retour principal si le critère échoue :** phase 10. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 11.1 Préparer l’accès et la présentation

**11.1.1 — Aligner le message**

- 11.1.1.1 — Présenter le bénéfice, les limites de cette version et la manière d’y accéder.
- 11.1.1.2 — Préparer une page ou une démonstration seulement si le canal retenu l’exige.

**11.1.2 — Préparer le démarrage**

- 11.1.2.1 — Vérifier invitation ou inscription, premier usage et récupération après une erreur.
- 11.1.2.2 — Rendre le support et la remontée d’un problème faciles à trouver.

### 11.2 Livrer et ouvrir à la bonne population

**11.2.1 — Déployer avec les outils du projet**

- 11.2.1.1 — Appliquer configuration, migrations et déploiement selon une procédure vérifiée.
- 11.2.1.2 — Faire un contrôle bref du parcours sur l’adresse effectivement livrée.

**11.2.2 — Ouvrir l’accès de manière proportionnée**

- 11.2.2.1 — Accueillir la première population prévue et surveiller les problèmes.
- 11.2.2.2 — Diffuser les messages uniquement dans le périmètre expressément autorisé ; versionner la release si utile.

### 11.3 Vérifier la boucle de retours

**11.3.1 — Contrôler la mesure**

- 11.3.1.1 — Vérifier que l’action de valeur est mesurée une seule fois et dans le bon contexte.
- 11.3.1.2 — Vérifier le fonctionnement des retours et du suivi d’erreurs sans collecter de données superflues.

**11.3.2 — Accompagner les premiers usages**

- 11.3.2.1 — Recueillir les difficultés et les réussites constatées.
- 11.3.2.2 — Corriger rapidement un problème de livraison avant d’élargir l’accès.

**Pour engager cette phase :**

```text
Prépare avec marketing-skills:launch une ouverture proportionnée à notre première population. Vérifie promesse, accès, démarrage, support et mesure. Le déploiement doit passer par les outils réels de notre hébergeur, car les plugins cités ne constituent pas un outil de déploiement universel. Utilise aidd-vcs:03-release-tag seulement si une version doit être publiée, après validation prévue par ce skill.
```


<a id="phase-12"></a>

## 12. Mesurer, apprendre et choisir la suite

**Ensemble :** Lancer et apprendre · **Dépendances :** 11.

**Question :** L’usage réel confirme-t-il la valeur supposée ?

**Entrée :** Les premières observations d’usage, les retours et la fenêtre de mesure prévue.

**Livrable :** Un bilan de validation et une décision : stabiliser, améliorer, réduire, réorienter ou arrêter.

**Critère de passage :** La décision s’appuie sur des faits datés et leurs limites ; le prochain changement ou l’arrêt est explicite.

**À adapter :** Avec peu d’utilisateurs, privilégier des observations et entretiens précis ; ne pas faire d’un petit échantillon une preuve statistique ni exiger un A/B test.

**Skills mobilisables :** `marketing-skills:customer-research`, `marketing-skills:product-marketing`, `aidd-orchestrator:02-backlog`, `aidd-refine:02-challenge`.

**Retour principal si le critère échoue :** phase 8. Le diagnostic peut conduire à une autre phase ; ne pas faire tourner une boucle sans nouvel élément.

### 12.1 Observer l’utilisation

**12.1.1 — Lire les mesures prévues**

- 12.1.1.1 — Examiner accès, activation et action de valeur selon les définitions convenues.
- 12.1.1.2 — Regarder retours d’usage, erreurs et réutilisation sur la fenêtre pertinente.

**12.1.2 — Recueillir le contexte qualitatif**

- 12.1.2.1 — Demander ce qui a aidé, bloqué ou conduit à abandonner.
- 12.1.2.2 — Relier les réponses aux comportements observés plutôt qu’à une satisfaction supposée.

### 12.2 Réviser les hypothèses

**12.2.1 — Comparer attentes et faits**

- 12.2.1.1 — Classer les hypothèses comme étayées, contredites ou encore indécidables.
- 12.2.1.2 — Vérifier taille d’échantillon, biais, période et qualité de mesure avant de conclure.

**12.2.2 — Choisir une réponse**

- 12.2.2.1 — Décider s’il faut stabiliser, améliorer une étape, revoir la cible ou arrêter.
- 12.2.2.2 — Séparer défaut produit, problème de compréhension et difficulté d’acquisition.

### 12.3 Préparer la prochaine boucle

**12.3.1 — Mettre à jour les décisions utiles**

- 12.3.1.1 — Mettre à jour les sources produit et marketing concernées avec leur justification.
- 12.3.1.2 — Préserver l’historique des décisions et ne pas réécrire une spec verrouillée.

**12.3.2 — Choisir la prochaine action**

- 12.3.2.1 — Créer ou réordonner la prochaine demande dans le backlog si la poursuite est décidée.
- 12.3.2.2 — Revenir à la découverte pour un problème de valeur, ou au SDLC pour une amélioration déjà comprise.

**Pour engager cette phase :**

```text
Compare les premiers usages aux critères définis avant lancement. Utilise marketing-skills:customer-research pour comprendre les comportements et contradictions, puis mets en cohérence le contexte marketing et le backlog avec les décisions approuvées. Distingue produit livré, utilisabilité observée et valeur démontrée ; propose une seule prochaine priorité.
```

## Sources locales et limites

La carte assemble les responsabilités décrites par les plugins installés. Les étapes générales de recherche, de conception et d’exploitation sont des recommandations de ce guide, pas de nouvelles commandes natives. Les liens suivants pointent vers les sources locales ; les chemins versionnés peuvent changer après une mise à jour.

- [aidd-context:01-bootstrap](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-context/2.9.0/skills/01-bootstrap/SKILL.md)
- [aidd-context:02-project-memory](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-context/2.9.0/skills/02-project-memory/SKILL.md)
- [aidd-dev:01-plan](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-dev/2.7.0/skills/01-plan/SKILL.md)
- [aidd-dev:02-implement](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-dev/2.7.0/skills/02-implement/SKILL.md)
- [aidd-dev:03-assert](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-dev/2.7.0/skills/03-assert/SKILL.md)
- [aidd-dev:05-review](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-dev/2.7.0/skills/05-review/SKILL.md)
- [aidd-dev:06-test](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-dev/2.7.0/skills/06-test/SKILL.md)
- [aidd-orchestrator:01-sdlc](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-orchestrator/2.4.0/skills/01-sdlc/SKILL.md)
- [aidd-orchestrator:02-backlog](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-orchestrator/2.4.0/skills/02-backlog/SKILL.md)
- [aidd-pm:02-user-stories](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/02-user-stories/SKILL.md)
- [aidd-pm:03-prd](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/03-prd/SKILL.md)
- [aidd-pm:04-spec](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/04-spec/SKILL.md)
- [aidd-pm:05-spike](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/05-spike/SKILL.md)
- [aidd-pm:06-product-brief](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/06-product-brief/SKILL.md)
- [aidd-pm:07-epic](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-pm/2.6.0/skills/07-epic/SKILL.md)
- [aidd-refine:01-brainstorm](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-refine/3.1.1/skills/01-brainstorm/SKILL.md)
- [aidd-refine:02-challenge](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-refine/3.1.1/skills/02-challenge/SKILL.md)
- [aidd-refine:03-shadow-areas](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-refine/3.1.1/skills/03-shadow-areas/SKILL.md)
- [aidd-vcs:00-repo-init](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-vcs/2.5.0/skills/00-repo-init/SKILL.md)
- [aidd-vcs:01-commit](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-vcs/2.5.0/skills/01-commit/SKILL.md)
- [aidd-vcs:02-pull-request](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-vcs/2.5.0/skills/02-pull-request/SKILL.md)
- [aidd-vcs:03-release-tag](/Users/yanis/.codex/plugins/cache/aidd-framework/aidd-vcs/2.5.0/skills/03-release-tag/SKILL.md)
- [impeccable:impeccable](/Users/yanis/.codex/plugins/cache/openai-curated-remote/impeccable/4.3.1/skills/impeccable/SKILL.md)
- [interfaces:better-interface](/Users/yanis/.codex/plugins/cache/interfaces/interfaces/1.17.0/skills/better-interface/SKILL.md)
- [marketing-skills:customer-research](/Users/yanis/.codex/plugins/cache/marketingskills/marketing-skills/2.13.0/skills/customer-research/SKILL.md)
- [marketing-skills:launch](/Users/yanis/.codex/plugins/cache/marketingskills/marketing-skills/2.13.0/skills/launch/SKILL.md)
- [marketing-skills:product-marketing](/Users/yanis/.codex/plugins/cache/marketingskills/marketing-skills/2.13.0/skills/product-marketing/SKILL.md)

Pour les frontières du SDLC, les modes et les pauses : les références `mode.md`, `01-frame.md`, `02-deliver.md` et `03-check.md` sous le skill `aidd-orchestrator:01-sdlc` ont aussi été consultées. Pour Impeccable : `reference/routing.md` et `reference/shape.md`. Les chemins de persistance du PRD ont été vérifiés dans son action `02-finalize.md`.

Ce guide ne démontre pas une connexion à un hébergeur, un outil de recherche terrain ou un dépôt distant. Leur disponibilité se vérifie au moment de la phase concernée. Aucun projet produit n’a parcouru ces phases dans ce dossier.
