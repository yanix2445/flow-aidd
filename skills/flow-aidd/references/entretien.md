# Entretien — obtenir les réponses du porteur

Conduire les questions d’une séquence avec le porteur pour obtenir des réponses réelles, sans questionnaire et sans réponses inventées. L’entretien aide à construire une réponse ; il ne la remplit jamais à la place du porteur.

> **Contexte nécessaire :** la fiche de la séquence (questions, réponse acceptable, réponse insuffisante), les sources produit déjà présentes et le champ `capabilities.a_confirmer` de `status`.

## Étape 1 : Partir de ce qui est déjà vrai

Avant de demander, relire ce que le projet sait déjà : `.flow/cadre.md`, livrables enregistrés, `PRODUCT.md`, `.agents/product-marketing.md`, artefacts AIDD, documents du dossier. Ne pas faire répéter un fait écrit ; s’il paraît dépassé, demander s’il tient toujours.

Ce que le dépôt laisse deviner reste une hypothèse : la proposer, ne pas la consigner comme décision.

## Étape 2 : Choisir les questions qui changent le résultat

Partir des questions de la fiche et des `a_confirmer`, puis garder seulement celles dont la réponse change le livrable ou la suite. Une question dont la réponse ne changerait rien attend son moment.

La « réponse acceptable, illustrative » de la fiche montre le niveau de précision visé. La « réponse insuffisante » montre ce qu’il faut faire préciser.

## Étape 3 : Le rythme

- **Deux ou trois questions liées par tour**, puis s’arrêter et attendre. Utiliser l’outil de question structurée quand il existe ; sinon, poser les questions et attendre la réponse.
- **Un tour par défaut** ; un second seulement si les réponses révèlent un manque qui change le résultat.
- **Proposer la lecture la plus probable** et inviter à la corriger plutôt que de demander à partir de rien : « Je comprends que la cible, ce sont des étudiants en licence qui révisent seuls le soir ; c’est bien ça ? »
- **Pas de menu artificiel** pour un fait évident, pas de jargon : « public externe » plutôt que `public_users`.
- **Aider à formuler** : si le porteur hésite, proposer deux ou trois formulations concrètes à choisir ou à corriger.
- **Une réponse floue** (« des gens », « plus tard ») appelle une relance précise, une seule fois ; ensuite, consigner l’inconnue et ce qui permettra de la lever.

## Étape 4 : Consigner

Chaque réponse obtenue s’enregistre avec `record` ([record.md](record.md)), avec sa source (le message du porteur) :

- une réponse de contexte → `context` (une inconnue reste `null`) ;
- une décision → une preuve `kind: "decision"` rattachée au livrable et à sa version ;
- une information manquante → la séquence en `attente_info`, avec `waiting_for` précis.

Rédiger ensuite le livrable à partir des réponses, et le présenter au porteur pour qu’il le reconnaisse comme le sien.

## Pannes fréquentes

| Situation | Que faire |
| --- | --- |
| Le porteur répond « vas-y, décide » | Proposer une option argumentée et demander de la confirmer ; la décision reste la sienne. |
| Le porteur ne connaît pas la réponse | Consigner l’inconnue, dire à quelle séquence elle deviendra nécessaire, continuer sur le reste. |
| Le porteur est absent | Ne pas simuler ses réponses ; enregistrer l’attente et s’arrêter. |
| Une réponse contredit une décision validée | Le signaler, demander laquelle tient ; une décision changée rouvre les validations qui en dépendent. |

## Avant de terminer

- Chaque réponse consignée vient du porteur, avec sa source.
- Aucune réponse illustrative de la fiche n’a été recopiée.
- Les inconnues restantes sont nommées, avec la séquence où elles deviendront nécessaires.
