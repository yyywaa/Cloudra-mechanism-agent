# Native Windows installer

The normal user flow is [Setup.exe installation](../../docs/INSTALL_WINDOWS.md). The Inno Setup wizard installs a self-contained application for the current user and creates Start menu and desktop shortcuts. The Start menu also provides **Stop Cloudra**, forwarding to the existing CLI stop command. It does not install system-wide Python, change the user's PATH, download dependencies at install time, or force-close running applications.

## Build on Windows

Build prerequisites are Python 3.13, Node.js ≥ 22.12 with npm, Git, and Inno Setup 6. These are build-machine tools; end users do not need them.

From a checkout of the `windows` branch:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File packaging/windows/build.ps1
```

The script creates `dist/Cloudra-VERSION-windows-x64-Setup.exe`. Intermediate files are under `%TEMP%\cloudra-windows-package`, which the build recreates. A short staging path keeps Inno Setup below its source-path limit even when the checkout lives in a deeply nested folder. The final `dist` directory is ignored by Git.

The payload contains:

- `resources/python`: the official x64 embeddable CPython runtime and core Python dependencies, including Cloudra and its JavaScript host dependencies.
- `resources/node`: Node.js and its license; no npm is required at runtime.
- `resources/frontend`: the frontend package descriptor and prebuilt `dist`.
- `desktop_launcher.py`: a windowless shortcut entrypoint using the bundled interpreter and the existing `cloudra web --skip-build` command.
- `licenses/frontend`: production frontend dependencies' original license and notice texts, copied by the shared collector.
- `LICENSE` and `BUILD_INFO.json`: the project license, exact source commit, and runtime versions. Dependency licenses remain in their runtime distributions and wheel metadata.

Runtime downloads are checked against the official Python release checksum and Node.js SHASUMS. Python is installed into the bundle rather than frozen into a synthetic executable, so existing `sys.executable -m ...` service launches continue to use a real interpreter. No model credentials, user configuration, research data, or builder-local source path are packaged.

## Verify and preview

The [Windows native installer workflow](../../.github/workflows/windows-installer.yml) builds the EXE, runs an actual per-user silent installation into a path containing spaces, checks both shortcuts and the bundled runtimes, then starts the installed web service with isolated empty data and checks the UI and JavaScript host. No model calls or quantum-chemistry calculations are run.

The workflow uploads `windows-installer-x64` and a screenshot of the real native wizard as `windows-installer-preview`. Builds remain unsigned unless signing is explicitly configured later; this workflow does not publish a release.
