@echo off
echo ========================================
echo 创建桌面快捷方式...
echo ========================================
echo.

set EXE_PATH=%~dp0dist\GitGUI提交工具.exe
set DESKTOP=%USERPROFILE%\Desktop

echo EXE 文件: %EXE_PATH%
echo.

if not exist "%EXE_PATH%" (
    echo 错误：找不到 exe 文件！
    echo 请先运行 build_exe.bat 打包程序。
    pause
    exit /b 1
)

echo 创建快捷方式到桌面...
set SHORTCUT_VBS=%TEMP%\create_shortcut.vbs

echo Set WshShell = WScript.CreateObject("WScript.Shell") > "%SHORTCUT_VBS%"
echo Set Shortcut = WshShell.CreateShortcut("%DESKTOP%\GitGUI提交工具.lnk") >> "%SHORTCUT_VBS%"
echo Shortcut.TargetPath = "%EXE_PATH%" >> "%SHORTCUT_VBS%"
echo Shortcut.WorkingDirectory = "%~dp0" >> "%SHORTCUT_VBS%"
echo Shortcut.Description = "Git GUI 提交工具" >> "%SHORTCUT_VBS%"
echo Shortcut.Save >> "%SHORTCUT_VBS%"

cscript //nologo "%SHORTCUT_VBS%"
del "%SHORTCUT_VBS%"

echo.
echo ========================================
echo 快捷方式创建成功！
echo.
echo 位置: %DESKTOP%\GitGUI提交工具.lnk
echo.
echo 你现在可以从桌面双击运行应用了！
echo ========================================
echo.

pause
