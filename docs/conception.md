# Fonctionnement de flow-aidd

**Prototype local.** Choix confirmés : nom `flow-aidd` et accompagnement guidé dans Codex avec les fichiers de suivi du projet.

## Usage

Le porteur donne une idée, choisit de reprendre un projet ou demande une explication. Le coordinateur identifie le dossier, lit les consignes et le suivi, charge la seule fiche utile, puis conduit la séquence avec les capacités disponibles.

L’accueil réutilise le skill principal : choisir démarrer, reprendre ou explorer, sans initialiser un produit sur le seul fait d’installer le plugin. Les trois propositions de départ sont déclarées dans le manifeste. L’invocation implicite reste autorisée par le réglage natif par défaut ; le déclenchement est ciblé sur l’usage du flow.

| Demande | Effet |
| --- | --- |
| « Explique-moi le parcours. » | Lecture des références ; aucun produit initialisé. |
| « Démarre ici ; mon idée est… » | Création du suivi puis conduite de S00. |
| « Reprends ce projet. » | Contrôle des sources et reprise de la séquence ou de son attente. |
| « Où en est-on ? » | Consultation et prochaine proposition. |
| « Continue » après résultat et destination présentés | Conservation de l’accord réel puis une séquence supplémentaire. |
| « Change cette partie de l’idée. » | Réexamen des résultats affectés avec historique conservé. |

Un dossier suffit pour l’idéation. Le démarrage n’impose ni application, ni dépôt Git, ni backlog distant, ni hébergement.

## Responsabilités et sept rubriques

Chaque séquence décrit entrée, responsable, action, sortie, preuve, validation et prochaine destination. Son responsable conduit le travail ; son validateur contrôle le résultat ; le porteur confirme le passage.

Le modèle unique [workflow.json](../skills/flow-aidd/references/workflow.json) définit les 12 phases et 20 séquences. Les fiches, le parcours, le glossaire, les règles, les versions de secours des agents, et dans `docs/` les schémas et l’exemple, sont générés depuis cette source.

L’ordre suit celui que prévoient les plugins eux-mêmes. AIDD : brainstorm (S10), brief (S30), PRD (S40), stack (S61), mémoire du projet (S71), epic, stories et spec (S80), puis SDLC jusqu’à la PR en brouillon (S90) et intégration (S91). Impeccable : `init` et `shape` (S50), prototype et `critique` (S51), `shape` de chaque tranche (S80), `document` après l’interface réellement intégrée (S91), puis `audit`, `critique`, `harden`, `polish` et `document` (S100). marketing-skills : `product-marketing` avant tout autre skill (S20), puis recherche, offre, mesure, lancement et croissance (S20 à S121).

AIDD conserve ses artefacts et pipelines natifs. Le SDLC conduit sa propre boucle, avec son préfixe `interactive` ; flow-aidd ne lance pas une seconde chaîne parallèle. Impeccable est la capacité de design de référence et marketing-skills couvre le public, la promesse, la mesure et le lancement ; ils interviennent lorsque la séquence et sa condition le justifient, en alimentant les artefacts AIDD. Une capacité Impeccable peut nommer sa sous-commande (`shape`, `critique`, `audit`…).

Une capacité peut dépendre du contexte du projet (`if`, par exemple `public_users` ou `commercial`) ou d’une condition à juger au cas par cas (`if_text`). `status` et `next` renvoient `capabilities` pour la séquence de travail : `utiliser`, `selon_le_cas`, `a_confirmer` (réponse de contexte encore inconnue, avec sa question) et `ecartees` (avec la raison). Une inconnue ne vaut jamais « non » : elle laisse la capacité à confirmer. Les fiches regroupent les mêmes capacités par condition. Une référence de skill n’établit ni installation ni connexion.

## Organisation du skill

Le skill suit la structure d’Impeccable :

- **SKILL.md court** : trois principes, la mise en route, un tableau des commandes du helper avec leur référence, et les agents de contrôle.
- **Une référence par commande**, rédigée à la main : `init.md`, `status.md`, `record.md`, `checkpoint.md`, `rattacher.md`. Quatre références transversales : `socle.md` (relu avant chaque `record` et `checkpoint`), `entretien.md` (rythme des questions au porteur), `capacites.md` et `hooks.md`. Toutes suivent le même gabarit : but, contexte nécessaire, étapes avec les cas selon la situation, pannes fréquentes, avant de terminer.
- **Un chargeur de contexte** : `status` renvoie `load` (les seules références à lire maintenant), `directives` (les actions immédiates), `capabilities` (les skills triés pour ce projet) et `agents` (les contrôles à lancer avant le `checkpoint`). Le hook SessionStart transmet les mêmes consignes à la reprise.
- **Des agents pour les rôles indépendants** : `flow_aidd_verificateur` contrôle preuves, versions et critères ; `flow_aidd_relecteur` confronte le livrable à la promesse, au contrat du MVP et aux réponses du porteur. Ils ne modifient rien, sont lancés à neuf sans l’historique, et rendent un verdict. La clé `agents` de `workflow.json` dit avant quelles séquences les lancer ; S90 garde le relecteur natif du SDLC.
- **Vues générées utiles à l’action seulement** : `parcours.md` (carte, équivalent du routage), `glossaire.md` (termes et rôles), `regles.md` (rubriques, règles, statuts et boucles, pour le vérificateur et les cas de doute) et les fiches `sequences/`. La fiche S00 porte la section « Adapter la profondeur ». Les schémas Mermaid et l’exemple complet MiniRévisions, destinés aux humains, sont générés dans `docs/schemas/` et `docs/exemple/`, hors du skill installé ; chaque fiche garde son cas d’école.
- **Une version de secours par agent** : `references/degraded/*.md`, générée par `build.py` depuis `agents/*.toml`, sert uniquement quand aucun sous-agent n’est possible ; la substitution est dite au porteur.

## Ce qui appartient au plugin et au produit

| Propriétaire | Contenu |
| --- | --- |
| Plugin | Modèle, fiches, références, agents de contrôle, gabarits, helpers, identité visuelle et hooks ; schémas et exemple dans `docs/`. |
| Produit | Besoin, décisions, architecture, design, code, sources natives, preuves et avancement. |
| Environnement | Plugins disponibles, accès, secrets et règles d’exécution. |

Dans le produit :

```text
.flow/
├── etat.json   # Source structurée
├── suivi.md    # Vue dérivée, jamais une seconde source à maintenir
└── cadre.md    # Produit pendant S00, pas créé vide au démarrage
```

`init` crée les deux premiers fichiers avec S00 à faire, des inconnues ouvertes et aucune preuve ou validation acquise. Il préserve un état déjà présent. Les autres fichiers apparaissent quand leur séquence les nécessite. Le suivi référence les documents existants plutôt que de les dupliquer.

L’initialisation ne modifie pas AGENTS.md, .gitignore ou la configuration de Codex et ne crée aucun commit.

## État et passage guidé

`project_flow.py` est le point d’écriture. Le coordinateur prépare un correctif temporaire pour `record` ; le porteur n’édite pas le JSON.

L’état sépare `execution_mode: guide` du `mode: reel` ou `illustration`. Il conserve une identité stable, la provenance du modèle, le dossier, la révision, les résultats et l’historique.

1. Lire `status`, suivre ses `directives` et lire seulement les fichiers de `load`, dont la fiche courante.
2. Conduire le travail avec les capacités triées (`capabilities`) et l’entretien du porteur, conserver acteurs, contexte, sources, preuves et résultat natif avec `record`.
3. Contrôler les critères et les versions, puis lancer les agents de `agents` (vérificateur, et relecteur selon la séquence) ; un verdict à reprendre se corrige avant de continuer. Une preuve simulée ne valide jamais une instance réelle.
4. Créer `checkpoint` lorsque le contrat est satisfait : résumé présenté, destination, identifiant et empreinte du résultat. La séquence reste courante.
5. Le porteur confirme, corrige ou attend. `approve` avance d’une seule séquence ; `correct` conserve le retour et reprend le travail ; `pause` garde le point et son attente.
6. Poursuivre dans Codex. `focus` rejoint seulement le prérequis recommandé lorsque le travail courant nécessite un retour.

Les écritures utilisent une révision attendue et un verrou exclusif ; un second accord sur le même point échoue. L’état est remplacé atomiquement. La vue est produite sous le même verrou.

La décision produit native et l’accord de passage sont distincts. Si une même réponse réelle approuve explicitement les deux, sa source sert aux deux enregistrements sans poser deux fois la question. Une décision native manquante reste en attente, avec son objet conservé ; le coordinateur ne fabrique pas un accord pour rendre le point disponible.

## Versions, déplacement et migration

Les sources locales ont une empreinte calculée sur leur contenu. Un dossier déclare les fichiers suivis ; l’état du flow et les sorties de construction ne doivent pas se retrouver dans cette liste. Les liens distants conservent leur référence et version ; ils ne sont pas vérifiés automatiquement.

Un contenu changé reçoit une nouvelle version et entraîne le réexamen des validations dépendantes. Les anciens enregistrements restent dans l’historique. Un point présenté sur une ancienne version ne peut pas être approuvé.

Après déplacement ou clonage, `relocate` rattache explicitement l’instance au bon dossier, garde son identité et normalise ses chemins internes. Les fichiers modifiés ou manquants sont signalés.

`migration-plan` compare les contrats et règles du modèle. `migrate` conserve un instantané et réouvre les validations affectées. Un changement majeur de format est refusé et demande une migration dédiée. `adopt` rattache un ancien état compatible après examen de sa provenance ; une illustration reste une illustration.

## Hooks

`hooks/hooks.json` déclare SessionStart, PreToolUse, PostToolUse, Stop et Interrupt. Le handler recherche un projet déjà initialisé en remontant depuis le dossier de l’événement, sans traverser la frontière d’un autre dépôt. Chaque événement fait le minimum qui peut changer ce que le porteur ou le coordinateur doit savoir.

| Événement | Quand il agit | Effet |
| --- | --- | --- |
| SessionStart | Reprise d’un projet initialisé | Contexte pour le modèle : séquence, statut, attente ou point de passage, écarts à examiner, fiche à relire. |
| PreToolUse | Seulement si l’appel mentionne `.flow/` (filtre shell, sans Python sinon) | Refuse une écriture directe de `etat.json` ou `suivi.md` (édition, redirection, `sed -i`, `rm`, `mv`, copie vers ces fichiers) et donne la commande `record` à utiliser. Lectures, `cadre.md`, livrables et appels du helper passent. |
| PostToolUse | Édition (`Edit\|Write\|apply_patch`) d’un livrable suivi dont le contenu diffère de son enregistrement | Point de passage en attente : message au porteur, l’accord présenté ne peut plus s’appliquer. Livrable déjà validé : message au porteur et séquences à réexaminer. Travail en cours : simple rappel au modèle. |
| Stop, Interrupt | Fin ou interruption du tour | Régénère `suivi.md` seulement si l’état ou un livrable est plus récent que la vue. |

Un conseil n’est donné qu’une fois par livrable et par version enregistrée dans une séance : les retouches successives ne relancent pas le même message, un nouvel enregistrement le réarme. Cette mémoire de séance est rangée dans le dossier temporaire du système, jamais dans le produit. Un livrable revenu à son contenu enregistré ne produit aucun message. Les modifications faites par une commande shell sont prises en compte à Stop et à la reprise.

Il fournit un rappel à la reprise et actualise la vue lorsque nécessaire. Il n’initialise pas de produit, n’infère aucun accord depuis un transcript, ne démarre pas de serveur et ne provoque aucune continuation.

Le handler est testé hors de Codex sur des données synthétiques. La découverte et la confiance dans Codex sont contrôlées séparément du test de ce handler ; voir [verification.md](verification.md). La [documentation OpenAI](https://developers.openai.com/plugins/build/plugins) précise que les hooks ne sont pas automatiquement approuvés à l’installation et excluent actuellement l’annuaire public.

## Identité et distribution

Le dépôt contient un seul manifeste, `.codex-plugin/plugin.json`, le skill `skills/flow-aidd/` et `hooks/`. Le catalogue `.agents/plugins/marketplace.json` pointe sur cette racine. Une seule icône, `skills/flow-aidd/assets/icon.png` (PNG 96 × 96 à fond transparent : une flèche orange qui revient sur une grille de points bleus), sert au manifeste et au skill ; sa couleur dominante donne `brandColor` (#E9A21C).

Le format de compatibilité Codex est intentionnel : dans Codex 0.164.0-alpha.11.1, les variantes portables essayées chargent le skill mais ne déclarent aucun hook dans `plugin/read`. Le manifeste de compatibilité exposait bien les quatre événements alors déclarés ; PreToolUse, ajouté ensuite, reste à vérifier dans Codex. Ne pas ajouter un deuxième manifeste pour contourner ce constat.

`tools/release.py --output CHEMIN_EXTERIEUR.zip` produit un ZIP autonome avec manifeste, catalogue, runtime, références, hooks et documentation. Il exclut les outils de développement et refuse une archive dans le dépôt ou l’écrasement d’un fichier existant.

Deux installations sont possibles, toujours sur demande explicite. Depuis GitHub (`codex plugin marketplace add yanix2445/flow-aidd`), la plus simple, décrite dans le README ; ce qu’elle copie dans le cache de Codex n’a pas encore été vérifié. Depuis le ZIP extrait dans un dossier durable extérieur au dépôt, qui n’embarque que le paquet : lors des essais, une installation depuis le dossier du dépôt copiait aussi son historique Git et ses outils dans le cache de Codex.

```sh
codex plugin marketplace add /chemin/vers/le/paquet-extrait --json
codex plugin add flow-aidd@flow-aidd --json
```

Codex gère son cache. Installation, activation, présence du skill, accueil déclaré et confiance dans les hooks se vérifient séparément dans une nouvelle session. Le cache installé n’est pas une seconde source à modifier. Les autres plugins et leurs connexions restent gérés séparément.

## Limites de ce prototype

Les helpers contrôlent la structure déclarée et les fichiers locaux. Ils ne certifient pas la vérité d’un entretien, un service distant, une identité humaine ou le résultat d’un skill tiers.

L’ensemble du parcours n’a pas encore été appliqué à un vrai produit dans Codex. La découverte par le runtime, l’interaction visuelle de l’accueil et le déclenchement des hooks sont des contrôles distincts. Les preuves obtenues et leurs limites sont dans [verification.md](verification.md).
