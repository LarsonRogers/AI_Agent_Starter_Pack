# Local tier on Windows — NSSM service (or Task Scheduler, no install)

Two ways to keep `llama-server` persistent on Windows so the KV/prompt cache
survives across agent turns. The human picks the wrapper (see README — OS decision
procedure); nothing auto-detects.

Both variants: fill `config/local-tier/llama-server.args` first, and keep the API
key OUT of the repo. The client config lives in
`%USERPROFILE%\.config\fablized\local-tier.env`; copy the shipped example and run
`python tools/delegate.py`. The service launcher uses a separate
`C:\local-tier\local-tier-server.cmd` so the client's strict parser never executes
shell syntax.

## Option A — NSSM-wrapped service

1. Install NSSM (`choco install nssm` or the zip from nssm.cc).
2. Create a launcher `local-tier.cmd` OUTSIDE the repo, e.g. `C:\local-tier\`:

   ```bat
   @echo off
   rem Populate variables from your filled .args file and server-only cmd file:
   call C:\local-tier\local-tier-server.cmd
   rem Power caps do not survive reboots — reapply at every service start.
   nvidia-smi -pl %POWER_LIMIT_W%
   set CUDA_VISIBLE_DEVICES=%CUDA_VISIBLE_DEVICES%
   llama-server -m %MODEL_PATH% -c %CTX_SIZE% -np %PARALLEL_SLOTS% ^
     --host 127.0.0.1 --port %PORT%
   ```

   Auth: llama-server reads `LLAMA_API_KEY` from its environment — the
   `local-tier-server.cmd` above sets it outside any repo. The client config carries
   the matching `LOCAL_TIER_API_KEY` as inert KEY=VALUE text. No key
   appears on the command line or in this repo.
3. `nssm install local-tier C:\local-tier\local-tier.cmd`, then
   `nssm set local-tier AppRestartDelay 5000`, `nssm start local-tier`.
4. Record the endpoint in AGENTS.md Part 2 → Model Tiers
   (URL `http://127.0.0.1:<port>`, model id, auth path, service name
   `local-tier`, decided date).

## Option B — Task Scheduler (no extra installs)

1. Same launcher script as above.
2. Task Scheduler → Create Task: run whether user is logged on or not; trigger
   **At startup**; action = the launcher; "If the task fails, restart every
   5 minutes". The power-cap line runs at every start, which is the point —
   caps reset on reboot.
3. Stop/start with `schtasks /End /TN local-tier` / `schtasks /Run /TN local-tier`.

## Notes

- Bind `127.0.0.1` only — never `0.0.0.0`. LAN/remote transport is out of scope
  for v13.1 (SSH tunnel or WireGuard is the future path if the endpoint leaves the box).
- Mixed GeForce + datacenter boxes: run the per-device dual-driver test from the
  README before trusting this setup; dual-boot Linux for the serving card is the
  fallback if one device misbehaves under the unified driver.
- Model files and agent workspaces belong on SSD/NVMe — cold-load time is part of
  every availability check.
