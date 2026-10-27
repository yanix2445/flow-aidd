# `record` — enregistrer un résultat

`record` ajoute à l’état du produit ce qui a réellement été obtenu : une réponse de contexte, un acteur, un livrable versionné, une preuve, l’avancement de la séquence courante. Il ne fait pas avancer le parcours et ne vaut pas accord : le passage se décide avec [checkpoint.md](checkpoint.md).

> **Contexte nécessaire :** la révision lue par `status`, et le résultat réel à consigner. Relire [socle.md](socle.md) juste avant.

## Étape 1 : Savoir quoi enregistrer

Enregistrer au fil du travail, sans attendre la fin de la séquence :

- **une réponse du porteur** à une question de contexte → `context` ;
- **qui tient quel rôle** → `actors` ;
- **un livrable créé ou modifié** → `artifacts` (le helper calcule l’empreinte) ;
- **une preuve obtenue** (décision, observation, test, verdict d’agent) → `evidence` ;
- **l’état de la séquence courante** (en cours, attente, validée, non applicable) → `sequences`.

Enregistrer aussi avant toute interruption, pour qu’une autre séance reprenne depuis les fichiers.

## Étape 2 : Préparer le correctif

Écrire un JSON dans un fichier temporaire. Seules les clés `context`, `actors`, `artifacts`, `evidence` et `sequences` sont acceptées, et seule la séquence courante (ou une non-applicabilité justifiée) peut être modifiée.

```json
{
  "actors": {"porteur": "Camille", "coordinateur": "Codex"},
  "context": {"public_users": false},
  "artifacts": {"cadre": {"path": ".flow/cadre.md", "version": "v1"}},
  "evidence": {
    "S00-cadre-decide": {
      "sequence": "S00", "criterion": "cadre_decide", "kind": "decision",
      "actor": "Camille", "artifact": "cadre", "version": "v1", "reference": "conversation du 27/10, réponse « oui, ce cadrage me va »",
      "result": "approved", "simulated": false
    }
  },
  "sequences": {
    "S00": {"status": "valide", "outcome": "valide", "produced_versions": {"cadre": "v1"},
            "validator_role": "porteur", "validated_by": "Camille", "validated_at": "2026-10-27T10:00:00+01:00",
            "performed_by": "Codex", "evidence_ids": ["S00-cadre-decide"]}
  }
}
```

Points clés :

- **`context`** : une inconnue reste `null`, jamais `false` par défaut.
- **`artifacts`** : un chemin local relatif au produit et un libellé de version ; sans `version`, le helper en calcule une depuis le contenu (`sha256:…`), à reprendre ensuite tel quel dans les preuves. Un dossier (comme le socle) déclare `files`, les seuls fichiers de code suivis, sans l’état du flow. Une référence distante utilise HTTPS et une version explicite.
- **`evidence`** : source vérifiable, auteur, résultat, artefact et **version exacte de cet artefact**. `simulated: false` qualifie une preuve réelle sans en garantir la vérité. Le verdict d’un agent de contrôle se cite avec sa date et les versions contrôlées.
- **`sequences`** : statut, issue, versions utilisées et produites, validateur (rôle et identité), date, preuves liées. Une attente se note avec `waiting_for`.

## Étape 3 : Enregistrer et vérifier

```sh
python3 -B SKILL_DIR/scripts/project_flow.py record --project CHEMIN_ABSOLU --input FICHIER_JSON --expected-revision REVISION_LUE
python3 -B SKILL_DIR/scripts/project_flow.py check --project CHEMIN_ABSOLU
```

Puis `status` pour la suite. Le helper tient seul `current_sequence`, `resume_sequence`, `history`, `runtime`, `project_root`, `execution_mode`, `revision`, `pending_transition` et `mode`.

## Pannes fréquentes

| Message du helper | Que faire |
| --- | --- |
| « Le suivi a changé : relire la version courante avant cette action. » | Relancer `status`, refaire le correctif sur la nouvelle révision. |
| « La révision lue est requise… » | Ajouter `--expected-revision`. |
| « Une écriture est déjà en cours… » | Attendre la fin de l’autre écriture ; après un arrêt brutal, signaler le verrou au porteur, ne pas le supprimer. |
| « record accepte seulement contexte, acteurs, livrables, preuves et contrats de séquences. » | Retirer les autres clés ; la navigation passe par `checkpoint`/`approve`. |
| « Enregistrer le travail courant ; utiliser focus pour une reprise proposée. » | Le correctif vise une autre séquence : ne consigner que la séquence courante. |
| « Le contenu a changé : choisir une nouvelle version ou laisser record calculer son empreinte. » | Retirer `version` ou en donner une nouvelle. |
| « Fichier absent, ou dossier sans liste explicite… » | Corriger le chemin ou déclarer `files`. |
| « Une preuve réelle explicitement qualifiée est requise. » | Ajouter `simulated: false` à une preuve réellement obtenue ; ne jamais le mettre sur une simulation. |
| « `Sxx` : … » | Les critères ou versions de la séquence ne tiennent pas : traiter chaque problème cité. |

## Avant de terminer

- Chaque élément enregistré a été réellement obtenu, avec sa source.
- `check` ne signale plus d’écart sur ce qui vient d’être enregistré.
- Le porteur n’a eu à copier ni modifier aucun JSON.
