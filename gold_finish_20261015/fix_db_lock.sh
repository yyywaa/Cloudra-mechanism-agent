#!/usr/bin/env bash
# 2026-10-15 compute.db persistent write-lock recovery (documented routine).
# Step 1: TERM only the API (uvicorn) -> launcher respawns it pinned to --port 8000.
# Step 2: wait for health; if not healthy, fall back to restart_cloudra_web_8000.sh.
# Step 3: verify compute.db writability and print the verdict.
LOG=/home/ly/Cloudra-mechanism-agent/gold_finish_20261015/db_lock_recovery.log
exec >>"$LOG" 2>&1
echo "=== recovery begin $(date -Is) ==="
echo "uvicorn before: [$(pgrep -af 'uvicorn cloudra.services.api_v2' | tr '\n' '|')]"
echo "scheduler before: [$(pgrep -af cloudra.scheduler | tr '\n' '|')]"
for p in $(pgrep -f 'uvicorn cloudra.services.api_v2'); do kill -TERM "$p" 2>/dev/null; done
sleep 10
OK=no
for i in $(seq 1 45); do
  if curl -s -o /dev/null -m 2 http://127.0.0.1:8000/; then OK=yes; break; fi
  sleep 2
done
echo "auto-respawn healthy8000=$OK at $(date -Is)"
if [ "$OK" != yes ]; then
  echo "fallback: restart_cloudra_web_8000.sh"
  /home/ly/restart_cloudra_web_8000.sh 5
fi
python3 - <<'PY'
import sqlite3, time
db = "/home/ly/.local/share/cloudra/compute.db"
t0 = time.time()
try:
    c = sqlite3.connect(db, timeout=10.0)
    c.execute("BEGIN IMMEDIATE"); c.execute("ROLLBACK"); c.close()
    print("DB WRITE OK after %.1fs" % (time.time() - t0))
except Exception as e:
    print("DB WRITE FAIL after %.1fs" % (time.time() - t0), type(e).__name__, e)
PY
echo "uvicorn after: [$(pgrep -af 'uvicorn cloudra.services.api_v2' | tr '\n' '|')]"
echo "scheduler after: [$(pgrep -af cloudra.scheduler | tr '\n' '|')]"
echo "=== recovery end $(date -Is) ==="
