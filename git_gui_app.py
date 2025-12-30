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
import re
import threading
import datetime
from pathlib import Path

class GitGuiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git GUI 提交工具")
        self.root.geometry("600x700")
        self.root.resizable(True, True)

        # 设置样式
        self.setup_styles()

        # 创建界面
        self.create_widgets()

        # 日志文件
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"app-{datetime.date.today().isoformat()}.log"

        self.log("INFO", "应用程序启动")

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
        title_frame.grid(row=row, column=0, columnspan=3, pady=(0, 25))
        title = ttk.Label(title_frame, text="🚀 Git GUI 提交工具",
                         style='Title.TLabel')
        title.pack()
        row += 1

        # Git 仓库名称
        ttk.Label(main_frame, text="仓库名称:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        self.repo_name = ttk.Entry(main_frame, width=50)
        self.repo_name.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.repo_name.insert(0, "")
        row += 1

        # 提交信息
        ttk.Label(main_frame, text="提交信息:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        self.commit_msg = tk.Text(main_frame, width=50, height=4, wrap=tk.WORD)
        self.commit_msg.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        self.commit_msg.insert("1.0", "Version")  # 默认值
        row += 1

        # 代码路径
        ttk.Label(main_frame, text="代码路径:",
                 style='Label.TLabel').grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1

        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        path_frame.columnconfigure(0, weight=1)

        self.code_path = ttk.Entry(path_frame, width=40)
        self.code_path.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        # 设置默认路径为当前目录
        default_path = str(Path(__file__).parent)
        self.code_path.insert(0, default_path)

        browse_btn = ttk.Button(path_frame, text="📁 浏览",
                               command=self.browse_folder,
                               width=8)
        browse_btn.grid(row=0, column=1)
        row += 1

        # 安全分析选项
        self.security_check_var = tk.BooleanVar(value=True)  # 默认选中
        security_check = ttk.Checkbutton(main_frame, text="提交前进行安全分析（检查API密钥等敏感信息）",
                                        variable=self.security_check_var)
        security_check.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=10)
        row += 1

        # 提交按钮
        self.submit_btn = ttk.Button(main_frame, text="📤 提交到 GitHub",
                                    style='Submit.TButton',
                                    command=self.on_submit)
        self.submit_btn.grid(row=row, column=0, columnspan=3, pady=(15, 25))
        row += 1

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        row += 1

        # 状态标签
        self.status_label = tk.Label(main_frame, text="",
                                    font=('Microsoft YaHei UI', 9),
                                    fg='#5a6c7d',
                                    bg='#f5f6fa')
        self.status_label.grid(row=row, column=0, columnspan=3, pady=5)
        row += 1

        # 日志输出区域
        log_label = tk.Label(main_frame, text="📋 运行日志",
                            font=('Microsoft YaHei UI', 10, 'bold'),
                            fg='#2c3e50',
                            bg='#f5f6fa')
        log_label.grid(row=row, column=0, sticky=tk.W, pady=(15, 8))
        row += 1

        # 创建日志框容器
        log_frame = tk.Frame(main_frame, bg='white', relief='solid', borderwidth=1)
        log_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        main_frame.rowconfigure(row, weight=1)

        self.log_output = scrolledtext.ScrolledText(log_frame,
                                                    width=60,
                                                    height=15,
                                                    wrap=tk.WORD,
                                                    font=('Consolas', 9),
                                                    bg='#fafbfc',
                                                    fg='#2c3e50',
                                                    insertbackground='white',
                                                    relief='flat',
                                                    borderwidth=0,
                                                    padx=10,
                                                    pady=8)
        self.log_output.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        """浏览文件夹"""
        folder = filedialog.askdirectory()
        if folder:
            self.code_path.delete(0, tk.END)
            self.code_path.insert(0, folder)

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
        self.log_output.insert(tk.END, message + '\n')
        self.log_output.see(tk.END)
        self.root.update_idletasks()

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
        # 获取输入
        repo_name = self.repo_name.get().strip()
        commit_msg = self.commit_msg.get("1.0", tk.END).strip()
        code_path = self.code_path.get().strip()

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
                                 args=(repo_url, commit_msg, code_path, enable_security_check))
        thread.daemon = True
        thread.start()

    def execute_git_operations(self, repo_url, commit_msg, code_path, enable_security_check=True):
        """执行 Git 操作"""
        try:
            self.set_loading(True)
            self.log("INFO", "开始执行 Git 提交操作")

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
                ('检查 Git 仓库', f'cd "{code_path}" && git rev-parse --git-dir 2>nul || git init'),
                ('添加文件', f'cd "{code_path}" && git add .'),
                ('提交更改', f'cd "{code_path}" && git commit -m "{commit_msg}"'),
                ('添加远程仓库', f'cd "{code_path}" && git remote add origin {repo_url} 2>nul || git remote set-url origin {repo_url}'),
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
                    # 忽略某些警告
                    if "nothing to commit" in error_output.lower():
                        self.log("INFO", "没有新的更改需要提交")
                        messagebox.showinfo("提示", "没有新的更改需要提交")
                        self.set_loading(False)
                        self.update_status("完成", "#009900")
                        return
                    elif "fatal:" in error_output or "error:" in error_output.lower():
                        raise Exception(f"Git 命令失败: {error_output}")

            # 在提交后获取当前分支名
            get_branch_cmd = f'cd "{code_path}" && git rev-parse --abbrev-ref HEAD'
            self.log("COMMAND", f"$ {get_branch_cmd}")  # 显示命令
            branch_result = subprocess.run(get_branch_cmd,
                                         shell=True,
                                         capture_output=True,
                                         text=True,
                                         encoding='utf-8',
                                         errors='replace')
            current_branch = branch_result.stdout.strip() or "master"
            self.log("INFO", f"当前分支: {current_branch}")

            # 推送到远程仓库
            push_cmd = f'cd "{code_path}" && git push -u origin {current_branch}'
            self.log("INFO", "执行: 推送到 GitHub")
            self.log("COMMAND", f"$ {push_cmd}")  # 显示命令
            self.update_status("正在推送到 GitHub...", "#0066cc")

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
                if "fatal:" in error_output or "error:" in error_output.lower():
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

def main():
    """主函数"""
    root = tk.Tk()
    app = GitGuiApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
