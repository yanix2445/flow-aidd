# Capacités — activer les bons skills

Choisir et activer les skills utiles à la séquence de travail, à partir du tri que fait `status` pour ce projet. Le modèle cite des capacités possibles ; il ne prouve ni leur installation, ni leur connexion. Ne jamais installer tous les plugins par principe.

> **Contexte nécessaire :** le champ `capabilities` de `status` et le catalogue de skills réellement disponible dans la session.

## Étape 1 : Comprendre qui fait quoi

- **AIDD** (`aidd-*`) est la chaîne principale : ses artefacts (PRD, spec, plan, mémoire) portent le besoin et le code. En cas de doute entre deux skills, celui d’AIDD fait foi.
- **Impeccable** est la capacité de design de référence. Une capacité qui nomme une commande s’invoque `$impeccable COMMANDE` et suit la référence de cette commande dans Impeccable ; il s’appuie sur `PRODUCT.md` et `DESIGN.md` du produit.
- **marketing-skills** s’appuie sur `.agents/product-marketing.md`. Créer ce contexte avec `product-marketing` avant tout autre skill marketing.

Chaque contexte a **une seule source qui fait foi** ; les autres la citent sans la recopier :

| Contexte | Source | Créée ou mise à jour |
| --- | --- | --- |
| Besoin, périmètre, critères | Brief et PRD (AIDD), puis epic, stories et spec | S30, S40, S80 |
| Public, positionnement, ton | `.agents/product-marketing.md` (`product-marketing`) | S20, puis S30 |
| Contexte de design | `PRODUCT.md` (`$impeccable init`), rédigé à partir des deux sources précédentes | S50 |
| Langage visuel construit | `DESIGN.md` (`$impeccable document`), tiré de l’interface réellement intégrée | S91, S100 |

Enregistrer ces fichiers avec `record` (`contexte_marketing`, `parcours`, `design_system`) pour que leurs changements soient suivis.

## Étape 2 : Lire le tri

| Groupe | Que faire |
| --- | --- |
| `utiliser` | Activer selon le besoin réel de la séquence, pas en série. |
| `selon_le_cas` | Activer seulement si la condition `si` est vraie pour ce projet ; en cas de doute, demander. |
| `a_confirmer` | Poser la `question` au porteur ([entretien.md](entretien.md)), consigner la réponse dans `context` avec `record`, puis relire `status`. |
| `ecartees` | Ne pas activer ; la raison est donnée. Si elle paraît fausse, corriger le `context`, pas le tri. |

Une réponse de contexte inconnue laisse la capacité à confirmer, jamais écartée.

## Étape 3 : Activer

1. Vérifier que le skill existe dans le catalogue de la session.
2. Lire son SKILL.md avant de l’employer, et respecter sa syntaxe et son mode courants.
3. Lui donner les sources produit déjà fiables (cadrage, brief, PRD, contexte marketing) plutôt que de refaire leurs questions au porteur.
4. Consigner ce qu’il produit comme livrable avec `record`.

## Cas particulier : la livraison (S90)

Le SDLC natif (`aidd-orchestrator:01-sdlc`) conduit sa propre boucle (cadrage du contrat, plan, implémentation, contrôles, revue, commit, PR en brouillon), avec son propre relecteur. La requête commence exactement par `interactive`, suivi d’une source concrète, et cite les sources qui font foi pour la tranche : contrat du MVP, mémoire du projet, et si la tranche touche l’interface ou le message, le brief shape de S80, `PRODUCT.md`, `DESIGN.md` et `.agents/product-marketing.md`. Le SDLC les suit ; Impeccable et marketing-skills ne lancent pas de chaîne parallèle pendant la livraison, ils reviennent après (S91, S100). Ne pas lancer une seconde chaîne plan, implémentation, revue à côté.

## Pannes fréquentes

| Situation | Que faire |
| --- | --- |
| Le skill n’existe pas dans la session | Dire ce qui bloque et comment le résoudre, enregistrer `attente_acces` ; employer un autre moyen disponible si le contrat de la fiche le permet. |
| Le skill demande une connexion ou un compte | Ne pas créer de compte ni saisir d’identifiant ; laisser le porteur faire. |
| Deux skills se recouvrent | Prendre celui d’AIDD pour le besoin et le code, Impeccable pour le design, marketing-skills pour public, offre, mesure et lancement. |

## Avant de terminer

- Chaque skill activé figurait dans `utiliser`, ou dans `selon_le_cas` avec sa condition vraie.
- Les questions `a_confirmer` ont été posées, pas devinées.
- Ce qu’ont produit les skills est enregistré comme livrable de la séquence.
