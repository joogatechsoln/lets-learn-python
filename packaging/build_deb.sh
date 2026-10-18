#!/bin/sh
# Builds lets-learn-python_<version>_all.deb. Run from anywhere: ./packaging/build_deb.sh
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="$(cat "$ROOT/VERSION")"
STAGE="$(mktemp -d)"
PKG="$STAGE/lets-learn-python_${VERSION}_all"
APP="$PKG/usr/share/lets-learn-python"
mkdir -p "$APP" "$PKG/usr/bin" "$PKG/usr/share/applications" "$PKG/usr/share/icons/hicolor/scalable/apps" "$PKG/DEBIAN"
# the app itself (no packaging folder, caches, or saved progress)
(cd "$ROOT" && tar --exclude='./packaging' --exclude='__pycache__' --exclude='./state*.json' --exclude='*.pyc' -cf - .) | (cd "$APP" && tar -xf -)
install -m 755 "$ROOT/packaging/launcher.sh" "$PKG/usr/bin/lets-learn-python"
install -m 644 "$ROOT/packaging/lets-learn-python.desktop" "$PKG/usr/share/applications/lets-learn-python.desktop"
install -m 644 "$ROOT/packaging/lets-learn-python.svg" "$PKG/usr/share/icons/hicolor/scalable/apps/lets-learn-python.svg"
find "$APP" -type d -exec chmod 755 {} \; ; find "$APP" -type f -exec chmod 644 {} \;
SIZE="$(du -sk "$PKG/usr" | cut -f1)"
cat > "$PKG/DEBIAN/control" <<CTRL
Package: lets-learn-python
Version: $VERSION
Section: education
Priority: optional
Architecture: all
Depends: python3 (>= 3.8)
Recommends: bubblewrap
Installed-Size: $SIZE
Maintainer: Let's Learn Python <noreply@example.invalid>
Description: Offline Python course built around your industry
 Interactive lessons, a bug lab, a spaced-review queue and a live 3D view of the
 system you are building. Runs entirely offline in your browser.
 Installing bubblewrap adds a stronger sandbox for your code.
CTRL
cat > "$PKG/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database -q /usr/share/applications || true
command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -q -t /usr/share/icons/hicolor || true
exit 0
POST
chmod 755 "$PKG/DEBIAN/postinst"
OUT="$ROOT/dist"; mkdir -p "$OUT"
dpkg-deb --root-owner-group --build "$PKG" "$OUT/lets-learn-python_${VERSION}_all.deb"
rm -rf "$STAGE"
echo "Built $OUT/lets-learn-python_${VERSION}_all.deb"
echo "Install with: sudo apt install ./dist/lets-learn-python_${VERSION}_all.deb"
