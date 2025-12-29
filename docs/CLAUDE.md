# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Git GUI Commit Tool** (Git GUI 提交工具) - a dual-interface application that provides a simplified way to commit code to GitHub with built-in security scanning to prevent accidental leakage of sensitive information.

The application provides two interfaces:
1. **Desktop Application**: Python/Tkinter GUI (`git_gui_app.py`)
2. **Web Application**: Node.js/Express server with HTML frontend (`server.js` + `index.html`)

## Key Architecture

### Dual Implementation Pattern

This project implements the same functionality in two different technology stacks:

- **Python Desktop App** (`git_gui_app.py`):
  - Uses Tkinter for native desktop GUI
  - Executes Git commands via subprocess
  - Contains security scanning logic in `scan_for_sensitive_data()` method (lines 308-403)
  - Runs operations in background threads to avoid UI freezing

- **Node.js Web App** (`server.js`):
  - Express server on port 3000
  - RESTful API endpoint: `POST /git-commit`
  - Contains security scanning logic in `scanForSensitiveData()` function (lines 108-255)
  - Serves static HTML frontend at root path

### Security Scanning System

Both implementations include **identical security scanning logic** that detects:
- API Keys (OpenAI, AWS, generic patterns)
- Passwords and authentication tokens
- Private keys (RSA, EC, OpenSSH)
- Database connection strings (MongoDB, MySQL, PostgreSQL, Redis)
- Webhook URLs (Slack, Discord)
- JWT secrets

**Critical**: The scanner uses regex pattern matching with false-positive filtering:
- Ignores placeholder text (e.g., `your_api_key`, `REPLACE_`, `example`, `xxxxx`)
- In Python: Special handling to avoid flagging regex pattern definitions in code (lines 370-389)
- In Node.js: Similar filtering for common placeholder patterns (lines 185-193)

**Ignored directories**: node_modules, .git, venv, __pycache__, dist, build, .venv, target, bin, obj

### Git Operations Flow

Both implementations execute Git commands in this sequence:
1. Check if Git repository exists (or initialize if not)
2. Add all files (`git add .`)
3. Commit with message (`git commit -m "message"`)
4. Add/set remote origin (`git remote add/set-url origin <url>`)
5. Push to remote repository (`git push -u origin <branch>`)

**Branch detection**: Python version detects current branch automatically; Node.js version pushes to `master` branch by default.

### Logging System

Both implementations maintain daily log files in the `logs/` directory:
- Python: `app-YYYY-MM-DD.log`
- Node.js: `server-YYYY-MM-DD.log`

Log format: `[timestamp] [level] message | data`

## Running the Application

### Web Application (Primary)

```bash
# Quick start (Windows)
start.bat

# Manual start
npm install       # Install dependencies (first time only)
npm start         # Start Express server on port 3000
```

Access at: http://localhost:3000

**Requirements**:
- Node.js
- Git
- npm dependencies (express, cors)

### Desktop Application (Python)

```bash
python git_gui_app.py
```

**Requirements**:
- Python 3.x
- Tkinter (usually included with Python)
- Git

### Testing Security Scanner

```bash
# Test Python version
python test_security_scan.py

# Debug regex patterns (Python)
python debug_match.py
```

## Code Structure

```
gitTool/
├── server.js                 # Node.js Express server
├── index.html                # Web frontend UI
├── git_gui_app.py            # Python Tkinter desktop app
├── package.json              # Node.js dependencies
├── start.bat                 # Windows startup script
├── test_security_scan.py     # Test scanner functionality
├── debug_match.py            # Debug regex patterns
├── logs/                     # Application logs (auto-created)
└── node_modules/             # Node.js dependencies
```

## API Endpoints

### POST /git-commit

Request body:
```json
{
  "repoUrl": "https://github.com/username/repo.git",
  "commitMsg": "Commit message here",
  "codePath": "C:\\path\\to\\code"
}
```

Response (success):
```json
{
  "success": true,
  "message": "代码成功提交到 GitHub!"
}
```

Response (security issue):
```json
{
  "success": false,
  "error": "安全检查失败！发现以下敏感信息：",
  "securityIssues": [
    {
      "category": "API Key",
      "file": "config.js",
      "match": "api_key = 'sk_1234567890abcdef...'"
    }
  ],
  "isSecurityIssue": true
}
```

## Important Notes

1. **Security False Positives**: Both implementations contain special logic to avoid flagging regex pattern definitions in source code. When modifying security patterns, test thoroughly to ensure the scanner doesn't flag code that defines similar patterns.

2. **Platform-Specific Commands**: Git commands use Windows-style syntax (`2>nul` for stderr redirect, `if not exist` for conditionals). The Python version uses cross-platform syntax where possible.

3. **Thread Safety**: Python desktop app runs Git operations in background threads to prevent UI freezing. Node.js is inherently non-blocking.

4. **Character Encoding**: Both implementations use UTF-8 encoding with error handling (`errors='replace'` or `'ignore'`) to handle various file encodings.

5. **Branch Handling**: Python version auto-detects current branch; Node.js hardcodes `master` branch for push operations.

6. **Error Handling**: Both implementations handle the "nothing to commit" scenario gracefully and inform the user accordingly.

## Development Workflow

When modifying security scanning patterns:
1. Test with `python test_security_scan.py` to verify Python implementation
2. Compare results between Python and Node.js versions
3. Ensure false-positive filters work correctly for both implementations
4. Check logs in `logs/` directory for detailed scanning information

When adding new Git operations:
1. Add commands to both `execute_git_operations()` (Python) and `executeGitCommands()` (Node.js)
2. Ensure proper error handling and logging
3. Test with both applications to verify consistent behavior
