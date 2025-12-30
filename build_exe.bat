@echo off
echo ========================================
echo 正在打包 Git GUI 提交工具...
echo ========================================
echo.

REM 尝试关闭正在运行的exe进程
echo 检查是否有正在运行的实例...
tasklist /FI "IMAGENAME eq GitGUI提交工具.exe" 2>nul | find /I "GitGUI提交工具.exe" >nul
if %ERRORLEVEL%==0 (
    echo 发现正在运行的实例，正在关闭...
    taskkill /F /IM "GitGUI提交工具.exe" >nul 2>&1
    timeout /t 2 /nobreak >nul
)

REM 清理之前的打包
if exist "build" (
    echo 清理旧的构建文件...
    rmdir /s /q build 2>nul
)

if exist "dist" (
    echo 清理旧的分发文件...
    rmdir /s /q dist 2>nul
)

echo.
echo 开始打包...
python -m PyInstaller --onefile --windowed --name "GitGUI提交工具" git_gui_app.py

echo.
echo ========================================
if exist "dist\GitGUI提交工具.exe" (
    echo 打包成功！
    echo.
    echo EXE 文件位置: dist\GitGUI提交工具.exe
    echo.
    echo 文件大小:
    for %%A in ("dist\GitGUI提交工具.exe") do echo %%~zA 字节
    echo.
    echo 你可以直接运行 dist\GitGUI提交工具.exe
) else (
    echo 打包失败！请检查错误信息。
)
echo ========================================
echo.

pause
