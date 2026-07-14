# GUIDE D’INSTALLATION — TESLA CHARGE COMPANION V3.2

Ce guide suppose que tu utilises un Mac et que tu ne souhaites pas utiliser le Terminal.

## 1. Décompresser le fichier

1. Télécharge `Tesla_Charge_Companion_V3_1.zip`.
2. Ouvre le Finder puis le dossier Téléchargements.
3. Double-clique sur le ZIP.
4. Un dossier `Tesla_Charge_Companion_V3_1` est créé.
5. Ouvre-le.

Tu dois voir notamment :

- `index.html`
- `manifest.webmanifest`
- `service-worker.js`
- `README.md`
- `INSTALLATION_GITHUB.md`
- le dossier `assets`
- le dossier `data`
- le dossier `scripts`
- le dossier caché `.github`

Le Finder masque normalement les fichiers commençant par un point. Pour afficher `.github`, appuie simultanément sur :

`Commande + Majuscule + .`

Refais la même combinaison pour masquer de nouveau les fichiers cachés.

## 2. Créer un dépôt GitHub neuf

1. Connecte-toi sur GitHub.
2. Clique sur le bouton `+` en haut à droite.
3. Clique sur `New repository`.
4. Dans `Repository name`, saisis :

`tesla-charge-companion`

5. Choisis `Public`.
6. Ne coche pas :
   - Add a README file
   - Add .gitignore
   - Choose a license
7. Clique sur `Create repository`.

## 3. Charger tous les fichiers sans perdre les dossiers cachés

Le téléchargement par glisser-déposer dans le navigateur ne gère pas toujours bien les dossiers cachés. La méthode la plus fiable sans Terminal est GitHub Desktop.

### Installer GitHub Desktop

1. Télécharge GitHub Desktop depuis son site officiel.
2. Installe-le dans Applications.
3. Ouvre-le.
4. Connecte-toi avec ton compte GitHub.

### Ajouter le projet

1. Dans GitHub Desktop, clique sur `File`.
2. Clique sur `Add Local Repository`.
3. Clique sur `Choose`.
4. Sélectionne le dossier décompressé `Tesla_Charge_Companion_V3_1`.
5. Si GitHub Desktop indique que ce dossier n’est pas encore un dépôt Git :
   - clique sur `create a repository`;
   - conserve le nom proposé;
   - vérifie que `Git Ignore` indique `None`;
   - clique sur `Create Repository`.
6. Dans la colonne de gauche, tous les fichiers doivent apparaître, y compris :
   - `.github/workflows/pages.yml`
   - `.github/workflows/update-tesla.yml`
   - `.github/workflows/update-fx.yml`
7. En bas à gauche, dans `Summary`, saisis :

`Installation Tesla Charge Companion V3.2`

8. Clique sur `Commit to main`.
9. Clique ensuite sur `Publish repository`.
10. Dans la fenêtre :
    - choisis le dépôt GitHub créé plus tôt, ou utilise le même nom;
    - décoche `Keep this code private`;
    - clique sur `Publish Repository`.

Si GitHub Desktop refuse parce que le dépôt existe déjà, supprime le dépôt GitHub vide et clique de nouveau sur `Publish Repository`. Comme il ne contenait rien, aucune donnée n’est perdue.

## 4. Vérifier les fichiers sur GitHub

Sur GitHub, ouvre le dépôt.

Tu dois voir à la racine :

- `.github`
- `assets`
- `data`
- `scripts`
- `.gitignore`
- `index.html`
- `INSTALLATION_GITHUB.md`
- `manifest.webmanifest`
- `README.md`
- `service-worker.js`

Clique sur `.github`, puis `workflows`.

Tu dois voir exactement :

- `pages.yml`
- `update-fx.yml`
- `update-tesla.yml`

## 5. Activer GitHub Actions

1. Clique sur l’onglet `Actions`.
2. Si GitHub affiche un bouton pour activer les workflows, accepte.
3. Les trois workflows doivent apparaître :
   - Publier le site
   - Mise à jour Tesla
   - Mise à jour des devises

## 6. Autoriser les mises à jour automatiques

1. Clique sur `Settings`.
2. Dans le menu de gauche, ouvre `Actions`, puis `General`.
3. Descends jusqu’à `Workflow permissions`.
4. Sélectionne :

`Read and write permissions`

5. Clique sur `Save`.

Cette autorisation permet aux workflows Tesla et devises de mettre à jour les fichiers du dépôt.

## 7. Configurer GitHub Pages

Cette V3 utilise un workflow Pages.

1. Dans `Settings`, clique sur `Pages`.
2. Dans `Build and deployment`, sélectionne :

`GitHub Actions`

3. Reviens dans l’onglet `Actions`.
4. Ouvre `Publier le site`.
5. Clique sur `Run workflow`.
6. Clique encore sur le bouton vert `Run workflow`.

Attends que le rond orange devienne une coche verte.

## 8. Ouvrir le site

Dans `Settings → Pages`, GitHub affiche l’adresse du site, normalement :

`https://TON-NOM.github.io/tesla-charge-companion/`

Ouvre cette adresse dans Safari.

La page doit afficher :

`Version 3.0`

## 9. Tester la synchronisation Tesla

1. Ouvre l’onglet `Actions`.
2. Clique sur `Mise à jour Tesla`.
3. Clique sur `Run workflow`.
4. Confirme avec le bouton vert.
5. Le traitement des 271 fiches peut prendre plusieurs minutes.
6. Quand il est terminé, une coche verte apparaît.
7. Ouvre le dossier `data`.
8. Clique sur `tesla_stations.json`.
9. La date du dernier commit doit avoir changé si Tesla a renvoyé des données nouvelles.

Le workflow se lancera ensuite automatiquement chaque dimanche.

## 10. Tester la synchronisation des devises

1. Dans `Actions`, ouvre `Mise à jour des devises`.
2. Clique sur `Run workflow`.
3. Attends la coche verte.
4. Ouvre `data/exchange_rates.json`.
5. Vérifie que plusieurs devises et une date récente apparaissent.

Le workflow se lancera automatiquement chaque lundi.

## 11. Installer l’application sur iPhone et iPad

1. Ouvre l’adresse GitHub Pages dans Safari.
2. Appuie sur le bouton Partager.
3. Choisis `Sur l’écran d’accueil`.
4. Donne le nom `Tesla Charge`.
5. Appuie sur `Ajouter`.

Répète la même opération sur l’iPad.

## 12. Où sont stockées les données ?

### Dans GitHub

- `data/tesla_stations.json` : base Tesla mise à jour automatiquement.
- `data/custom_stations.json` : bornes tierces livrées avec le projet.
- `data/exchange_rates.json` : taux de change publiés.
- `data/metadata.json` : dates de mise à jour.

### Sur ton appareil uniquement

Les bornes créées ou modifiées dans l’application, les exclusions temporaires, l’adresse de départ et certains réglages sont enregistrés dans le stockage local du navigateur.

Une mise à jour Tesla ne doit donc pas effacer tes choix locaux.

## 13. Cloudflare

Cloudflare n’est pas nécessaire pour la V3.2.

GitHub Pages et GitHub Actions sont gratuits pour ce projet public et suffisent pour :

- publier l’application;
- actualiser les tarifs Tesla;
- actualiser les taux de change.

Cloudflare pourra être ajouté plus tard pour des mises à jour à la demande, une API intermédiaire ou une protection d’accès. L’ajouter maintenant compliquerait l’installation sans bénéfice indispensable.


# Mise à jour Tesla depuis le Mac

Le workflow Tesla GitHub a été retiré, car Tesla refuse les requêtes provenant de GitHub Actions.

1. Ouvre le dossier local du dépôt.
2. Clic droit sur `Mettre_a_jour_Tesla.command`.
3. Clique sur **Ouvrir**.
4. Attends la fin.
5. Dans GitHub Desktop : `Commit to main`, puis `Push origin`.

La mise à jour des devises reste automatique.


# Installation Playwright

Aucune commande manuelle n'est nécessaire.

Au premier lancement de `Mettre_a_jour_Tesla.command`, le programme :

1. crée un environnement Python local ;
2. installe Playwright ;
3. télécharge Chromium ;
4. teste une station ;
5. demande confirmation avant la mise à jour complète.
