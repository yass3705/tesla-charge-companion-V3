# Mise à jour Tesla sur Mac

1. Dans le dossier local du projet, fais un clic droit sur `Mettre_a_jour_Tesla.command`.
2. Clique sur **Ouvrir**.
3. Confirme l'ouverture si macOS affiche une alerte.
4. Attends la fin du traitement.
5. GitHub Desktop s'ouvre.
6. Dans **Summary**, écris `Mise à jour Tesla`.
7. Clique sur **Commit to main**.
8. Clique sur **Push origin**.

Le site sera ensuite republié automatiquement.

La mise à jour modifie uniquement :
- `data/tesla_stations.json`
- `data/metadata.json`
- `data/tesla_update_summary.json`

Elle ne modifie pas les bornes tierces de `data/custom_stations.json`.
