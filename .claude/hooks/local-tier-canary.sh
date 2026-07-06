#!/usr/bin/env bash
# .claude/hooks/local-tier-canary.sh — SessionStart canary (v13, Amendment 02).
# NOTIFY-ONLY: prints ONE line about the local Light-tier endpoint and exits 0 on
# every path. Doubles as the regression detector for driver-update breakage and
# cooling drift (tok/s band + temperature threshold, both configurable).
#
# Config: same env file as tools/delegate.sh (path outside the repo,
# ~/.config/fablized/local-tier.env or FABLIZED_LOCAL_TIER_ENV). Not configured →
# silent no-op. Thresholds: CANARY_MIN_TOKS (default 5), CANARY_MAX_TEMP (default 85).

set -u

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
     -o /dev/null "$url/v1/models" 2>/dev/null; then
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
