# Windows 新手安装：双击打开 Cloudra

[English](INSTALL_WINDOWS.md) · [项目首页](../README_CN.md)

这份指南使用原生 Windows，不需要 WSL、Git 或手动输入命令。首次安装需要联网，建议使用 Windows 10/11 的 64 位系统。

## 1. 安装 Python 和 Node.js

两个软件只需安装一次；已安装 Python ≥ 3.11、Node.js ≥ 22.12 和 npm 的用户可直接继续。

1. 打开 [Python 官方 Windows 下载页](https://www.python.org/downloads/windows/)，选择 **Python 3.13 的 Windows installer (64-bit)**。运行安装程序，勾选 **Add python.exe to PATH**，再点 **Install Now**。保留默认的 pip 和 Python Launcher。普通 Intel/AMD 电脑使用 64-bit 安装包；ARM 电脑选择对应架构。
2. 打开 [Node.js 官方下载页](https://nodejs.org/en/download)，选择 **Windows Installer (.msi)**。建议选择 **22.x 的最新维护版本**，最低需要 **22.12**；保留默认的 npm 和 PATH 选项。额外的原生模块编译工具无需勾选。
3. 完成后关闭之前打开的安装窗口，再进行下一步。如果 Cloudra 仍提示找不到它们，重新登录 Windows 后再试。

Python 官方的安装选项说明见[安装步骤](https://docs.python.org/3.13/using/windows.html#installation-steps)。不要下载仅供嵌入程序使用的 embeddable ZIP。

## 2. 下载 Windows 版 Cloudra

1. 打开仓库的 [windows 分支](https://github.com/yyywaa/Cloudra-mechanism-agent/tree/windows)。确认页面上的分支名是 **windows**，点击绿色 **Code → Download ZIP**；也可以[直接下载 windows 分支 ZIP](https://github.com/yyywaa/Cloudra-mechanism-agent/archive/refs/heads/windows.zip)。
2. 下载后右键 ZIP → **属性**。如果底部显示“解除锁定 / Unblock”，在确认文件来自上面的仓库后勾选并确定，再右键 → **全部解压缩**。不要在 ZIP 预览窗口里运行文件。
3. 将解压出来的项目文件夹放到长期保留的位置，例如 `C:\Cloudra` 或用户目录下的 `Cloudra`。后续快捷方式会使用这个位置；尽量选较短的路径。

这里安装的是 **windows 分支**；master 分支面向 Linux/macOS。

## 3. 双击安装

打开项目文件夹，双击 **install.cmd**。如果资源管理器隐藏扩展名，它可能只显示为 **install**，类型为“Windows 命令脚本”。

窗口会依次创建项目自己的 Python 环境，下载 Cloudra 的基础依赖、JavaScript 工具运行环境和网页依赖，并构建网页。首次需要几分钟，取决于网络速度；保留窗口，直到出现 **Installation complete**。随后桌面会出现 **Cloudra** 快捷方式。

安装过程中不需要填写模型、API Key，也不需要以管理员身份运行。脚本只给这次 PowerShell 进程设置执行策略，不修改系统的执行策略。若系统或单位策略阻止执行，请保留提示并咨询管理员；不要关闭防护功能。

## 4. 从桌面打开

1. 双击桌面的 **Cloudra**。它会打开一个运行窗口，并在默认浏览器中打开 Cloudra 网页。
2. 在左侧 **全局设置（Global Settings）** 中填写主 Agent 和协作 Agent 的模型、服务地址与凭据；也可选择 ChatGPT / Codex 账号登录，然后保存。
3. 新建项目，选择工作目录，写下你的研究需求。模型与联网搜索配置见[配置指南](CONFIGURATION_CN.md)。

使用时保留运行窗口；只关闭浏览器标签页不会退出 Cloudra。需要关闭界面服务时，在运行窗口按 **Ctrl+C**；量化计算作业与网页服务的生命周期分别管理。再次使用时双击桌面快捷方式即可。若已有 Cloudra 服务，快捷方式会复用现有服务并打开网页。

## 需要帮助时

- **找不到 Python、Node.js 或 npm**：确认完成第一步；重新登录 Windows，再运行 `install.cmd`。Node.js 应使用官方安装包并包含 npm。
- **安装下载失败**：保留窗口中的具体错误，检查网络后再次双击 `install.cmd`。它会复用已有的 `.venv`，重新安装依赖、构建网页并重建快捷方式。
- **启动失败**：错误窗口会保留。复制或截图最早出现的错误；也可从项目文件夹直接双击 `launch-cloudra.cmd`。
- **桌面没有快捷方式**：查看安装窗口是否已经成功结束；桌面被 OneDrive 管理时，快捷方式使用 Windows 实际的桌面目录。可以直接使用项目内的 `launch-cloudra.cmd`。
- **移动了项目文件夹**：Python 虚拟环境不适合搬家。删除移动后项目内的 `.venv` 文件夹，再双击 `install.cmd` 重新安装；桌面快捷方式会更新到新位置。无需删除 Cloudra 的研究数据或全局配置。
- **提示 Windows 已保护你的电脑**：先确认下载来源和文件内容。仅对你信任的这份下载按系统提示处理或解除文件锁定；不要关闭 SmartScreen 或安全软件。

安装脚本仅安装 Cloudra 基础运行依赖。ORCA、Gaussian、xTB、CREST 等计算软件以及可选化学、浏览器、PDF、可视化依赖，需要按研究任务单独安装配置；本地软件还必须支持 Windows。远端计算可参考 [SSH 远端计算](../deploy/ssh_remote_node.md)与 [HPC / Slurm 部署](../deploy/hpc_cluster_deployment.md)。
