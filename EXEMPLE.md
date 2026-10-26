# Exemple complet — MiniRévisions

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


**CAS FICTIF — AUCUNE PREUVE RÉELLE.** Exemple fictif de petite application personnelle pour créer, conserver et retrouver des fiches. Tous les faits, preuves, décisions et états du cas d’école sont illustratifs ; aucune application n’a été construite ou publiée.

**Parcours critique :** Créer une fiche avec un titre et un contenu, recharger puis retrouver la fiche ; un titre vide déclenche une erreur compréhensible.

**Exclusions :** Comptes et authentification multi-utilisateur, Paiement, Partage public, Synchronisation entre appareils.

## Cadrage illustratif

```json
{
  "project_kind": "application_personnelle",
  "has_graphical_ui": true,
  "critical_technical_risk": false,
  "commercial": false,
  "public_users": false,
  "existing_repository": false,
  "integration_owner": "porteur_fictif",
  "operations_owner": "porteur_fictif"
}
```

Les emplacements `illustration://` du fichier d’état sont des identifiants de cas d’école. Ils ne représentent pas un service ou un fichier produit. Toutes ses preuves portent `simulated: true` et son mode est `illustration`.

## Parcours de bout en bout

### S00 — Cadrer le projet et choisir la profondeur

MiniRévisions est un exemple fictif : application personnelle avec interface graphique, sans objectif commercial, sans dépôt initial et sans risque technique bloquant identifié. Le porteur fictif assure intégration et exploitation.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | Intention de départ |
| Responsable | coordinateur_fictif |
| Action | Recueillir le contexte, résoudre les responsabilités et proposer le parcours adapté avant d’activer une chaîne de travail. |
| Sortie | cadre |
| Preuve | S00:cadre_decide — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S10 |

### S10 — Transformer l’idée en intention claire

L’étudiant fictif veut créer une fiche et la retrouver plus tard. Le besoin d’autres étudiants reste une hypothèse ; aucune recherche collective n’est prétendue.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre |
| Responsable | coordinateur_fictif |
| Action | Activer le brainstorm pour aider à formuler une situation et un résultat utiles, puis proposer une note d’intention. |
| Sortie | idee |
| Preuve | S10:intention_approuvee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S20 |

### S20 — Éclairer le besoin avec des observations

Dans le cas d’école, le porteur observe sa propre manière de chercher une fiche. Cette observation illustrative ne valide pas un marché et ne remplace pas des données réelles.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, idee |
| Responsable | coordinateur_fictif |
| Action | Choisir une recherche proportionnée, analyser les faits accessibles et proposer une décision sur le besoin. |
| Sortie | besoin |
| Preuve | S20:sources, S20:decision_besoin — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S30 |

### S30 — Choisir la promesse et sa viabilité

Promesse fictive : retrouver ses propres fiches dans un outil simple. Le modèle économique est non pertinent pour ce MVP personnel ; la maintenance reste une contrainte.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, idee, besoin |
| Responsable | coordinateur_fictif |
| Action | Formaliser pourquoi poursuivre, pour qui, avec quelle promesse et quels moyens ; faire décider le porteur. |
| Sortie | brief |
| Preuve | S30:opportunite_approuvee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S40 |

### S40 — Fixer le parcours du MVP et ses critères

Le MVP fictif crée et liste des fiches avec persistance locale. Comptes, paiement, partage et synchronisation entre appareils sont exclus. Les critères de recette sont écrits avant le code.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, brief, besoin |
| Responsable | coordinateur_fictif |
| Action | Choisir une source d’exigences proportionnée et définir ce qu’il faudra observer pour accepter le MVP. |
| Sortie | mvp |
| Preuve | S40:contrat_verifiable, S40:perimetre_approuve — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | ['S50', 'S61', 'S80', 'S110'] |

### S50 — Concevoir le parcours et l’interface utiles

Le cas d’école comporte un écran de liste, un formulaire et un message d’erreur. La direction vise la lisibilité ; aucun système de design exhaustif n’est exigé.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp |
| Responsable | coordinateur_fictif |
| Action | Activer la conception pour transformer les exigences en parcours compréhensible et en direction d’interface confirmée. |
| Sortie | parcours |
| Preuve | S50:parcours_coherent, S50:direction_confirmee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S51 |

### S51 — Éprouver le parcours avant de le généraliser

Dans MiniRévisions, le scénario de création puis de retour à la liste est joué sur un prototype. Les hésitations de ce récit sont fictives et ne constituent pas une observation de vraie personne.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, parcours |
| Responsable | coordinateur_fictif |
| Action | Choisir un prototype proportionné et examiner la réussite d’une tâche, puis proposer les corrections utiles. |
| Sortie | prototype |
| Preuve | S51:epreuve_usage, S51:decision_ux — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S90 |

### S60 — Lever une inconnue technique déterminante

Le cadrage fictif ne relève pas de risque technique déterminant : S60 est notée non applicable avec référence au cadrage, sans inventer un spike réussi.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre |
| Responsable | coordinateur_fictif |
| Action | Activer un spike borné dès qu’un risque déterminant apparaît, y compris avant le cadrage détaillé du MVP. |
| Sortie | Aucun livrable de spike ; justification de non-applicabilité |
| Preuve | S00:cadre_decide — illustration uniquement |
| Validation | non_applicable dans la simulation ; aucune validation réelle |
| Destination | S61 |

### S61 — Choisir une architecture suffisante

Le cas fictif choisit une application locale au navigateur pour une seule personne. La limite de stockage local et l’absence de synchronisation sont rendues visibles ; ce choix ne prétend pas convenir à tous les projets.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp |
| Responsable | coordinateur_fictif |
| Action | Décider comment réaliser le parcours avec les moyens disponibles, en réutilisant l’existant si possible. |
| Sortie | architecture |
| Preuve | S61:choix_trace, S61:architecture_acceptee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S70 |

### S70 — Faire fonctionner le socle réel

Les commandes et l’URL mentionnées dans le récit MiniRévisions sont des emplacements illustratifs ; aucun build ni déploiement de cette application n’est prétendu.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, architecture |
| Responsable | coordinateur_fictif |
| Action | Préparer un dépôt et un environnement reproductibles, puis vérifier un chemin technique minimal et sa livraison de préproduction. |
| Sortie | socle |
| Preuve | S70:socle_execute, S70:preproduction_socle — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S71 |

### S71 — Conserver le contexte réellement vérifié

Le contexte fictif indique le parcours local, les commandes du socle et les exclusions du MVP ; il reste un exemple de rédaction et non une mémoire d’application installée.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, architecture, socle |
| Responsable | coordinateur_fictif |
| Action | Transmettre aux outils IA les conventions, commandes et limites réellement présentes, en liant les sources propriétaires. |
| Sortie | memoire |
| Preuve | S71:contexte_lisible — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S90 |

### S80 — Préparer une prochaine tranche vérifiable

Une seule story fictive décrit création et relecture persistante d’une fiche. L’exemple évite des epics et une spec séparée lorsqu’ils n’ajoutent aucune précision.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp |
| Responsable | coordinateur_fictif |
| Action | Activer la gestion du backlog et formaliser surtout la prochaine petite livraison utile. |
| Sortie | tranche |
| Preuve | S80:demande_prete, S80:priorite_decidee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S90 |

### S90 — Livrer une tranche avec le SDLC natif

La requête fictive commence par interactive et cite la story creer-et-retrouver-une-fiche.md. Les journaux et la revue décrits sont illustratifs ; l’application n’a pas été construite dans ce dossier.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, architecture, socle, memoire, tranche |
| Responsable | coordinateur_fictif |
| Action | Passer une demande prête au SDLC avec le mode explicitement encodé ; laisser sa boucle interne cadrer, réaliser, vérifier et revoir. |
| Sortie | candidat |
| Preuve | S90:controles_candidat, S90:revue_independante, S90:resultat_accepte — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S91 |

### S91 — Intégrer le candidat et vérifier la préproduction

Le récit fictif relie une révision de candidat à une révision intégrée et à une adresse de préproduction. Ces identifiants restent des exemples, pas une vraie fusion.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, candidat, socle |
| Responsable | porteur_fictif |
| Action | Fermer explicitement le passage entre candidat revu et version intégrée réellement disponible pour la recette. |
| Sortie | integration |
| Preuve | S91:autorisation_integration, S91:integration_constatee, S91:candidat_preproduction — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S100 |

### S100 — Vérifier le MVP intégré et décider sa préparation

La recette fictive couvre création, titre vide et relecture après rechargement. Le scénario décrit les preuves qui seraient requises ; il ne prétend pas que ces tests ont été exécutés sur MiniRévisions.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, integration |
| Responsable | coordinateur_fictif |
| Action | Vérifier le parcours complet sur le candidat intégré et préparer une décision d’ouverture fondée sur des preuves. |
| Sortie | recette |
| Preuve | S100:parcours_integre, S100:usage_qualifie, S100:recette_acceptee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S111 |

### S110 — Préparer l’ouverture, le support et la mesure

MiniRévisions prévoit un usage privé par le porteur fictif. Une campagne marketing et des emails ne sont donc pas requis ; le plan conserve support et observation de la tâche.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, brief, mvp |
| Responsable | coordinateur_fictif |
| Action | Préparer suffisamment tôt la première population, le message et la boucle de retours, sans publier avant l’autorisation et la recette. |
| Sortie | ouverture |
| Preuve | S110:preparation_ouverture, S110:cadre_ouverture_accepte — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S111 |

### S111 — Déployer puis contrôler l’adresse réellement livrée

Le cas d’école indique une adresse finale et un contrôle attendus. Aucune URL publique, aucun tag ni déploiement réel n’est créé pour cet exemple.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, integration, recette, ouverture |
| Responsable | porteur_fictif |
| Action | Utiliser le mécanisme réel de livraison autorisé, puis vérifier la version et le parcours sur son adresse finale. |
| Sortie | deploiement |
| Preuve | S111:livraison_executee, S111:adresse_finale — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S112 |

### S112 — Ouvrir l’accès à la première population

La livraison fictive concerne seulement le porteur. Le statut de MVP livré du récit n’est pas une affirmation de livraison réelle de l’application.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, ouverture, deploiement |
| Responsable | porteur_fictif |
| Action | Ouvrir dans le périmètre autorisé et constater que la première population dispose du parcours, du support et de la mesure. |
| Sortie | acces |
| Preuve | S112:population_acces, S112:premier_parcours, S112:mesure_operationnelle — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S120 |

### S120 — Observer les usages sur la fenêtre prévue

Les observations finales du récit sont fictives. Un encadré montre aussi le cas où la fenêtre n’est pas terminée : S120 reste en attente_info, sans créer une amélioration arbitraire.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, mvp, ouverture, acces |
| Responsable | coordinateur_fictif |
| Action | Recueillir les observations nécessaires et attendre explicitement quand il manque une donnée, un accès ou le recul prévu. |
| Sortie | observations |
| Preuve | S120:usage_date, S120:limites_mesure — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | S121 |

### S121 — Décider de la prochaine priorité ou de l’arrêt

Le cas d’école choisit fictivement de stabiliser la version personnelle et de reporter le partage. Cette décision illustre un raisonnement ; elle ne démontre aucun résultat de marché.

| Rubrique | Dans le cas d’école |
| --- | --- |
| Entrée | cadre, brief, mvp, observations |
| Responsable | coordinateur_fictif |
| Action | Comparer les faits à la promesse et aux critères, puis faire choisir une seule réponse utile au porteur. |
| Sortie | suite |
| Preuve | S121:bilan_trace, S121:suite_decidee — illustration uniquement |
| Validation | valide dans la simulation ; aucune validation réelle |
| Destination | END |

## Variantes à comprendre

- Si un test de code échoue à S90, conserver la séquence et réparer dans Deliver ; ne pas retourner arbitrairement au backlog.
- Si la fenêtre d’observation n’est pas terminée, S120 reste en `attente_info` avec le manque nommé.
- Si le MVP change de version, les séquences qui utilisaient l’ancienne version sont à réexaminer ; la note d’intention ne devient pas automatiquement fausse.
- Si le projet n’a pas d’interface graphique, tracer les non-applicabilités S50 et S51 à partir du cadrage approuvé.
- Si seule une PR en brouillon existe, S91 reste à faire et S100 ne peut pas être déclarée validée.

L’instance [examples/minirevisions.etat.json](examples/minirevisions.etat.json) illustre la structure de reprise. Un contrôle de cohérence de cet exemple ne prouve ni une livraison réelle ni la facilité du parcours pour un novice.

## Livrables remplis

Lire les [notes et contrats renseignés](examples/minirevisions/livrables.md) : intention, périmètre avec critères, demande prête, différence entre sortie et preuve, puis reprise en attente.
