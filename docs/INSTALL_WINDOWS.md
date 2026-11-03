# Windows beginner installation: open Cloudra with a double-click

[中文](INSTALL_WINDOWS_CN.md) · [Project home](../README.md)

This guide runs Cloudra natively on Windows. You do not need WSL, Git, or terminal commands. The first installation needs an internet connection; use 64-bit Windows 10/11.

## 1. Install Python and Node.js

You only need to install these once. Skip ahead if Python ≥ 3.11, Node.js ≥ 22.12, and npm are already installed.

1. Open the [official Python Windows downloads page](https://www.python.org/downloads/windows/) and choose the **Python 3.13 Windows installer (64-bit)**. Run it, check **Add python.exe to PATH**, and click **Install Now**. Keep the default pip and Python Launcher options. Most Intel/AMD PCs use the 64-bit installer; choose the matching architecture for an ARM PC.
2. Open the [official Node.js download page](https://nodejs.org/en/download) and choose **Windows Installer (.msi)**. We suggest the **latest maintained 22.x release**, with **22.12** as the minimum. Keep the default npm and PATH options. You do not need the optional native-module compilation tools.
3. Close any installation windows opened before these installations. If Cloudra still cannot find Python or Node.js, sign out of Windows and sign back in.

See Python's official [installation steps](https://docs.python.org/3.13/using/windows.html#installation-steps) for the installer options. Do not use the embeddable ZIP distribution.

## 2. Download the Windows branch

1. Open the repository's [windows branch](https://github.com/yyywaa/Cloudra-mechanism-agent/tree/windows). Check that the branch selector says **windows**, then choose **Code → Download ZIP**. You can also [download the windows ZIP directly](https://github.com/yyywaa/Cloudra-mechanism-agent/archive/refs/heads/windows.zip).
2. Right-click the downloaded ZIP and open **Properties**. If **Unblock** appears, check it after verifying that the file came from the repository above, then apply. Right-click the ZIP and choose **Extract All**. Do not run the installer inside a ZIP preview.
3. Keep the extracted project folder in a permanent location, such as `C:\Cloudra` or a `Cloudra` folder in your user directory. Prefer a short path. The desktop shortcut will point to this folder.

Use the **windows branch** for this guide. The master branch targets Linux/macOS.

## 3. Double-click the installer

Open the project folder and double-click **install.cmd**. If file extensions are hidden, it may appear as **install**, with type “Windows Command Script.”

The window creates a project-local Python environment, installs Cloudra's core dependencies and JavaScript tool runtime, and installs and builds the web interface. Allow a few minutes for the first download and keep the window open until **Installation complete** appears. A **Cloudra** shortcut will then appear on your desktop.

Installation does not ask for model credentials or require administrator access. The script sets the PowerShell execution policy only for its own process. If Windows or an organization policy blocks execution, keep the message and contact your administrator; do not turn off protection features.

## 4. Open Cloudra from the desktop

1. Double-click **Cloudra** on your desktop. A console window opens, followed by the Cloudra interface in your default browser.
2. Open **Global Settings** in the left sidebar, fill in the coordinator and follower models, service addresses, and credentials, then save. You can also choose ChatGPT / Codex account login.
3. Create a project, choose a working directory, and describe your research task. See the [configuration guide](CONFIGURATION.md) for model and web-search settings.

Keep the console window open while using Cloudra. Closing the browser tab does not stop Cloudra. To stop the web service, press **Ctrl+C** in the console window; quantum-chemistry jobs have a separate lifecycle. Double-click the desktop shortcut to open it again. When Cloudra is already running, the shortcut reuses that service and opens the browser.

## Help

- **Python, Node.js, or npm not found:** complete step 1, sign out of Windows and back in, then run `install.cmd` again. Use the official Node.js installer with npm included.
- **Download or installation failure:** keep the specific error shown in the window. Check your connection and double-click `install.cmd` again. It reuses `.venv`, reinstalls dependencies, rebuilds the web interface, and recreates the shortcut.
- **Startup failure:** the error window stays open. Copy or capture the first error, or double-click `launch-cloudra.cmd` in the project folder.
- **No desktop shortcut:** check whether installation finished successfully. If OneDrive manages your desktop, the shortcut uses Windows' actual desktop folder. You can also use the project's `launch-cloudra.cmd` directly.
- **Project folder moved:** Python virtual environments should be recreated after moving. Delete `.venv` inside the moved project folder and double-click `install.cmd` again. The desktop shortcut updates to the new location. You do not need to delete Cloudra research data or global settings.
- **“Windows protected your PC”:** verify the source and file contents first. Follow Windows' prompts or unblock only this trusted download. Do not disable SmartScreen or security software.

The installer installs Cloudra's core runtime dependencies. Install ORCA, Gaussian, xTB, CREST, and optional chemistry, browser, PDF, or visualization dependencies separately as needed; local tools must support Windows. For remote computations, see [SSH remote nodes](../deploy/ssh_remote_node.md) and [HPC / Slurm deployment](../deploy/hpc_cluster_deployment.md).
