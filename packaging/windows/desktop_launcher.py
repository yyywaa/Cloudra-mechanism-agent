"""Windowless Windows shortcut entrypoint; the existing CLI owns the UI lifecycle."""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    resources = Path(__file__).resolve().parent / "resources"
    python = resources / "python" / "python.exe"
    command = ["stop"] if "--stop" in sys.argv[1:] else ["web", "--skip-build"]
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join((str(resources / "python"), str(resources / "node"), env.get("PATH", "")))
    env["CLOUDRA_FRONTEND_DIR"] = str(resources / "frontend")
    log_dir = Path(env["LOCALAPPDATA"]) / "Cloudra" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "desktop-launch.log"
    try:
        with log_path.open("a", encoding="utf-8") as log:
            # Descendants inherit one hidden console instead of creating visible ones.
            startup = subprocess.STARTUPINFO()
            startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startup.wShowWindow = subprocess.SW_HIDE
            process = subprocess.Popen(
                [str(python), "-m", "cloudra", *command],
                cwd=resources,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                startupinfo=startup,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            for line in process.stdout:
                # The browser receives the token directly; keep it out of launch logs.
                if line.startswith("[cloudra] web UI: "):
                    line = "[cloudra] Web interface opened in your browser.\n"
                log.write(line)
                log.flush()
            code = process.wait()
        if code not in (0, -15, 143, 241):
            raise RuntimeError(f"Cloudra exited with code {code}. See {log_path}")
    except Exception as exc:
        ctypes.windll.user32.MessageBoxW(0, str(exc), "Cloudra", 0x10)


if __name__ == "__main__":
    main()
