# `adopt`, `relocate`, `migration-plan`, `migrate` — rattacher un état

Ces commandes rattachent un suivi existant au bon dossier et au modèle actuel du plugin, en conservant son identité, son historique et ses preuves. Elles ne valident aucune séquence et ne transforment jamais un exemple en projet réel.

> **Contexte nécessaire :** l’erreur exacte renvoyée par `status`, la révision lue, et l’accord du porteur pour toute opération qui rouvre des validations.

## Étape 1 : Lire l’écart

`status` signale le problème dans `errors` et charge cette référence. Choisir le cas :

| Message de `status` | Situation | Aller à |
| --- | --- | --- |
| « État non rattaché : examiner sa provenance avant adopt. » ou « État sans protocole guidé actuel : examiner adopt. » | Ancien suivi v2 sans empreinte | Étape 2 |
| « Dossier différent : vérifier l’instance avant relocate. » | Projet déplacé, renommé ou cloné | Étape 3 |
| « Version du modèle différente » ou « Empreinte du modèle différente : examiner migration-plan. » | Plugin mis à jour depuis le dernier enregistrement | Étape 4 |
| « Un cas illustratif ne pilote pas un projet réel. » | Exemple copié dans un produit | Ne rien rattacher ; proposer `init` sur un vrai projet. |

## Étape 2 : Adopter un ancien état

Examiner d’où vient le fichier (auteur, date, projet), puis :

```sh
python3 -B SKILL_DIR/scripts/project_flow.py adopt --project CHEMIN_ABSOLU
```

Les données sont conservées et la provenance ajoutée. Aucune séquence n’est validée par l’adoption.

## Étape 3 : Rattacher après un déplacement

Vérifier avec le porteur qu’il s’agit bien du même produit (et pas d’une copie à faire vivre séparément), puis :

```sh
python3 -B SKILL_DIR/scripts/project_flow.py relocate --project CHEMIN_ABSOLU --reference "RAISON DU DEPLACEMENT" --expected-revision N
```

Le helper garde l’identité, normalise les chemins et signale les fichiers modifiés ou manquants, à traiter ensuite avec `record`.

## Étape 4 : Migrer vers le modèle actuel

1. Lire le plan, sans rien modifier :

```sh
python3 -B SKILL_DIR/scripts/project_flow.py migration-plan --project CHEMIN_ABSOLU
```

2. Présenter au porteur `changed_sequences` (les validations qui seront rouvertes) et `retired_sequences`.
3. Avec son accord :

```sh
python3 -B SKILL_DIR/scripts/project_flow.py migrate --project CHEMIN_ABSOLU --reference "ACCORD DU PORTEUR" --expected-revision N
```

Un instantané est conservé dans l’historique ; seules les validations affectées sont rouvertes.

## Pannes fréquentes

| Message du helper | Que faire |
| --- | --- |
| « Ce projet est déjà rattaché à ce dossier. » | Rien à faire ; relancer `status`. |
| « Examiner les références absolues situées hors de l’ancien projet. » | Des livrables pointent hors du projet : les signaler au porteur avant de rattacher. |
| « Rattacher le bon dossier avant la migration. » | Faire l’étape 3 d’abord. |
| « Changement majeur du format : une migration dédiée est nécessaire. » ou « Provenance ou format de suivi inconnu… » | Ne pas forcer ; expliquer au porteur qu’une migration dédiée est nécessaire. |
| « Les exemples ne sont pas migrés en projets réels. » | L’état est une illustration : partir d’un `init`. |

## Avant de terminer

- Jamais `runtime`, `project_root` ou `flow_version` modifiés à la main pour faire disparaître un écart.
- Le porteur a vu les validations rouvertes avant `migrate`.
- `status` ne signale plus d’erreur de rattachement.
