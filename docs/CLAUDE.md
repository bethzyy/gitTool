# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 **Git GUI 提交工具** - Python桌面应用程序，简化Git操作并内置安全扫描功能，防止敏感信息意外泄露。

**当前版本**: v1.3.0

## 核心架构

### 应用程序结构

这是一个**单文件Python Tkinter桌面应用** (`git_gui_app.py`):

- **GUI框架**: Tkinter with ttk样式组件
- **窗口尺寸**: 550x650像素（紧凑设计）
- **线程模型**: Git操作在后台线程运行，防止UI冻结
- **日志系统**: 双输出到文件和UI（日志存储在`logs/`目录）

### 关键组件

#### 1. 仓库名称自动构建
- 用户只需输入仓库名（如 `myrepo`）
- 应用自动构建完整URL: `git@github.com:bethzyy/{repo_name}.git`
- **GitHub用户名硬编码在第296行**: 修改`bethzyy`可更改默认用户

#### 2. 统一输入控件 (v1.3.0)
所有输入字段使用`ttk.Entry`保持高度一致:
- 仓库名称 (第130行)
- 提交信息 (第139行) - v1.3.0从`tk.Text`改为`ttk.Entry`
- 代码路径 (第153行)

#### 3. 安全扫描系统

位于`scan_for_sensitive_data()`方法（第433-531行），这是**防止敏感数据泄露的最关键代码**。

**检测内容**:
- API密钥 (OpenAI `sk_*`, AWS `AKIA*`, 通用模式)
- 密码和token
- 私钥 (RSA, OpenSSH)
- 数据库连接字符串 (MongoDB, MySQL)
- JWT密钥

**假阳性过滤** (第494-517行):
- 忽略占位符文本: `your_*`, `REPLACE_`, `example`, `xxxxx`, `*****`
- **Python正则定义的关键处理**: 特殊逻辑避免标记正则字符类(`[^`)
- 检查匹配周围的上下文（前后各5个字符）以判断是否是定义模式的代码

**忽略的目录** (第463行): `node_modules`, `.git`, `venv`, `__pycache__`, `dist`, `build`, `.venv`, `target`, `bin`, `obj`

**支持的文件扩展名** (第467行): `.js`, `.ts`, `.py`, `.java`, `.go`, `.rs`, `.c`, `.cpp`, `.h`, `.php`, `.rb`, `.swift`, `.json`, `.xml`, `.yaml`, `.yml`, `.toml`, `.env`, `.txt`, `.md`, `.sh`, `.bash`

#### 4. Git操作流程

位于`execute_git_operations()`方法（第307-431行）:

**执行顺序**:
1. **安全检查**（如果通过复选框启用，默认: 开启）
2. Git初始化（如果还不是仓库）
3. `git add .`
4. `git commit -m "{message}"`
5. `git remote add/set-url origin {url}`
6. 检测当前分支（第384-393行）
7. `git push -u origin {branch}`

**错误处理**:
- "nothing to commit": 优雅处理（第370-375行）
- "warning:" 消息: 记录但不导致失败
- "fatal:" 或 "error:": 导致操作失败
- **特殊情况**: 忽略"error: short read"（Windows上nul重定向的副作用）

**平台特定**: 使用Windows风格的Git命令（`2>nul`重定向stderr，`if not exist`条件判断）

#### 5. 日志系统

**文件日志** (第227-243行):
- 位置: `logs/app-YYYY-MM-DD.log`
- 格式: `[timestamp] [level] message | data`
- UTF-8编码，错误替换

**UI日志** (第245-255行):
- ScrolledText组件处于DISABLED状态（只读）
- 临时启用写入，然后立即禁用（防止用户编辑）
- 新消息时自动滚动到末尾

### UI布局和间距 (v1.3.0)

**紧凑设计的优化间距**:
- 进度条底部边距: `pady=(0, 3)` (第181行)
- 状态标签边距: `pady=2` (第189行)
- 日志标签顶部边距: `pady=(8, 5)` (第197行)
- 这些优化为日志输出区域节省约20px垂直空间

## 运行和构建

### 开发模式

```bash
# 直接用Python运行
python git_gui_app.py

# 或使用启动脚本
启动应用.bat
```

**要求**:
- Python 3.11+ (测试版本 3.11.9)
- Tkinter (通常随Python捆绑)
- 已安装并配置Git
- GitHub SSH密钥或Personal Access Token

### 构建EXE

```bash
# 快速构建（关闭运行实例，清理，构建）
build_exe.bat

# 手动构建
python -m PyInstaller --onefile --windowed --name "GitGUI提交工具" git_gui_app.py
```

**输出**: `dist/GitGUI提交工具.exe` (~9.7 MB)

**PyInstaller参数**:
- `--onefile`: 单个可执行文件
- `--windowed`: 无控制台窗口（仅GUI）
- `--name`: 指定输出文件名

## 重要开发说明

### 修改UI

1. **所有输入控件应使用`ttk.Entry`**保持高度一致（单行输入不要用`tk.Text`）
2. **保持紧凑间距** - 设计目标是550x650窗口
3. **使用ttk组件和自定义样式**，在`setup_styles()`中定义（第37-103行）
4. **配色方案** (第43-47行):
   - 背景: `#f5f6fa`
   - 主色: `#4a90e2`
   - 成功: `#52c41a`
   - 文字: `#2c3e50`

### 修改安全模式

**警告**: 假阳性过滤器很复杂。添加新模式时:

1. 对真实代码库进行全面测试
2. 检查Python代码中的正则模式定义不会被标记
3. 上下文检查逻辑（第505-517行）很关键 - 它检测匹配是否在定义正则模式的字符串字面量内
4. 在`patterns`字典中添加新模式（第438-460行）

### 更改Git用户名

编辑第296行:
```python
repo_url = f"git@github.com:bethzyy/{repo_name}.git"
```
将`bethzyy`替换为目标GitHub用户名。

### 线程安全

- Git操作在守护线程中运行（第304行）
- 来自后台线程的UI更新使用`update_idletasks()`（第260, 252行）
- **永远不要阻塞主线程** - 始终在线程中运行长操作

### 文件编码

- 所有文件读取使用`encoding='utf-8', errors='ignore'`（第486行）
- 这优雅地处理各种编码
- Git命令使用`encoding='utf-8', errors='replace'`（第361行）

## 项目结构

```
gitTool/
├── git_gui_app.py           # 主应用（单文件包含所有内容）
├── build_exe.bat            # PyInstaller构建脚本
├── 启动应用.bat              # 快速启动脚本
├── 创建快捷方式.bat          # 创建桌面快捷方式
├── GitGUI提交工具.spec      # PyInstaller规范（自动生成）
├── exe使用说明.md           # EXE用户文档
├── 重新打包说明.md          # 构建说明
├── docs/                    # 文档目录
│   ├── README.md           # 项目主README
│   ├── 快速开始.md          # 快速入门指南
│   ├── 使用说明.md          # 详细使用指南
│   ├── 文件说明.md          # 文件结构说明
│   └── CLAUDE.md           # 本文件
├── scripts/                 # 测试工具（如果存在）
├── logs/                    # 应用日志（自动创建）
├── build/                   # PyInstaller构建产物（自动生成）
└── dist/                    # 最终EXE输出（自动生成）
    └── GitGUI提交工具.exe   # 可分发的可执行文件
```

## 常见问题

### 问题: 出现"nothing to commit"消息
**原因**: 所有文件都是最新的
**行为**: 应用检测到此情况并通知用户（第370-375行）

### 问题: 安全扫描器错误标记代码
**原因**: 源代码中的正则模式定义匹配了这些模式
**修复**: 上下文检查器（第505-517行）应该处理此问题，但新模式可能需要改进

### 问题: 无法在UI中修改GitHub用户名
**当前限制**: 用户名硬编码
**变通方法**: 编辑`git_gui_app.py`第296行

### 问题: EXE无法启动
**检查**:
1. Git已安装
2. SSH密钥已配置
3. Windows Defender未阻止（添加到排除项）
