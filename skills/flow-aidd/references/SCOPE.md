# Périmètre du flow

> Généré depuis `workflow.json`. Modifier la source puis reconstruire les vues.


**Objectif :** Guider un porteur de projet et son coordinateur IA d’une idée vague à un premier parcours utilisable, puis à une décision fondée sur les premiers usages.

**Point de départ :** Une intention, une difficulté ou un projet existant à reprendre.

**MVP livré :** Le premier MVP est livré à S112 lorsque la population prévue accède à la version vérifiée, accomplit la tâche centrale et peut remonter un problème.

**Fin de la première boucle :** La boucle initiale se termine à S121 par une décision justifiée ; elle peut rester en attente de données à S120 sans annuler la livraison du MVP.

## Projets concernés

- Petit produit numérique, application web, site, API ou outil en ligne de commande.
- Projet commercial, projet personnel ou projet d’apprentissage ; la profondeur est choisie à S00.
- Projet neuf ou existant : réutiliser un livrable actuel accompagné d’une preuve plutôt que le refaire.

## Profondeur et adaptation

- Commencer par une note courte et un parcours critique ; approfondir seulement si une décision, une dépendance ou un risque reste ambigu.
- Le nombre d’étapes est libre. Les séquences sont des unités de décision et de preuve, pas des cérémonies obligatoirement longues.
- Si un livrable équivalent existe, le relire, vérifier sa fraîcheur, enregistrer sa version et sa preuve, puis le réutiliser.
- S50 et S51 ne s’appliquent qu’à une interface graphique. S60 ne s’applique que lorsqu’un risque technique déterminant est identifié.
- Le contexte marketing détaillé, les personas B2B, la tarification et les epics sont conditionnels à leur utilité ; ne pas employer tous les plugins par principe.

## Limites

- Les règles décrivent une conduite de projet ; les scripts locaux contrôlent des fichiers et suggèrent la prochaine action.
- Le moteur de séquences ne lance aucun skill, agent, déploiement, fusion, campagne ou automatisation. Le guidage se fait dans Codex, avec les fichiers de suivi du projet.
- La syntaxe des appels et les droits se vérifient dans les capacités réellement disponibles au moment d’agir.
- Les exigences particulières d’un domaine sensible demandent un cadrage spécifique ; ce guide ne les certifie pas.

## Responsabilités

- **porteur** — Personne qui porte le projet. Elle décide du besoin, du périmètre, des risques acceptés et de l’ouverture aux utilisateurs.
- **coordinateur** — IA ou personne qui conduit la séquence, choisit les capacités, conserve l’état et propose la prochaine action.
- **verificateur** — Personne ou capacité qui contrôle une preuve technique. Un contrôle automatisé ne remplace pas une décision produit.
- **relecteur** — Relecteur distinct de l’implémentation lorsque l’indépendance est exigée, notamment le checker natif du SDLC.
- **integration** — Responsable de l’intégration identifié avant S91 selon la politique du dépôt ; son attribution peut rester une inconnue prévue pendant l’idéation.
- **exploitation** — Responsable de la livraison et du support initial identifié avant S110 ; son nom ne vaut pas autorisation de publication.

## Informations à préciser progressivement

Une inconnue peut rester ouverte pendant l’idéation. Le coordinateur aide à la résoudre au plus tard avant la séquence qui l’utilise ; il ne transforme pas une inconnue en réponse négative.

- Type de produit à réaliser ou reprendre. À résoudre avant : S40.
- Le projet possède-t-il une interface graphique à concevoir ou vérifier ? À résoudre avant : S40.
- Un risque technique déterminant bloque-t-il une décision ? Une inconnue reste null. À résoudre avant : S61.
- Une viabilité commerciale est-elle recherchée ? À résoudre avant : S30.
- Un public externe est-il visé par cette première version ? À résoudre avant : S20.
- Un dépôt existe-t-il déjà ? À résoudre avant : S70.
- Identité du responsable de l’intégration. À résoudre avant : S91.
- Identité du responsable de la livraison et du support initial. À résoudre avant : S110.
