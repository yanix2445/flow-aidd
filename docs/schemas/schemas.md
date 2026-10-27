# Schémas des séquences

> Généré depuis `skills/flow-aidd/references/workflow.json` par `tools/build.py`. Ne pas modifier à la main.


Les flèches du premier schéma montrent les prérequis, pas une validation automatique. Pour une séquence conditionnelle, une non-applicabilité tracée peut satisfaire le prérequis. Les tables de chaque fiche portent les retours et attentes. Dans chaque contrat, le bloc bleu nomme les plugins mobilisés (AIDD, Impeccable, marketing-skills, outils du projet) et le bloc beige les agents de contrôle ; `*` signale une capacité activée seulement selon le contexte ou le cas.

```mermaid
---
title: "Prérequis des séquences — le routage est détaillé dans chaque fiche"
---
flowchart TB
  SequenceS00["S00 · Cadrer le projet et choisir la profondeur"]
  SequenceS10["S10 · Transformer l’idée en intention claire"]
  SequenceS20["S20 · Éclairer le besoin avec des observations"]
  SequenceS30["S30 · Choisir la promesse et sa viabilité"]
  SequenceS40["S40 · Fixer le parcours du MVP et ses critères"]
  SequenceS50["S50 · Concevoir le parcours et l’interface utiles"]
  SequenceS51["S51 · Éprouver le parcours avant de le généraliser"]
  SequenceS60["S60 · Lever une inconnue technique déterminante"]
  SequenceS61["S61 · Choisir une architecture suffisante"]
  SequenceS70["S70 · Faire fonctionner le socle réel"]
  SequenceS71["S71 · Conserver le contexte réellement vérifié"]
  SequenceS80["S80 · Préparer une prochaine tranche vérifiable"]
  SequenceS90["S90 · Livrer une tranche avec le SDLC natif"]
  SequenceS91["S91 · Intégrer le candidat et vérifier la préproduction"]
  SequenceS100["S100 · Vérifier le MVP intégré et décider sa préparation"]
  SequenceS110["S110 · Préparer l’ouverture, le support et la mesure"]
  SequenceS111["S111 · Déployer puis contrôler l’adresse réellement livrée"]
  SequenceS112["S112 · Ouvrir l’accès à la première population"]
  SequenceS120["S120 · Observer les usages sur la fenêtre prévue"]
  SequenceS121["S121 · Décider de la prochaine priorité ou de l’arrêt"]
  SequenceS00 --> SequenceS10
  SequenceS10 --> SequenceS20
  SequenceS20 --> SequenceS30
  SequenceS30 --> SequenceS40
  SequenceS40 -. "Si applicable" .-> SequenceS50
  SequenceS50 -. "Si applicable" .-> SequenceS51
  SequenceS00 -. "Si applicable" .-> SequenceS60
  SequenceS40 --> SequenceS61
  SequenceS60 --> SequenceS61
  SequenceS61 --> SequenceS70
  SequenceS70 --> SequenceS71
  SequenceS40 --> SequenceS80
  SequenceS51 --> SequenceS90
  SequenceS71 --> SequenceS90
  SequenceS80 --> SequenceS90
  SequenceS90 --> SequenceS91
  SequenceS91 --> SequenceS100
  SequenceS40 --> SequenceS110
  SequenceS100 --> SequenceS111
  SequenceS110 --> SequenceS111
  SequenceS111 --> SequenceS112
  SequenceS110 --> SequenceS112
  SequenceS112 --> SequenceS120
  SequenceS120 --> SequenceS121
```

## Contrats détaillés

### S00 — Cadrer le projet et choisir la profondeur

```mermaid
---
title: "S00 — Cadrer le projet et choisir la profondeur"
---
flowchart TB
  Entree["Entrée : Une intention, une difficulté ou un projet existant à reprendre."]
  Responsable["Responsable : coordinateur"]
  Action["Action : Cadrer le projet et choisir la profondeur"]
  Sortie["Sortie : cadre"]
  Preuve["Preuves : cadre decide"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S10"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S00.md) pour les questions, capacités, critères de preuve et destinations.

### S10 — Transformer l’idée en intention claire

```mermaid
---
title: "S10 — Transformer l’idée en intention claire"
---
flowchart TB
  Entree["Entrée : cadre"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Transformer l’idée en intention claire"]
  Plugins["AIDD : refine/01-brainstorm"]
  Sortie["Sortie : idee"]
  Preuve["Preuves : intention approuvee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S20"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S10.md) pour les questions, capacités, critères de preuve et destinations.

### S20 — Éclairer le besoin avec des observations

```mermaid
---
title: "S20 — Éclairer le besoin avec des observations"
---
flowchart TB
  Entree["Entrée : cadre, idee"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Éclairer le besoin avec des observations"]
  Plugins["Marketing : product-marketing, customer-research, competitor-profiling"]
  Sortie["Sortie : besoin"]
  Preuve["Preuves : sources, decision besoin"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S30"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S20.md) pour les questions, capacités, critères de preuve et destinations.

### S30 — Choisir la promesse et sa viabilité

```mermaid
---
title: "S30 — Choisir la promesse et sa viabilité"
---
flowchart TB
  Entree["Entrée : cadre, idee, besoin"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Choisir la promesse et sa viabilité"]
  Plugins["AIDD : pm/06-product-brief<br/>Marketing : product-marketing, launch, pricing*, offers*, marketing-psychology"]
  Sortie["Sortie : brief"]
  Preuve["Preuves : opportunite approuvee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S40"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S30.md) pour les questions, capacités, critères de preuve et destinations.

### S40 — Fixer le parcours du MVP et ses critères

```mermaid
---
title: "S40 — Fixer le parcours du MVP et ses critères"
---
flowchart TB
  Entree["Entrée : cadre, brief, besoin"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Fixer le parcours du MVP et ses critères"]
  Plugins["AIDD : pm/03-prd, refine/03-shadow-areas"]
  Sortie["Sortie : mvp"]
  Preuve["Preuves : contrat verifiable, perimetre approuve"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S50, S61, S80, S110"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S40.md) pour les questions, capacités, critères de preuve et destinations.

### S50 — Concevoir le parcours et l’interface utiles

```mermaid
---
title: "S50 — Concevoir le parcours et l’interface utiles"
---
flowchart TB
  Entree["Entrée : cadre, mvp"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Concevoir le parcours et l’interface utiles"]
  Plugins["Impeccable : init, shape<br/>Marketing : copywriting*, site-architecture*"]
  Sortie["Sortie : parcours"]
  Preuve["Preuves : parcours coherent, direction confirmee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S51"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S50.md) pour les questions, capacités, critères de preuve et destinations.

### S51 — Éprouver le parcours avant de le généraliser

```mermaid
---
title: "S51 — Éprouver le parcours avant de le généraliser"
---
flowchart TB
  Entree["Entrée : cadre, mvp, parcours"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Éprouver le parcours avant de le généraliser"]
  Plugins["Impeccable : impeccable, critique, clarify, onboard*, live*"]
  Sortie["Sortie : prototype"]
  Preuve["Preuves : epreuve usage, decision ux"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S90"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S51.md) pour les questions, capacités, critères de preuve et destinations.

### S60 — Lever une inconnue technique déterminante

```mermaid
---
title: "S60 — Lever une inconnue technique déterminante"
---
flowchart TB
  Entree["Entrée : cadre"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Lever une inconnue technique déterminante"]
  Plugins["AIDD : pm/05-spike"]
  Sortie["Sortie : spike"]
  Preuve["Preuves : essai borne, conclusion risque"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par verificateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : RESUME"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S60.md) pour les questions, capacités, critères de preuve et destinations.

### S61 — Choisir une architecture suffisante

```mermaid
---
title: "S61 — Choisir une architecture suffisante"
---
flowchart TB
  Entree["Entrée : cadre, mvp"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Choisir une architecture suffisante"]
  Plugins["AIDD : context/01-bootstrap, dev/01-plan"]
  Sortie["Sortie : architecture"]
  Preuve["Preuves : choix trace, architecture acceptee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S70"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S61.md) pour les questions, capacités, critères de preuve et destinations.

### S70 — Faire fonctionner le socle réel

```mermaid
---
title: "S70 — Faire fonctionner le socle réel"
---
flowchart TB
  Entree["Entrée : cadre, mvp, architecture"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Faire fonctionner le socle réel"]
  Plugins["AIDD : vcs/00-repo-init, dev/01-plan, dev/02-implement, dev/03-assert"]
  Sortie["Sortie : socle"]
  Preuve["Preuves : socle execute, preproduction socle"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par verificateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S71"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S70.md) pour les questions, capacités, critères de preuve et destinations.

### S71 — Conserver le contexte réellement vérifié

```mermaid
---
title: "S71 — Conserver le contexte réellement vérifié"
---
flowchart TB
  Entree["Entrée : cadre, architecture, socle"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Conserver le contexte réellement vérifié"]
  Plugins["AIDD : context/02-project-memory"]
  Sortie["Sortie : memoire"]
  Preuve["Preuves : contexte lisible"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par coordinateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S90"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S71.md) pour les questions, capacités, critères de preuve et destinations.

### S80 — Préparer une prochaine tranche vérifiable

```mermaid
---
title: "S80 — Préparer une prochaine tranche vérifiable"
---
flowchart TB
  Entree["Entrée : cadre, mvp"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Préparer une prochaine tranche vérifiable"]
  Plugins["AIDD : orchestrator/02-backlog, pm/02-user-stories, pm/07-epic, pm/04-spec<br/>Impeccable : shape*"]
  Sortie["Sortie : tranche"]
  Preuve["Preuves : demande prete, priorite decidee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S90"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S80.md) pour les questions, capacités, critères de preuve et destinations.

### S90 — Livrer une tranche avec le SDLC natif

```mermaid
---
title: "S90 — Livrer une tranche avec le SDLC natif"
---
flowchart TB
  Entree["Entrée : cadre, mvp, architecture, socle, memoire, tranche"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Livrer une tranche avec le SDLC natif"]
  Plugins["AIDD : orchestrator/01-sdlc"]
  Sortie["Sortie : candidat"]
  Preuve["Preuves : controles candidat, revue independante, resultat accepte"]
  Controle["Contrôle indépendant : relecteur natif du SDLC"]
  Validation{"Validation par relecteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S91"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S90.md) pour les questions, capacités, critères de preuve et destinations.

### S91 — Intégrer le candidat et vérifier la préproduction

```mermaid
---
title: "S91 — Intégrer le candidat et vérifier la préproduction"
---
flowchart TB
  Entree["Entrée : cadre, candidat, socle"]
  Responsable["Responsable : integration"]
  Action["Action : Intégrer le candidat et vérifier la préproduction"]
  Plugins["AIDD : vcs/02-pull-request, vcs/05-resolve-conflict<br/>Impeccable : document*<br/>Outils du projet : integration du depot"]
  Sortie["Sortie : integration"]
  Preuve["Preuves : autorisation integration, integration constatee, candidat preproduction"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par verificateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S100"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S91.md) pour les questions, capacités, critères de preuve et destinations.

### S100 — Vérifier le MVP intégré et décider sa préparation

```mermaid
---
title: "S100 — Vérifier le MVP intégré et décider sa préparation"
---
flowchart TB
  Entree["Entrée : cadre, mvp, integration"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Vérifier le MVP intégré et décider sa préparation"]
  Plugins["AIDD : dev/03-assert, dev/06-test, refine/02-challenge<br/>Impeccable : audit*, critique*, harden*, polish*, document*"]
  Sortie["Sortie : recette"]
  Preuve["Preuves : parcours integre, usage qualifie, recette acceptee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S111"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S100.md) pour les questions, capacités, critères de preuve et destinations.

### S110 — Préparer l’ouverture, le support et la mesure

```mermaid
---
title: "S110 — Préparer l’ouverture, le support et la mesure"
---
flowchart TB
  Entree["Entrée : cadre, brief, mvp"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Préparer l’ouverture, le support et la mesure"]
  Plugins["Impeccable : onboard*<br/>Marketing : launch, product-marketing, analytics, conversion-tracking*, onboarding, copywriting, emails*, cro*, signup*, seo-audit*, schema*, ai-seo*, image, social*"]
  Sortie["Sortie : ouverture"]
  Preuve["Preuves : preparation ouverture, cadre ouverture accepte"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S111"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S110.md) pour les questions, capacités, critères de preuve et destinations.

### S111 — Déployer puis contrôler l’adresse réellement livrée

```mermaid
---
title: "S111 — Déployer puis contrôler l’adresse réellement livrée"
---
flowchart TB
  Entree["Entrée : cadre, mvp, integration, recette, ouverture"]
  Responsable["Responsable : exploitation"]
  Action["Action : Déployer puis contrôler l’adresse réellement livrée"]
  Plugins["AIDD : vcs/03-release-tag<br/>Marketing : analytics, seo-audit*<br/>Outils du projet : hebergeur du projet"]
  Sortie["Sortie : deploiement"]
  Preuve["Preuves : livraison executee, adresse finale"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par verificateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S112"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S111.md) pour les questions, capacités, critères de preuve et destinations.

### S112 — Ouvrir l’accès à la première population

```mermaid
---
title: "S112 — Ouvrir l’accès à la première population"
---
flowchart TB
  Entree["Entrée : cadre, mvp, ouverture, deploiement"]
  Responsable["Responsable : exploitation"]
  Action["Action : Ouvrir l’accès à la première population"]
  Plugins["Marketing : launch, analytics, onboarding, emails, social, directory-submissions*<br/>Outils du projet : acces et support du projet"]
  Sortie["Sortie : acces"]
  Preuve["Preuves : population acces, premier parcours, mesure operationnelle"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S120"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S112.md) pour les questions, capacités, critères de preuve et destinations.

### S120 — Observer les usages sur la fenêtre prévue

```mermaid
---
title: "S120 — Observer les usages sur la fenêtre prévue"
---
flowchart TB
  Entree["Entrée : cadre, mvp, ouverture, acces"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Observer les usages sur la fenêtre prévue"]
  Plugins["Marketing : customer-research, analytics, attribution*, cro<br/>Outils du projet : mesure du projet"]
  Sortie["Sortie : observations"]
  Preuve["Preuves : usage date, limites mesure"]
  Controle["Contrôle indépendant : verificateur"]
  Validation{"Validation par verificateur : critères et preuves satisfaits ?"}
  Destination["Suite validée : S121"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S120.md) pour les questions, capacités, critères de preuve et destinations.

### S121 — Décider de la prochaine priorité ou de l’arrêt

```mermaid
---
title: "S121 — Décider de la prochaine priorité ou de l’arrêt"
---
flowchart TB
  Entree["Entrée : cadre, brief, mvp, observations"]
  Responsable["Responsable : coordinateur"]
  Action["Action : Décider de la prochaine priorité ou de l’arrêt"]
  Plugins["AIDD : refine/02-challenge, orchestrator/02-backlog<br/>Marketing : product-marketing, marketing-plan, pricing*, churn-prevention*, ab-testing*, marketing-ideas"]
  Sortie["Sortie : suite"]
  Preuve["Preuves : bilan trace, suite decidee"]
  Controle["Contrôle indépendant : verificateur, relecteur"]
  Validation{"Validation par porteur : critères et preuves satisfaits ?"}
  Destination["Suite validée : END"]
  AutreIssue["Sinon : préciser, réparer ou attendre selon le tableau"]
  Entree --> Responsable
  Responsable --> Action
  Action --> Plugins
  Plugins --> Sortie
  Sortie --> Preuve
  Preuve --> Controle
  Controle --> Validation
  Validation -- "Oui" --> Destination
  Validation -- "Non ou inconnu" --> AutreIssue
  classDef plugins fill:#eef3fb,stroke:#7f9cc7
  class Plugins plugins
  classDef controle fill:#f6f0e6,stroke:#b08a4f
  class Controle controle
```

Lire le [contrat complet](../../skills/flow-aidd/references/sequences/S121.md) pour les questions, capacités, critères de preuve et destinations.
