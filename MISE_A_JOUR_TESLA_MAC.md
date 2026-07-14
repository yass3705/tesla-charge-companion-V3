# Mise à jour Tesla V3.2 avec Playwright

Cette version utilise un véritable navigateur Chromium piloté par Playwright.

## Première utilisation

1. Clic droit sur `Mettre_a_jour_Tesla.command`.
2. Clique sur **Ouvrir**.
3. Confirme l'ouverture.
4. Le programme crée automatiquement un environnement Python local.
5. Il installe Playwright.
6. Il télécharge Chromium.
7. Il teste d'abord une seule fiche Tesla.
8. Si le test réussit, appuie sur Entrée pour lancer les 271 stations.

La première installation peut prendre plusieurs minutes.

## Après la mise à jour

GitHub Desktop s'ouvre.

1. Summary : `Mise à jour Tesla`
2. Clique sur `Commit to main`.
3. Clique sur `Push origin`.

## Test avec navigateur visible

Le fichier `Tester_Tesla_avec_navigateur.command` ouvre Chromium visiblement et teste une seule station. Utilise-le si le mode normal échoue.

## Important

Playwright améliore fortement les chances de réussite, mais Tesla peut encore modifier ou renforcer ses protections. Le script commence donc toujours par tester une seule station avant de lancer la mise à jour complète.
