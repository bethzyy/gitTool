@echo off
echo ========================================
echo 正在打包 Git GUI 提交工具...
echo ========================================
echo.

REM 清理之前的打包
if exist "build" (
    echo 清理旧的构建文件...
    rmdir /s /q build
)

if exist "dist" (
    echo 清理旧的分发文件...
    rmdir /s /q dist
)

echo.
echo 开始打包...
pyinstaller --onefile --windowed --name "GitGUI提交工具" --icon=NONE git_gui_app.py

echo.
echo ========================================
if exist "dist\GitGUI提交工具.exe" (
    echo 打包成功！
    echo.
    echo EXE 文件位置: dist\GitGUI提交工具.exe
    echo.
    echo 你可以直接运行 dist\GitGUI提交工具.exe
) else (
    echo 打包失败！请检查错误信息。
)
echo ========================================
echo.

pause
