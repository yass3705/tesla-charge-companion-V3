# Mise à jour Tesla depuis Firefox — V3.3

1. Ouvre Firefox.
2. Saisis `about:debugging#/runtime/this-firefox`.
3. Clique sur **Charger un module complémentaire temporaire…**
4. Sélectionne `firefox_extension/manifest.json`.
5. Clique sur l’icône de l’extension.
6. Sélectionne `data/tesla_stations.json`.
7. Clique sur **Démarrer**.
8. Laisse Firefox ouvert.
9. À la fin, remplace `data/tesla_stations.json` par le fichier téléchargé.
10. Dans GitHub Desktop : **Commit to main**, puis **Push origin**.

L’extension reste active jusqu’à la fermeture complète de Firefox.
