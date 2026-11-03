# Install Cloudra on Windows with Setup.exe

[中文](INSTALL_WINDOWS_CN.md) · [Project home](../README.md)

Use the native Windows installer. **You do not need to install Python, Node.js, Git, or WSL first.** The package includes the runtimes, Cloudra core dependencies, JavaScript tool host, and prebuilt web interface.

The current build targets Windows 10/11 x64. The installer is unsigned; a test build is not a formal release. Install quantum-chemistry tools separately as needed.

## 1. Download the installer

When a package is available on the [releases page](https://github.com/yyywaa/Cloudra-mechanism-agent/releases), choose **Cloudra-VERSION-windows-x64-Setup.exe**. A source ZIP is not an installer.

During PR review, packages are produced by the [Windows native installer workflow](https://github.com/yyywaa/Cloudra-mechanism-agent/actions/workflows/windows-installer.yml):

1. Open a successful workflow run for the branch or PR you intend to test.
2. Under **Artifacts**, download **windows-installer-x64**. GitHub usually requires you to sign in.
3. Extract the downloaded ZIP and open **Cloudra-VERSION-windows-x64-Setup.exe** inside it.

These are test packages. Do not treat a build as verified until its installation checks pass. When the runner supports desktop capture, the same run's **windows-installer-preview** artifact contains a screenshot of the actual setup wizard.

## 2. Click through setup

1. Double-click **Setup.exe**. If Windows shows an unknown-publisher warning, verify that the file came from the repository and build above. Current packages are unsigned. Do not disable SmartScreen or security software, or bypass your organization's policy.
2. Click **Next**, read the license, choose an installation folder, and click **Install**. No model names or API keys are requested.
3. Installation is per-user and does not require administrator privileges. The default location is `%LOCALAPPDATA%\Programs\Cloudra`.
4. The desktop shortcut is selected by default; a **Cloudra** Start menu entry is also created. On the final page, leave **Launch Cloudra** checked and click **Finish** to open the interface.

Setup uses files already in the package; it does not download Python, Node.js, or frontend dependencies. Model requests and online tools still require internet access.

## 3. Start using Cloudra

Double-click **Cloudra** on the desktop or use the Start menu. It starts the local service and opens your default browser without a console window.

1. Open **Global Settings** in the left sidebar, configure the coordinator and follower models, addresses, and credentials, or select ChatGPT / Codex account login, then save.
2. Create a project, choose a working directory, and describe your research task. See the [configuration guide](CONFIGURATION.md) for model and web-search settings.
3. Install ORCA, Gaussian, xTB, CREST, or configure remote compute nodes according to your task. Installing Cloudra does not install these engines.

Closing the browser tab does not stop Cloudra or automatically end calculations. Clicking the shortcut again reopens the running service. To exit the service, select **Stop Cloudra** in the Start menu; active quantum-chemistry jobs retain their existing independent lifecycle. Before updating or uninstalling, end any research tasks you need to stop in Cloudra, then choose Stop Cloudra.

## Updates, removal, and help

- **Update:** download the new installer, stop the Cloudra service, and run setup again. Setup does not force-close running Python or quantum-chemistry processes.
- **Uninstall:** open Windows **Settings → Apps → Installed apps**, find **Cloudra**, and uninstall. Keep your project files and user data separately; they are not disposable installation files.
- **Interface will not open:** startup failures display a message. The launch log is `%LOCALAPPDATA%\Cloudra\logs\desktop-launch.log`. Share the earliest error when requesting help, after removing personal paths or credentials.
- **No desktop shortcut:** use the Start menu, or rerun setup with the desktop shortcut selected. If OneDrive manages the desktop, setup uses Windows' actual desktop directory.
- **Optional dependencies:** the package includes the core runtime. Optional chemistry, browser, PDF, visualization components, and external scientific tools need separate task-specific setup; local tools must support Windows.

See [deployment and configuration](README_EN.md#deployment-and-configuration) for SSH and Slurm remote calculations.

## Developer or source installation

Ordinary users can skip this section. To modify the code, use the [windows branch](https://github.com/yyywaa/Cloudra-mechanism-agent/tree/windows), install [Python 3.13](https://www.python.org/downloads/windows/) with **Add python.exe to PATH**, and install [Node.js 22.12 or newer](https://nodejs.org/en/download) with npm.

Extract the source into a permanent folder and double-click **install.cmd**. This source-installation path uses a console window and an internet connection to create `.venv`, install core dependencies, build the frontend, and create a shortcut pointing to the source folder. It is separate from the native Setup.exe installation above. If you move the source folder, delete its `.venv` and rerun `install.cmd`; do not delete research data or global settings.

See the [Windows packaging notes](../packaging/windows/README.md) to build the native installer.
