# Windows 安装：下载 Setup.exe，点击安装

[English](INSTALL_WINDOWS.md) · [项目首页](../README_CN.md)

普通用户使用原生 Windows 安装包，**不需要预先安装 Python、Node.js、Git 或 WSL**。安装向导自带运行环境、Cloudra 基础依赖、JavaScript 工具运行环境及已构建的网页。

目前构建目标是 Windows 10/11 x64。安装包还未经过 Windows 代码签名；这不等于已经正式发布。量化软件按研究任务单独准备。

## 1. 下载安装包

如果[正式发布页](https://github.com/yyywaa/Cloudra-mechanism-agent/releases)已经提供安装包，选择 **Cloudra-版本号-windows-x64-Setup.exe**，不要下载源码 ZIP 代替安装程序。

PR 审查期间，安装包由 [Windows native installer 工作流](https://github.com/yyywaa/Cloudra-mechanism-agent/actions/workflows/windows-installer.yml)生成：

1. 打开已成功完成的构建，确认对应你要测试的分支或 PR。
2. 在页面下方 **Artifacts** 下载 **windows-installer-x64**（通常需要登录 GitHub）。
3. 解压下载的 ZIP，取出其中的 **Cloudra-版本号-windows-x64-Setup.exe**。

构建产物属于测试包；工作流通过之前不能将其视为已验证的发布版本。运行器支持桌面截图时，同一次构建的 **windows-installer-preview** 提供实际安装向导截图。

## 2. 点击安装

1. 双击 **Setup.exe**。如果 Windows 提示来自未知发布者，先确认文件来自上面的仓库和构建。当前包未签名；不要关闭 SmartScreen 或安全软件，也不要绕过单位管理策略。
2. 在原生安装向导中点 **Next**，阅读许可协议，选择安装位置，再点 **Install**。不需要填写模型名称或 API Key。
3. 安装默认仅面向当前用户，不需要管理员权限。默认位置是 `%LOCALAPPDATA%\Programs\Cloudra`。
4. “创建桌面快捷方式”默认勾选；开始菜单也会添加 **Cloudra**。安装完成后保留 **Launch Cloudra** 勾选，点 **Finish** 即可打开界面。

安装阶段使用包内文件，不再联网下载 Python、Node.js 或网页依赖。首次调用模型和联网工具仍需要网络。

## 3. 开始使用

以后双击桌面 **Cloudra**，或从开始菜单打开。它会直接启动本机服务并在默认浏览器打开 Cloudra，无需终端窗口。

1. 在左侧 **全局设置（Global Settings）** 中填写主 Agent 和协作 Agent 的模型、服务地址与凭据，或选择 ChatGPT / Codex 账号登录，然后保存。
2. 新建项目，选择工作目录，描述你的研究任务。模型及联网搜索配置见[配置指南](CONFIGURATION_CN.md)。
3. ORCA、Gaussian、xTB、CREST 等计算软件按任务单独安装或配置远端节点；安装 Cloudra 不代表这些软件也已安装。

关闭浏览器标签页不会停止 Cloudra，正在运行的计算也不会因此自动结束。再次点击快捷方式会打开已有服务。需要退出服务时，从开始菜单选择 **Stop Cloudra**；它停止 Cloudra 服务，正在运行的量化作业按既有机制自行收尾。更新或卸载前，先在 Cloudra 中结束需要停止的研究任务，再选择 Stop Cloudra。

## 更新、卸载与排错

- **更新**：下载新安装包，关闭 Cloudra 服务后重新运行安装向导。安装器不会强制结束运行中的 Python 或量化计算进程。
- **卸载**：在 Windows“设置 → 应用 → 已安装的应用”中找到 **Cloudra** 并卸载。项目文件及用户数据不属于程序安装目录中的临时文件，请自行保管。
- **打不开界面**：启动失败会弹出提示。启动日志位于 `%LOCALAPPDATA%\Cloudra\logs\desktop-launch.log`；求助时提供最早的错误，注意遮盖个人路径或凭据。
- **没有桌面图标**：可从开始菜单打开 Cloudra，或重新运行安装包并勾选桌面快捷方式。OneDrive 管理桌面时，快捷方式使用 Windows 实际的桌面目录。
- **需要可选依赖**：安装包包含基础运行依赖。可选化学、浏览器、PDF、可视化组件和外部计算软件不在基础包中，按具体任务单独配置；本地软件须支持 Windows。

SSH / Slurm 远端计算见[部署与配置](README.md#部署与配置)。

## 开发者或源码安装

只想使用软件时，无需执行本节。需要改代码的用户，使用 [windows 分支](https://github.com/yyywaa/Cloudra-mechanism-agent/tree/windows)源码并先安装 [Python 3.13](https://www.python.org/downloads/windows/)（勾选 Add python.exe to PATH）和 [Node.js 22.12 或更新版本](https://nodejs.org/en/download)（保留 npm）。

解压源码到长期保留的文件夹，双击根目录 **install.cmd**。这是带终端输出的源码安装方式，会联网创建 `.venv`、安装基础依赖及构建网页，然后创建指向源码目录的桌面快捷方式。它与上面的原生 Setup.exe 是两条不同的安装路径。移动源码文件夹后应删除其中的 `.venv`，再运行 `install.cmd`；不用删除研究数据或全局配置。

开发者构建原生安装包见[Windows 打包说明](../packaging/windows/README.md)。
