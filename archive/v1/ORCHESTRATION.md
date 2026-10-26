# Conduire le parcours avec les plugins

Cette convention est une proposition pour ce dossier. Elle n’ajoute aucun skill, hook ou agent aux plugins installés et n’exécute aucune action en arrière-plan.

## Le principe de conduite

À chaque séance : **lire l’état → identifier la décision ou le résultat suivant → choisir une capacité responsable → produire le livrable → vérifier → consigner la suite**.

Le coordinateur tient le fil du projet et choisit les bons outils. Il ne redéfinit pas les règles de chaque skill. Il lit le `SKILL.md`, puis la référence ou l’action utile avant de l’exécuter. Les noms cités ici sont des identifiants vérifiés de skills ; les prompts peuvent les demander en langage naturel, sans supposer une commande globale de workflow.

## Trois niveaux de coordination

| Niveau | Responsable | Résultat |
| --- | --- | --- |
| Projet | Toi avec un coordinateur qui lit ce guide | Prochaine décision utile, cohérence entre phases et preuves. |
| Backlog | `aidd-orchestrator:02-backlog` | Demandes cohérentes, ordonnées et suffisamment prêtes. |
| Changement | `aidd-orchestrator:01-sdlc` | Contrat → plan → réalisation vérifiée → revue indépendante → PR en brouillon. |

SDLC ne remplace pas la découverte du marché, la conception de l’expérience ou la livraison en production. Une PR en brouillon n’est ni une fusion, ni un déploiement, ni une validation du produit par ses utilisateurs.

Pour apprendre et garder une lecture du travail, demander **le mode interactif** du SDLC. Il prévoit une pause sur le contrat, une sur le plan et une sur le résultat. Le mode par défaut documenté est `auto` ; il peut commiter et pousser le candidat puis ouvrir la PR. Le choisir suppose que ce périmètre est voulu. Dans les deux modes, lire les règles en vigueur avant l’exécution.

## Une seule capacité propriétaire par résultat

| Besoin immédiat | Capacité responsable | Frontière à respecter |
| --- | --- | --- |
| L’idée reste confuse | `aidd-refine:01-brainstorm` | Clarifie ; ne produit ni plan technique ni code. |
| Cadrer l’opportunité et sa validation | `aidd-pm:06-product-brief` | Le Brief n’est pas un PRD. |
| Définir quoi construire et pourquoi | `aidd-pm:03-prd` | Le PRD n’est ni un plan technique ni une liste de stories. |
| Rechercher un besoin réel | `marketing-skills:customer-research` | Distingue preuves, proxys et hypothèses ; ne fabrique pas de personas. |
| Poser la cible et le positionnement partagés | `marketing-skills:product-marketing` | Contexte marketing provisoire avant les autres skills marketing ; enrichissement au fil de la recherche. |
| Concevoir le parcours et sa direction | `impeccable:impeccable`, commandes `init` puis `shape` | `shape` retourne un brief confirmé sans code ; la construction vient ensuite. |
| Examiner l’interface dans son ensemble | `interfaces:better-interface` | Revue appuyée sur les skills de domaine et des preuves ; une revue seule ne modifie pas la source. |
| Choisir l’architecture d’un nouveau SaaS | `aidd-context:01-bootstrap` | Produit `aidd_docs/INSTALL.md` ; ne crée pas le scaffold. |
| Lever une inconnue précise | `aidd-pm:05-spike` | Question bornée, preuve et condition d’arrêt ; pas une recherche infinie. |
| Rendre une demande livrable | `aidd-pm:02-user-stories`, éventuellement `aidd-pm:04-spec` | Critères observables ; pas d’explication de l’implémentation dans la spec. Une spec validée est verrouillée. |
| Planifier une réalisation | `aidd-dev:01-plan` | Explore le code et décrit comment livrer un résultat déjà cadré. |
| Exécuter un plan existant | `aidd-dev:02-implement` | Ne remplace pas le cadrage ; commits locaux par tâche validée par défaut. |
| Vérifier et réparer la réalisation | `aidd-dev:03-assert` | Exécute les assertions ; ne remplace pas l’écriture des tests. |
| Écrire des tests ou parcourir le produit | `aidd-dev:06-test` | Vérification développeur ; ne pas la présenter comme une recette indépendante ou une preuve utilisateur. |
| Revoir le changement | `aidd-dev:05-review` | Revue statique, distincte de l’implémentation et de l’exécution des parcours. |
| Challenger le résultat | `aidd-refine:02-challenge` | Compare le travail et la référence convenue ; peut conclure que le résultat doit être simplifié. |
| Créer une PR | `aidd-vcs:02-pull-request` | Toujours en brouillon ; ne crée ni commit, ni push, ni fusion. Le candidat doit être prêt. |
| Préparer une ouverture aux utilisateurs | `marketing-skills:launch` | Stratégie et préparation ; le déploiement utilise les outils de l’hébergeur. |

Quand SDLC pilote une tranche, les capacités de plan, implémentation, assertions, tests, revue, challenge, commit et PR sont ses sous-étapes. **Ne pas lancer une deuxième chaîne identique à côté.** Le SDLC documenté isole exécution et contrôle dans des agents dédiés ; préserver cette indépendance lors de son exécution.

## Les preuves de passage

Chaque phase se termine par un résultat vérifiable, pas seulement par un fichier créé. Il y a quatre issues possibles :

- **Poursuivre** : le critère est satisfait et la prochaine étape est utile.
- **Reprendre** : un manque empêche la décision ; revenir à la phase concernée.
- **Réduire ou réorienter** : la preuve remet en cause la cible, la promesse ou le périmètre.
- **Arrêter** : les faits ou les moyens ne justifient plus la poursuite.

Une hypothèse peut rester ouverte si son effet et le risque accepté sont visibles. Ne pas traduire « document rédigé » par « besoin validé », « tests verts » par « expérience compréhensible », ou « produit publié » par « valeur démontrée ».

Les phases 5, 6 et 8 peuvent démarrer après la phase 4. Les fondations dépendent des décisions techniques. Une tranche produit attend un cadrage UX suffisant, un socle opérationnel et une demande prête. Les risques majeurs et les préparatifs d’acquisition peuvent être traités plus tôt : l’ordre protège les dépendances, il n’impose pas un cycle rigide.

## L’état minimal d’une séance

Le modèle suivant est une convention proposée, à remplir pour un vrai projet. Il n’est pas un statut natif AIDD et ne remplace pas les statuts internes des plans, stories ou autres artefacts.

```markdown
# État du projet

- Résultat recherché :
- Phase / sous-phase en cours :
- Sources approuvées à lire :
- Faits et preuves disponibles :
- Décisions approuvées :
- Hypothèses et inconnues restantes :
- Livrable de la séance et preuve de vérification :
- Critère de passage : satisfait / à reprendre / risque accepté
- Décision à prendre, si nécessaire :
- Prochaine action utile et skill responsable :
```

Au début d’une reprise, lire cet état et les sources avant de poser des questions. Ne pas rouvrir les choix approuvés sans un fait nouveau. Ne pas prétendre qu’une source a été validée si elle n’a pas été lue ou si la preuve date d’un autre candidat.

## Sources et documents sans doublons

| Information | Source propriétaire recommandée |
| --- | --- |
| Observation, entretien, retour, preuve | Note de recherche avec source, date et limites. Emplacement à convenir. |
| Opportunité et validation | Product Brief produit par le skill PM ; laisser le skill résoudre son chemin natif. |
| Cible, promesse, langage, positionnement | `.agents/product-marketing.md`, contexte Marketing Skills versionné. |
| Périmètre et exigences | PRD ; le skill installé enregistre dans `aidd_docs/tasks/<yyyy_mm>/<yyyy_mm_dd>-<feature_name>-prd.md`. |
| Contexte du produit pour le design | `PRODUCT.md`, synthèse dérivée et liée aux décisions approuvées du Brief et du PRD. |
| Direction d’interface | `DESIGN.md` et briefs de surfaces Impeccable selon le workflow du plugin. |
| Architecture et installation d’un nouveau SaaS | `aidd_docs/INSTALL.md` produit par bootstrap. |
| Règles et contexte du code existant | Mémoire projet AIDD, aux emplacements que le skill courant résout. |
| Demandes, contrats et plans de livraison | Artefacts natifs PM / Dev ; ne pas inventer un second backlog concurrent. |
| Résultats de validation | Rapports et preuves reliés au candidat exact, avec ce qui n’a pas été vérifié. |
| Fil de conduite du projet | Une note d’état sur le modèle ci-dessus, sans recopier toutes les sources. |

Ne pas précréer tous ces documents vides. Les produire à la phase utile et respecter les règles de persistance du skill. Une approbation de contenu et l’autorisation de le sauvegarder peuvent être distinctes dans les skills PM ; une autorisation bornée explicite peut aussi permettre cette sauvegarde. Ne pas demander deux fois une autorisation déjà donnée.

## Ce qui reste conditionnel

Un projet personnel n’impose pas tarification ou personas B2B. Une petite application ne demande pas une architecture distribuée, un système de design exhaustif ou un epic par écran. Paiement, authentification, intégrations, exigences réglementaires et tests spécialisés entrent dans le parcours lorsqu’ils découlent du produit réel.

Les plugins cités ne fournissent pas à eux seuls une plateforme universelle de déploiement, de recherche terrain ou d’analytics. Utiliser les outils réels disponibles ; signaler un accès absent au lieu de simuler le résultat. Les prises de contact, messages, campagnes, dépenses et publications externes suivent le périmètre expressément autorisé.

Pour les travaux locaux, commencer par `portly status`, réutiliser un serveur sain et gérer les serveurs avec Portly. Builds, tests, génération et previews bornés passent par `portly temp` puis `portly wait`. Aucun serveur permanent ne doit être lancé directement.

## Point de fin du premier MVP

Le premier MVP est livré quand une première population peut accomplir le parcours choisi sur la version accessible prévue, que les états essentiels et les problèmes connus sont traités à un niveau acceptable, et que le support et la mesure permettent d’apprendre. Il n’a pas à couvrir toute la vision du produit.

La phase 12 conclut la première boucle d’apprentissage. Elle peut rester **indécidable** tant que la fenêtre d’usage ou les retours manquent. Cela ne rend pas rétroactivement le produit non livré ; cela empêche seulement de prétendre que sa valeur est démontrée.
