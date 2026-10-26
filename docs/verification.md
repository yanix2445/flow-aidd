# Vérifications de flow-aidd

Constat du 26 octobre 2026. Paquet local 0.2.0, **non installé dans Codex**.

## Organisation

- Un seul `plugin.json`, un seul skill et un seul `workflow.json`.
- 51 vues générées sous `skills/flow-aidd/references/`, sans copie à la racine.
- Helpers, références et identité visuelle dans `skills/flow-aidd/` ; événements dans `hooks/` ; outils de développement dans `tools/`.
- Le guidage se fait dans Codex avec les fichiers du projet. Le paquet ne fournit aucune interface web et n’exige aucun serveur local.
- Aucun dossier `plugin-src/` ou `plugins/` et aucun suivi produit `.flow/` dans ce dépôt.
- La génération préserve le README d’accueil. L’export refuse une distribution interne au dépôt.

## Contrôles

Les vérifications de génération et de tests passent par des jobs Portly.

- Job `tmp_d963e5a8` : régénération des 51 vues, contrôle sans divergence et **68 tests réussis**.
- Les tests des hooks sont dans `tools/test_hooks.py`. Les tests HTTP ont été retirés avec l’interface web.
- Le serveur de l’interface a été arrêté, puis sa configuration et son projet Portly vide ont été retirés. Aucun serveur du plugin ne reste enregistré.
- La recherche dans le paquet, les outils et la documentation ne relève aucune référence à l’ancienne interface ni à son adresse locale.

Les tests du modèle et des helpers couvrent contrats, routage, initialisation, isolation des projets, versions, reprise dans un autre processus, accord lié au point et à sa révision, contenu modifié, doubles accords, correction, déplacement et migration.

Les tests de hooks sont conservés séparément : aucun produit créé au démarrage, aucun accord déduit d’un transcript, aucune continuation à Stop ou Interrupt, frontière de dépôt respectée.

L’export est testé par vérification de l’archive, extraction dans un autre dossier, exécution du helper extrait et génération du suivi.

Les 21 schémas avaient été parsés et rendus avec Mermaid 10.9.5 après simplification. Le graphe et les contrats des séquences restent inchangés ; les vues sont contrôlées après régénération.

Le validateur officiel de skills avait retourné `Skill is valid!`. Sa dépendance PyYAML avait été utilisée dans un environnement temporaire supprimé après validation.

## Conservation et limites

Une sauvegarde de **195 fichiers**, vérifiée par SHA-256 avant simplification, reste hors du dépôt :
[archive avant simplification](/Users/yanis/Developer/.flow-aidd-backups/2026-10-26-avant-simplification-9ec8932d.zip).

La réorganisation du paquet est conservée dans l’historique Git. Le catalogue local est déclaré sur disque ; cela n’établit pas son importation dans Codex.

L’accueil natif, la présentation dans Codex, le chargement du skill et la confiance dans les hooks restent à éprouver lors d’une installation future demandée. Les tests de handlers ne prouvent pas le déclenchement natif des hooks.

Aucun vrai produit n’a été conduit jusqu’au MVP. Les tests utilisent des projets synthétiques isolés et les exemples restent fictifs. Les scripts ne prouvent pas la vérité d’une observation, d’une identité humaine ou d’une preuve distante.
