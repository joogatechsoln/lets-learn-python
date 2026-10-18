#!/bin/sh
# Builds a single-file AppImage. Needs appimagetool (https://github.com/AppImage/appimagetool) on your PATH.
# The AppImage uses the python3 already installed on the computer; it does not bundle Python.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(cat "$ROOT/VERSION")"
command -v appimagetool >/dev/null 2>&1 || { echo "appimagetool was not found. Download it first, then run this script again."; exit 1; }
STAGE="$(mktemp -d)"; APPDIR="$STAGE/LetsLearnPython.AppDir"
mkdir -p "$APPDIR/usr/share/lets-learn-python"
(cd "$ROOT" && tar --exclude='./packaging' --exclude='./dist' --exclude='__pycache__' --exclude='./state*.json' -cf - .) | (cd "$APPDIR/usr/share/lets-learn-python" && tar -xf -)
cat > "$APPDIR/AppRun" <<'RUN'
#!/bin/sh
HERE="$(dirname "$(readlink -f "$0")")"
export LLP_APP_DIR="$HERE/usr/share/lets-learn-python" LLP_IDLE_MINUTES=3
exec python3 "$LLP_APP_DIR/server.py" "$@"
RUN
chmod 755 "$APPDIR/AppRun"
cp "$ROOT/packaging/lets-learn-python.desktop" "$APPDIR/lets-learn-python.desktop"
cp "$ROOT/packaging/lets-learn-python.svg" "$APPDIR/lets-learn-python.svg"
mkdir -p "$ROOT/dist"
ARCH="$(uname -m)" appimagetool "$APPDIR" "$ROOT/dist/LetsLearnPython-$VERSION-$(uname -m).AppImage"
rm -rf "$STAGE"
