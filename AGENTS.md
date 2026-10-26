# Travailler dans ce dépôt

Ce dépôt contient un modèle de conduite de projet. Une demande d’explication ou de modification du modèle n’autorise pas l’exécution d’un produit, une fusion, un déploiement ou une prise de contact.

- Pour maintenir le flow, modifier `workflow.json`, seule source propriétaire des séquences, règles, rôles, conditions, preuves, glossaire et exemples. Régénérer les vues avec `python3 scripts/flow.py build`, puis contrôler leur cohérence.
- Pour appliquer le flow à un projet, lire `README.md`, `ORCHESTRATION.md`, son fichier `.flow/etat.json` et la seule fiche de séquence utile dans `sequences/`. Ne pas charger tous les guides et tous les skills par défaut.
- Le coordinateur conserve l’état après une décision, un contrôle significatif, un livrable versionné et avant interruption. Les preuves citent leur source et la bonne version ; ne pas transformer une hypothèse ou une illustration en fait.
- Lire le SKILL.md courant avant d’activer une capacité. La présence d’un identifiant dans ce modèle ne prouve ni chargement, ni activation, ni connexion du plugin.
- Réutiliser une autorisation bornée déjà donnée. Une nouvelle décision produit revient au porteur ; une autorisation manque seulement lorsqu’elle est nécessaire à l’action concrète suivante.
- Le SDLC possède sa boucle interne. Sa requête interactive commence exactement par `interactive`, avec une source concrète. Ne pas lancer une deuxième boucle de développement à côté.
- Les instances sous `examples/` sont fictives. Le mode `illustration` et les preuves `simulated: true` ne sont jamais des preuves réelles.
- `archive/v1/` conserve la version précédente et son audit. Ne pas la modifier pour faire passer les contrôles de la version actuelle.

<!-- portly:managed-rule:start -->
## Development servers

- Always use Portly (`portly ...`) to start, stop, restart, inspect, or keep local development servers running.
- Start with `portly status`. Use `portly status --details` only for the full inventory and metrics, and `--json` only for machine-readable fields. Reuse a healthy managed server; if an in-scope server is running outside Portly, register it and use `portly take-over <project/server> --json`.
- For long-lived or reusable work, create a project and server.
- For builds, tests, code generation, previews, demos, and other bounded one-off work, run `job_id="$(portly temp '<command>' --path <folder> --timeout 30m)"`, then `portly wait "$job_id"`. `temp` returns immediately with an ID; `wait` prints captured logs and exits with the command's real code. A timeout kills the whole process group and exits with code `124`.
- Never launch persistent development servers directly, in the background, or through another supervisor.
<!-- portly:managed-rule:end -->
