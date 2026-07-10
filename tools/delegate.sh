#!/usr/bin/env bash
# Compatibility wrapper. Windows users may run: python tools/delegate.py ...
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if python3 -c "import sys" >/dev/null 2>&1; then
  PYTHON=python3
elif python -c "import sys" >/dev/null 2>&1; then
  PYTHON=python
else
  echo "delegate.sh: Python 3.11+ is required" >&2
  exit 1
fi
exec "$PYTHON" "$ROOT/tools/delegate.py" "$@"
