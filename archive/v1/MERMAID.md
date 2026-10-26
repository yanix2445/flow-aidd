# Du concept au MVP — schémas Mermaid

Le contenu reprend les 12 phases et 36 sous-phases du parcours existant. La vue globale montre les dépendances ; chaque phase détaille questions, réponses attendues, capacités et résultats.

**Lecture :** entrée → sous-phase → question → réponse attendue → skill → résultat → décision de passage.

**Les réponses sont attendues, pas acquises.** Les sorties décrivent des livrables à produire ; leur présence ici ne signifie pas que les fichiers existent. `Proposé` indique une convention de ce guide ; `natif` indique un emplacement défini par le skill. Les valeurs entre chevrons sont des gabarits.

Les libellés des schémas sont abrégés pour rester lisibles. Les identifiants exacts et les chemins complets figurent sous chaque phase ; les questions complètes sont dans [SCHEMA.md](SCHEMA.md). Les 72 étapes et 144 sous-étapes restent dans [FLOW.md](FLOW.md).

Une liste de capacités ne prescrit pas plusieurs appels simultanés. Le coordinateur choisit le skill responsable ; SDLC pilote déjà ses sous-étapes de développement. Les variantes conditionnelles restent décrites sous les phases.

Les nœuds « Reprendre » sont des renvois vers les phases numérotées. Ils évitent de tirer des flèches de retour à travers tout le schéma.

## Vue globale

```mermaid
---
title: "Vue d’ensemble : de l’idée au premier MVP"
---
flowchart TB
  subgraph Groupe1["Explorer"]
  Phase1["01 · Clarifier l’idée"]
  Phase2["02 · Comprendre le besoin"]
  DecisionBesoin{"Besoin étayé ou risque accepté ?"}
  Phase3["03 · Positionner le produit"]
  end
  subgraph Groupe2["Concevoir"]
  Phase4["04 · Délimiter le MVP"]
  Phase5["05 · Concevoir l’UX et l’UI"]
  Phase6["06 · Valider la technique"]
  end
  subgraph Groupe3["Construire"]
  Phase7["07 · Préparer le socle"]
  Phase8["08 · Préparer le backlog"]
  Phase9["09 · Livrer une tranche avec SDLC"]
  end
  subgraph Groupe4["Lancer et apprendre"]
  Phase10["10 · Faire la recette du MVP"]
  DecisionRecette{"Parcours du MVP validé ?"}
  Phase11["11 · Ouvrir le MVP"]
  Phase12["12 · Mesurer et décider"]
  end
  RetourIdee["Reprendre 01 : cible ou problème"]
  RetourMVP["Reprendre 04 : périmètre ou parcours"]
  RetourTranche["Reprendre 08 : prochaine tranche"]
  RetourCorrections["Reprendre 09 : corrections"]
  RetourDecouverte["Reprendre 02 : valeur incertaine"]
  RetourPriorite["Reprendre 08 : amélioration comprise"]

  Phase1 --> Phase2
  Phase2 --> DecisionBesoin
  DecisionBesoin -- "Oui" --> Phase3
  DecisionBesoin -- "Non" --> RetourIdee
  Phase3 --> Phase4
  Phase4 -- "UX et UI" --> Phase5
  Phase4 -- "Technique" --> Phase6
  Phase4 -- "Backlog" --> Phase8
  Phase6 --> Phase7
  Phase5 --> Phase9
  Phase7 --> Phase9
  Phase8 --> Phase9
  Phase9 --> Phase10
  Phase10 --> DecisionRecette
  DecisionRecette -- "Oui" --> Phase11
  DecisionRecette -- "Non" --> RetourCorrections
  Phase11 --> Phase12
  Phase9 -. "Si une autre tranche est nécessaire" .-> RetourTranche
  Phase5 -. "Si le parcours change" .-> RetourMVP
  Phase6 -. "Si le périmètre change" .-> RetourMVP
  Phase12 -. "Si la valeur reste incertaine" .-> RetourDecouverte
  Phase12 -. "Si la prochaine amélioration est comprise" .-> RetourPriorite
```

**Pour la construction :** la phase 9 attend une conception suffisante, un socle opérationnel et une demande prête. UX, technique et backlog peuvent avancer après le cadrage du MVP selon ces dépendances. Un risque majeur se teste dès son apparition.

## Phases détaillées

### 01. Clarifier l’idée

**À adapter :** Explorer plusieurs pistes seulement si le problème ou la cible restent ouverts.

```mermaid
---
title: "Phase 01 : Clarifier l’idée"
---
flowchart TB
  Entree1["Entrée : Une idée encore vague"]
  subgraph Phase1SousPhase1["1.1 · Faire émerger l’intention"]
  Question1Partie1["Question : Qui rencontre quelle difficulté ?"]
  Reponse1Partie1["Réponse attendue : Une cible, une situation et un résultat souhaité"]
  Skills1Partie1["AIDD Refine : 01-brainstorm"]
  Resultat1Partie1["Résultat : Note d’intention : docs/idee.md, nom proposé"]
  end
  subgraph Phase1SousPhase2["1.2 · Ouvrir puis choisir une piste"]
  Question1Partie2["Question : Quelle piste explorer en premier ?"]
  Reponse1Partie2["Réponse attendue : Une piste retenue et les autres reportées"]
  Skills1Partie2["AIDD Refine : 01-brainstorm"]
  Resultat1Partie2["Résultat : Piste et alternatives dans idee.md, proposé"]
  end
  subgraph Phase1SousPhase3["1.3 · Cadrer l’exploration"]
  Question1Partie3["Question : Quelles limites et quelle inconnue prioritaire ?"]
  Reponse1Partie3["Réponse attendue : Temps, budget, objectif et hypothèse à tester"]
  Skills1Partie3["AIDD Refine : 01-brainstorm"]
  Resultat1Partie3["Résultat : Contraintes et hypothèses dans idee.md, proposé"]
  end
  Decision1{"Cible, problème et résultat assez clairs ?"}
  Suite1["Oui : Phase 2 : comprendre le besoin"]
  Reprise1["Non ou inconnu : reprendre le point manquant, retour possible en phase 1"]

  Entree1 --> Question1Partie1
  Question1Partie1 --> Reponse1Partie1
  Reponse1Partie1 --> Skills1Partie1
  Skills1Partie1 --> Resultat1Partie1
  Resultat1Partie1 --> Question1Partie2
  Question1Partie2 --> Reponse1Partie2
  Reponse1Partie2 --> Skills1Partie2
  Skills1Partie2 --> Resultat1Partie2
  Resultat1Partie2 --> Question1Partie3
  Question1Partie3 --> Reponse1Partie3
  Reponse1Partie3 --> Skills1Partie3
  Skills1Partie3 --> Resultat1Partie3
  Resultat1Partie3 --> Decision1
  Decision1 -- "Oui" --> Suite1
  Decision1 -- "Non ou inconnu" --> Reprise1
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 1.1 | `aidd-refine:01-brainstorm` | **Note d’intention** : `docs/idee.md` (proposé) |
| 1.2 | `aidd-refine:01-brainstorm` | **Piste retenue et alternatives** : `docs/idee.md` (proposé) |
| 1.3 | `aidd-refine:01-brainstorm` | **Contraintes et hypothèses** : `docs/idee.md` (proposé) |

**Critère complet :** Tu peux expliquer une situation concrète, une personne concernée et le résultat espéré ; les inconnues sont visibles.

[Source Mermaid de la phase](mermaid/01-phase.mmd).

### 02. Comprendre le besoin et les alternatives

**À adapter :** Étude de marché large et personas détaillés seulement si la décision le nécessite ; une hypothèse de segment ne devient pas un persona prouvé.

```mermaid
---
title: "Phase 02 : Comprendre le besoin et les alternatives"
---
flowchart TB
  Entree2["Entrée : La note d’intention et une hypothèse à tester"]
  subgraph Phase2SousPhase1["2.1 · Préparer une recherche utile"]
  Question2Partie1["Question : Qui étudier et quelle observation rechercher ?"]
  Reponse2Partie1["Réponse attendue : Un segment, une question et une limite d’effort"]
  Skills2Partie1["Marketing : product-marketing ; AIDD PM : 06-product-brief"]
  Resultat2Partie1["Résultat : Contexte marketing natif + recherche.md proposé"]
  end
  subgraph Phase2SousPhase2["2.2 · Recueillir des faits"]
  Question2Partie2["Question : Que font les personnes et où peinent-elles ?"]
  Reponse2Partie2["Réponse attendue : Des faits datés, des sources et les alternatives"]
  Skills2Partie2["Marketing : customer-research"]
  Resultat2Partie2["Résultat : Sources et observations dans recherche.md, proposé"]
  end
  subgraph Phase2SousPhase3["2.3 · Interpréter sans surconclure"]
  Question2Partie3["Question : Les faits justifient-ils de poursuivre ?"]
  Reponse2Partie3["Réponse attendue : Signaux, contradictions, limites et décision"]
  Skills2Partie3["Marketing : customer-research ; AIDD PM : 06-product-brief"]
  Resultat2Partie3["Résultat : Synthèse et décision dans recherche.md, proposé"]
  end
  Decision2{"Besoin étayé ou risque accepté ?"}
  Suite2["Oui : Phase 3 : choisir le positionnement"]
  Reprise2["Non ou inconnu : reprendre le point manquant, retour possible en phase 1"]

  Entree2 --> Question2Partie1
  Question2Partie1 --> Reponse2Partie1
  Reponse2Partie1 --> Skills2Partie1
  Skills2Partie1 --> Resultat2Partie1
  Resultat2Partie1 --> Question2Partie2
  Question2Partie2 --> Reponse2Partie2
  Reponse2Partie2 --> Skills2Partie2
  Skills2Partie2 --> Resultat2Partie2
  Resultat2Partie2 --> Question2Partie3
  Question2Partie3 --> Reponse2Partie3
  Reponse2Partie3 --> Skills2Partie3
  Skills2Partie3 --> Resultat2Partie3
  Resultat2Partie3 --> Decision2
  Decision2 -- "Oui" --> Suite2
  Decision2 -- "Non ou inconnu" --> Reprise2
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 2.1 | `marketing-skills:product-marketing`; `aidd-pm:06-product-brief` | **Contexte marketing provisoire** : `.agents/product-marketing.md` (natif); **Plan de recherche** : `docs/recherche.md` (proposé) |
| 2.2 | `marketing-skills:customer-research` | **Observations, sources et verbatims** : `docs/recherche.md` (proposé) |
| 2.3 | `marketing-skills:customer-research`; `aidd-pm:06-product-brief` | **Synthèse et décision de découverte** : `docs/recherche.md` (proposé) |

**Critère complet :** Des éléments réels éclairent le problème ; la poursuite repose sur des preuves identifiées ou sur un risque explicitement accepté.

[Source Mermaid de la phase](mermaid/02-phase.mmd).

### 03. Choisir le positionnement et la viabilité

**À adapter :** Prix, payeur et modèle économique si le projet est commercial ; sinon coût d’usage, maintenance et bénéfice attendu.

```mermaid
---
title: "Phase 03 : Choisir le positionnement et la viabilité"
---
flowchart TB
  Entree3["Entrée : Les observations et contraintes connues"]
  subgraph Phase3SousPhase1["3.1 · Définir une promesse crédible"]
  Question3Partie1["Question : Quel bénéfice pour quelle cible ?"]
  Reponse3Partie1["Réponse attendue : Une promesse crédible face à une alternative"]
  Skills3Partie1["Marketing : product-marketing"]
  Resultat3Partie1["Résultat : Positionnement dans le contexte marketing natif"]
  end
  subgraph Phase3SousPhase2["3.2 · Vérifier la soutenabilité"]
  Question3Partie2["Question : Comment atteindre la cible et financer l’usage ?"]
  Reponse3Partie2["Réponse attendue : Un premier canal et une hypothèse de viabilité"]
  Skills3Partie2["AIDD PM : 06-product-brief ; Marketing : product-marketing"]
  Resultat3Partie2["Résultat : Viabilité et canal dans le Product Brief natif"]
  end
  subgraph Phase3SousPhase3["3.3 · Formaliser le choix produit"]
  Question3Partie3["Question : Quelle opportunité et comment la valider ?"]
  Reponse3Partie3["Réponse attendue : Objectif, risques et critères de poursuite approuvés"]
  Skills3Partie3["AIDD PM : 06-product-brief"]
  Resultat3Partie3["Résultat : Product Brief approuvé, chemin du skill"]
  end
  Decision3{"Promesse, accès aux utilisateurs et viabilité décidés ?"}
  Suite3["Oui : Phase 4 : délimiter le MVP"]
  Reprise3["Non ou inconnu : reprendre le point manquant, retour possible en phase 2"]

  Entree3 --> Question3Partie1
  Question3Partie1 --> Reponse3Partie1
  Reponse3Partie1 --> Skills3Partie1
  Skills3Partie1 --> Resultat3Partie1
  Resultat3Partie1 --> Question3Partie2
  Question3Partie2 --> Reponse3Partie2
  Reponse3Partie2 --> Skills3Partie2
  Skills3Partie2 --> Resultat3Partie2
  Resultat3Partie2 --> Question3Partie3
  Question3Partie3 --> Reponse3Partie3
  Reponse3Partie3 --> Skills3Partie3
  Skills3Partie3 --> Resultat3Partie3
  Resultat3Partie3 --> Decision3
  Decision3 -- "Oui" --> Suite3
  Decision3 -- "Non ou inconnu" --> Reprise3
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 3.1 | `marketing-skills:product-marketing` | **Positionnement et promesse** : `.agents/product-marketing.md` (natif) |
| 3.2 | `aidd-pm:06-product-brief`; `marketing-skills:product-marketing` | **Viabilité et accès aux utilisateurs** : `aidd_docs/product/<product-slug>.md` (natif) |
| 3.3 | `aidd-pm:06-product-brief` | **Product Brief approuvé** : `aidd_docs/product/<product-slug>.md` (natif) |

**Critère complet :** Une cible prioritaire, une promesse crédible, un premier accès aux utilisateurs et une hypothèse de viabilité sont décidés.

[Source Mermaid de la phase](mermaid/03-phase.mmd).

### 04. Délimiter le MVP

**À adapter :** Paiement, comptes, rôles complexes et intégrations seulement s’ils sont nécessaires à la promesse du MVP.

```mermaid
---
title: "Phase 04 : Délimiter le MVP"
---
flowchart TB
  Entree4["Entrée : Le Product Brief approuvé"]
  subgraph Phase4SousPhase1["4.1 · Définir la preuve de valeur"]
  Question4Partie1["Question : Quelle tâche complète prouve la valeur ?"]
  Reponse4Partie1["Réponse attendue : Un résultat, un indicateur et une fenêtre de mesure"]
  Skills4Partie1["AIDD PM : 03-prd"]
  Resultat4Partie1["Résultat : Résultat et mesure dans le PRD natif"]
  end
  subgraph Phase4SousPhase2["4.2 · Réduire le périmètre"]
  Question4Partie2["Question : Que garder et que reporter ?"]
  Reponse4Partie2["Réponse attendue : Le nécessaire, les exclusions et les règles métier"]
  Skills4Partie2["AIDD PM : 03-prd"]
  Resultat4Partie2["Résultat : Périmètre du MVP dans le PRD natif"]
  end
  subgraph Phase4SousPhase3["4.3 · Rendre le contrat vérifiable"]
  Question4Partie3["Question : Quels états ou angles morts restent ouverts ?"]
  Reponse4Partie3["Réponse attendue : Qualité attendue et lacunes bloquantes traitées"]
  Skills4Partie3["AIDD Refine : 03-shadow-areas ; AIDD PM : 03-prd"]
  Resultat4Partie3["Résultat : PRD validé et angles morts traités"]
  end
  Decision4{"Parcours complet, périmètre et critères approuvés ?"}
  Suite4["Oui : Phases 5, 6 et 8 selon leurs dépendances"]
  Reprise4["Non ou inconnu : reprendre le point manquant, retour possible en phase 3"]

  Entree4 --> Question4Partie1
  Question4Partie1 --> Reponse4Partie1
  Reponse4Partie1 --> Skills4Partie1
  Skills4Partie1 --> Resultat4Partie1
  Resultat4Partie1 --> Question4Partie2
  Question4Partie2 --> Reponse4Partie2
  Reponse4Partie2 --> Skills4Partie2
  Skills4Partie2 --> Resultat4Partie2
  Resultat4Partie2 --> Question4Partie3
  Question4Partie3 --> Reponse4Partie3
  Reponse4Partie3 --> Skills4Partie3
  Skills4Partie3 --> Resultat4Partie3
  Resultat4Partie3 --> Decision4
  Decision4 -- "Oui" --> Suite4
  Decision4 -- "Non ou inconnu" --> Reprise4
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 4.1 | `aidd-pm:03-prd` | **Résultat et mesure de réussite** : `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` (natif) |
| 4.2 | `aidd-pm:03-prd` | **Périmètre du MVP** : `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` (natif) |
| 4.3 | `aidd-refine:03-shadow-areas`; `aidd-pm:03-prd` | **PRD validé et angles morts traités** : `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md` (natif) |

**Critère complet :** Le parcours principal est complet à son échelle ; les inclusions, exclusions et critères de réussite sont explicites.

[Source Mermaid de la phase](mermaid/04-phase.mmd).

### 05. Concevoir et éprouver l’expérience

**À adapter :** Prototype cliquable et tests terrain approfondis pour une interaction incertaine ; croquis et vérification ciblée pour un parcours simple connu.

```mermaid
---
title: "Phase 05 : Concevoir et éprouver l’expérience"
---
flowchart TB
  Entree5["Entrée : Le PRD et les contenus disponibles"]
  subgraph Phase5SousPhase1["5.1 · Structurer le parcours"]
  Question5Partie1["Question : Quel parcours mène au résultat ?"]
  Reponse5Partie1["Réponse attendue : Entrée, actions, écrans, décisions et états utiles"]
  Skills5Partie1["Impeccable : init puis shape"]
  Resultat5Partie1["Résultat : PRODUCT.md natif + parcours.md proposé"]
  end
  subgraph Phase5SousPhase2["5.2 · Choisir une direction d’interface"]
  Question5Partie2["Question : Quelle direction sert ce parcours ?"]
  Reponse5Partie2["Réponse attendue : Une direction et des règles d’interface choisies"]
  Skills5Partie2["Impeccable : direction après shape"]
  Resultat5Partie2["Résultat : DESIGN.md natif + prototype au chemin choisi"]
  end
  subgraph Phase5SousPhase3["5.3 · Tester avant de généraliser"]
  Question5Partie3["Question : La personne comprend-elle et réussit-elle ?"]
  Reponse5Partie3["Réponse attendue : Des observations, des corrections et les limites du test"]
  Skills5Partie3["Interfaces : better-interface ; Impeccable : critique"]
  Resultat5Partie3["Résultat : Prototype corrigé + retours-ux.md proposé"]
  end
  Decision5{"Parcours compréhensible et limites des tests connues ?"}
  Suite5["Oui : Phase 9 quand socle et demande sont aussi prêts"]
  Reprise5["Non ou inconnu : reprendre le point manquant, retour possible en phase 4"]

  Entree5 --> Question5Partie1
  Question5Partie1 --> Reponse5Partie1
  Reponse5Partie1 --> Skills5Partie1
  Skills5Partie1 --> Resultat5Partie1
  Resultat5Partie1 --> Question5Partie2
  Question5Partie2 --> Reponse5Partie2
  Reponse5Partie2 --> Skills5Partie2
  Skills5Partie2 --> Resultat5Partie2
  Resultat5Partie2 --> Question5Partie3
  Question5Partie3 --> Reponse5Partie3
  Reponse5Partie3 --> Skills5Partie3
  Skills5Partie3 --> Resultat5Partie3
  Resultat5Partie3 --> Decision5
  Decision5 -- "Oui" --> Suite5
  Decision5 -- "Non ou inconnu" --> Reprise5
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 5.1 | `impeccable:impeccable — init puis shape` | **Contexte produit** : `PRODUCT.md` (natif); **Parcours et brief UX** : `docs/parcours.md` (proposé) |
| 5.2 | `impeccable:impeccable — direction après shape` | **Direction de design** : `DESIGN.md` (natif); **Prototype du parcours** : `Emplacement choisi dans le projet` (à résoudre) |
| 5.3 | `interfaces:better-interface`; `impeccable:impeccable — critique` | **Retours UX et prototype corrigé** : `docs/retours-ux.md` (proposé) |

**Critère complet :** Le parcours principal est compréhensible ; les états importants sont conçus et les tests réalisés ou leurs limites sont consignés.

[Source Mermaid de la phase](mermaid/05-phase.mmd).

### 06. Valider la faisabilité et l’architecture

**À adapter :** Un spike dès qu’un risque peut invalider le projet, même plus tôt ; bootstrap est conçu pour un nouveau SaaS et produit de la documentation, jamais le scaffold.

```mermaid
---
title: "Phase 06 : Valider la faisabilité et l’architecture"
---
flowchart TB
  Entree6["Entrée : Le PRD et les contraintes techniques"]
  subgraph Phase6SousPhase1["6.1 · Réduire les incertitudes"]
  Question6Partie1["Question : Quel risque technique peut invalider la promesse ?"]
  Reponse6Partie1["Réponse attendue : Une question bornée et une preuve de faisabilité"]
  Skills6Partie1["AIDD PM : 05-spike"]
  Resultat6Partie1["Résultat : Résultat de spike, preuve et limites"]
  end
  subgraph Phase6SousPhase2["6.2 · Choisir une architecture proportionnée"]
  Question6Partie2["Question : Quelle architecture répond aux besoins ?"]
  Reponse6Partie2["Réponse attendue : Des options comparées et un choix proportionné"]
  Skills6Partie2["AIDD Context : 01-bootstrap, pour un nouveau SaaS"]
  Resultat6Partie2["Résultat : Décisions dans aidd_docs/INSTALL.md, natif"]
  end
  subgraph Phase6SousPhase3["6.3 · Préparer la réalisation"]
  Question6Partie3["Question : Comment installer et exploiter à coût acceptable ?"]
  Reponse6Partie3["Réponse attendue : Environnements, installation, coûts et impacts"]
  Skills6Partie3["AIDD Context : 01-bootstrap, pour un nouveau SaaS"]
  Resultat6Partie3["Résultat : INSTALL.md complété ; le scaffold reste à créer"]
  end
  Decision6{"Faisabilité et architecture suffisamment éprouvées ?"}
  Suite6["Oui : Phase 7 : préparer les fondations"]
  Reprise6["Non ou inconnu : reprendre le point manquant, retour possible en phase 4"]

  Entree6 --> Question6Partie1
  Question6Partie1 --> Reponse6Partie1
  Reponse6Partie1 --> Skills6Partie1
  Skills6Partie1 --> Resultat6Partie1
  Resultat6Partie1 --> Question6Partie2
  Question6Partie2 --> Reponse6Partie2
  Reponse6Partie2 --> Skills6Partie2
  Skills6Partie2 --> Resultat6Partie2
  Resultat6Partie2 --> Question6Partie3
  Question6Partie3 --> Reponse6Partie3
  Reponse6Partie3 --> Skills6Partie3
  Skills6Partie3 --> Resultat6Partie3
  Resultat6Partie3 --> Decision6
  Decision6 -- "Oui" --> Suite6
  Decision6 -- "Non ou inconnu" --> Reprise6
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 6.1 | `aidd-pm:05-spike` | **Résultat de spike et preuve** : `Chemin résolu par le skill` (à résoudre) |
| 6.2 | `aidd-context:01-bootstrap — nouveau SaaS` | **Décisions d’architecture SaaS** : `aidd_docs/INSTALL.md` (natif) |
| 6.3 | `aidd-context:01-bootstrap — nouveau SaaS` | **Installation et exploitation prévues** : `aidd_docs/INSTALL.md` (natif) |

**Critère complet :** Les risques techniques déterminants sont éprouvés ou bornés ; architecture, coût et plan d’installation correspondent au MVP.

[Source Mermaid de la phase](mermaid/06-phase.mmd).

### 07. Préparer les fondations du projet

**À adapter :** Réutiliser dépôt, stack et conventions existants ; repo-init est expérimental. Créer les accès externes uniquement dans le périmètre autorisé.

```mermaid
---
title: "Phase 07 : Préparer les fondations du projet"
---
flowchart TB
  Entree7["Entrée : Les décisions techniques et le plan d’installation"]
  subgraph Phase7SousPhase1["7.1 · Mettre en place le socle"]
  Question7Partie1["Question : Quel socle créer ou réutiliser ?"]
  Reponse7Partie1["Réponse attendue : Dépôt, conventions, dépendances et environnements"]
  Skills7Partie1["AIDD VCS : 00-repo-init ; AIDD Dev : plan et implement"]
  Resultat7Partie1["Résultat : Dépôt, code et configuration adaptés à la stack"]
  end
  subgraph Phase7SousPhase2["7.2 · Vérifier le chemin de livraison"]
  Question7Partie2["Question : Une petite tranche fonctionne-t-elle réellement ?"]
  Reponse7Partie2["Réponse attendue : Un parcours local et de préproduction vérifié"]
  Skills7Partie2["AIDD Dev : 03-assert et 06-test"]
  Resultat7Partie2["Résultat : Socle vérifié, configuration et URL de préproduction"]
  end
  subgraph Phase7SousPhase3["7.3 · Transmettre le contexte aux agents"]
  Question7Partie3["Question : Que doit lire un agent pour reprendre le projet ?"]
  Reponse7Partie3["Réponse attendue : Architecture réelle, règles, commandes et accès"]
  Skills7Partie3["AIDD Context : 02-project-memory"]
  Resultat7Partie3["Résultat : Contexte projet et configuration des outils IA"]
  end
  Decision7{"Une tranche tourne et se vérifie de façon reproductible ?"}
  Suite7["Oui : Phase 9 quand UX et demande sont aussi prêtes"]
  Reprise7["Non ou inconnu : reprendre le point manquant, retour possible en phase 6"]

  Entree7 --> Question7Partie1
  Question7Partie1 --> Reponse7Partie1
  Reponse7Partie1 --> Skills7Partie1
  Skills7Partie1 --> Resultat7Partie1
  Resultat7Partie1 --> Question7Partie2
  Question7Partie2 --> Reponse7Partie2
  Reponse7Partie2 --> Skills7Partie2
  Skills7Partie2 --> Resultat7Partie2
  Resultat7Partie2 --> Question7Partie3
  Question7Partie3 --> Reponse7Partie3
  Reponse7Partie3 --> Skills7Partie3
  Skills7Partie3 --> Resultat7Partie3
  Resultat7Partie3 --> Decision7
  Decision7 -- "Oui" --> Suite7
  Decision7 -- "Non ou inconnu" --> Reprise7
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 7.1 | `aidd-vcs:00-repo-init`; `aidd-dev:01-plan`; `aidd-dev:02-implement` | **Dépôt et scaffold réels** : `Fichiers adaptés à la stack choisie` (à résoudre) |
| 7.2 | `aidd-dev:03-assert`; `aidd-dev:06-test` | **Socle vérifié** : `Code, configuration CI et URL de préproduction` (à résoudre) |
| 7.3 | `aidd-context:02-project-memory` | **Contexte projet relié aux outils IA** : `Chemins résolus par project-memory` (à résoudre) |

**Critère complet :** Une petite tranche de bout en bout peut tourner localement et en préproduction avec des vérifications reproductibles.

[Source Mermaid de la phase](mermaid/07-phase.mmd).

### 08. Organiser le backlog et la première tranche

**À adapter :** Epics si plusieurs résultats doivent être regroupés ; spec séparée si le contrat manque de précision. Ne pas dupliquer une demande déjà prête.

```mermaid
---
title: "Phase 08 : Organiser le backlog et la première tranche"
---
flowchart TB
  Entree8["Entrée : Le PRD et les décisions UX et techniques utiles"]
  subgraph Phase8SousPhase1["8.1 · Décomposer par résultat"]
  Question8Partie1["Question : Quelles petites livraisons apportent de la valeur ?"]
  Reponse8Partie1["Réponse attendue : Des tranches verticales, regroupées si nécessaire"]
  Skills8Partie1["AIDD Orchestrator : backlog ; AIDD PM : epic et user-stories"]
  Resultat8Partie1["Résultat : Stories Markdown ; epics seulement si utiles"]
  end
  subgraph Phase8SousPhase2["8.2 · Rendre la prochaine demande prête"]
  Question8Partie2["Question : Comment saura-t-on que la demande est faite ?"]
  Reponse8Partie2["Réponse attendue : Acteur, résultat, critères et dépendances levées"]
  Skills8Partie2["AIDD PM : 02-user-stories et 04-spec si nécessaire"]
  Resultat8Partie2["Résultat : Story prête + spec.md si le contrat manque"]
  end
  subgraph Phase8SousPhase3["8.3 · Ordonner sans tout figer"]
  Question8Partie3["Question : Quelle tranche livrer maintenant ?"]
  Reponse8Partie3["Réponse attendue : Une demande prête, ordonnée selon valeur et risque"]
  Skills8Partie3["AIDD Orchestrator : 02-backlog ; AIDD PM : 02-user-stories"]
  Resultat8Partie3["Résultat : Backlog ordonné et prochaine story identifiée"]
  end
  Decision8{"Prochaine demande petite, utile et prête ?"}
  Suite8["Oui : Phase 9 quand UX et socle sont aussi prêts"]
  Reprise8["Non ou inconnu : reprendre le point manquant, retour possible en phase 4"]

  Entree8 --> Question8Partie1
  Question8Partie1 --> Reponse8Partie1
  Reponse8Partie1 --> Skills8Partie1
  Skills8Partie1 --> Resultat8Partie1
  Resultat8Partie1 --> Question8Partie2
  Question8Partie2 --> Reponse8Partie2
  Reponse8Partie2 --> Skills8Partie2
  Skills8Partie2 --> Resultat8Partie2
  Resultat8Partie2 --> Question8Partie3
  Question8Partie3 --> Reponse8Partie3
  Reponse8Partie3 --> Skills8Partie3
  Skills8Partie3 --> Resultat8Partie3
  Resultat8Partie3 --> Decision8
  Decision8 -- "Oui" --> Suite8
  Decision8 -- "Non ou inconnu" --> Reprise8
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 8.1 | `aidd-orchestrator:02-backlog`; `aidd-pm:07-epic`; `aidd-pm:02-user-stories` | **Stories du MVP** : `aidd_docs/backlog/stories/<slug>.md` (natif) |
| 8.2 | `aidd-pm:02-user-stories`; `aidd-pm:04-spec — si nécessaire` | **Story prête** : `aidd_docs/backlog/stories/<slug>.md` (natif); **Contrat si nécessaire** : `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>_<slug>/spec.md` (natif) |
| 8.3 | `aidd-orchestrator:02-backlog`; `aidd-pm:02-user-stories` | **Ordre et prochaine story** : `Backlog existant, sans copie concurrente` (à résoudre) |

**Critère complet :** La prochaine tranche est petite, utile, vérifiable et sans décision produit bloquante ; le reste peut rester moins détaillé.

[Source Mermaid de la phase](mermaid/08-phase.mmd).

### 09. Livrer par petites boucles SDLC

**À adapter :** Une boucle par changement cohérent. SDLC inclut déjà le cadrage, le plan, l’exécution, la validation, la revue et la PR ; ne pas les relancer en double.

```mermaid
---
title: "Phase 09 : Livrer par petites boucles SDLC"
---
flowchart TB
  Entree9["Entrée : Une demande prête et les contextes du projet"]
  subgraph Phase9SousPhase1["9.1 · Frame : établir le contrat"]
  Question9Partie1["Question : Le contrat permet-il de construire ?"]
  Reponse9Partie1["Réponse attendue : Résultat, limites et critères suffisamment clairs"]
  Skills9Partie1["AIDD Orchestrator : SDLC Frame ; PM : spec si nécessaire"]
  Resultat9Partie1["Résultat : Contrat existant ou spec.md dans le dossier de tâche"]
  end
  subgraph Phase9SousPhase2["9.2 · Deliver : planifier, construire, vérifier"]
  Question9Partie2["Question : Quel plan et quelles preuves de réalisation ?"]
  Reponse9Partie2["Réponse attendue : Un plan confirmé puis un candidat construit et vérifié"]
  Skills9Partie2["SDLC Deliver : Dev plan, implement, assert, test ; VCS commit"]
  Resultat9Partie2["Résultat : plan.md, phase-N.md, code, tests, commits et preuves"]
  end
  subgraph Phase9SousPhase3["9.3 · Check : revoir et challenger"]
  Question9Partie3["Question : La revue indépendante confirme-t-elle le résultat ?"]
  Reponse9Partie3["Réponse attendue : Écarts traités et résultat conforme au contrat"]
  Skills9Partie3["SDLC Check : Dev review ; Refine challenge ; VCS pull-request"]
  Resultat9Partie3["Résultat : Rapports du candidat et PR en brouillon"]
  end
  Decision9{"Contrat satisfait et conclusions de revue traitées ?"}
  Suite9["Oui : Phase 8 : prochaine tranche ; phase 10 : MVP intégré"]
  Reprise9["Non ou inconnu : reprendre le point manquant, retour possible en phase 8"]

  Entree9 --> Question9Partie1
  Question9Partie1 --> Reponse9Partie1
  Reponse9Partie1 --> Skills9Partie1
  Skills9Partie1 --> Resultat9Partie1
  Resultat9Partie1 --> Question9Partie2
  Question9Partie2 --> Reponse9Partie2
  Reponse9Partie2 --> Skills9Partie2
  Skills9Partie2 --> Resultat9Partie2
  Resultat9Partie2 --> Question9Partie3
  Question9Partie3 --> Reponse9Partie3
  Reponse9Partie3 --> Skills9Partie3
  Skills9Partie3 --> Resultat9Partie3
  Resultat9Partie3 --> Decision9
  Decision9 -- "Oui" --> Suite9
  Decision9 -- "Non ou inconnu" --> Reprise9
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 9.1 | `aidd-orchestrator:01-sdlc — Frame`; `aidd-pm:04-spec — si le contrat manque` | **Contrat prêt** : `Source existante ou spec.md dans le dossier de tâche` (à résoudre) |
| 9.2 | `aidd-orchestrator:01-sdlc — Deliver`; `aidd-dev:01-plan`; `aidd-dev:02-implement`; `aidd-dev:03-assert`; `aidd-dev:06-test`; `aidd-vcs:01-commit` | **Plan et phases techniques** : `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>_<feature-slug>/plan.md + phase-<n>.md` (natif); **Candidat vérifié** : `Code, tests, commits et preuves du candidat` (à résoudre) |
| 9.3 | `aidd-orchestrator:01-sdlc — Check`; `aidd-dev:05-review`; `aidd-refine:02-challenge`; `aidd-vcs:02-pull-request` | **Revue et livraison révisable** : `Rapports du candidat + URL de PR en brouillon` (à résoudre) |

**Critère complet :** Le contrat est satisfait, les vérifications pertinentes passent et les conclusions de revue sont traitées.

[Source Mermaid de la phase](mermaid/09-phase.mmd).

### 10. Valider le MVP dans son ensemble

**À adapter :** Paiement, rôles, charge, restauration ou intégrations à vérifier lorsqu’ils existent ; la profondeur suit le risque réel.

```mermaid
---
title: "Phase 10 : Valider le MVP dans son ensemble"
---
flowchart TB
  Entree10["Entrée : Les tranches intégrées en préproduction"]
  subgraph Phase10SousPhase1["10.1 · Vérifier le parcours intégré"]
  Question10Partie1["Question : Le parcours intégré fonctionne-t-il ?"]
  Reponse10Partie1["Réponse attendue : Tâche, erreurs, données, droits et qualité vérifiés"]
  Skills10Partie1["AIDD Dev : 03-assert et 06-test"]
  Resultat10Partie1["Résultat : Rapport et preuves dans recette-mvp.md, proposé"]
  end
  subgraph Phase10SousPhase2["10.2 · Vérifier l’usage réel"]
  Question10Partie2["Question : La cible peut-elle accomplir la tâche ?"]
  Reponse10Partie2["Réponse attendue : Observations d’usage et d’accessibilité contextualisées"]
  Skills10Partie2["Interfaces : better-interface ; Impeccable : audit et polish"]
  Resultat10Partie2["Résultat : Recette d’usage et interface corrigée"]
  end
  subgraph Phase10SousPhase3["10.3 · Décider de l’ouverture"]
  Question10Partie3["Question : Peut-on ouvrir et revenir en arrière si besoin ?"]
  Reponse10Partie3["Réponse attendue : Écarts bloquants traités et limites acceptées"]
  Skills10Partie3["AIDD Refine : 02-challenge"]
  Resultat10Partie3["Résultat : Décision et retour arrière dans lancement.md, proposé"]
  end
  Decision10{"Parcours du MVP validé et écarts bloquants traités ?"}
  Suite10["Oui : Phase 11 : ouvrir à la première population"]
  Reprise10["Non ou inconnu : reprendre le point manquant, retour possible en phase 9"]

  Entree10 --> Question10Partie1
  Question10Partie1 --> Reponse10Partie1
  Reponse10Partie1 --> Skills10Partie1
  Skills10Partie1 --> Resultat10Partie1
  Resultat10Partie1 --> Question10Partie2
  Question10Partie2 --> Reponse10Partie2
  Reponse10Partie2 --> Skills10Partie2
  Skills10Partie2 --> Resultat10Partie2
  Resultat10Partie2 --> Question10Partie3
  Question10Partie3 --> Reponse10Partie3
  Reponse10Partie3 --> Skills10Partie3
  Skills10Partie3 --> Resultat10Partie3
  Resultat10Partie3 --> Decision10
  Decision10 -- "Oui" --> Suite10
  Decision10 -- "Non ou inconnu" --> Reprise10
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 10.1 | `aidd-dev:03-assert`; `aidd-dev:06-test` | **Vérification globale du candidat** : `docs/recette-mvp.md` (proposé) |
| 10.2 | `interfaces:better-interface`; `impeccable:impeccable — audit puis polish si utile` | **Recette d’usage et corrections** : `docs/recette-mvp.md` (proposé) |
| 10.3 | `aidd-refine:02-challenge` | **Décision d’ouverture et retour arrière** : `docs/lancement.md` (proposé) |

**Critère complet :** Le parcours principal passe en environnement représentatif ; aucun problème bloquant connu ne reste sans résolution et les limites restantes sont acceptées.

[Source Mermaid de la phase](mermaid/10-phase.mmd).

### 11. Mettre le MVP entre les mains des utilisateurs

**À adapter :** Pilote fermé, accès privé ou lancement public selon l’objectif ; une grande campagne et un tag de release ne sont pas indispensables à tout MVP.

```mermaid
---
title: "Phase 11 : Mettre le MVP entre les mains des utilisateurs"
---
flowchart TB
  Entree11["Entrée : Le candidat validé et la population de lancement"]
  subgraph Phase11SousPhase1["11.1 · Préparer l’accès et la présentation"]
  Question11Partie1["Question : Comment la cible comprend-elle et démarre-t-elle ?"]
  Reponse11Partie1["Réponse attendue : Message, accès, premier usage et support prêts"]
  Skills11Partie1["Marketing : launch et product-marketing"]
  Resultat11Partie1["Résultat : Page, invitation ou démonstration selon le canal"]
  end
  subgraph Phase11SousPhase2["11.2 · Livrer et ouvrir à la bonne population"]
  Question11Partie2["Question : La version livrée est-elle accessible et fonctionnelle ?"]
  Reponse11Partie2["Réponse attendue : Adresse et parcours vérifiés pour la population prévue"]
  Skills11Partie2["Hébergeur réel ; Marketing launch ; VCS release-tag si utile"]
  Resultat11Partie2["Résultat : URL livrée ; tag et notes de version si nécessaires"]
  end
  subgraph Phase11SousPhase3["11.3 · Vérifier la boucle de retours"]
  Question11Partie3["Question : Peut-on mesurer la valeur et recevoir les problèmes ?"]
  Reponse11Partie3["Réponse attendue : Mesure sans doublon et canal de retours fonctionnel"]
  Skills11Partie3["Marketing : launch ; outils de mesure et de support"]
  Resultat11Partie3["Résultat : Événements vérifiés et premiers retours datés"]
  end
  Decision11{"Produit accessible et action de valeur observable ?"}
  Suite11["Oui : Phase 12 : observer et choisir la suite"]
  Reprise11["Non ou inconnu : reprendre le point manquant, retour possible en phase 10"]

  Entree11 --> Question11Partie1
  Question11Partie1 --> Reponse11Partie1
  Reponse11Partie1 --> Skills11Partie1
  Skills11Partie1 --> Resultat11Partie1
  Resultat11Partie1 --> Question11Partie2
  Question11Partie2 --> Reponse11Partie2
  Reponse11Partie2 --> Skills11Partie2
  Skills11Partie2 --> Resultat11Partie2
  Resultat11Partie2 --> Question11Partie3
  Question11Partie3 --> Reponse11Partie3
  Reponse11Partie3 --> Skills11Partie3
  Skills11Partie3 --> Resultat11Partie3
  Resultat11Partie3 --> Decision11
  Decision11 -- "Oui" --> Suite11
  Decision11 -- "Non ou inconnu" --> Reprise11
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 11.1 | `marketing-skills:launch`; `marketing-skills:product-marketing` | **Présentation et démarrage** : `Page, invitation ou démonstration selon le canal` (à résoudre) |
| 11.2 | `Outil réel de l’hébergeur — hors de ces neuf plugins`; `marketing-skills:launch`; `aidd-vcs:03-release-tag — si utile` | **Version accessible** : `URL de production ou accès privé vérifié` (à résoudre); **Version et notes si nécessaires** : `Tag et notes de release` (à résoudre) |
| 11.3 | `marketing-skills:launch`; `Outils de mesure et de support du projet` | **Mesure et retours opérationnels** : `Événements vérifiés, retours et suivi d’erreurs` (à résoudre) |

**Critère complet :** Le produit fonctionne après livraison pour la population prévue et le résultat principal peut être observé.

[Source Mermaid de la phase](mermaid/11-phase.mmd).

### 12. Mesurer, apprendre et choisir la suite

**À adapter :** Avec peu d’utilisateurs, privilégier des observations et entretiens précis ; ne pas faire d’un petit échantillon une preuve statistique ni exiger un A/B test.

```mermaid
---
title: "Phase 12 : Mesurer, apprendre et choisir la suite"
---
flowchart TB
  Entree12["Entrée : Les usages et retours sur la fenêtre prévue"]
  subgraph Phase12SousPhase1["12.1 · Observer l’utilisation"]
  Question12Partie1["Question : Que font réellement les utilisateurs ?"]
  Reponse12Partie1["Réponse attendue : Mesures et retours avec leur contexte et leurs limites"]
  Skills12Partie1["Marketing : customer-research ; mesure du projet"]
  Resultat12Partie1["Résultat : Premiers usages dans bilan-mvp.md, proposé"]
  end
  subgraph Phase12SousPhase2["12.2 · Réviser les hypothèses"]
  Question12Partie2["Question : Quelles hypothèses sont étayées ou contredites ?"]
  Reponse12Partie2["Réponse attendue : Un bilan et une décision justifiés par les faits"]
  Skills12Partie2["Marketing : customer-research ; AIDD Refine : 02-challenge"]
  Resultat12Partie2["Résultat : Bilan de validation et décision dans bilan-mvp.md"]
  end
  subgraph Phase12SousPhase3["12.3 · Préparer la prochaine boucle"]
  Question12Partie3["Question : Quelle est la prochaine priorité utile ?"]
  Reponse12Partie3["Réponse attendue : Une demande, une recherche ou un arrêt explicite"]
  Skills12Partie3["AIDD Orchestrator : 02-backlog ; Marketing : product-marketing"]
  Resultat12Partie3["Résultat : Backlog et contexte marketing mis à jour"]
  end
  Decision12{"Décision justifiée et prochaine action explicite ?"}
  Suite12["Oui : Stabiliser, reprendre le backlog, réorienter ou arrêter"]
  Reprise12["Non ou inconnu : reprendre le point manquant, retour possible en phase 8"]

  Entree12 --> Question12Partie1
  Question12Partie1 --> Reponse12Partie1
  Reponse12Partie1 --> Skills12Partie1
  Skills12Partie1 --> Resultat12Partie1
  Resultat12Partie1 --> Question12Partie2
  Question12Partie2 --> Reponse12Partie2
  Reponse12Partie2 --> Skills12Partie2
  Skills12Partie2 --> Resultat12Partie2
  Resultat12Partie2 --> Question12Partie3
  Question12Partie3 --> Reponse12Partie3
  Reponse12Partie3 --> Skills12Partie3
  Skills12Partie3 --> Resultat12Partie3
  Resultat12Partie3 --> Decision12
  Decision12 -- "Oui" --> Suite12
  Decision12 -- "Non ou inconnu" --> Reprise12
```

| Sous-phase | Identifiants de skills et capacités | Livrables et chemins complets |
| --- | --- | --- |
| 12.1 | `marketing-skills:customer-research`; `Outils de mesure du projet` | **Premiers usages et retours** : `docs/bilan-mvp.md` (proposé) |
| 12.2 | `marketing-skills:customer-research`; `aidd-refine:02-challenge` | **Bilan de validation** : `docs/bilan-mvp.md` (proposé) |
| 12.3 | `aidd-orchestrator:02-backlog`; `marketing-skills:product-marketing` | **Prochaine boucle et contexte à jour** : `Backlog + .agents/product-marketing.md` (à résoudre) |

**Critère complet :** La décision s’appuie sur des faits datés et leurs limites ; le prochain changement ou l’arrêt est explicite.

[Source Mermaid de la phase](mermaid/12-phase.mmd).

## Sources

[workflow.json](workflow.json) et [schema.json](schema.json) portent le contenu ; les sources des skills sont répertoriées dans [FLOW.md](FLOW.md). Les conventions Mermaid appliquées viennent du skill local AIDD Context 09-mermaid : titres en frontmatter, identifiants descriptifs, libellés sur une ligne, déclarations avant les liens et aucune personnalisation de style.
