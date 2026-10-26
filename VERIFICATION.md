# Vérification de la version 2

Constat du 26 octobre 2026 sur les fichiers de ce dossier.

## Réalisé

- Le modèle courant comporte 12 phases de repérage et 20 séquences à identifiants stables, avec les sept rubriques de contrat.
- Le nombre d’étapes est libre ; les conditions d’applicabilité et les échéances de clarification sont explicites.
- Les guides, fiches, glossaire, périmètre, schémas et cas d’école dérivent de `workflow.json` ; le contrôle détecte une divergence de fichier généré.
- L’exemple est au mode `illustration` et ses preuves sont marquées simulées. Aucun produit MiniRévisions n’a été construit, testé ou déployé.
- La version 1 et son audit sont conservés dans `archive/v1/`. Les empreintes de son manifeste ont été contrôlées.

## Contrôles exécutés

`python3 scripts/test_flow.py`, dans un job temporaire Portly : **28 tests passés**.

Ils couvrent notamment :

- intégrité des contrats, références, destinations, prérequis et liens documentaires ;
- idéation possible avec des inconnues futures, puis contrôle des informations lorsqu’elles deviennent nécessaires ;
- maintien d’un défaut de code dans la livraison et d’une fenêtre d’observation incomplète en attente ;
- distinction entre PR en brouillon et candidat intégré ;
- non-applicabilité justifiée et refus d’écarter une séquence obligatoire ;
- versions d’entrée, de sortie et de preuve, avec réexamen des validations affectées ;
- refus d’une revue attribuée au réalisateur et d’une preuve simulée dans une instance réelle ;
- conservation explicite d’une nouvelle itération et de la destination de reprise après spike ;
- cohérence du cas d’école et fonctionnement des commandes de lecture `check` et `next` ;
- correspondance du contenu généré avec le modèle courant et intégrité de l’archive.

`scripts/verify_mermaid.cjs`, dans un job temporaire Portly, avec le runtime navigateur déjà disponible : **21 schémas parsés et rendus avec Mermaid 10.9.5**. Les rendus des séquences S00 et S91 ont été inspectés visuellement.

## Ce que ces contrôles ne démontrent pas

Les tests portent sur le modèle, les guides et la cohérence des informations déclarées. Ils ne prouvent ni la vérité d’une observation utilisateur, ni une permission externe, ni le résultat d’un projet produit réel.

Le préfixe de la requête SDLC est contrôlé dans le modèle. Aucun appel de livraison SDLC réel n’a été exécuté dans ce travail. La disponibilité, la version et les droits des plugins et services restent à vérifier lors d’une application du flow.

Un essai avec un novice et un pilote de projet réel restent nécessaires pour mesurer la compréhension, les reprises et l’efficacité de l’accompagnement. La version 2 est une structure contrôlable prête à éprouver, sans promesse de réussite automatique.
