#!/bin/bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# Kill entire process group on exit so both servers die with Ctrl+C
trap 'kill 0' EXIT

echo "Starting Flask backend  → http://localhost:5001"
(cd "$ROOT/backend" && venv/bin/python app.py) &

echo "Starting React frontend → http://localhost:5173  ← open this in your browser"
(cd "$ROOT/frontend" && npm run dev) &

wait
