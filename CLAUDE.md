# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Git GUI Commit Tool** - a desktop application built with Python and Tkinter that simplifies Git workflows for GitHub repositories. It provides a user-friendly interface for committing and pushing code to GitHub with built-in security scanning to prevent sensitive data leaks.

**Current Version**: v1.4.0
**Main File**: `git_gui_app.py`
**Executable**: `dist/GitGUI提交工具.exe`

## Key Architecture

### Application Structure

The application follows a classic Tkinter MVC pattern:

1. **`GitGuiApp` class** - Main controller that:
   - Initializes and configures the GUI (`create_widgets()`, `setup_styles()`)
   - Handles user interactions (button clicks, form validation)
   - Executes Git operations in background threads
   - Manages logging and status updates

2. **Cleanup Layer** - `cleanup_temp_files()` method:
   - Automatically removes Windows reserved device names (nul, con, prn, aux, com*, lpt*)
   - Removes common temporary files (*.tmp, *.bak, *.swp, Thumbs.db, .DS_Store, etc.)
   - Skips sensitive directories (.git, node_modules, venv, __pycache__, etc.)
   - Logs all deleted files for transparency
   - **NEW**: If a file cannot be deleted (e.g., system-protected), automatically adds it to `.gitignore`
   - Prevents "short read" errors and false success reports

3. **Security Layer** - `scan_for_sensitive_data()` method:
   - Scans code files before commit for sensitive information (API keys, passwords, tokens, private keys)
   - Uses regex patterns to detect common secrets
   - Excludes common directories (node_modules, .git, venv, etc.)
   - Filters out false positives (example values, regex definitions)

4. **Git Operations** - `execute_git_operations()` method:
   - Validates inputs
   - **NEW: Automatically cleans temp files before Git operations**
   - Performs security checks (optional but enabled by default)
   - Executes Git commands: init → add → commit → push
   - Checks if remote branch exists before pushing
   - Supports pushing to different remote branches (main/master/custom)
   - **FIXED: Properly detects and reports Git errors (no more false success)**

### Remote Branch Selection

The tool provides three options for remote push branch:
- **main** (default) - pushes to remote main branch
- **master** - pushes to remote master branch
- **custom** - allows user to specify any branch name

Before pushing, the tool:
1. Fetches latest remote info (`git fetch origin`)
2. Verifies the remote branch exists (`git rev-parse --verify origin/{branch}`)
3. If branch doesn't exist, shows error and terminates
4. Pushes using format: `git push -u origin {local_branch}:{remote_branch}`

### Configuration

**GitHub Username**: Hardcoded as `bethzyy` in `on_submit()` method (line 296):
```python
repo_url = f"git@github.com:bethzyy/{repo_name}.git"
```
To change for different users, modify this value.

**Default Code Path**: Set to `C:\D\CAIE_tool\MyAIProduct\gitTool`

**Default Branch**: `main`

## Build & Development Commands

### Development

```bash
# Run the application directly (requires Python 3.11+)
python git_gui_app.py

# Check syntax
python -m py_compile git_gui_app.py

# Install dependencies (if needed)
pip install pyinstaller
```

### Building Executable

The project uses PyInstaller to create a standalone Windows executable.

**Quick Build** (recommended):
```bash
# Windows: Double-click the batch file
build_exe.bat

# Or manually:
rm -rf build dist
python -m PyInstaller --onefile --windowed --name "GitGUI提交工具" git_gui_app.py
```

**Build Parameters**:
- `--onefile` - Creates single exe file
- `--windowed` - No console window (GUI only)
- `--name "GitGUI提交工具"` - Output filename

**Output**: `dist/GitGUI提交工具.exe` (~9.7 MB)

### Testing Changes

After modifying `git_gui_app.py`:
1. Close any running instances of the exe
2. Run `build_exe.bat` or manual PyInstaller command
3. Test the new exe in `dist/` folder

## Important Implementation Details

### GUI Layout (v1.3.0)

Window size: **550x600 pixels** (compact design)

Component order:
1. Title (reduced padding)
2. **GitHub Configuration Section**:
   - Repository name input
   - Branch selection (main/master/custom) - tightly grouped
   - Visual separator
3. **Other Configuration**:
   - Commit message
   - Code path (with browse button)
   - Security checkbox and Submit button on same row
4. Progress bar
5. Status label
6. Log output area (12 lines, optimized spacing)

### Threading Model

Git operations run in a background thread to keep GUI responsive:
```python
thread = threading.Thread(target=self.execute_git_operations,
                         args=(repo_url, commit_msg, code_path, enable_security_check, target_branch))
thread.daemon = True
thread.start()
```

### Logging System

- **File logging**: Writes to `logs/app-{date}.log`
- **GUI logging**: Displays in scrolled text area
- **Log levels**: INFO, DEBUG, WARN, ERROR, COMMAND
- All Git commands are logged with `COMMAND` level for transparency

### Error Handling

The application handles Git errors by:
- Ignoring warnings (`warning:` in stderr)
- Catching fatal errors (`fatal:` or `error:` in stderr)
- Handling "nothing to commit" gracefully
- Showing user-friendly error messages in message boxes

## File Structure

```
gitTool/
├── git_gui_app.py          # Main application source
├── build_exe.bat           # Build script
├── GitGUI提交工具.spec      # PyInstaller spec (auto-generated)
├── dist/
│   └── GitGUI提交工具.exe   # Final executable
├── build/                  # Temporary build files (can be deleted)
├── logs/                   # Application logs
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── *.md                    # Documentation files
```

## Common Modifications

### Change GitHub Username

Edit line 337 in `git_gui_app.py`:
```python
repo_url = f"git@github.com:YOUR_USERNAME/{repo_name}.git"
```

### Adjust Window Size

Edit line 21 in `git_gui_app.py`:
```python
self.root.geometry("550x600")  # width x height
```

### Modify Default Branch

Edit line 183 in `git_gui_app.py`:
```python
self.branch_var = tk.StringVar(value="main")  # Change to "master" or other
```

### Add/Remove Security Patterns

Edit `scan_for_sensitive_data()` method (line 433), modify the `patterns` dictionary.

## Dependencies

**Runtime**:
- Python 3.11.9 (development)
- Tkinter (included with Python)

**Build-time**:
- PyInstaller 6.17.0

**No pip install required** for end users - the exe is self-contained.

## Known Limitations

1. **Windows-only**: The exe is built for Windows platforms
2. **SSH-only**: Assumes SSH key authentication with GitHub
3. **Single repository**: Uses hardcoded GitHub username
4. **No branch creation**: Will not create remote branches if they don't exist

## Version History

### v1.4.0 (2025-12-30)
- **NEW**: Automatic temp file cleanup before Git operations
  - Removes Windows reserved device names (nul, con, prn, aux, com*, lpt*)
  - Removes common temp files (*.tmp, *.bak, *.swp, Thumbs.db, etc.)
  - Prevents "short read" errors caused by conflicting filenames
  - **BONUS**: If a file cannot be deleted, automatically adds it to `.gitignore`
- **FIXED**: Improved error detection logic
  - Now properly catches all `fatal:` and `error:` messages
  - Eliminates false success reports
  - Better user feedback on actual failures
- **IMPROVED**: Better logging for cleanup operations

### v1.3.0 (Initial Release)
- Basic Git GUI functionality
- Security scanning for sensitive data
- Remote branch selection (main/master/custom)
- Background thread execution
- Comprehensive logging system

## Documentation

- `exe使用说明.md` - User guide for the exe
- `重新打包说明.md` - Build instructions
- Files are in Chinese for target users
