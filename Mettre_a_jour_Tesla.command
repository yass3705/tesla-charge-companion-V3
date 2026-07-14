#!/bin/zsh
set -u
cd "$(dirname "$0")"
clear
echo "=============================================="
echo " Tesla Charge Companion — Mise à jour Tesla"
echo "=============================================="
echo
echo "Cette opération peut durer plusieurs minutes."
echo

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="$(command -v python3)"
elif [ -x "/usr/bin/python3" ]; then
  PYTHON_BIN="/usr/bin/python3"
else
  echo "ERREUR : Python 3 n'est pas disponible sur ce Mac."
  echo "Installe Python 3 depuis python.org, puis relance ce fichier."
  read "?Appuie sur Entrée pour fermer..."
  exit 1
fi

"$PYTHON_BIN" scripts/update_tesla.py \
  --stations data/tesla_stations.json \
  --delay 0.75

STATUS=$?
echo
if [ "$STATUS" -eq 0 ]; then
  echo "Mise à jour terminée."
  echo "GitHub Desktop va s'ouvrir."
  if [ -d "/Applications/GitHub Desktop.app" ]; then
    open -a "GitHub Desktop" .
  fi
  echo
  echo "Dans GitHub Desktop : Commit to main, puis Push origin."
else
  echo "La mise à jour n'a pas abouti. Consulte les messages ci-dessus."
fi
echo
read "?Appuie sur Entrée pour fermer..."
exit "$STATUS"
