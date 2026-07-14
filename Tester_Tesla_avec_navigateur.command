#!/bin/zsh
set -u
cd "$(dirname "$0")"

if [ ! -d ".tesla-updater-venv" ]; then
  echo "Lance d'abord Mettre_a_jour_Tesla.command pour installer Playwright."
  read "?Appuie sur Entrée pour fermer..."
  exit 1
fi

source ".tesla-updater-venv/bin/activate"
python scripts/update_tesla.py \
  --stations data/tesla_stations.json \
  --limit 1 \
  --headed \
  --delay 1.2

read "?Appuie sur Entrée pour fermer..."
