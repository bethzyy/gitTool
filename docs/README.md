# Git GUI 提交工具

一个简洁的 Git 桌面应用程序，帮助你轻松提交代码到 GitHub。

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能特性

- 🖥️ **桌面图形界面** - 基于 Tkinter 的原生应用
- 🔒 **安全扫描** - 自动检测敏感信息，防止泄露
- 📝 **实时日志** - 详细的操作日志和状态显示
- 🚀 **一键操作** - 自动完成初始化、添加、提交、推送
- 📅 **日志记录** - 每日日志文件，方便追溯
- 🎯 **分支检测** - 自动识别当前分支

## 📋 前置要求

1. **Python 3.x** - [下载地址](https://www.python.org/downloads/)
2. **Git** - [下载地址](https://git-scm.com/downloads)
3. **配置 Git 用户信息**（首次使用）：
   ```bash
   git config --global user.name "你的名字"
   git config --global user.email "你的邮箱"
   ```

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

1. **Git 仓库地址**
   - 输入你的 GitHub 仓库地址
   - 示例：`https://github.com/username/repo.git`

2. **提交信息**
   - 描述这次提交的更改内容
   - 示例：`更新了主页样式`

3. **代码路径**
   - 输入要提交的代码所在文件夹的完整路径
   - 或点击"浏览..."按钮选择文件夹
   - 示例：`C:\Users\YourName\project`

4. **点击"提交到 GitHub"按钮**

5. **等待处理完成**
   - 查看实时日志输出
   - 等待成功提示

## 🔒 安全检查功能

工具会自动扫描以下敏感信息：

- 🔑 **API Keys** - OpenAI、AWS 等
- 🔐 **密码和Token** - 各种认证信息
- 🗝️ **私钥文件** - RSA、EC、OpenSSH
- 💾 **数据库连接** - MongoDB、MySQL、PostgreSQL
- 🔗 **Webhook URL** - Slack、Discord
- 🎫 **JWT Secret** - JWT 密钥

如果检测到敏感信息，会：
- ⚠️ 弹出安全警告
- 📍 显示文件位置和内容
- 🚫 阻止提交，保护安全

## 📁 项目结构

```
gitTool/
│
├── git_gui_app.py          # 主程序文件
├── 启动应用.bat            # 启动脚本 ⭐
├── docs/                   # 文档目录
│   ├── README.md          # 项目说明
│   ├── 快速开始.md        # 快速上手指南
│   ├── 使用说明.md        # 详细使用说明
│   ├── 文件说明.md        # 文件结构说明
│   └── CLAUDE.md          # 开发指南
│
├── scripts/                # 测试脚本目录
│   ├── test_security_scan.py # 测试安全扫描
│   └── debug_match.py     # 调试正则匹配
│
└── logs/                   # 日志目录（运行时生成）
    ├── app-YYYY-MM-DD.log # 应用日志
```

## ⚠️ 注意事项

- 确保代码路径存在且包含要提交的文件
- 如果是私有仓库，需要提前配置 GitHub 认证
- 首次推送到新仓库时，可能需要在 GitHub 上确认
- 工具会自动检测当前分支并推送到该分支
- 扫描会忽略 `node_modules`、`.git`、`__pycache__` 等目录

## 🔧 常见问题

### Q: 应用无法启动？

**A:** 检查以下项目：
1. Python 是否已安装：`python --version`
2. Git 是否已安装：`git --version`
3. 查看 `logs/` 目录中的日志文件

### Q: 提示"代码路径不存在"？

**A:**
- 检查输入的路径是否正确
- 使用"浏览..."按钮选择文件夹
- 确保使用完整路径

### Q: 推送失败，提示认证错误？

**A:** 需要配置 GitHub 凭证：
- 使用 SSH 密钥：[生成 SSH 密钥](https://docs.github.com/zh/authentication/connecting-to-github-with-ssh)
- 或使用 Personal Access Token

### Q: 检测到敏感信息但实际是安全的？

**A:**
- 检查是否使用了示例代码（如 `your_api_key`）
- 正则表达式模式定义可能被误报，已添加过滤逻辑
- 如果仍有误报，可以临时修改 `git_gui_app.py` 中的扫描规则

### Q: 提示"没有新的更改需要提交"？

**A:** 说明所有文件都是最新的，没有需要提交的修改。

## 🛠️ 技术栈

- **GUI 框架**：Tkinter（Python 内置）
- **Git 操作**：subprocess 执行 Git 命令
- **安全扫描**：正则表达式模式匹配
- **日志系统**：文件 + 界面双输出

## 📝 更新日志

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

- [快速开始](docs/快速开始.md) - 5分钟快速上手
- [使用说明](docs/使用说明.md) - 详细功能说明
- [文件说明](docs/文件说明.md) - 目录结构说明
- [开发指南](docs/CLAUDE.md) - 代码架构说明

---

**享受简洁的 Git 提交体验！** 🎉
