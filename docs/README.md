# Git GUI 提交工具

一个简洁、美观的 Git 桌面应用程序，帮助你轻松提交代码到 GitHub。

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能特性

- 🖥️ **清爽图形界面** - 现代化设计，简洁美观
- 🚀 **简化操作** - 只需输入仓库名称，自动构建完整地址
- 🔒 **可选安全扫描** - 默认开启，可检测敏感信息，防止泄露
- 📝 **完整日志** - 显示所有 Git 命令，操作透明可追溯
- ⚡ **一键提交** - 自动完成初始化、添加、提交、推送
- 🎯 **智能分支** - 自动识别当前分支
- 💾 **智能默认值** - 预填提交信息和代码路径
- 📏 **紧凑界面** - 优化布局，界面小巧精致

## 📋 前置要求

1. **Python 3.x** - [下载地址](https://www.python.org/downloads/)
2. **Git** - [下载地址](https://git-scm.com/downloads)
3. **配置 Git 用户信息**（首次使用）：
   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱"
   ```
4. **配置 GitHub SSH 密钥**（推荐）：
   - 生成 SSH 密钥：[GitHub SSH 文档](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
   - 或使用 Personal Access Token

## 🚀 快速开始

**双击启动应用**：
```
启动应用.bat
```

命令行运行：
```bash
python git_gui_app.py
```

## 📖 使用方法

### 1. 输入仓库名称
- 只需输入仓库名，例如：`myrepo`
- 程序自动构建完整地址：`git@github.com:bethzyy/{repo_name}.git`

### 2. 填写提交信息
- 默认值：`Version`
- 可自定义描述

### 3. 选择代码路径
- 默认路径：当前工具目录
- 可点击"📁 浏览"选择其他文件夹

### 4. 安全分析选项（默认选中）
- ✅ 选中：提交前扫描敏感信息（API Key、密码等）
- ❌ 未选中：跳过检查，直接提交

### 5. 点击"📤 提交到 GitHub"
- 查看实时日志输出
- 等待成功提示

## 🔒 安全检查功能

工具会自动扫描以下敏感信息：

- 🔑 **API Keys** - OpenAI、AWS、GitHub Tokens
- 🔐 **密码和Token** - 各种认证信息
- 🗝️ **私钥文件** - RSA、EC、OpenSSH
- 💾 **数据库连接** - MongoDB、MySQL、PostgreSQL、Redis
- 🔗 **Webhook URL** - Slack、Discord
- 🎫 **JWT Secret** - JWT 密钥

**如果检测到敏感信息**：
- ⚠️ 弹出安全警告
- 📍 显示问题类型、文件位置和内容
- 🚫 阻止提交，保护安全

**如果安全检查通过**：
- ✅ 自动完成代码到 GitHub 的更新

## 📋 运行日志

日志框会显示所有执行的 Git 命令：

```
[2025-12-30 08:00:00] [INFO] 开始执行 Git 提交操作
[2025-12-30 08:00:00] [COMMAND] $ cd "C:\path\to\code" && git init
[2025-12-30 08:00:01] [COMMAND] $ cd "C:\path\to\code" && git add .
[2025-12-30 08:00:02] [COMMAND] $ cd "C:\path\to\code" && git commit -m "Version"
[2025-12-30 08:00:03] [COMMAND] $ cd "C:\path\to\code" && git remote add origin git@github.com:bethzyy/repo.git
[2025-12-30 08:00:04] [COMMAND] $ cd "C:\path\to\code" && git push -u origin master
```

## 📁 项目结构

```
gitTool/
│
├── 🚀 核心应用
│   ├── git_gui_app.py        # Python 桌面应用主程序
│   └── 启动应用.bat           # 双击启动 ⭐
│
├── 📖 文档目录 (docs/)
│   ├── README.md             # 项目说明
│   ├── 快速开始.md           # 快速上手指南
│   ├── 使用说明.md           # 详细使用说明
│   ├── 文件说明.md           # 文件结构说明
│   └── CLAUDE.md             # 开发指南
│
├── 🔧 测试脚本目录 (scripts/)
│   ├── test_security_scan.py # 测试安全扫描
│   └── debug_match.py        # 调试正则匹配
│
└── 📁 运行时生成
    ├── logs/                 # 应用日志
    └── __pycache__/          # Python 缓存
```

## ⚠️ 注意事项

- 确保代码路径存在且包含要提交的文件
- 默认使用 SSH 地址：`git@github.com:bethzyy/{repo_name}.git`
- 如需修改用户名，请编辑 `git_gui_app.py` 第 296 行
- 工具会自动检测当前分支并推送到该分支
- 安全扫描会忽略 `node_modules`、`.git`、`__pycache__` 等目录

## 🔧 常见问题

### Q: 应用无法启动？

**A:** 检查以下项目：
1. Python 是否已安装：`python --version`
2. Git 是否已安装：`git --version`
3. 查看 `logs/` 目录中的日志文件

### Q: 提示"代码路径不存在"？

**A:**
- 检查输入的路径是否正确
- 使用"📁 浏览"按钮选择文件夹
- 确保使用完整路径

### Q: 推送失败，提示认证错误？

**A:** 需要配置 GitHub 凭证：
- **推荐**：使用 SSH 密钥：[生成 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
- 或使用 Personal Access Token

### Q: 检测到敏感信息但实际是安全的？

**A:**
- 检查是否使用了示例代码（如 `your_api_key`）
- 正则表达式模式定义已被过滤，不应误报
- 如果仍有误报，可以取消勾选"安全分析"选项

### Q: 提示"没有新的更改需要提交"？

**A:** 说明所有文件都是最新的，没有需要提交的修改。

### Q: 如何修改 GitHub 用户名？

**A:** 编辑 `git_gui_app.py` 文件，找到第 296 行：
```python
repo_url = f"git@github.com:bethzyy/{repo_name}.git"
```
将 `bethzyy` 改为你的 GitHub 用户名。

## 🛠️ 技术栈

- **GUI 框架**：Tkinter（Python 内置）
- **Git 操作**：subprocess 执行 Git 命令
- **安全扫描**：正则表达式模式匹配 + 上下文分析
- **日志系统**：文件 + 界面双输出
- **配色方案**：清新蓝色主题

## 📝 更新日志

### v1.3.0 (2025-12-30)
- 🎨 优化界面布局：提交信息框改为Entry控件，与其他输入框高度一致
- 📏 紧凑窗口尺寸：从600x700调整为550x650，界面更小巧
- 📦 优化间距：减少进度条和日志框之间的间距，腾出更多空间给运行日志

### v1.2.0 (2025-12-30)
- 🎨 优化界面布局：提交信息输入框改为单行，腾出更多空间给运行日志
- 🧹 清理项目：移除无用文件（nul、testSafetey.txt）
- 📚 更新文档：完善说明文档

### v1.1.0 (2025-12-30)
- ✨ 新增仓库名称输入（简化操作）
- ✨ 添加可选安全分析功能（默认开启）
- ✨ 显示所有 Git 命令（透明可追溯）
- 🎨 全新清爽界面设计
- 💾 添加智能默认值

### v1.0.0 (2024-12-29)
- ✨ 初始版本发布
- 🔒 添加安全扫描功能
- 📝 添加日志记录系统
- 🖥️ 桌面图形界面

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 👤 作者

MyAIProduct

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📚 相关文档

- [快速开始](快速开始.md) - 5分钟快速上手
- [使用说明](使用说明.md) - 详细功能说明
- [文件说明](文件说明.md) - 目录结构说明
- [开发指南](CLAUDE.md) - 代码架构说明

---

**享受简洁、美观的 Git 提交体验！** 🎉
