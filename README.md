# Tesla Charge Companion V3.3

Application PWA personnelle pour comparer les coûts, distances et durées de recharge.

## Architecture

- `data/tesla_stations.json` : base Tesla automatisée
- `data/custom_stations.json` : bornes tierces séparées
- `data/exchange_rates.json` : taux de change
- `scripts/update_tesla.py` : synchronisation Tesla
- `scripts/update_fx.py` : synchronisation des devises
- `.github/workflows/` : publication et mises à jour automatiques
- `assets/` : interface et logique de l’application

## Installation

Lire `INSTALLATION_GITHUB.md`.

## Cloudflare

Non requis pour cette version. GitHub Pages et GitHub Actions suffisent et sont gratuits pour ce projet public.


## Mise à jour Tesla sur Mac

Tesla bloque les serveurs GitHub Actions avec une erreur HTTP 403.  
Le workflow Tesla automatique a donc été retiré.

Double-cliquer sur `Mettre_a_jour_Tesla.command`, puis publier les fichiers modifiés avec GitHub Desktop.

Voir `MISE_A_JOUR_TESLA_MAC.md`.


## V3.2 — Playwright

La mise à jour Tesla utilise maintenant un véritable navigateur Chromium via Playwright.

- installation automatique au premier lancement ;
- test sur une station avant le traitement complet ;
- mode navigateur visible disponible avec `Tester_Tesla_avec_navigateur.command`.


## Diagnostic Playwright

Lancer `Diagnostiquer_Tesla.command` si la mise à jour échoue.


## V3.3
La mise à jour Tesla se fait via `firefox_extension`. Lire `MISE_A_JOUR_TESLA_FIREFOX.md`.
