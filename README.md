# Tesla Charge Companion V5.0

Le projet comprend deux parties :

## Site GitHub Pages

- comparaison coût + distance ;
- gestion des bornes ;
- tarifs au kWh ou à la minute ;
- horaires d’accès ;
- devises ;
- opérateurs ;
- simulations de durée et coût.

## Tesla Companion pour Mac

Le dossier `companion` contient `Tesla Companion.app`.

Fonctions :

- lancement guidé de la mise à jour Tesla dans Firefox ;
- mise à jour locale des devises ;
- sauvegarde des bases JSON ;
- ouverture de GitHub Desktop ;
- ouverture du site et du dossier du projet.

## Installation

Lire dans cet ordre :

1. `PREMIER_LANCEMENT.md`
2. `INSTALLATION_MAC.md`
3. `MISE_A_JOUR_TESLA.md`
4. `INSTALLATION_GITHUB.md`

## Limitation Tesla

Tesla bloque actuellement les requêtes automatisées Python, GitHub Actions et Playwright. La récupération des prix Tesla passe donc encore par l’extension Firefox temporaire incluse dans `firefox_extension`.
