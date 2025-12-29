#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试安全扫描功能
"""

import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from git_gui_app import GitGuiApp
import tkinter as tk

def test_security_scan():
    """测试当前目录的安全扫描"""
    print("========================================")
    print("测试安全扫描功能")
    print("========================================\n")

    # 创建临时应用实例（只用于测试安全扫描）
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    app = GitGuiApp(root)

    # 测试扫描当前目录
    current_dir = Path(__file__).parent.parent
    print("扫描目录: %s\n" % current_dir)

    issues = app.scan_for_sensitive_data(str(current_dir))

    if issues:
        print("发现 %d 个问题:\n" % len(issues))
        for i, issue in enumerate(issues, 1):
            print("%d. 类型: %s" % (i, issue['category']))
            print("   文件: %s" % issue['file'])
            print("   内容: %s..." % issue['match'][:80])
            print()
    else:
        print("[OK] 未发现敏感信息！")
        print("[OK] 正则表达式模式已被正确过滤！")

    # 销毁窗口
    root.destroy()

    print("\n========================================")
    print("测试完成")
    print("========================================")

if __name__ == '__main__':
    test_security_scan()
