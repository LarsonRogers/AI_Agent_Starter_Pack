#!/usr/bin/env bash
# tools/delegate.sh — dispatch one briefing to the local Light-tier endpoint
# (v13, Amendment 02). The delegation protocol's transport: never call the
# endpoint raw.
#
# Contract: health check before dispatch; single-flight mkdir lock (portable —
# flock is absent on Git Bash) with stale reclaim; hard request timeout; request
# = BRIEFING file + the fablized-micro system prompt; response printed in
# landing-report format; one JSONL metrics line per task; API key sourced at
# runtime from a user config OUTSIDE the repo and never echoed.
#
# Usage:
#   tools/delegate.sh --briefing FILE [--task-id ID] [--self-test]
#
# Config (env file, default ~/.config/fablized/local-tier.env, override path via
# FABLIZED_LOCAL_TIER_ENV; env vars): LOCAL_TIER_URL, LOCAL_TIER_MODEL, LOCAL_TIER_API_KEY,
# optional LOCAL_TIER_TIMEOUT (s, default 300), LOCAL_TIER_LOCK_STALE (s, default
# 900). Overrides for tests: LOCAL_TIER_METRICS (metrics file path).

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MICRO="$ROOT/adapters/system-prompt/fablized-micro.md"
METRICS="${LOCAL_TIER_METRICS:-$ROOT/var/metrics/local-tier.jsonl}"
LOCKDIR="${LOCAL_TIER_LOCKDIR:-$ROOT/var/lock/local-tier.lock}"

BRIEFING=""
TASK_ID="task-$$"
SELF_TEST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --briefing) BRIEFING="${2:-}"; shift 2 ;;
    --task-id)  TASK_ID="${2:-}"; shift 2 ;;
    --self-test) SELF_TEST=1; shift ;;
    *) echo "delegate.sh: unknown argument: $1"; exit 2 ;;
  esac
done

load_config() {
  cfg="${FABLIZED_LOCAL_TIER_ENV:-$HOME/.config/fablized/local-tier.env}"
  # shellcheck disable=SC1090 # user config, path outside the repo by design
  [ -f "$cfg" ] && . "$cfg"
  URL="${LOCAL_TIER_URL:-}"
  MODEL="${LOCAL_TIER_MODEL:-unknown}"
  TIMEOUT="${LOCAL_TIER_TIMEOUT:-300}"
  STALE="${LOCAL_TIER_LOCK_STALE:-900}"
  if [ -z "$URL" ]; then
    echo "delegate.sh: no LOCAL_TIER_URL configured (env file: $cfg)"; exit 2
  fi
}

auth_curl() {
  curl -sS -H "Authorization: Bearer ${LOCAL_TIER_API_KEY:-}" "$@"  # key from the env file (outside the repo); never printed
}

health_check() {
  # Order covers both endpoint shapes (decision 13): llama-server (/health),
  # any OpenAI-compatible incl. Ollama's shim (/v1/models), Ollama native (/api/tags).
  echo "health: checking $URL"
  auth_curl -f --max-time 5 -o /dev/null "$URL/health" 2>/dev/null && return 0
  auth_curl -f --max-time 5 -o /dev/null "$URL/v1/models" 2>/dev/null && return 0
  auth_curl -f --max-time 5 -o /dev/null "$URL/api/tags" 2>/dev/null && return 0
  return 1
}

acquire_lock() {
  mkdir -p "$(dirname "$LOCKDIR")" 2>/dev/null  # parent only — the lock mkdir must stay bare (atomic)
  if mkdir "$LOCKDIR" 2>/dev/null; then return 0; fi
  now="$(date +%s)"
  mt="$(date -r "$LOCKDIR" +%s 2>/dev/null || echo "$now")"
  if [ $((now - mt)) -gt "$STALE" ]; then
    rmdir "$LOCKDIR" 2>/dev/null && echo "stale lock reclaimed (${STALE}s timeout)" \
      && mkdir "$LOCKDIR" 2>/dev/null && return 0
  fi
  echo "delegate.sh: lock held ($LOCKDIR) — one task at a time on a single-GPU endpoint"
  return 1
}

release_lock() { rmdir "$LOCKDIR" 2>/dev/null || true; }

record_metric() {
  # $1 status, $2 tokens_in, $3 tokens_out, $4 duration_ms — no content, no key.
  mkdir -p "$(dirname "$METRICS")"
  printf '{"ts":"%s","task_id":"%s","model":"%s","tokens_in":%s,"tokens_out":%s,"duration_ms":%s,"status":"%s"}\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$TASK_ID" "$MODEL" "$2" "$3" "$4" "$1" >> "$METRICS"
}

dispatch() {
  [ -f "$BRIEFING" ] || { echo "delegate.sh: briefing file not found: $BRIEFING"; exit 2; }
  [ -f "$MICRO" ] || { echo "delegate.sh: micro prompt missing: $MICRO (run tools/build.py)"; exit 2; }

  if ! health_check; then
    echo "[OBSERVED] local tier unreachable: health check failed for $URL (/health and /v1/models)."
    echo "Per the delegation protocol: queue this task or escalate to the capable tier per the briefing's Budget & escalation line."
    exit 3
  fi

  acquire_lock || exit 4
  trap release_lock EXIT

  start_ms="$(python -c 'import time;print(int(time.time()*1000))')"
  payload="$(python - "$MICRO" "$BRIEFING" "$MODEL" <<'PYEOF'
import json, sys
micro, briefing, model = open(sys.argv[1], encoding="utf-8").read(), open(sys.argv[2], encoding="utf-8").read(), sys.argv[3]
print(json.dumps({
    "model": model,
    "messages": [
        {"role": "system", "content": micro},
        {"role": "user", "content": briefing +
         "\n\nReturn your result as a landing report: outcome first; "
         "Verified (with how, [OBSERVED]); Assumed/unverified; "
         "Noticed but not done; Remaining risk."},
    ],
    "temperature": 0.2,
}))
PYEOF
)"

  resp_file="$(mktemp)"
  do_request() {
    auth_curl --max-time "$TIMEOUT" -H "Content-Type: application/json" \
      -d "$payload" "$URL/v1/chat/completions" -o "$resp_file" 2>/dev/null
  }

  if ! do_request; then
    # At most ONE retry, and only after a fresh health check passes.
    if health_check && do_request; then
      :
    else
      dur=$(( $(python -c 'import time;print(int(time.time()*1000))') - start_ms ))
      record_metric "failed" 0 0 "$dur"
      echo "[OBSERVED] local tier unreachable: request to $URL timed out or failed (after one health-gated retry)."
      echo "Queue or escalate to the capable tier per the briefing's Budget & escalation line."
      rm -f "$resp_file"
      exit 3
    fi
  fi

  dur=$(( $(python -c 'import time;print(int(time.time()*1000))') - start_ms ))
  python - "$resp_file" <<'PYEOF'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
print(r["choices"][0]["message"]["content"])
u = r.get("usage", {})
print("\n---\ntokens_in=%s tokens_out=%s" % (u.get("prompt_tokens", 0), u.get("completion_tokens", 0)), file=sys.stderr)
PYEOF
  usage="$(python - "$resp_file" <<'PYEOF'
import json, sys
u = json.load(open(sys.argv[1], encoding="utf-8")).get("usage", {})
print(u.get("prompt_tokens", 0), u.get("completion_tokens", 0))
PYEOF
)"
  rm -f "$resp_file"
  record_metric "ok" "${usage% *}" "${usage#* }" "$dur"
}

self_test() {
  self="$ROOT/tools/delegate.sh"
  tdir="$(mktemp -d)"
  status=0
  briefing="$tdir/briefing.md"
  printf '## Goal\nSay OK.\n## Done means\nOutput contains OK.\n' > "$briefing"
  metrics="$tdir/metrics.jsonl"
  export LOCAL_TIER_API_KEY=x  # synthetic test value, standing in for the env file

  # --- a) endpoint down: claim-tagged, nonzero, ONE health check, no JSONL ----
  out="$(LOCAL_TIER_URL=http://127.0.0.1:59999 LOCAL_TIER_MODEL=m \
         FABLIZED_LOCAL_TIER_ENV=/nonexistent LOCAL_TIER_METRICS="$metrics" \
         LOCAL_TIER_LOCKDIR="$tdir/lock1" bash "$self" --briefing "$briefing" 2>&1)" \
    && { echo "self-test FAIL: down endpoint exited 0"; status=1; }
  case "$out" in *"[OBSERVED] local tier unreachable"*) echo "self-test PASS: down endpoint claim-tagged" ;;
    *) echo "self-test FAIL: no claim-tagged unreachable line"; status=1 ;; esac
  hc="$(printf '%s\n' "$out" | grep -c '^health: checking')"
  if [ "$hc" -eq 1 ]; then echo "self-test PASS: exactly one health check, zero retries"
  else echo "self-test FAIL: $hc health checks on down path"; status=1; fi
  if [ ! -f "$metrics" ]; then echo "self-test PASS: no JSONL line on unreachable"
  else echo "self-test FAIL: metrics written on unreachable"; status=1; fi

  # --- b) mock endpoint: landing output, exit 0, exactly one JSONL line -------
  # Two shapes (decision 13): llama-server-shaped (GET /health ok) on $port and
  # Ollama-shaped (only GET /api/tags answers; /health and /v1/models 404) on $port2.
  port=58231
  port2=58232
  python - "$port" "$port2" <<'PYEOF' &
import json, sys, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
COMPLETION = {"choices": [{"message": {"content":
    "Outcome: OK printed.\nVerified: ran the check [OBSERVED].\nAssumed: none.\nNoticed but not done: none.\nRemaining risk: none."}}],
    "usage": {"prompt_tokens": 100, "completion_tokens": 42}}
def handler(shape):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, code, obj):
            b = json.dumps(obj).encode()
            self.send_response(code); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
        def do_GET(self):
            if shape == "ollama":
                if self.path == "/api/tags": self._send(200, {"models": [{"name": "mock"}]})
                else: self._send(404, {})
            else:
                self._send(200, {"status": "ok"})
        def do_POST(self):
            self.rfile.read(int(self.headers.get("Content-Length", 0)))
            self._send(200, COMPLETION)
    return H
srvs = [HTTPServer(("127.0.0.1", int(sys.argv[1])), handler("llama")),
        HTTPServer(("127.0.0.1", int(sys.argv[2])), handler("ollama"))]
for s in srvs: s.timeout = 30
def run(s):
    for _ in range(16): s.handle_request()
ts = [threading.Thread(target=run, args=(s,)) for s in srvs]
for t in ts: t.start()
for t in ts: t.join()
PYEOF
  srv_pid=$!
  sleep 1
  out="$(LOCAL_TIER_URL="http://127.0.0.1:$port" LOCAL_TIER_MODEL=mock \
         FABLIZED_LOCAL_TIER_ENV=/nonexistent LOCAL_TIER_METRICS="$metrics" \
         LOCAL_TIER_LOCKDIR="$tdir/lock2" bash "$self" --briefing "$briefing" --task-id st-mock 2>/dev/null)" \
    || { echo "self-test FAIL: mock endpoint dispatch exited nonzero"; status=1; }
  case "$out" in *"Verified"*"[OBSERVED]"*) echo "self-test PASS: landing-format output returned" ;;
    *) echo "self-test FAIL: output not landing-format"; status=1 ;; esac
  lines="$(wc -l < "$metrics" 2>/dev/null || echo 0)"
  if [ "$lines" -eq 1 ]; then echo "self-test PASS: exactly one JSONL metrics line"
  else echo "self-test FAIL: $lines metrics lines"; status=1; fi

  # --- b2) Ollama-shaped mock: health falls through to /api/tags, dispatch OK --
  out="$(LOCAL_TIER_URL="http://127.0.0.1:$port2" LOCAL_TIER_MODEL=mock-ollama \
         FABLIZED_LOCAL_TIER_ENV=/nonexistent LOCAL_TIER_METRICS="$metrics" \
         LOCAL_TIER_LOCKDIR="$tdir/lock2b" bash "$self" --briefing "$briefing" --task-id st-ollama 2>/dev/null)" \
    || { echo "self-test FAIL: ollama-shaped dispatch exited nonzero"; status=1; }
  case "$out" in *"Verified"*"[OBSERVED]"*) echo "self-test PASS: ollama-shaped endpoint served via /api/tags fallback" ;;
    *) echo "self-test FAIL: ollama-shaped output wrong"; status=1 ;; esac

  # --- c) lock (against the live mock: health precedes lock by contract) -------
  mkdir -p "$tdir/lock3"
  out="$(LOCAL_TIER_URL="http://127.0.0.1:$port" LOCAL_TIER_MODEL=mock \
         FABLIZED_LOCAL_TIER_ENV=/nonexistent LOCAL_TIER_METRICS="$metrics" \
         LOCAL_TIER_LOCKDIR="$tdir/lock3" bash "$self" --briefing "$briefing" 2>&1)" \
    && { echo "self-test FAIL: held lock did not block"; status=1; }
  case "$out" in *"lock held"*) echo "self-test PASS: second invocation fails fast on held lock" ;;
    *) echo "self-test FAIL: held lock not detected"; status=1 ;; esac
  touch -d "@$(( $(date +%s) - 2000 ))" "$tdir/lock3"
  out="$(LOCAL_TIER_URL="http://127.0.0.1:$port" LOCAL_TIER_MODEL=mock \
         FABLIZED_LOCAL_TIER_ENV=/nonexistent LOCAL_TIER_METRICS="$metrics" \
         LOCAL_TIER_LOCK_STALE=900 LOCAL_TIER_LOCKDIR="$tdir/lock3" bash "$self" --briefing "$briefing" 2>&1)"
  case "$out" in *"stale lock reclaimed"*) echo "self-test PASS: stale lock reclaimed" ;;
    *) echo "self-test FAIL: stale lock not reclaimed"; status=1 ;; esac
  kill "$srv_pid" 2>/dev/null; wait "$srv_pid" 2>/dev/null

  exit "$status"
}

if [ "$SELF_TEST" -eq 1 ]; then
  # Self-test provides its own config via env; skip load_config requirements it
  # doesn't meet by letting each sub-invocation carry its own vars.
  self_test
fi

load_config
dispatch
