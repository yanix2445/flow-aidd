# `status` et `next` — savoir où en est le projet

`status` lit l’état du produit et dit quoi lire et quoi faire maintenant ; `next` renvoie la même lecture centrée sur la recommandation. Ils ne modifient rien. Une recommandation n’est jamais un accord du porteur, et une demande d’avancement n’autorise pas à exécuter la suite.

> **Contexte nécessaire :** le chemin absolu du dossier produit.

## Étape 1 : Lire l’état

```sh
python3 -B SKILL_DIR/scripts/project_flow.py status --project CHEMIN_ABSOLU
```

Lancer une fois en début de séance, puis après chaque `record`, `checkpoint` ou décision. `check` fait la même lecture et sort en erreur s’il reste des écarts. Code de sortie 1 : lire `errors` avant tout.

## Étape 2 : Suivre la situation

Lire `directives` dans l’ordre et **seulement** les fichiers de `load` (chemins relatifs à `skill_root`). Selon ce que renvoie `status` :

- **`errors` contient « adopt », « relocate » ou « migration-plan » :** l’état n’est pas rattaché à ce dossier ou à ce modèle ; aller à [rattacher.md](rattacher.md) avant tout travail.
- **`pending_transition` présent :** un accord est attendu. Présenter le résultat s’il ne l’a pas été, sinon attendre la réponse du porteur. Ne pas commencer la séquence suivante. Si `checkpoint_stale` est vrai, le contenu a changé : `record` puis un nouveau `checkpoint` ([checkpoint.md](checkpoint.md)).
- **Statut `attente_info`, `attente_acces` ou `attente_validation` :** nommer précisément ce qui manque (`waiting_for`) et qui peut le fournir. Avancer seulement sur ce qui est déjà autorisé et indépendant.
- **`capabilities.a_confirmer` non vide :** poser ces questions au porteur ([entretien.md](entretien.md)) et consigner les réponses dans `context` avec `record`.
- **`recommendation.result` = `sequence_a_realiser` :** conduire la séquence selon sa fiche.
- **Autre `recommendation.result`** (`information_requise`, `non_applicabilite_a_consigner`, `a_reexaminer`) : suivre la `reason` ou le `field` indiqués.

Les statuts possibles sont décrits dans [regles.md](regles.md#statuts).

## Étape 3 : Répondre au porteur

À « où en est-on ? », répondre en quelques lignes, en langage simple :

1. la séquence en cours et son intention ;
2. ce qui est déjà acquis (livrables et preuves enregistrés) ;
3. ce qui manque ou ce qui est attendu de lui ;
4. la prochaine action proposée, présentée comme une proposition.

Exemple de forme : « On est sur S20, éclairer le besoin. Le cadrage et l’intention sont validés. Il manque deux retours de personnes de la cible. Je propose de préparer le guide d’entretien ; tu me dis si on y va. »

Ne pas annoncer de résultat que le helper n’a pas produit, ni présenter la recommandation comme décidée.

## Pannes fréquentes

| Situation | Que faire |
| --- | --- |
| `initialized: false` sur un projet qu’on croyait suivi | Vérifier le dossier ; un autre dossier porte peut-être `.flow/`. Ne pas relancer `init` à l’aveugle. |
| « Le fichier d’état doit être un objet JSON. » | `etat.json` a été abîmé hors du helper : le signaler au porteur, ne pas le réécrire à la main. |
| `errors` sur un livrable « contenu modifié » | Le fichier a changé depuis son enregistrement : `record` sa nouvelle version. |

## Avant de terminer

- Seuls les fichiers de `load` ont été lus.
- La réponse distingue acquis, manque et proposition.
- Rien n’a été lancé sur la seule foi de la recommandation.
