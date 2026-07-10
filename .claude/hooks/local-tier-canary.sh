#!/usr/bin/env bash
# Compatibility hook wrapper around the cross-platform Python canary.
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
if python3 -c "import sys" >/dev/null 2>&1; then
  PYTHON=python3
elif python -c "import sys" >/dev/null 2>&1; then
  PYTHON=python
else
  echo "local tier: Python 3.11+ unavailable"
  exit 0
fi
exec "$PYTHON" "$ROOT/tools/local_tier_canary.py" "$@"
