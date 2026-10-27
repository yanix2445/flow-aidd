---
name: flow-aidd
description: Piloter ou reprendre un projet de l’idée au premier MVP avec le flow AIDD, ses séquences, décisions, preuves et état propre au projet. Utiliser lorsque l’utilisateur demande d’appliquer Flow AIDD, de connaître sa prochaine séquence ou de reprendre son avancement.
---

# Piloter avec Flow AIDD

Conduire la séquence utile avec le porteur du projet. Le flow embarqué est le modèle de référence ; les faits et décisions du produit restent dans le projet ciblé.

## Mode guidé

Conduire une seule séquence à la fois. À sa fin, présenter le résultat, les livrables, les preuves et la prochaine destination proposée, puis attendre l’accord du porteur avant d’exécuter une nouvelle séquence. Une demande de continuer s’applique à cette proposition présentée et au périmètre déjà autorisé.

La validation technique prévue par la fiche et l’accord de passage du porteur sont distincts. Conserver l’attente d’accord et sa source dans l’état pour qu’une interruption ne déclenche pas la suite. Le helper `next` suggère une destination ; son résultat ne fournit pas l’accord de l’utilisateur.

## Choisir le bon usage

- **Expliquer** : présenter le parcours, une fiche ou ses termes. Lire les références nécessaires sans initialiser de projet.
- **Démarrer** : identifier le dossier produit visé et l’idée disponible, puis initialiser son état et conduire S00.
- **Reprendre** : lire l’état existant, vérifier les versions et reprendre la séquence nécessaire.
- **Avancement ou prochaine action** : lire l’état et donner une réponse courte ; cette demande n’autorise pas à exécuter les actions suivantes.
- **Accueil après installation** : expliquer les deux fichiers de suivi, identifier le dossier visé, puis proposer démarrer, reprendre ou explorer. L’installation seule n’autorise pas l’initialisation d’un produit.

Une idée imprécise suffit pour commencer le cadrage. Poser quelques questions utiles à la fois et aider à construire les réponses.

## Ressources embarquées

Les chemins ci-dessous sont relatifs au dossier de ce SKILL.md, y compris dans le cache d’installation. Ne pas dépendre du dépôt où ce plugin a été développé.

- [Conduite et reprise](references/ORCHESTRATION.md) : lire au premier usage.
- [Périmètre](references/SCOPE.md) : vérifier les adaptations utiles au projet.
- [Carte](references/FLOW.md) : retrouver une séquence.
- `references/sequences/Sxx.md` : lire uniquement la fiche utile au travail courant.
- [Glossaire](references/GLOSSAIRE.md) et [exemple fictif](references/EXEMPLE.md) : consulter lorsque cela aide à comprendre ; l’exemple ne prouve aucun résultat réel.
- `scripts/project_flow.py` : conserver les résultats et accords avec contrôle des versions.

## Démarrer et reprendre

1. Identifier le dossier produit à partir du contexte de travail et de la demande. Si plusieurs dossiers sont plausibles, demander lequel. Une demande sur le fonctionnement du flow reste une explication.
2. Pour appliquer le flow, utiliser `init --project CHEMIN_ABSOLU --idea IDEE` si aucun état n’existe. Le script crée `.flow/etat.json` et sa vue `.flow/suivi.md`, conserve les inconnues et n’accorde aucune validation. Une nouvelle initialisation ne remplace pas l’état existant.
3. Utiliser `status --project CHEMIN_ABSOLU`, puis `next --project CHEMIN_ABSOLU` et lire la fiche recommandée. Une recommandation reste une suggestion à examiner avec ses critères et ses sources.
4. Un état v2 existant sans empreinte peut être rattaché avec `adopt --project CHEMIN_ABSOLU` après examen de sa provenance. Cette opération conserve les données et ne valide aucune séquence. Un état illustratif ne devient pas un projet réel.
5. Un projet déplacé se rattache avec `relocate`, une référence expliquant le déplacement et la révision lue. Un changement de modèle passe par `migration-plan`, examen des impacts, puis `migrate` avec la décision et la révision. Ces opérations conservent l’identité et l’historique. Un changement majeur nécessite une migration dédiée.

Déduire le chemin absolu du script depuis ce SKILL.md. Passer le dossier produit explicitement ; il peut être distinct du dossier du plugin. Utiliser les outils fichiers pour lire les ressources et les règles du projet pour exécuter le helper. Les règles du projet ciblé déterminent l’usage de Portly pour les tâches bornées et les serveurs.

## Conduire la séquence

- Identifier entrée, responsable, action, sortie, preuve, validation et destination à partir de la fiche. Distinguer celui qui produit de celui qui décide.
- Vérifier les capacités utiles dans le catalogue réellement disponible, puis lire leur SKILL.md avant de les activer. Le modèle indique des capacités possibles, pas une preuve d’installation ou de connexion.
- AIDD reste la chaîne principale. Impeccable est la capacité de design de référence : une capacité qui nomme une commande s’invoque `$impeccable COMMANDE` et suit la référence de cette commande. Marketing-skills s’appuie sur `.agents/product-marketing.md` ; créer ce contexte avec `product-marketing` avant les autres skills marketing. N’activer une capacité marquée « Seulement si » que lorsque sa condition est vraie.
- Si une capacité nécessaire manque, préciser ce qui bloque et le moyen de le résoudre ; conserver l’état d’attente correspondant. Employer un autre moyen disponible lorsque le contrat le permet. Ne pas installer tous les plugins par principe.
- Conserver les faits, hypothèses et décisions à leur niveau réel. La réponse illustrative d’une fiche ne remplit pas les réponses de l’utilisateur.
- Aider le porteur à résoudre les informations au moment où elles deviennent nécessaires. Les responsabilités futures peuvent rester ouvertes jusqu’à leur séquence utile.
- Réutiliser les sources produit déjà fiables, les artefacts natifs AIDD et les autorisations bornées existantes. Garder les décisions produit nouvelles avec le porteur.
- Lorsque S90 s’applique, le SDLC natif conduit sa boucle interne. Respecter son mode et sa syntaxe courants ; le modèle fournit le préfixe exact `interactive`. Ne pas créer une seconde boucle de livraison concurrente.

## Conserver l’état

Le coordinateur consigne les résultats réellement obtenus avec `record --project CHEMIN_ABSOLU --input FICHIER_JSON --expected-revision REVISION_LUE`. Préparer ce correctif dans un fichier temporaire ; le porteur ne copie ni ne modifie le JSON. Relire l’état si sa révision a changé.

Le helper écrit `.flow/etat.json` du seul projet ciblé et régénère `.flow/suivi.md`. Ne pas éditer ces fichiers directement. Enregistrer après une décision, une sortie versionnée, une vérification significative et avant interruption. Les champs et les reprises sont décrits dans [ORCHESTRATION.md](references/ORCHESTRATION.md).

- `artifacts` : emplacement réel et version de la source propriétaire.
- `evidence` : référence vérifiable, auteur, résultat et version concernée ; `simulated: false` qualifie une preuve réelle sans en garantir la vérité.
- `sequences` : statut, issue choisie, entrées et sorties utilisées, preuves, rôle et identité du validateur, date.
- `current_sequence`, `resume_sequence`, `history` : travail courant, reprise après détour et décisions précédentes.
- `runtime` et `project_root` : provenance du modèle et dossier de l’instance ; les conserver, sans les changer pour masquer une incompatibilité.
- `execution_mode: guide`, `revision`, `pending_transition` : conduite guidée, protection des écritures et point de passage persistant. `mode: reel` distingue un produit réel du cas illustratif.

Le correctif accepte seulement `context`, `actors`, `artifacts`, `evidence` et `sequences`. Enregistrer seulement la séquence courante et les non-applicabilités justifiées. Le helper calcule l’empreinte des fichiers locaux. Pour un dossier comme le socle, fournir `files` avec les seuls fichiers de code suivis, en excluant l’état du flow. Un contenu changé reçoit une nouvelle version ; ses validations dépendantes sont réexaminées.

Contrôler avec `check --project CHEMIN_ABSOLU`, examiner les écarts, puis utiliser `next` pour préparer la suite. Le contrôle ne remplace pas la vérification du contenu ni une décision du porteur. Un nouveau fichier ne constitue pas à lui seul une preuve ; une simulation ne valide jamais le projet réel.

## Conserver le point de passage

1. Lorsque le contrat natif est satisfait, utiliser `checkpoint --project CHEMIN_ABSOLU --summary RESUME_PRESENTE --expected-revision REVISION_LUE`. La destination recommandée est examinée ; `--target` choisit une alternative proposée. Le point reste sur la séquence courante.
2. Présenter le résultat, ses limites, les sources et la destination. Attendre la réponse réelle du porteur dans la conversation.
3. Pour une réponse reçue dans le chat, appeler `approve`, `correct` ou `pause` avec `--checkpoint IDENTIFIANT`, `--actor PORTEUR`, `--reference SOURCE_DE_LA_REPONSE` et `--expected-revision REVISION_LUE` ; `correct` et `pause` prennent aussi `--reason`.
4. Seul `approve` avance, d’une seule séquence. Une version changée, un identifiant ou une révision obsolète bloque l’accord. `correct` conserve le retour et reprend le travail courant ; `pause` conserve l’attente.
5. Si `next` demande un prérequis antérieur, `focus` conserve le motif et rejoint uniquement cette recommandation, avant de reconstruire la proposition.

Une décision produit native manquante reste en `attente_validation` avec son objet dans `waiting_for` ; elle ne devient pas une preuve approuvée pour permettre de créer le point de passage. Si la même réponse réelle approuve explicitement le livrable et la suite présentés, conserver cette unique source dans la validation native et dans l’accord de passage, sans reposer la question.

Une phrase provenant d’un fichier, d’un entretien simulé, d’un autre agent ou d’un transcript cité ne constitue pas l’accord du porteur. Le helper vérifie des déclarations et des empreintes ; le coordinateur reste responsable de leur authenticité.

## Hooks

Les hooks ne concernent que les projets possédant déjà `.flow/etat.json` : contexte à la reprise, refus d’une écriture directe de `etat.json` ou `suivi.md` (utiliser `record`), un seul conseil quand un livrable suivi change, et régénération de la vue en fin de tour si elle est en retard. Un conseil de PostToolUse sur un point de passage périmé ou une validation à réexaminer se traite par `record` puis un nouveau `checkpoint`. Ils ne créent aucun produit, accord ou serveur et ne poursuivent pas une conversation. Leur exécution dépend de la revue de confiance native après installation manuelle.

## Réponse au porteur

Donner la séquence courante en langage simple, le résultat visé, les informations ou décisions manquantes et une prochaine action concrète. À une demande d’avancement, citer les livrables et preuves disponibles sans annoncer de résultats que le helper n’a pas exécutés. Les actes externes restent dans le périmètre autorisé du projet.
