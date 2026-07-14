# Tesla Charge Companion V3.0

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
