#!/usr/bin/env bash
# .claude/hooks/local-tier-canary.sh — SessionStart canary + endpoint discovery
# (v13, Amendments 02 + 03). NOTIFY-ONLY: prints at most a few lines and exits 0
# on every hook path.
#
# Default mode (endpoint configured): one status line —
#   local tier: up|down, <model>, ~<tok/s>, <temp>   (band via CANARY_MIN_TOKS,
#   CANARY_MAX_TEMP) — doubles as the driver-update / cooling-drift detector.
#
# --discover (decision 13, probe-then-offer): when Part 2 -> Model Tiers has no
# endpoint recorded, probe localhost 11434 (Ollama), 8080 (llama-server),
# 1234 (LM Studio), 8000 (vLLM). On a hit: identify server + models and print a
# PROPOSAL for the agent to raise — recording is ask-first, this script NEVER
# writes Part 2. Zero hits: print the ask-once tier question, exactly once.
# Probe list is env-overridable (CANARY_PROBE_SPEC="name:port ...") for tests.
#
# --discover --self-test: mock-port fixtures assert both discover behaviors.

set -u

project_dir="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
PROBE_SPEC="${CANARY_PROBE_SPEC:-ollama:11434 llama-server:8080 lm-studio:1234 vllm:8000}"

DISCOVER=0; SELF_TEST=0
for a in "$@"; do
  case "$a" in
    --discover) DISCOVER=1 ;;
    --self-test) SELF_TEST=1 ;;
    *) : ;;
  esac
done

endpoint_recorded() {
  # A recorded endpoint = the Part 2 tier-map "Local endpoint" line carries a URL.
  grep -A1 "Local endpoint" "$project_dir/AGENTS.md" 2>/dev/null | grep -q "http" && return 0
  return 1
}

probe_models() {
  # $1 = server name, $2 = port. Prints a short model list; empty on failure.
  case "$1" in
    ollama)
      curl -sf --max-time 3 "http://127.0.0.1:$2/api/tags" 2>/dev/null \
        | sed -n 's/.*"name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -3 | paste -sd ', ' - ;;
    *)
      curl -sf --max-time 3 "http://127.0.0.1:$2/v1/models" 2>/dev/null \
        | sed -n 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -3 | paste -sd ', ' - ;;
  esac
}

probe_alive() {
  # $1 = server name, $2 = port. Health probe matched to the server shape.
  case "$1" in
    ollama) curl -sf --max-time 3 -o /dev/null "http://127.0.0.1:$2/api/tags" 2>/dev/null ;;
    llama-server) curl -sf --max-time 3 -o /dev/null "http://127.0.0.1:$2/health" 2>/dev/null \
      || curl -sf --max-time 3 -o /dev/null "http://127.0.0.1:$2/v1/models" 2>/dev/null ;;
    *) curl -sf --max-time 3 -o /dev/null "http://127.0.0.1:$2/v1/models" 2>/dev/null ;;
  esac
}

discover() {
  endpoint_recorded && exit 0   # already resolved — nothing to onboard
  for entry in $PROBE_SPEC; do  # spec order IS the priority order
    name="${entry%%:*}"; port="${entry##*:}"
    if probe_alive "$name" "$port"; then
      models="$(probe_models "$name" "$port")"
      echo "local tier candidate: $name at http://127.0.0.1:$port${models:+, models: $models} — propose recording this as the Light tier in Part 2 -> Model Tiers (endpoint URL, model id, auth path, service name, date). Ask the user first; do not write Part 2 without their yes."
      exit 0
    fi
  done
  # Zero probes answered -> the single ask-once tier question, exactly once.
  echo "ask-once: no local endpoint found on 11434/8080/1234/8000 — do you want a Light-tier model for delegated checks (a local server or a cheaper API model), or shall I record single-tier? Single-tier is always valid."
  exit 0
}

discover_self_test() {
  tdir="$(mktemp -d)"
  status=0
  # Skeleton AGENTS.md: endpoint line present but no URL -> unresolved.
  printf -- '- Local endpoint (if Light is a local GPU): [URL · model id]\n' > "$tdir/AGENTS.md"

  # Mock servers on high ports: Ollama-shaped (priority 1) + llama-shaped (priority 2).
  python - 58341 58342 <<'PYEOF' &
import json, sys, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
def handler(shape):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a): pass
        def _send(self, code, obj):
            b = json.dumps(obj).encode()
            self.send_response(code); self.send_header("Content-Length", str(len(b))); self.end_headers()
            self.wfile.write(b)
        def do_GET(self):
            if shape == "ollama":
                if self.path == "/api/tags": self._send(200, {"models": [{"name": "qwen3:32b"}]})
                else: self._send(404, {})
            else:
                if self.path in ("/health", "/v1/models"): self._send(200, {"data": [{"id": "qwen-32b"}]})
                else: self._send(404, {})
    return H
srvs = [HTTPServer(("127.0.0.1", int(sys.argv[1])), handler("ollama")),
        HTTPServer(("127.0.0.1", int(sys.argv[2])), handler("llama"))]
for s in srvs: s.timeout = 20
def run(s):
    for _ in range(6): s.handle_request()
ts = [threading.Thread(target=run, args=(s,)) for s in srvs]
for t in ts: t.start()
for t in ts: t.join()
PYEOF
  srv_pid=$!
  sleep 1

  out="$(CLAUDE_PROJECT_DIR="$tdir" CANARY_PROBE_SPEC="ollama:58341 llama-server:58342" \
         bash "${BASH_SOURCE[0]}" --discover 2>&1)"; rc=$?
  case "$out" in
    *"candidate: ollama at http://127.0.0.1:58341"*) echo "self-test PASS: highest-priority hit (ollama) proposed" ;;
    *) echo "self-test FAIL: expected ollama proposal, got: $out"; status=1 ;;
  esac
  case "$out" in
    *"Ask the user first"*) echo "self-test PASS: proposal asks before writing" ;;
    *) echo "self-test FAIL: proposal does not ask first"; status=1 ;;
  esac
  [ "$rc" -eq 0 ] || { echo "self-test FAIL: discover (hit) exit $rc"; status=1; }
  kill "$srv_pid" 2>/dev/null; wait "$srv_pid" 2>/dev/null

  out="$(CLAUDE_PROJECT_DIR="$tdir" CANARY_PROBE_SPEC="ollama:58343 llama-server:58344" \
         bash "${BASH_SOURCE[0]}" --discover 2>&1)"; rc=$?
  n="$(printf '%s\n' "$out" | grep -c '^ask-once:')"
  if [ "$n" -eq 1 ] && [ "$rc" -eq 0 ]; then echo "self-test PASS: zero ports -> ask-once exactly once, exit 0"
  else echo "self-test FAIL: ask-once count=$n rc=$rc"; status=1; fi

  # Recorded endpoint -> discover stays silent.
  printf -- '- Local endpoint (if Light is a local GPU): http://127.0.0.1:9999 · m · auth · svc · 2026-07-06\n' > "$tdir/AGENTS.md"
  out="$(CLAUDE_PROJECT_DIR="$tdir" CANARY_PROBE_SPEC="ollama:58343" bash "${BASH_SOURCE[0]}" --discover 2>&1)"
  if [ -z "$out" ]; then echo "self-test PASS: recorded endpoint -> silent"
  else echo "self-test FAIL: discover spoke despite recorded endpoint"; status=1; fi
  exit "$status"
}

if [ "$DISCOVER" -eq 1 ] && [ "$SELF_TEST" -eq 1 ]; then discover_self_test; fi
if [ "$DISCOVER" -eq 1 ]; then discover; fi

# ---------------- default mode: status canary (Amendment 02) -------------------

cfg="${FABLIZED_LOCAL_TIER_ENV:-$HOME/.config/fablized/local-tier.env}"
[ -f "$cfg" ] || exit 0
# shellcheck disable=SC1090 # user config, outside the repo by design
. "$cfg" 2>/dev/null || exit 0
url="${LOCAL_TIER_URL:-}"
[ -n "$url" ] || exit 0
model="${LOCAL_TIER_MODEL:-unknown}"
min_toks="${CANARY_MIN_TOKS:-5}"
max_temp="${CANARY_MAX_TEMP:-85}"

# API key comes from the env file above; never echoed.
if ! curl -sf --max-time 4 -H "Authorization: Bearer ${LOCAL_TIER_API_KEY:-}" \
     -o /dev/null "$url/health" 2>/dev/null \
   && ! curl -sf --max-time 4 -H "Authorization: Bearer ${LOCAL_TIER_API_KEY:-}" \
     -o /dev/null "$url/v1/models" 2>/dev/null \
   && ! curl -sf --max-time 4 -H "Authorization: Bearer ${LOCAL_TIER_API_KEY:-}" \
     -o /dev/null "$url/api/tags" 2>/dev/null; then
  echo "local tier: down ($url)"
  exit 0
fi

start="$(date +%s%N 2>/dev/null || date +%s)"
resp="$(curl -sf --max-time 30 -H "Authorization: Bearer ${LOCAL_TIER_API_KEY:-}" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"$model\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with the single word: ready\"}],\"max_tokens\":24}" \
  "$url/v1/chat/completions" 2>/dev/null)" || { echo "local tier: up, $model, completion FAILED"; exit 0; }
end="$(date +%s%N 2>/dev/null || date +%s)"

toks="$(printf '%s' "$resp" | sed -n 's/.*"completion_tokens"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p' | head -1)"
[ -n "$toks" ] || toks=0
# nanosecond math when %N is real; fall back to 1s resolution otherwise
if [ "${#start}" -gt 12 ] && [ "${#end}" -gt 12 ]; then
  dur_ms=$(( (end - start) / 1000000 ))
else
  dur_ms=$(( (end - start) * 1000 ))
fi
[ "$dur_ms" -gt 0 ] 2>/dev/null || dur_ms=1
tps=$(( toks * 1000 / dur_ms ))

temp="n/a"
if command -v nvidia-smi >/dev/null 2>&1; then
  t="$(nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)"
  [ -n "$t" ] && temp="${t}C"
fi

line="local tier: up, $model, ~${tps} tok/s, $temp"
[ "$tps" -lt "$min_toks" ] 2>/dev/null && line="$line [WARN: below ${min_toks} tok/s band — driver/config regression?]"
case "$temp" in
  n/a) : ;;
  *) [ "${temp%C}" -gt "$max_temp" ] 2>/dev/null && line="$line [WARN: over ${max_temp}C — cooling drift?]" ;;
esac
echo "$line"
exit 0
