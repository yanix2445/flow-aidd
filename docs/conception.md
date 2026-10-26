# Fonctionnement de flow-aidd

**Prototype local non installé.** Choix confirmés : nom `flow-aidd` et accompagnement guidé dans Codex avec les fichiers de suivi du projet.

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

Le modèle unique [workflow.json](../skills/flow-aidd/references/workflow.json) définit les 12 phases et 20 séquences. Les fiches, le glossaire, les exemples et Mermaid sont générés depuis cette source.

AIDD conserve ses artefacts et pipelines natifs. Le SDLC conduit sa propre boucle, avec son préfixe `interactive` ; flow-aidd ne lance pas une seconde chaîne parallèle. Marketing, Interfaces et Impeccable interviennent lorsque la séquence le justifie. Une référence de skill n’établit ni installation ni connexion.

## Ce qui appartient au plugin et au produit

| Propriétaire | Contenu |
| --- | --- |
| Plugin | Modèle, fiches, gabarits, exemples, instructions, helpers, identité visuelle et hooks. |
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

1. Lire `status` et la fiche courante.
2. Conduire le travail, conserver acteurs, contexte, sources, preuves et résultat natif avec `record`.
3. Contrôler les critères et les versions. Une preuve simulée ne valide jamais une instance réelle.
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

`hooks/hooks.json` déclare SessionStart, PostToolUse, Stop et Interrupt. Le handler recherche un projet déjà initialisé en remontant depuis le dossier de l’événement, sans traverser la frontière d’un autre dépôt.

Il fournit un rappel à la reprise et actualise la vue lorsque nécessaire. Il n’initialise pas de produit, n’infère aucun accord depuis un transcript, ne démarre pas de serveur et ne provoque aucune continuation.

Le handler est testé hors de Codex sur des données synthétiques. Son déclenchement natif reste à éprouver après installation et revue de confiance. La [documentation OpenAI](https://developers.openai.com/plugins/build/plugins) précise que les hooks ne sont pas automatiquement approuvés à l’installation et excluent actuellement l’annuaire public.

## Identité et distribution

Le dépôt est directement le paquet : `plugin.json`, `skills/flow-aidd/` et `hooks/`. Le catalogue `.agents/plugins/marketplace.json` pointe sur cette racine. Une seule icône SVG sert au manifeste et au skill.

`tools/release.py --output CHEMIN_EXTERIEUR.zip` produit un ZIP autonome avec manifeste, catalogue, runtime, références, hooks et documentation. Il exclut les outils de développement et refuse une archive dans le dépôt ou l’écrasement d’un fichier existant.

L’installation demeure reportée. Lorsqu’elle sera demandée :

```sh
codex plugin marketplace add /chemin/vers/flow-aidd --json
codex plugin add flow-aidd@flow-aidd-local --json
```

Codex gère son cache. Installation, activation, présence du skill et confiance dans les hooks seront vérifiées séparément dans une nouvelle session. Les autres plugins et leurs connexions restent gérés séparément.

## Limites de ce prototype

Les helpers contrôlent la structure déclarée et les fichiers locaux. Ils ne certifient pas la vérité d’un entretien, un service distant, une identité humaine ou le résultat d’un skill tiers.

L’ensemble du parcours n’a pas encore été appliqué à un vrai produit dans Codex. Cet essai, l’accueil natif, l’affichage des métadonnées et les hooks restent à vérifier lors de l’installation future. Les preuves déjà obtenues et leurs limites sont dans [verification.md](verification.md).
