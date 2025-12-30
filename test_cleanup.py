#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试临时文件清理功能"""

import os
import sys

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

def cleanup_temp_files(code_path):
    """清理可能导致 Git 操作失败的临时文件

    Args:
        code_path: 代码路径

    Returns:
        list: 被删除的文件列表
    """
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
                        print(f"[INFO] 已删除 Windows 保留设备名文件: {file_path}")
                    except Exception as e:
                        print(f"[WARN] 无法删除 {file_path}: {str(e)}")

                # 2. 常见的临时文件模式
                temp_patterns = ['~$', '.tmp', '.temp', '.bak', '.swp', '.DS_Store',
                               'Thumbs.db', '.log', '.cache']

                if any(file_lower.endswith(pattern) for pattern in temp_patterns):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                        print(f"[DEBUG] 已删除临时文件: {file_path}")
                    except Exception as e:
                        print(f"[DEBUG] 无法删除临时文件 {file_path}: {str(e)}")

    except Exception as e:
        print(f"[WARN] 清理临时文件时出错: {str(e)}")

    return deleted_files

if __name__ == "__main__":
    test_path = r"C:\D\CAIE_tool\MyAIProduct\jobMatchTool"

    print("=" * 60)
    print("测试临时文件清理功能")
    print("=" * 60)
    print(f"\n测试路径: {test_path}\n")

    print("清理前:")
    print("-" * 60)
    os.system(f'cd "{test_path}" && ls -la | grep -E "(nul|con|aux|\.tmp|\.bak)"')

    print("\n开始清理...\n")
    deleted = cleanup_temp_files(test_path)

    print("\n清理后:")
    print("-" * 60)
    os.system(f'cd "{test_path}" && ls -la | grep -E "(nul|con|aux|\.tmp|\.bak)" || echo "没有找到临时文件"')

    print("\n" + "=" * 60)
    print(f"清理完成! 共删除 {len(deleted)} 个文件")
    print("=" * 60)
