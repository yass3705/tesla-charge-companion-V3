# Tesla Charge Companion V4.0

La V4 ajoute un onglet Maintenance intégré.

## Limite technique importante
Une page GitHub Pages ne peut ni lire directement `tesla.com` (isolation inter-domaines), ni modifier les fichiers de ton dépôt. Le compagnon Firefox reste donc nécessaire pour la récupération Tesla. L’interface de commande et le suivi sont maintenant intégrés dans l’application.

## Mise à jour Tesla
1. Charge temporairement `firefox_extension/manifest.json` depuis `about:debugging#/runtime/this-firefox`.
2. Recharge le site.
3. Ouvre l’onglet Maintenance.
4. Clique sur Mettre à jour les Superchargeurs.
5. Importe le JSON téléchargé, puis remplace le fichier du dépôt pour publier.
