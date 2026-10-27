# MiniRévisions — livrables renseignés

**Exemple fictif, aucune exécution ni observation réelle du produit.** Les notes ci-dessous montrent le niveau de précision recherché ; elles ne constituent pas un projet lancé.

<a id="idee"></a>

## Note d’intention remplie

- Cible : le porteur de l’exemple, étudiant qui rédige ses propres fiches de révision.
- Difficulté supposée : ses fiches sont dispersées et il veut les retrouver dans un seul outil.
- Résultat souhaité : créer une fiche puis retrouver le même contenu plus tard.
- Fait sur le cas d’école : il s’agit d’un scénario inventé pour expliquer le flow. Aucune observation d’étudiant réel n’est fournie.
- Hypothèse à vérifier dans un vrai projet : centraliser les fiches améliore effectivement la tâche du porteur.

<a id="mvp"></a>

## Contrat du MVP rempli

- Périmètre retenu : un usage personnel, dans un navigateur et sur un appareil ; créer une fiche avec titre et contenu, puis lister et relire les fiches.
- Hors périmètre : comptes, paiement, partage, synchronisation et promesse de conservation sur plusieurs appareils.
- Critère 1 : une fiche comportant un titre et un contenu réapparaît avec les mêmes valeurs après rechargement du navigateur.
- Critère 2 : un titre vide empêche la création et affiche un message compréhensible ; le contenu déjà saisi reste disponible.
- Critère 3 : une liste vide propose une action claire pour créer la première fiche.
- Contrainte à présenter : une conservation locale dépend du navigateur utilisé ; le produit ne promet pas une sauvegarde distante inexistante.
- Action de valeur : retrouver une fiche précédemment créée. Dans ce cas personnel, le protocole de départ peut être une observation du parcours par le porteur plutôt qu’une plateforme d’analytics.
- Validation illustrative : le porteur fictif approuve cette version du périmètre. Dans une instance réelle, il faut conserver sa vraie décision sur la vraie révision.

<a id="tranche"></a>

## Demande prête remplie

- Acteur : le porteur utilise son outil personnel de révision.
- Besoin : conserver une fiche et la retrouver après avoir quitté la page.
- Résultat : le titre et le contenu enregistrés sont relus sans perte lors du rechargement prévu au contrat.
- Critères d’acceptation : les trois critères du contrat MVP sont repris comme scénarios vérifiables, avec les erreurs prévues.
- Tranche verticale : interface de saisie, logique de validation, conservation locale et restitution de la fiche sont livrées ensemble pour cette seule tâche.
- Dépendances : le périmètre et l’architecture locale sont décidés ; aucun accès distant n’est supposé disponible.
- Choix de proportion : une story peut suffire ; aucune spec séparée n’est imposée si ce contrat est déjà assez clair pour planifier.

<a id="preuve"></a>

## Ce qui ferait preuve, sans prétendre l’avoir exécuté

- Un fichier de code présent ne prouve pas que la fiche est conservée.
- Une preuve technique recevable serait un résultat de test ou une observation du parcours sur une révision et une adresse identifiées.
- La preuve doit indiquer le scénario, le résultat réellement obtenu, l’auteur, la date et la révision du candidat.
- Une preuve de décision serait la référence à l’approbation réelle du porteur sur le périmètre, avec sa révision et ses éventuelles réserves.
- Dans les fichiers de ce cas d’école, ces preuves sont simulées. Elles ne doivent pas être converties en preuves réelles par un simple changement de statut.

<a id="attente"></a>

## Reprise concrète après interruption

- Situation illustrative : le MVP est ouvert, mais la fenêtre d’observation choisie n’est pas terminée.
- Séquence courante : S120. Statut : attente_info.
- Élément attendu : observations de la tâche centrale sur la fenêtre prévue, avec leurs limites.
- Prochaine action : reprendre la lecture des observations à cette même séquence lorsque l’élément devient disponible.
- Action évitée : créer arbitrairement une nouvelle fonctionnalité dans le backlog pour remplacer les données absentes.

[Revenir au parcours complet](exemple.md)
