#!/bin/zsh
set -u
cd "$(dirname "$0")"
clear

echo "================================================="
echo " Tesla Charge Companion — Mise à jour Tesla V3.2"
echo "================================================="
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERREUR : Python 3 n'est pas installé."
  echo "Installe-le depuis https://www.python.org/downloads/macos/"
  read "?Appuie sur Entrée pour fermer..."
  exit 1
fi

VENV=".tesla-updater-venv"

if [ ! -d "$VENV" ]; then
  echo "Première utilisation : création de l'environnement Python..."
  python3 -m venv "$VENV" || exit 1
fi

source "$VENV/bin/activate"

echo "Vérification de Playwright..."
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt || {
  echo "Échec de l'installation de Playwright."
  read "?Appuie sur Entrée pour fermer..."
  exit 1
}

if [ ! -d "$HOME/Library/Caches/ms-playwright" ]; then
  echo "Première utilisation : téléchargement du navigateur Chromium..."
  python -m playwright install chromium || {
    echo "Échec du téléchargement de Chromium."
    read "?Appuie sur Entrée pour fermer..."
    exit 1
  }
fi

echo
echo "Test sur une station avant la mise à jour complète..."
python scripts/update_tesla.py \
  --stations data/tesla_stations.json \
  --delay 1.2 \
  --limit 1

TEST_STATUS=$?
if [ "$TEST_STATUS" -ne 0 ]; then
  echo
  echo "Le test sur une station a échoué."
  echo "Aucune mise à jour complète n'a été lancée."
  read "?Appuie sur Entrée pour fermer..."
  exit 1
fi

echo
read "?Le test a réussi. Appuie sur Entrée pour mettre à jour les 271 stations..."

python scripts/update_tesla.py \
  --stations data/tesla_stations.json \
  --delay 1.2

STATUS=$?

echo
if [ "$STATUS" -eq 0 ]; then
  echo "Mise à jour terminée."
  if [ -d "/Applications/GitHub Desktop.app" ]; then
    open -a "GitHub Desktop" .
  fi
  echo
  echo "Dans GitHub Desktop :"
  echo "1. Summary : Mise à jour Tesla"
  echo "2. Commit to main"
  echo "3. Push origin"
else
  echo "La mise à jour n'a pas abouti."
  echo "Consulte data/tesla_update_summary.json."
fi

echo
read "?Appuie sur Entrée pour fermer..."
exit "$STATUS"
