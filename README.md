# flow-aidd

Un plugin Codex pour passer d’une idée vague au premier MVP, **une séquence à la fois**, avec résultats, preuves et accord avant la suite.

**Version locale en développement.** Installation manuelle dans Codex depuis un paquet exporté.

## Fonctionnement

Le guidage se fait dans la conversation Codex. Le coordinateur conduit une séquence, conserve les résultats et leurs preuves, puis attend la décision du porteur : poursuivre, corriger ou attendre.

L’avancement est conservé dans les fichiers du projet. Aucune interface web ni serveur local n’est nécessaire au plugin.

## Comprendre les fichiers

Ce dépôt contient la source unique du plugin. L’archive exportée contient les fichiers distribués ; le cache d’installation est géré par Codex.

| Emplacement                                 | Rôle                                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------------ |
| `.codex-plugin/plugin.json`               | Unique manifeste Codex : identité, présentation, accueil et hooks.           |
| `skills/flow-aidd/`                       | Le skill, son modèle unique, ses références, helpers et identité visuelle. |
| `hooks/`                                  | Événements de reprise et d’actualisation du suivi.                          |
| [docs/conception.md](docs/conception.md)     | Utilisation, fichiers du produit, distribution et limites.                     |
| [docs/verification.md](docs/verification.md) | Vérifications et limites constatées.                                         |
| `tools/`                                  | Développement, génération des guides, tests et création d’archive.        |
| `AGENTS.md` et `.agents/`               | Consignes de ce dépôt et catalogue d’installation locale.                   |

Dans le **produit accompagné**, le démarrage crée seulement :

```text
.flow/
├── etat.json     # État structuré, décisions et références
└── suivi.md      # Vue humaine régénérable
```

Les livrables arrivent ensuite selon les besoins. Les documents existants et les sources natives AIDD sont réutilisés ; aucune pile de documents vides n’est créée.

## Utiliser le plugin installé

Sélectionner `flow-aidd` et écrire normalement :

- « Démarre flow-aidd ici ; mon idée est… »
- « Reprends flow-aidd sur ce projet. »
- « Explique-moi la séquence en cours. »

L’accueil aide à choisir le dossier et l’usage. Un contrat satisfait reste sur sa séquence jusqu’à l’accord de passage. Une version modifiée rend un ancien accord obsolète. Les décisions et les reprises survivent à une nouvelle conversation.

Le plugin référence les autres skills utiles et vérifie leur disponibilité ; il ne les installe pas tous et ne copie pas leur code.

## Lire le parcours

[Carte des séquences](skills/flow-aidd/references/FLOW.md) · [S00](skills/flow-aidd/references/sequences/S00.md) · [Glossaire](skills/flow-aidd/references/GLOSSAIRE.md) · [Exemple fictif](skills/flow-aidd/references/EXEMPLE.md) · [Schémas Mermaid](skills/flow-aidd/references/MERMAID.md)

## Maintenir et distribuer

Prérequis des helpers : Python 3.10 ou plus. Ce dépôt utilise Portly pour les tâches bornées. Node et Playwright servent seulement à vérifier les diagrammes Mermaid.

```sh
job_id="$(portly temp 'python3 -B tools/build.py --check && python3 -B -m unittest discover -s tools -p "test_*.py"' --path . --timeout 30m)"
portly wait "$job_id"
```

Les règles des séquences se modifient dans `skills/flow-aidd/references/workflow.json`, puis les vues se régénèrent sur place avec `python3 -B tools/build.py` dans un job Portly.

`tools/release.py --output CHEMIN_EXTERIEUR_AU_DEPOT.zip` construit une archive autonome sans installation. Extraire ce paquet hors du dépôt, puis enregistrer son catalogue et installer le plugin :

```sh
codex plugin marketplace add /chemin/vers/le/paquet-extrait --json
codex plugin add flow-aidd@flow-aidd --json
codex plugin list --marketplace flow-aidd --json
```

Le paquet exporté exclut l’historique Git, les outils de développement et les caches. Une installation directe depuis le dépôt copie ces fichiers dans le cache de Codex ; utiliser l’archive pour tester la distribution.

Le manifeste de compatibilité `.codex-plugin/plugin.json` est utilisé seul : Codex 0.164.0-alpha.11.1 charge ses hooks, contrairement au manifeste portable à la racine lors de notre essai. Les hooks restent soumis à la revue de confiance native via `/hooks`. Avec ses hooks, cette version vise l’installation manuelle locale ou privée ; elle n’est pas éligible à l’annuaire public selon la [documentation OpenAI](https://developers.openai.com/plugins/build/plugins).
