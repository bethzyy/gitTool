# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Git GUI Commit Tool** - a desktop application built with Python and Tkinter that simplifies Git workflows for GitHub repositories. It provides a user-friendly interface for committing and pushing code to GitHub with built-in security scanning to prevent sensitive data leaks.

**Current Version**: v1.6.0
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
   - If a file cannot be deleted (e.g., system-protected), automatically adds it to `.gitignore`
   - Prevents "short read" errors and false success reports

3. **Configuration Layer** - `save_config()` and `load_config()` methods:
   - Automatically saves user parameters on submit and window close
   - Loads saved parameters on startup
   - Saves to `user_config.json` in exe directory (handles PyInstaller paths correctly)
   - Detailed logging of all saved/loaded parameters for debugging

4. **.gitignore Management** - `ensure_gitignore_exists()` method:
   - Checks if project has `.gitignore` before Git operations
   - If exists: **keeps it completely unchanged** (respects user configuration)
   - If missing: creates new `.gitignore` with common rules including `*.exe`
   - Runs between cleanup and security check phases

5. **Security Layer** - `scan_for_sensitive_data()` method:
   - Scans code files before commit for sensitive information (API keys, passwords, tokens, private keys)
   - Uses regex patterns to detect common secrets
   - Excludes common directories (node_modules, .git, venv, etc.)
   - Filters out false positives (example values, regex definitions)

6. **Git Operations** - `execute_git_operations()` method:
   - Validates inputs
   - Execution order: cleanup → ensure .gitignore → security check → Git init/add/commit → remote setup → branch check → push
   - Checks if remote branch exists before pushing
   - **NEW**: If remote branch doesn't exist, asks user whether to create it
   - Supports pushing to different remote branches (main/master/custom)
   - Properly detects and reports Git errors (no more false success)

### Remote Branch Selection

The tool provides three options for remote push branch:
- **main** (default) - pushes to remote main branch
- **master** - pushes to remote master branch
- **custom** - allows user to specify any branch name

Before pushing, the tool:
1. Fetches latest remote info (`git fetch origin`)
2. Verifies the remote branch exists (`git rev-parse --verify origin/{branch}`)
3. **NEW**: If branch doesn't exist, asks user whether to create it via `messagebox.askyesno()`
4. If user confirms: `git push -u origin {local_branch}:{remote_branch}` creates new branch automatically
5. If user cancels: operation terminates

### Configuration

**GitHub Username**: Hardcoded as `bethzyy` in `on_submit()` method (line ~462):
```python
repo_url = f"git@github.com:bethzyy/{repo_name}.git"
```
To change for different users, modify this value.

**User Configuration**:
- Saved to `user_config.json` in same directory as exe (handles PyInstaller paths via `sys.frozen` check)
- Saved on: submit button click and window close
- Loaded on: application startup (after log file initialization)
- Contains: repo_name, commit_msg, code_path, branch_selection, custom_branch, security_check
- Detailed logging with `[配置保存]` and `[配置加载]` prefixes

**Default Code Path**: Set to `C:\D\CAIE_tool\MyAIProduct\gitTool`

**Default Branch**: `main`

**Initialization Order** (critical for config loading):
1. Setup paths and config_file location (checks `sys.frozen` for PyInstaller)
2. **Initialize log_file first** (must happen before load_config)
3. Setup styles
4. Create widgets
5. Load config (now log_file is available)
6. Log startup message

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
- Configuration operations use prefixes: `[配置保存]` and `[配置加载]`
- Each parameter is logged individually with value for debugging

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

## Version History

### v1.6.0 (2026-01-03)
- **NEW**: Automatic .gitignore creation for new projects
  - Creates `.gitignore` if project doesn't have one
  - Includes `*.exe` and other common ignore rules
  - **Important**: If `.gitignore` already exists, keeps it completely unchanged
  - Respects user's existing configuration

### v1.5.1 (2026-01-03)
- **FIXED**: Configuration loading failure
  - Adjusted initialization order: log_file now initialized before load_config
  - Fixed path check: changed from `.exists()` to `os.path.exists()`
- **IMPROVED**: Enhanced logging for configuration operations
  - Detailed parameter logging for save/load operations
  - Error stack traces for debugging

### v1.5.0 (2026-01-03)
- **NEW**: Automatic remote branch creation
  - Asks user if they want to create non-existent remote branch
  - Creates and pushes new branch automatically on confirmation
  - Cancels operation if user declines

### v1.4.0 (2025-12-30)
- **NEW**: Automatic temp file cleanup before Git operations
  - Removes Windows reserved device names (nul, con, prn, aux, com*, lpt*)
  - Removes common temp files (*.tmp, *.bak, *.swp, Thumbs.db, etc.)
  - Prevents "short read" errors caused by conflicting filenames
  - If a file cannot be deleted, automatically adds it to `.gitignore`
- **FIXED**: Improved error detection logic
  - Now properly catches all `fatal:` and `error:` messages
  - Eliminates false success reports

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
