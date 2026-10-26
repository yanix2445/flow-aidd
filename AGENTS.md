# Travailler dans flow-aidd

Ce dépôt est directement le plugin, pas un projet produit à initialiser.

- Lire README.md pour les repères et docs/conception.md pour le contrat de fonctionnement.
- Le plugin est constitué de plugin.json, skills/flow-aidd/ et hooks/. Il n’existe pas de copie de distribution à entretenir.
- Le guidage se fait dans Codex et les fichiers du projet. Le plugin ne fournit aucune interface web ni serveur local.
- Modifier le modèle unique dans skills/flow-aidd/references/workflow.json pour les séquences, rôles, règles, preuves et exemples. Régénérer les vues sur place avec python3 -B tools/build.py ; ne pas modifier manuellement les fiches générées.
- Les instructions et le helper sont directement dans skills/flow-aidd/. Les outils de développement restent dans tools/.
- Le mode choisi est guidé : une séquence à la fois, avec accord avant la suite. Une proposition de destination n’est pas un accord de passage.
- L’installation et l’activation dans Codex exigent une demande explicite. Les essais d’intégration utilisent un projet temporaire distinct de ce dépôt.
- Une explication, une conception ou une modification du plugin n’autorise pas l’exécution d’un produit, une fusion, un déploiement ou une prise de contact.
- Pour appliquer le flow, lire les consignes et l’état du produit ciblé, la conduite embarquée et la seule fiche utile. Vérifier la disponibilité réelle des skills nécessaires et lire leurs SKILL.md avant emploi.
- Le coordinateur conserve les décisions, versions, preuves et attentes dans le produit. Les exemples restent fictifs et ne fournissent aucune preuve réelle.
- Le SDLC natif conserve sa boucle interne ; respecter sa syntaxe courante et le préfixe exact interactive prévu dans le modèle.
- Les versions antérieures ont été sauvegardées hors du dépôt avant simplification ; voir docs/verification.md. Ne pas réintroduire leurs copies dans l’arborescence active.

<!-- portly:managed-rule:start -->
## Development servers

- Always use Portly (`portly ...`) to start, stop, restart, inspect, or keep local development servers running.
- Start with `portly status`. Use `portly status --details` only for the full inventory and metrics, and `--json` only for machine-readable fields. Reuse a healthy managed server; if an in-scope server is running outside Portly, register it and use `portly take-over <project/server> --json`.
- For long-lived or reusable work, create a project and server.
- For builds, tests, code generation, previews, demos, and other bounded one-off work, run `job_id="$(portly temp '<command>' --path <folder> --timeout 30m)"`, then `portly wait "$job_id"`. `temp` returns immediately with an ID; `wait` prints captured logs and exits with the command's real code. A timeout kills the whole process group and exits with code `124`.
- Never launch persistent development servers directly, in the background, or through another supervisor.
<!-- portly:managed-rule:end -->
