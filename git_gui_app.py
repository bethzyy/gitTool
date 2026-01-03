#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git GUI 提交工具 - 桌面应用版本
一个简单的 Git 提交工具，带安全检查功能
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os
import sys
import re
import threading
import datetime
import json
from pathlib import Path

class GitGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git GUI 提交工具")
        self.root.geometry("550x600")
        self.root.resizable(True, True)

        # 注册窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 配置文件路径 - 正确处理PyInstaller打包后的路径
        if getattr(sys, 'frozen', False):
            # PyInstaller打包后的情况,使用EXE所在目录
            base_dir = os.path.dirname(sys.executable)
        else:
            # 正常Python脚本运行
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_dir, 'user_config.json')

        # 日志文件 (必须在 load_config 之前初始化)
        self.log_dir = Path(base_dir) / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"app-{datetime.date.today().isoformat()}.log"

        # 设置样式
        self.setup_styles()

        # 创建界面
        self.create_widgets()

        # 加载保存的配置 (现在 log_file 已经初始化了)
        self.load_config()

        self.log("INFO", f"应用程序启动 (配置文件: {self.config_file})")

    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 定义清新的配色方案
        bg_color = '#f5f6fa'  # 浅灰蓝背景
        primary_color = '#4a90e2'  # 清新蓝色
        success_color = '#52c41a'  # 成功绿
        text_color = '#2c3e50'  # 深灰文字
        border_color = '#d9e2ec'  # 边框颜色

        # 设置根窗口背景
        self.root.configure(bg=bg_color)

        # 按钮样式 - 使用渐变蓝色
        style.configure('Submit.TButton',
                       font=('Microsoft YaHei UI', 11, 'bold'),
                       padding=12,
                       background=primary_color,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        style.map('Submit.TButton',
                 background=[('active', '#357abd'),
                           ('pressed', '#2e68a8')])

        # 标题样式
        style.configure('Title.TLabel',
                       font=('Microsoft YaHei UI', 18, 'bold'),
                       foreground=text_color,
                       background=bg_color)

        # 标签样式
        style.configure('Label.TLabel',
                       font=('Microsoft YaHei UI', 10),
                       foreground='#5a6c7d',
                       background=bg_color)

        # TFrame 样式
        style.configure('TFrame',
                       background=bg_color)

        # TEntry 样式
        style.configure('TEntry',
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=8)
        style.map('TEntry',
                 bordercolor=[('focus', primary_color)],
                 lightcolor=[('focus', primary_color)],
                 darkcolor=[('focus', primary_color)])

        # TCheckbutton 样式
        style.configure('TCheckbutton',
                       font=('Microsoft YaHei UI', 9),
                       foreground='#5a6c7d',
                       background=bg_color)

        # TProgressbar 样式
        style.configure('TProgressbar',
                       thickness=8,
                       troughcolor='#e1e8ed',
                       background=primary_color,
                       borderwidth=0,
                       relief='flat')

    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置行列权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        row = 0

        # 标题 - 居中显示
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=row, column=0, columnspan=3, pady=(0, 12))
        title = ttk.Label(title_frame, text="🚀 Git GUI 提交工具",
                         style='Title.TLabel')
        title.pack()
        row += 1

        # === GitHub 仓库配置区域 ===
        # 仓库名称和推送分支放在一个区域内

        # Git 仓库名称
        ttk.Label(main_frame, text="仓库名称:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=3)
        row += 1
        self.repo_name = ttk.Entry(main_frame, width=50)
        self.repo_name.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(3, 2))
        self.repo_name.insert(0, "")
        row += 1

        # 推送分支选择（紧跟在仓库名称下面）
        ttk.Label(main_frame, text="推送分支:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=(2, 3))

        # 创建分支选择框架
        branch_frame = ttk.Frame(main_frame)
        branch_frame.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(2, 3))

        # 单选按钮变量
        self.branch_var = tk.StringVar(value="main")  # 默认为 main

        # Main 选项
        main_radio = ttk.Radiobutton(branch_frame, text="main", variable=self.branch_var, value="main")
        main_radio.grid(row=0, column=0, padx=(0, 10))

        # Master 选项
        master_radio = ttk.Radiobutton(branch_frame, text="master", variable=self.branch_var, value="master")
        master_radio.grid(row=0, column=1, padx=(0, 10))

        # 自定义分支选项
        custom_radio = ttk.Radiobutton(branch_frame, text="自定义:", variable=self.branch_var, value="custom")
        custom_radio.grid(row=0, column=2, padx=(0, 5))

        # 自定义分支名输入框
        self.custom_branch = ttk.Entry(branch_frame, width=20)
        self.custom_branch.grid(row=0, column=3, sticky=(tk.W, tk.E))

        row += 1

        # 分隔线（视觉分隔）
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(8, 10))
        row += 1

        # === 其他配置区域 ===

        # 提交信息
        ttk.Label(main_frame, text="提交信息:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=3)
        row += 1
        self.commit_msg = ttk.Entry(main_frame, width=50)
        self.commit_msg.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)
        self.commit_msg.insert(0, "Version")  # 默认值
        row += 1

        # 代码路径
        ttk.Label(main_frame, text="代码路径:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=3)
        row += 1

        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=3)
        path_frame.columnconfigure(0, weight=1)

        self.code_path = ttk.Entry(path_frame, width=40)
        self.code_path.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        # 设置默认路径
        default_path = r"C:\D\CAIE_tool\MyAIProduct\gitTool"
        self.code_path.insert(0, default_path)

        browse_btn = ttk.Button(path_frame, text="📁 浏览",
                               command=self.browse_folder,
                               width=8)
        browse_btn.grid(row=0, column=1)
        row += 1

        # 安全分析选项和提交按钮放在同一行
        self.security_check_var = tk.BooleanVar(value=True)  # 默认选中
        security_check = ttk.Checkbutton(main_frame, text="提交前进行安全分析（检查API密钥等敏感信息）",
                                        variable=self.security_check_var)
        security_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.submit_btn = ttk.Button(main_frame, text="📤 提交",
                                    style='Submit.TButton',
                                    command=self.on_submit)
        self.submit_btn.grid(row=row, column=2, pady=(10, 5))
        row += 1

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 2))
        row += 1

        # 状态标签
        self.status_label = tk.Label(main_frame, text="",
                                    font=('Microsoft YaHei UI', 9),
                                    fg='#5a6c7d',
                                    bg='#f5f6fa')
        self.status_label.grid(row=row, column=0, columnspan=3, pady=2)
        row += 1

        # 日志输出区域
        log_label = tk.Label(main_frame, text="📋 运行日志",
                            font=('Microsoft YaHei UI', 10, 'bold'),
                            fg='#2c3e50',
                            bg='#f5f6fa')
        log_label.grid(row=row, column=0, sticky=tk.W, pady=(5, 3))
        row += 1

        # 创建日志框容器
        log_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 0))
        main_frame.rowconfigure(row, weight=1)

        self.log_output = scrolledtext.ScrolledText(log_frame,
                                                    width=60,
                                                    height=12,
                                                    wrap=tk.WORD,
                                                    font=('Consolas', 9),
                                                    bg='#fafbfc',
                                                    fg='#2c3e50',
                                                    insertbackground='white',
                                                    relief='flat',
                                                    borderwidth=0,
                                                    padx=10,
                                                    pady=8,
                                                    state=tk.DISABLED)  # 初始设置为只读
        self.log_output.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        """浏览文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            self.code_path.delete(0, tk.END)
            self.code_path.insert(0, folder)

    def save_config(self):
        """保存当前界面参数到配置文件"""
        try:
            config = {
                'repo_name': self.repo_name.get().strip(),
                'commit_msg': self.commit_msg.get().strip(),
                'code_path': self.code_path.get().strip(),
                'branch_selection': self.branch_var.get(),
                'custom_branch': self.custom_branch.get().strip(),
                'security_check': self.security_check_var.get(),
                'last_saved': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # 记录详细的参数信息
            self.log("INFO", f"[配置保存] 准备保存配置到: {self.config_file}")
            self.log("INFO", f"[配置保存] 仓库名称: {config['repo_name']}")
            self.log("INFO", f"[配置保存] 提交信息: {config['commit_msg']}")
            self.log("INFO", f"[配置保存] 代码路径: {config['code_path']}")
            self.log("INFO", f"[配置保存] 分支选择: {config['branch_selection']}")
            self.log("INFO", f"[配置保存] 自定义分支: {config['custom_branch']}")
            self.log("INFO", f"[配置保存] 安全检查: {config['security_check']}")

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            self.log("INFO", f"[配置保存] 配置保存成功")
        except Exception as e:
            self.log("ERROR", f"[配置保存] 配置保存失败: {str(e)}")
            import traceback
            self.log("ERROR", f"[配置保存] 错误详情: {traceback.format_exc()}")

    def load_config(self):
        """从配置文件加载参数"""
        try:
            self.log("INFO", f"[配置加载] 配置文件路径: {self.config_file}")
            self.log("INFO", f"[配置加载] 文件是否存在: {os.path.exists(self.config_file)}")

            if not os.path.exists(self.config_file):
                self.log("INFO", "[配置加载] 配置文件不存在，使用默认值")
                return

            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            self.log("INFO", f"[配置加载] 成功读取配置文件")
            self.log("INFO", f"[配置加载] 上次保存时间: {config.get('last_saved', '未知')}")

            # 加载仓库名称
            if 'repo_name' in config and config['repo_name']:
                self.repo_name.delete(0, tk.END)
                self.repo_name.insert(0, config['repo_name'])
                self.log("INFO", f"[配置加载] ✓ 仓库名称: {config['repo_name']}")
            else:
                self.log("DEBUG", "[配置加载] 仓库名称为空，跳过")

            # 加载提交信息
            if 'commit_msg' in config and config['commit_msg']:
                self.commit_msg.delete(0, tk.END)
                self.commit_msg.insert(0, config['commit_msg'])
                self.log("INFO", f"[配置加载] ✓ 提交信息: {config['commit_msg']}")
            else:
                self.log("DEBUG", "[配置加载] 提交信息为空，跳过")

            # 加载代码路径
            if 'code_path' in config and config['code_path']:
                self.code_path.delete(0, tk.END)
                self.code_path.insert(0, config['code_path'])
                self.log("INFO", f"[配置加载] ✓ 代码路径: {config['code_path']}")
            else:
                self.log("DEBUG", "[配置加载] 代码路径为空，跳过")

            # 加载分支选择
            if 'branch_selection' in config:
                self.branch_var.set(config['branch_selection'])
                self.log("INFO", f"[配置加载] ✓ 分支选择: {config['branch_selection']}")
            else:
                self.log("DEBUG", "[配置加载] 分支选择不存在，跳过")

            # 加载自定义分支名
            if 'custom_branch' in config and config['custom_branch']:
                self.custom_branch.delete(0, tk.END)
                self.custom_branch.insert(0, config['custom_branch'])
                self.log("INFO", f"[配置加载] ✓ 自定义分支: {config['custom_branch']}")
            else:
                self.log("DEBUG", "[配置加载] 自定义分支为空，跳过")

            # 加载安全检查选项
            if 'security_check' in config:
                self.security_check_var.set(config['security_check'])
                self.log("INFO", f"[配置加载] ✓ 安全检查: {config['security_check']}")
            else:
                self.log("DEBUG", "[配置加载] 安全检查选项不存在，跳过")

            self.log("INFO", "[配置加载] ✓ 配置加载完成")
        except Exception as e:
            self.log("ERROR", f"[配置加载] 加载配置失败: {str(e)}")
            import traceback
            self.log("ERROR", f"[配置加载] 错误详情: {traceback.format_exc()}")

    def log(self, level, message, data=None):
        """记录日志"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"

        if data:
            log_message += f" | {data}"

        # 写入文件
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_message + '\n')
        except Exception as e:
            print(f"无法写入日志文件: {e}")

        # 显示在界面
        self.log_message(log_message)

    def log_message(self, message):
        """在日志区域显示消息"""
        try:
            self.log_output.config(state=tk.NORMAL)
            self.log_output.insert(tk.END, message + '\n')
            self.log_output.config(state=tk.DISABLED)
            self.log_output.see(tk.END)
            self.log_output.update_idletasks()
        except Exception as e:
            # 如果界面还未准备好，打印到控制台
            print(message)

    def update_status(self, message, color='#555'):
        """更新状态标签"""
        self.status_label.config(text=message, foreground=color)
        self.root.update_idletasks()

    def set_loading(self, loading):
        """设置加载状态"""
        if loading:
            self.submit_btn.config(state='disabled')
            self.progress.start(10)
        else:
            self.submit_btn.config(state='normal')
            self.progress.stop()

    def on_submit(self):
        """提交按钮点击事件"""
        # 保存当前参数
        self.save_config()

        # 获取输入
        repo_name = self.repo_name.get().strip()
        commit_msg = self.commit_msg.get().strip()
        code_path = self.code_path.get().strip()

        # 获取推送分支
        branch_selection = self.branch_var.get()
        if branch_selection == "custom":
            target_branch = self.custom_branch.get().strip()
            if not target_branch:
                messagebox.showerror("错误", "请输入自定义分支名")
                return
        else:
            target_branch = branch_selection

        # 验证输入
        if not repo_name:
            messagebox.showerror("错误", "请输入仓库名称")
            return

        if not commit_msg:
            messagebox.showerror("错误", "请输入提交信息")
            return

        if not code_path:
            messagebox.showerror("错误", "请选择代码路径")
            return

        if not os.path.exists(code_path):
            messagebox.showerror("错误", f"代码路径不存在: {code_path}")
            return

        # 构建完整的仓库地址
        repo_url = f"git@github.com:bethzyy/{repo_name}.git"

        # 获取安全检查选项
        enable_security_check = self.security_check_var.get()

        # 在新线程中执行
        thread = threading.Thread(target=self.execute_git_operations,
                                 args=(repo_url, commit_msg, code_path, enable_security_check, target_branch))
        thread.daemon = True
        thread.start()

    def cleanup_temp_files(self, code_path):
        """清理可能导致 Git 操作失败的临时文件

        Args:
            code_path: 代码路径

        Returns:
            list: 被删除的文件列表
        """
        import os
        deleted_files = []

        # Windows 保留设备名列表(会导致 Git 失败)
        windows_reserved_names = ['nul', 'con', 'prn', 'aux', 'com1', 'com2', 'com3', 'com4',
                                  'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2',
                                  'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']

        try:
            # 遍历代码目录
            for root, dirs, files in os.walk(code_path):
                # 跳过 .git 目录
                if '.git' in dirs:
                    dirs.remove('.git')

                # 跳过常见的虚拟环境和依赖目录
                skip_dirs = {'node_modules', 'venv', '.venv', 'env', '__pycache__', 'dist', 'build'}
                dirs[:] = [d for d in dirs if d not in skip_dirs]

                # 检查并删除临时文件
                for file in files:
                    file_lower = file.lower()

                    # 1. Windows 保留设备名
                    if file_lower in windows_reserved_names:
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                            deleted_files.append(file_path)
                            self.log("INFO", f"已删除 Windows 保留设备名文件: {file_path}")
                        except Exception as e:
                            # 如果无法删除,添加到 .gitignore
                            self.log("WARN", f"无法删除 {file_path}: {str(e)}")
                            self._add_to_gitignore(code_path, file)
                            self.log("INFO", f"已将 {file} 添加到 .gitignore")

                    # 2. 常见的临时文件模式
                    temp_patterns = ['~$', '.tmp', '.temp', '.bak', '.swp', '.DS_Store',
                                   'Thumbs.db', '.log', '.cache']

                    if any(file_lower.endswith(pattern) for pattern in temp_patterns):
                        file_path = os.path.join(root, file)
                        try:
                            os.remove(file_path)
                            deleted_files.append(file_path)
                            self.log("DEBUG", f"已删除临时文件: {file_path}")
                        except Exception as e:
                            self.log("DEBUG", f"无法删除临时文件 {file_path}: {str(e)}")

        except Exception as e:
            self.log("WARN", f"清理临时文件时出错: {str(e)}")

        return deleted_files

    def _add_to_gitignore(self, code_path, filename):
        """将文件添加到 .gitignore

        Args:
            code_path: 代码路径
            filename: 要忽略的文件名
        """
        import os
        gitignore_path = os.path.join(code_path, '.gitignore')

        try:
            # 读取现有的 .gitignore 内容
            existing_entries = set()
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    existing_entries = set(line.strip() for line in f if line.strip())

            # 如果文件名不在 .gitignore 中,添加它
            if filename not in existing_entries:
                with open(gitignore_path, 'a', encoding='utf-8') as f:
                    # 如果文件不为空且最后一行没有换行符,先添加换行
                    if os.path.getsize(gitignore_path) > 0:
                        f.write('\n')
                    f.write(f'{filename}\n')
        except Exception as e:
            self.log("DEBUG", f"更新 .gitignore 失败: {str(e)}")

    def ensure_gitignore_exists(self, code_path):
        """确保项目中存在 .gitignore 文件
        注意: 如果项目已有 .gitignore,则保持不变,不做任何修改

        Args:
            code_path: 项目根目录路径
        """
        import os
        gitignore_path = os.path.join(code_path, '.gitignore')

        try:
            # 检查 .gitignore 是否存在
            if os.path.exists(gitignore_path):
                self.log("INFO", f"✓ .gitignore 已存在,保持不变: {gitignore_path}")
            else:
                # 创建 .gitignore 文件
                self.log("INFO", f"创建 .gitignore 文件: {gitignore_path}")

                default_gitignore_content = """# 忽略可执行文件
*.exe
*.app
*.out

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv

# Node.js
node_modules/
npm-debug.log*

# 日志文件
*.log
logs/

# 临时文件
*.tmp
*.bak
*.swp
*~
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.suo
*.user

# 构建产物
dist/
build/
*.spec
"""

                with open(gitignore_path, 'w', encoding='utf-8') as f:
                    f.write(default_gitignore_content)

                self.log("INFO", "✓ .gitignore 文件创建成功 (包含 *.exe 等常见规则)")

        except Exception as e:
            self.log("WARN", f"创建/检查 .gitignore 失败: {str(e)}")

    def execute_git_operations(self, repo_url, commit_msg, code_path, enable_security_check=True, target_branch="main"):
        """执行 Git 操作"""
        try:
            self.set_loading(True)
            self.log("INFO", "开始执行 Git 提交操作")

            # 步骤0: 清理临时文件
            self.update_status("正在清理临时文件...", "#0066cc")
            self.log("INFO", "执行: 清理临时文件")
            deleted_files = self.cleanup_temp_files(code_path)
            if deleted_files:
                self.log("INFO", f"已清理 {len(deleted_files)} 个临时文件")
            else:
                self.log("INFO", "没有需要清理的临时文件")

            # 步骤0.5: 确保 .gitignore 文件存在
            self.update_status("正在检查 .gitignore...", "#0066cc")
            self.log("INFO", "执行: 检查/创建 .gitignore")
            self.ensure_gitignore_exists(code_path)

            # 步骤1: 安全检查（如果启用）
            if enable_security_check:
                self.update_status("正在执行安全检查...", "#0066cc")
                self.log("INFO", "执行安全检查...")
                security_issues = self.scan_for_sensitive_data(code_path)

                if security_issues:
                    self.set_loading(False)

                    # 显示安全问题
                    issue_text = "检测到敏感信息，为了安全起见，请先移除或替换以下内容后再提交：\n\n"
                    for issue in security_issues[:10]:  # 只显示前10个
                        issue_text += f"• 类型: {issue['category']}\n"
                        issue_text += f"  文件: {issue['file']}\n"
                        issue_text += f"  内容: {issue['match'][:80]}...\n\n"

                    if len(security_issues) > 10:
                        issue_text += f"\n... 还有 {len(security_issues) - 10} 个问题未显示"

                    messagebox.showwarning("安全警告", issue_text)
                    self.update_status("安全检查失败", "#cc0000")
                    self.log("WARN", f"发现 {len(security_issues)} 个安全问题")
                    return

                self.log("INFO", "安全检查通过")
            else:
                self.log("INFO", "安全检查已跳过")

            self.update_status("正在执行 Git 操作...", "#0066cc")

            # 步骤2: 执行 Git 命令
            commands = [
                ('检查 Git 仓库', f'cd "{code_path}" && (git rev-parse --git-dir >nul 2>&1 || git init)'),
                ('添加文件', f'cd "{code_path}" && git add .'),
                ('提交更改', f'cd "{code_path}" && git commit -m "{commit_msg}"'),
                ('添加远程仓库', f'cd "{code_path}" && (git remote add origin {repo_url} >nul 2>&1 || git remote set-url origin {repo_url} >nul 2>&1)'),
            ]

            # 执行前面的命令
            for desc, cmd in commands:
                self.log("INFO", f"执行: {desc}")
                self.log("COMMAND", f"$ {cmd}")  # 显示完整命令
                self.update_status(f"正在{desc}...", "#0066cc")

                result = subprocess.run(cmd,
                                      shell=True,
                                      capture_output=True,
                                      text=True,
                                      encoding='utf-8',
                                      errors='replace')

                if result.stdout:
                    self.log("DEBUG", result.stdout.strip())

                if result.stderr:
                    error_output = result.stderr.strip()
                    # 忽略某些警告和信息
                    if "nothing to commit" in error_output.lower():
                        self.log("INFO", "没有新的更改需要提交")
                        messagebox.showinfo("提示", "没有新的更改需要提交")
                        self.set_loading(False)
                        self.update_status("完成", "#009900")
                        return
                    elif "warning:" in error_output.lower():
                        # 警告信息，记录但不抛出异常
                        self.log("DEBUG", f"警告: {error_output}")
                    elif "fatal:" in error_output or "error:" in error_output.lower():
                        # 处理所有致命错误和错误（除了 warning）
                        raise Exception(f"Git 命令失败: {error_output}")

            # 步骤3: 检查远程分支是否存在
            self.update_status("正在检查远程分支...", "#0066cc")
            self.log("INFO", f"检查远程分支 '{target_branch}' 是否存在")

            # 先确保远程仓库信息是最新的
            fetch_cmd = f'cd "{code_path}" && git fetch origin'
            self.log("COMMAND", f"$ {fetch_cmd}")
            fetch_result = subprocess.run(fetch_cmd,
                                         shell=True,
                                         capture_output=True,
                                         text=True,
                                         encoding='utf-8',
                                         errors='replace')

            # 检查远程分支是否存在
            check_branch_cmd = f'cd "{code_path}" && git rev-parse --verify origin/{target_branch}'
            self.log("COMMAND", f"$ {check_branch_cmd}")
            check_result = subprocess.run(check_branch_cmd,
                                        shell=True,
                                        capture_output=True,
                                        text=True,
                                        encoding='utf-8',
                                        errors='replace')

            if check_result.returncode != 0:
                # 远程分支不存在,询问用户是否创建
                self.set_loading(False)  # 暂时停止加载状态以便显示对话框
                self.log("WARN", f"远程分支 '{target_branch}' 不存在")

                question_msg = f"远程仓库中不存在分支 '{target_branch}'。\n\n是否要创建并推送该分支?"
                result = messagebox.askyesno("创建分支", question_msg, icon='question')

                if not result:
                    # 用户选择不创建
                    self.log("INFO", "用户取消创建分支")
                    self.update_status("操作已取消", "#cc0000")
                    return

                # 用户确认创建分支
                self.log("INFO", f"用户确认创建远程分支 '{target_branch}'")
                self.set_loading(True)  # 恢复加载状态

            self.log("INFO", f"远程分支 '{target_branch}' 准备就绪")

            # 获取当前分支名
            get_branch_cmd = f'cd "{code_path}" && git rev-parse --abbrev-ref HEAD'
            self.log("COMMAND", f"$ {get_branch_cmd}")
            branch_result = subprocess.run(get_branch_cmd,
                                         shell=True,
                                         capture_output=True,
                                         text=True,
                                         encoding='utf-8',
                                         errors='replace')
            current_branch = branch_result.stdout.strip() or "master"
            self.log("INFO", f"当前本地分支: {current_branch}")

            # 步骤4: 推送到远程仓库的指定分支(如果不存在会自动创建)
            push_cmd = f'cd "{code_path}" && git push -u origin {current_branch}:{target_branch}'
            branch_action = "创建并推送" if check_result.returncode != 0 else "推送到"
            self.log("INFO", f"执行: {branch_action}远程分支 '{target_branch}'")
            self.log("COMMAND", f"$ {push_cmd}")
            self.update_status(f"正在{branch_action} {target_branch} 分支...", "#0066cc")

            result = subprocess.run(push_cmd,
                                  shell=True,
                                  capture_output=True,
                                  text=True,
                                  encoding='utf-8',
                                  errors='replace')

            if result.stdout:
                self.log("DEBUG", result.stdout.strip())

            if result.stderr:
                error_output = result.stderr.strip()
                # 忽略警告，只处理真正的错误
                if "warning:" in error_output.lower():
                    self.log("DEBUG", f"警告: {error_output}")
                elif "fatal:" in error_output or ("error:" in error_output.lower() and "short read" not in error_output.lower()):
                    raise Exception(f"Git 命令失败: {error_output}")

            # 成功
            self.log("INFO", "Git 操作成功完成")
            self.update_status("提交成功！", "#009900")
            messagebox.showinfo("成功", "代码已成功提交到 GitHub！")

        except Exception as e:
            error_msg = str(e)
            self.log("ERROR", error_msg)
            self.update_status("操作失败", "#cc0000")
            messagebox.showerror("错误", f"操作失败：\n{error_msg}")

        finally:
            self.set_loading(False)

    def scan_for_sensitive_data(self, dir_path):
        """扫描敏感数据"""
        issues = []

        # 敏感信息模式
        patterns = {
            'API Key': [
                r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9_-]{20,}["\']?',
                r'["\']sk_[a-zA-Z0-9_-]{20,}["\']',  # OpenAI
                r'["\']AKIA[0-9A-Z]{16}["\']',  # AWS
            ],
            '密码': [
                r'password\s*[=:]\s*["\'][^"\']{4,}["\']',
                r'passwd\s*[=:]\s*["\'][^"\']{4,}["\']',
            ],
            'Token': [
                r'token\s*[=:]\s*["\'][a-zA-Z0-9_-]{20,}["\']',
                r'bearer\s+[a-zA-Z0-9_-]{20,}',
            ],
            '私钥': [
                r'-----BEGIN\s+RSA\s+PRIVATE\s+KEY-----',
                r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----',
            ],
            '数据库连接': [
                r'mongodb://[^@]+@',
                r'mysql://[^:]+:[^@]+@',
            ],
        }

        # 忽略的目录
        ignore_dirs = {'node_modules', '.git', 'venv', '__pycache__',
                      'dist', 'build', '.venv', 'target', 'bin', 'obj'}

        # 支持的文件扩展
        text_extensions = {'.js', '.ts', '.py', '.java', '.go', '.rs',
                          '.c', '.cpp', '.h', '.php', '.rb', '.swift',
                          '.json', '.xml', '.yaml', '.yml', '.toml',
                          '.env', '.txt', '.md', '.sh', '.bash'}

        try:
            for root, dirs, files in os.walk(dir_path):
                # 过滤忽略的目录
                dirs[:] = [d for d in dirs if d not in ignore_dirs]

                for file in files:
                    file_path = Path(root) / file
                    ext = file_path.suffix.lower()

                    # 只扫描文本文件
                    if ext not in text_extensions and file != '.env' and file != 'Dockerfile':
                        continue

                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')

                        for category, regex_list in patterns.items():
                            for pattern in regex_list:
                                matches = re.finditer(pattern, content, re.IGNORECASE)
                                for match in matches:
                                    matched_text = match.group()

                                    # 排除假阳性
                                    # 1. 示例和占位符
                                    if any(keyword in matched_text.lower()
                                          for keyword in ['your_', 'replace_', 'example',
                                                         'xxxxx', '*****', 'your_api_key',
                                                         '<username>', '<password>']):
                                        continue

                                    # 2. Python 代码中的正则表达式定义
                                    # 检查是否匹配了代码中的正则表达式模式字符串
                                    # 特征: 包含 [^ 说明是正则字符类
                                    if '[^' in matched_text:
                                        # 检查源代码中匹配位置前后的字符
                                        start_pos = match.start()
                                        end_pos = match.end()

                                        # 获取上下文（前后各5个字符）
                                        context_start = max(0, start_pos - 5)
                                        context_end = min(len(content), end_pos + 5)
                                        context = content[context_start:context_end]

                                        # 如果上下文中包含引号或r前缀，说明是正则定义
                                        if "'" in context or '"' in context or "r'" in context or 'r"' in context:
                                            continue

                                    issues.append({
                                        'category': category,
                                        'file': str(file_path.relative_to(dir_path)),
                                        'match': matched_text[:100]
                                    })

                    except Exception as e:
                        self.log("DEBUG", f"无法读取文件 {file_path}: {e}")

        except Exception as e:
            self.log("ERROR", f"扫描目录失败: {e}")

        return issues

    def on_closing(self):
        """窗口关闭事件处理"""
        # 保存当前参数
        self.save_config()
        # 关闭窗口
        self.root.destroy()

def main():
    """主函数"""
    root = tk.Tk()
    app = GitGuiApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
