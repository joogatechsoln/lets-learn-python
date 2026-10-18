#!/bin/sh
# Starts Let's Learn Python and opens it in the browser. Closing the browser tab ends the app after a few minutes.
APP_DIR="${LLP_APP_DIR:-/usr/share/lets-learn-python}"
export LLP_IDLE_MINUTES="${LLP_IDLE_MINUTES:-3}"
exec python3 "$APP_DIR/server.py" "$@"
