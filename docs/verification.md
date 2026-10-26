# Vérifications de flow-aidd

Constat du 26 octobre 2026. **flow-aidd 0.2.1 installé et activé**, testé avec Codex CLI `0.164.0-alpha.11.1`.

## Organisation

- Un seul manifeste `.codex-plugin/plugin.json`, un seul skill et un seul `workflow.json`.
- 51 vues générées sous `skills/flow-aidd/references/`, sans copie à la racine.
- Helpers, références et identité visuelle dans `skills/flow-aidd/` ; événements dans `hooks/` ; outils de développement dans `tools/`.
- Le guidage se fait dans Codex avec les fichiers du projet. Le paquet ne fournit aucune interface web et n’exige aucun serveur local.
- Aucun dossier `plugin-src/` ou `plugins/` et aucun suivi produit `.flow/` dans ce dépôt.
- La génération préserve le README d’accueil. L’export refuse une distribution interne au dépôt.

## Contrôles

Les vérifications de génération et de tests passent par des jobs Portly.

- Job `tmp_ea08842a` : contrôle final des 51 vues sans divergence et **68 tests réussis**, avec le manifeste de compatibilité et l’accueil corrigés.
- Les tests des hooks sont dans `tools/test_hooks.py`. Les tests HTTP ont été retirés avec l’interface web.
- Le serveur de l’interface a été arrêté, puis sa configuration et son projet Portly vide ont été retirés. Aucun serveur du plugin ne reste enregistré.
- La recherche dans le paquet, les outils et la documentation ne relève aucune référence à l’ancienne interface ni à son adresse locale.

Les tests du modèle et des helpers couvrent contrats, routage, initialisation, isolation des projets, versions, reprise dans un autre processus, accord lié au point et à sa révision, contenu modifié, doubles accords, correction, déplacement et migration.

Les tests de hooks sont conservés séparément : aucun produit créé au démarrage, aucun accord déduit d’un transcript, aucune continuation à Stop ou Interrupt, frontière de dépôt respectée.

L’export est testé par vérification de l’archive, extraction dans un autre dossier, exécution du helper extrait et génération du suivi.

Les 21 schémas avaient été parsés et rendus avec Mermaid 10.9.5 après simplification. Le graphe et les contrats des séquences restent inchangés ; les vues sont contrôlées après régénération.

Le validateur officiel de skills avait retourné `Skill is valid!`. Sa dépendance PyYAML avait été utilisée dans un environnement temporaire supprimé après validation.

## Intégration native

Les essais utilisent des processus neufs et des conversations éphémères, sur un dossier temporaire distinct de ce dépôt. Ils ne conduisent aucun vrai produit et ne créent aucune conversation persistante de démonstration.

### Installation et découverte

Le catalogue `flow-aidd-local` a été enregistré avec `codex plugin marketplace add`, puis le paquet avec `codex plugin add flow-aidd@flow-aidd-local --json`. `codex plugin list --marketplace flow-aidd-local --json` confirme `installed: true` et `enabled: true`.

Le catalogue enregistré pointe vers `~/.codex/plugins/sources/flow-aidd-local-0.2.1`, extrait du ZIP. Codex a installé le paquet sous `~/.codex/plugins/cache/flow-aidd-local/flow-aidd/0.2.1`. Ces emplacements sont des artefacts d’installation ; la source à modifier reste ce dépôt.

Le paquet et son cache contiennent 65 fichiers, avec les seules entrées `.agents/`, `.codex-plugin/`, `README.md`, `docs/`, `hooks/` et `skills/`. L’installation directe depuis le dépôt copiait également `.git/`, `tools/` et `.DS_Store` ; cet essai a été remplacé par l’installation du ZIP propre.

Dans un app-server neuf :

- `skills/list` avec `forceReload: true` charge exactement un skill du plugin : `flow-aidd:flow-aidd`, activé, depuis son cache.
- `plugin/read` résout les métadonnées, les icônes et le skill d’accueil.
- `hooks/list` expose les quatre hooks, activés et `trusted` après la revue native réalisée par l’utilisateur ; job `tmp_4d066aa8`.

### Corrections de compatibilité

Avec cette version de Codex, `plugin/read` ne retournait aucun hook pour le manifeste portable à la racine : chemin simple, tableau de chemins, deux variantes inline et découverte du fichier par défaut ont été essayés. Le même paquet avec le seul manifeste de compatibilité `.codex-plugin/plugin.json` expose les quatre événements.

Le champ d’accueil au premier niveau de ce manifeste était également ignoré. Sa déclaration sous `extensions.com.openai.onboardingSkill` est effectivement résolue. Le champ `hooks` reste au premier niveau du manifeste de compatibilité.

Ce sont des constats sur le runtime installé, pas une affirmation que le format portable est invalide. Le [format de compatibilité reste officiellement pris en charge](https://developers.openai.com/plugins/build/plugins).

### Usage réel du skill installé

| Essai | Preuve observée |
| --- | --- |
| Expliquer S00 — `tmp_54f0095b` | Invocation `$flow-aidd` résolue, lecture du SKILL.md et des références dans le cache, aucun fichier créé. |
| Initialiser — `tmp_19ecda4b` | Helper installé exécuté : seulement `.flow/etat.json` et `.flow/suivi.md` ; S00 `a_faire`, révision 0, inconnues à `null`, aucune validation ni preuve inventée. |
| Reprendre — `tmp_05251fa9` | Nouveau processus après installation de 0.2.1 ; même identité, même révision, même séquence et état JSON identique octet pour octet. |

L’initialisation a d’abord été bloquée par l’accès à Portly depuis le sandbox CLI. Le test a été relancé avec le réglage limité à ce processus `sandbox_workspace_write.network_access=true` pour joindre Portly localement. Aucune configuration globale du sandbox n’a été changée.

### Déclenchement réel des hooks

Après la revue de confiance, le job `tmp_6eaaddc9` ouvre un thread natif éphémère via l’app-server, exécute un tour de lecture puis interrompt réellement un second tour. Les notifications natives `hook/completed` proviennent du fichier du plugin installé :

| Événement | Statut natif | Durée |
| --- | --- | --- |
| SessionStart | `completed` | 56 ms |
| PostToolUse | `completed` | 58 ms |
| Stop | `completed` | 94 ms |
| Interrupt | `completed` | 58 ms |

SessionStart a fourni le contexte `flow-aidd · project · S00 · a_faire.`. La vue de suivi, retirée dans le dossier d’essai avant l’exécution, a été restaurée par les hooks. L’état JSON est resté identique ; le premier tour est terminé, le second est interrompu. Aucune séquence supplémentaire ni décision n’a été créée.

Dans ce runtime, réinstaller le ZIP après actualisation de sa documentation a replacé les quatre hooks à `modified`, alors que leurs commandes et handlers étaient inchangés. La revue de confiance doit donc intervenir après la dernière synchronisation du paquet. Ne pas réinstaller le plugin après cette revue pour simplement actualiser un compte rendu.

## Conservation et limites

Une sauvegarde de **195 fichiers**, vérifiée par SHA-256 avant simplification, reste hors du dépôt :
[archive avant simplification](/Users/yanis/Developer/.flow-aidd-backups/2026-10-26-avant-simplification-9ec8932d.zip).

La réorganisation, les corrections et ce compte rendu sont conservés dans Git. Aucun dépôt distant n’est configuré et aucun push n’a été réalisé.

La résolution de l’accueil est vérifiée dans le runtime ; son bouton et la présentation graphique n’ont pas été testés visuellement dans l’application. Les essais de cycle de vie confirment cette fois le déclenchement natif des hooks, en complément des tests de handlers.

Aucun vrai produit n’a été conduit jusqu’au MVP. Les tests utilisent des projets synthétiques isolés et les exemples restent fictifs. Les scripts ne prouvent pas la vérité d’une observation, d’une identité humaine ou d’une preuve distante.
