# Glossaire

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


Définitions pour lire le flow ; chaque exemple illustre un terme et ne constitue pas une preuve sur un projet réel.

<a id="phase"></a>

## Phase

Grande intention du projet qui regroupe des séquences.

**Exemple :** La phase de lancement regroupe préparation, déploiement et ouverture.

<a id="sequence"></a>

## Séquence

Unité de travail pilotable avec ses sept rubriques et une issue explicite.

**Exemple :** S91 vérifie l’intégration d’un candidat avant la recette.

<a id="etape"></a>

## Étape

Action concrète à l’intérieur d’une séquence ; leur nombre dépend du travail.

**Exemple :** Dans S91 : vérifier la CI puis constater la révision déployée.

<a id="perimetre"></a>

## Périmètre / scope

Ce qui est inclus, exclu et soumis à une décision.

**Exemple :** Le MVP permet de créer et retrouver une fiche ; le partage attendra.

<a id="mvp"></a>

## MVP

Première version utilisable qui accomplit un parcours utile complet sur un périmètre réduit.

**Exemple :** Créer une fiche, la sauvegarder et la retrouver après rechargement.

<a id="entree"></a>

## Entrée

Information, document, accès ou preuve nécessaire pour commencer.

**Exemple :** La story validée et le contexte du code sont des entrées de S90.

<a id="responsable"></a>

## Responsable

Pilote qui veille à la conduite et à la traçabilité du travail.

**Exemple :** Le coordinateur conserve l’état ; le porteur décide du périmètre.

<a id="sortie"></a>

## Sortie / livrable

Résultat concret produit ou réutilisé par la séquence.

**Exemple :** Une note approuvée, une révision de code ou une décision.

<a id="preuve"></a>

## Preuve

Élément vérifiable qui soutient une conclusion, avec sa source et sa version.

**Exemple :** Un journal de test réussi sur le commit réellement proposé.

<a id="validation"></a>

## Validation

Décision compétente fondée sur les critères et les preuves de la bonne version.

**Exemple :** Le porteur approuve le périmètre v2 ; un testeur constate le résultat technique.

<a id="hypothese"></a>

## Hypothèse

Supposition à distinguer d’un fait et à vérifier si elle compte pour la décision.

**Exemple :** Des étudiants pourraient vouloir retrouver rapidement leurs fiches.

<a id="decision"></a>

## Décision

Choix attribué et daté qui engage le périmètre autorisé.

**Exemple :** Reporter les comptes utilisateurs pour cette première version personnelle.

<a id="risque"></a>

## Risque accepté

Manque ou incertitude que le porteur accepte explicitement avec raison et prochaine vérification.

**Exemple :** Ouvrir un petit pilote malgré un test externe encore absent, en le consignant.

<a id="brief"></a>

## Product Brief / brief produit

Note expliquant pour qui une opportunité est utile et comment la vérifier.

**Exemple :** Cible, difficulté, promesse, contraintes et condition de poursuite.

<a id="prd"></a>

## PRD

Document d’exigences : décrit ce que le produit doit permettre et pourquoi.

**Exemple :** Parcours, règles, exclusions, états utiles et critères de réussite.

<a id="spec"></a>

## Spec / contrat de changement

Exigences observables d’un changement borné, sans imposer son implémentation.

**Exemple :** Une fiche vide ne se sauvegarde pas ; le texte saisi reste accessible après l’erreur.

<a id="backlog"></a>

## Backlog

Liste de demandes à examiner et ordonner ; toutes ne sont pas encore prêtes.

**Exemple :** Créer une fiche, puis lister les fiches, puis améliorer la recherche.

<a id="story"></a>

## User story / demande utilisateur

Petite demande liée à un acteur, un besoin, un résultat et des critères.

**Exemple :** Un étudiant retrouve la fiche qu’il a enregistrée.

<a id="epic"></a>

## Epic

Regroupement de plusieurs résultats liés, utile seulement si la liste devient difficile à comprendre.

**Exemple :** Organiser sa bibliothèque de fiches peut regrouper plusieurs stories.

<a id="tranche"></a>

## Tranche verticale

Petite livraison utile qui traverse les couches nécessaires jusqu’au résultat utilisateur.

**Exemple :** Formulaire, logique et sauvegarde fonctionnent ensemble pour une seule tâche.

<a id="spike"></a>

## Spike

Essai borné qui répond à une inconnue précise avant d’engager une réalisation.

**Exemple :** Vérifier si une API fournit les données nécessaires dans le budget disponible.

<a id="ux"></a>

## UX

Expérience d’usage : compréhension, effort et réussite d’une tâche.

**Exemple :** Une personne sait où créer puis retrouver sa fiche.

<a id="ui"></a>

## UI

Interface visible avec laquelle la personne interagit.

**Exemple :** Formulaire, liste et messages d’erreur.

<a id="prototype"></a>

## Prototype

Représentation ou essai pour éprouver une idée ; pas une preuve de production.

**Exemple :** Un parcours cliquable avec des contenus représentatifs.

<a id="socle"></a>

## Socle / scaffold

Base réelle du projet : fichiers, configuration et services minimaux.

**Exemple :** Le dépôt démarre, se vérifie et montre un premier parcours en préproduction.

<a id="sdlc"></a>

## SDLC

Boucle AIDD qui cadre, réalise, vérifie et revoit un changement jusqu’à une PR en brouillon.

**Exemple :** Le coordinateur lance S90 sur une seule demande prête.

<a id="frame"></a>

## Frame

Partie du SDLC qui établit le contrat du changement.

**Exemple :** Clarifier le comportement demandé avant de planifier le code.

<a id="deliver"></a>

## Deliver

Partie du SDLC qui planifie, implémente et vérifie le candidat.

**Exemple :** Corriger un test qui échoue dans la réalisation de la tranche.

<a id="check"></a>

## Check

Partie du SDLC qui fait revoir et challenger le candidat indépendamment.

**Exemple :** Un relecteur compare le résultat au contrat et aux preuves.

<a id="commit"></a>

## Commit

Instantané identifié de changements dans Git.

**Exemple :** Un identifiant de commit désigne exactement le code testé.

<a id="pr"></a>

## PR / demande de fusion

Proposition de modification soumise au dépôt ; un brouillon n’est pas une fusion.

**Exemple :** La PR décrit la tranche et les contrôles déjà réalisés.

<a id="ci"></a>

## CI / intégration continue

Contrôles automatisés associés à une révision du dépôt.

**Exemple :** Build, typage et tests s’exécutent sur le candidat.

<a id="integration"></a>

## Intégration

Passage du changement revu au code effectivement réuni et testable.

**Exemple :** La révision fusionnée est disponible en préproduction.

<a id="preproduction"></a>

## Préproduction / preview

Environnement pour vérifier le candidat avant l’ouverture prévue.

**Exemple :** Une URL permet d’essayer la version intégrée avant le pilote.

<a id="production"></a>

## Production

Version réellement accessible à la population prévue.

**Exemple :** L’adresse du MVP privé ou public utilisée par les premiers utilisateurs.

<a id="recette"></a>

## Recette

Vérification du parcours et des critères sur une version identifiée.

**Exemple :** Créer une fiche, recharger, la retrouver et vérifier les erreurs prévues.

<a id="retour_arriere"></a>

## Retour arrière / rollback

Procédure pour revenir à un état acceptable après un problème de livraison.

**Exemple :** Rétablir la version précédente et traiter les conséquences éventuelles sur les données.

<a id="activation"></a>

## Activation

Premier moment où l’utilisateur obtient le bénéfice défini pour le produit.

**Exemple :** Il retrouve une fiche qu’il a créée plutôt que de seulement ouvrir la page.

<a id="revision"></a>

## Version / révision

Identité du contenu précis utilisé ou vérifié.

**Exemple :** Un hash de document ou un commit ; une décision doit citer la bonne révision.

<a id="non_applicable"></a>

## Non applicable

Élément écarté parce qu’une condition explicite est fausse, avec justification.

**Exemple :** Une API sans interface graphique ne passe pas les séquences de design graphique.

<a id="attente"></a>

## Attente

Travail suspendu pour une information, un accès ou une validation nommée.

**Exemple :** S120 attend la fin de la fenêtre d’observation ; il ne crée pas de fausses données.

<a id="source"></a>

## Source propriétaire

Emplacement qui fait autorité pour une information ; les autres vues en dérivent.

**Exemple :** Le contrat du MVP porte le périmètre ; les schémas le résument.

<a id="simulation"></a>

## Simulation / illustration

Donnée inventée ou mise en situation pour expliquer, jamais preuve d’un résultat réel.

**Exemple :** L’exemple MiniRévisions illustre une approbation sans prétendre qu’un utilisateur l’a donnée.

<a id="skill"></a>

## Skill / capacité

Instructions spécialisées à lire et activer pour conduire une tâche précise.

**Exemple :** customer-research aide à analyser des observations ; il ne crée pas de vrais entretiens fictifs.

<a id="portly"></a>

## Portly

Outil utilisé dans ce workspace pour gérer les serveurs et exécuter les tâches bornées.

**Exemple :** Un build est lancé comme job temporaire puis ses logs sont attendus.
