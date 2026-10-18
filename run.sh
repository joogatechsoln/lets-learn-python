#!/bin/sh
# Starts Let's Learn Python and opens it in your browser. Needs Python 3.8+ only.
cd "$(dirname "$0")" && exec python3 server.py "$@"
