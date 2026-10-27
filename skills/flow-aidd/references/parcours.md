# Parcours

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


12 phases de référence et 20 séquences. Le nombre d’actions varie ; le contrat de chaque séquence est stable.

| Séquence | Phase | Intention | Prérequis |
| --- | --- | --- | --- |
| [S00](sequences/S00.md) | Cadrage transversal | Cadrer le projet et choisir la profondeur | Intention ou état existant |
| [S10](sequences/S10.md) | 1 — Clarifier l’idée | Transformer l’idée en intention claire | S00 |
| [S20](sequences/S20.md) | 2 — Comprendre le besoin | Éclairer le besoin avec des observations | S10 |
| [S30](sequences/S30.md) | 3 — Choisir la promesse et la viabilité | Choisir la promesse et sa viabilité | S20 |
| [S40](sequences/S40.md) | 4 — Délimiter le MVP | Fixer le parcours du MVP et ses critères | S30 |
| [S50](sequences/S50.md) | 5 — Concevoir et éprouver l’expérience | Concevoir le parcours et l’interface utiles | S40 |
| [S51](sequences/S51.md) | 5 — Concevoir et éprouver l’expérience | Éprouver le parcours avant de le généraliser | S50 |
| [S60](sequences/S60.md) | 6 — Valider la faisabilité | Lever une inconnue technique déterminante | S00 |
| [S61](sequences/S61.md) | 6 — Valider la faisabilité | Choisir une architecture suffisante | S40, S60 |
| [S70](sequences/S70.md) | 7 — Préparer les fondations | Faire fonctionner le socle réel | S61 |
| [S71](sequences/S71.md) | 7 — Préparer les fondations | Conserver le contexte réellement vérifié | S70 |
| [S80](sequences/S80.md) | 8 — Préparer la prochaine tranche | Préparer une prochaine tranche vérifiable | S40 |
| [S90](sequences/S90.md) | 9 — Livrer et intégrer | Livrer une tranche avec le SDLC natif | S51, S71, S80 |
| [S91](sequences/S91.md) | 9 — Livrer et intégrer | Intégrer le candidat et vérifier la préproduction | S90 |
| [S100](sequences/S100.md) | 10 — Valider le MVP intégré | Vérifier le MVP intégré et décider sa préparation | S91 |
| [S110](sequences/S110.md) | 11 — Ouvrir le MVP | Préparer l’ouverture, le support et la mesure | S40 |
| [S111](sequences/S111.md) | 11 — Ouvrir le MVP | Déployer puis contrôler l’adresse réellement livrée | S100, S110 |
| [S112](sequences/S112.md) | 11 — Ouvrir le MVP | Ouvrir l’accès à la première population | S111, S110 |
| [S120](sequences/S120.md) | 12 — Observer et décider | Observer les usages sur la fenêtre prévue | S112 |
| [S121](sequences/S121.md) | 12 — Observer et décider | Décider de la prochaine priorité ou de l’arrêt | S120 |

Les prérequis indiquent l’ordre possible ; la table **Prochaine destination** de chaque fiche décide du routage selon le résultat. Une séquence ne se déduit pas terminée de l’existence d’un fichier.

Les séquences S50/S51 et S60 ont des conditions explicites. Une non-applicabilité est conservée avec sa raison et le cadrage approuvé ; un prérequis déjà satisfait peut être réutilisé avec une preuve actuelle.
