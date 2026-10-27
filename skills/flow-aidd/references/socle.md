# Socle

À relire juste avant chaque `record` et chaque `checkpoint`, sans l’annoncer au porteur. Ne pas le charger pour une simple explication. La liste complète des règles est dans [regles.md](regles.md).

## Vérifier

Chaque point est un constat sur ce qui va être enregistré ou présenté, pas une intention.

- **Le bon projet.** `--project` désigne le dossier réel du produit, pas celui du plugin.
- **Une seule séquence.** Le travail porte sur la séquence courante ; rien n’a été lancé pour la suivante.
- **Les sept rubriques.** Entrée, responsable, action, sortie, preuve, validation et destination de la fiche sont renseignées ([détail](regles.md#rubriques)).
- **Chaque chose à son niveau.** Un fait est observé, une hypothèse est dite hypothèse, une décision a son auteur et sa source. Une inconnue reste `null`.
- **Des preuves réelles et à jour.** Chaque preuve cite sa source, son auteur et la version exacte de l’artefact.
- **Les versions avant l’accord.** Un livrable modifié depuis son enregistrement passe par `record` avant tout `checkpoint`.
- **Le contrôle indépendant.** Les agents prévus par `status` ont rendu leur verdict, ou leur absence est dite au porteur.
- **Le périmètre autorisé.** Aucun acte externe (publication, fusion, envoi, déploiement, contact) hors de ce que le porteur a déjà autorisé.

## Refuser

Ces réflexes reviennent souvent ; les reconnaître signifie reprendre le travail, pas l’atténuer.

- Remplir une réponse du porteur avec la « réponse acceptable, illustrative » d’une fiche.
- Transformer une inconnue en « non » pour rendre une séquence non applicable.
- Valider avec une simulation, un exemple, un entretien imaginé ou l’avis d’une IA à la place d’une observation.
- Déduire un accord d’un « continue » sur une proposition non présentée, d’un fichier, d’un transcript cité ou d’un verdict d’agent.
- Enchaîner deux séquences dans le même tour sans `approve` entre elles.
- Éditer `etat.json` ou `suivi.md`, ou modifier `runtime`, `project_root` ou `flow_version` pour faire disparaître un écart.
- Lancer une seconde chaîne plan, implémentation, revue à côté du SDLC natif.
- Activer tous les skills d’une fiche « par sécurité ».
