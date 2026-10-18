#!/bin/sh
# Installs for the current user only, with no root needed: ./packaging/install.sh   (remove with: ./packaging/install.sh --remove)
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.local/share/lets-learn-python"
BIN="$HOME/.local/bin"; APPS="$HOME/.local/share/applications"; ICONS="$HOME/.local/share/icons/hicolor/scalable/apps"
if [ "$1" = "--remove" ]; then
  rm -rf "$DEST" "$BIN/lets-learn-python" "$APPS/lets-learn-python.desktop" "$ICONS/lets-learn-python.svg"
  echo "Removed. Your progress in ~/.letslearnpython was kept."; exit 0
fi
mkdir -p "$DEST" "$BIN" "$APPS" "$ICONS"
(cd "$ROOT" && tar --exclude='./packaging' --exclude='./dist' --exclude='__pycache__' --exclude='./state*.json' -cf - .) | (cd "$DEST" && tar -xf -)
sed "s#/usr/share/lets-learn-python#$DEST#" "$ROOT/packaging/launcher.sh" > "$BIN/lets-learn-python"; chmod 755 "$BIN/lets-learn-python"
sed "s#^Exec=.*#Exec=$BIN/lets-learn-python#" "$ROOT/packaging/lets-learn-python.desktop" > "$APPS/lets-learn-python.desktop"
cp "$ROOT/packaging/lets-learn-python.svg" "$ICONS/"
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database -q "$APPS" || true
echo "Installed. Find \"Let's Learn Python\" in your applications menu, or run: $BIN/lets-learn-python"
