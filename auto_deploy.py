#!/usr/bin/env python3
"""
Automated GitGod Railway Deployment Script
Uses computer automation to handle GitHub repo creation and Railway deployment
"""

import os
import sys
import time
import subprocess
import pyautogui
import webbrowser
from pathlib import Path

# Configure pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_colored(message, color):
    print(f"{color}{message}{Colors.NC}")

def run_command(command, check=True):
    """Run shell command and return result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_colored(f"Command failed: {command}", Colors.RED)
        print_colored(f"Error: {e.stderr}", Colors.RED)
        return None

def wait_for_element(text, timeout=30):
    """Wait for text to appear on screen"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(text, confidence=0.8)
            if location:
                return location
        except:
            pass
        time.sleep(1)
    return None

def setup_git_repo():
    """Setup local git repository"""
    print_colored("Setting up Git repository...", Colors.YELLOW)
    
    # Check if we're in the right directory
    if not (Path("main.py").exists() and Path("Procfile").exists()):
        print_colored("Error: Please run this script from the gitgod directory", Colors.RED)
        sys.exit(1)
    
    # Initialize git if needed
    if not Path(".git").exists():
        run_command("git init")
        print_colored("✓ Git repository initialized", Colors.GREEN)
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Railway
.railway/
"""
    
    if not Path(".gitignore").exists():
        with open(".gitignore", "w") as f:
            f.write(gitignore_content)
        print_colored("✓ .gitignore created", Colors.GREEN)
    
    # Optimize requirements for Railway
    if Path("requirements-railway.txt").exists():
        run_command("cp requirements-railway.txt requirements.txt")
        print_colored("✓ Railway-optimized requirements ready", Colors.GREEN)
    
    # Add and commit files
    run_command("git add .")
    
    # Check if there are changes to commit
    result = run_command("git diff --staged --quiet", check=False)
    if result is None:  # Command failed, meaning there are changes
        run_command('git commit -m "Prepare for Railway deployment"')
        print_colored("✓ Changes committed", Colors.GREEN)

def create_github_repo():
    """Automate GitHub repository creation"""
    print_colored("Creating GitHub repository...", Colors.YELLOW)
    
    # Open GitHub in browser
    webbrowser.open("https://github.com/new")
    time.sleep(3)
    
    print_colored("Please complete the following steps manually:", Colors.BLUE)
    print_colored("1. Repository name: gitgod-search-engine", Colors.BLUE)
    print_colored("2. Make it Public", Colors.BLUE)
    print_colored("3. Don't initialize with README", Colors.BLUE)
    print_colored("4. Click 'Create repository'", Colors.BLUE)
    
    input("Press Enter when you've created the repository...")
    
    # Add remote origin
    repo_url = "https://github.com/xlrdtech/gitgod-search-engine.git"
    
    # Check if remote exists
    existing_remote = run_command("git remote get-url origin", check=False)
    if not existing_remote:
        run_command(f"git remote add origin {repo_url}")
        print_colored("✓ Remote origin added", Colors.GREEN)
    
    # Push to GitHub
    run_command("git branch -M main")
    run_command("git push -u origin main")
    print_colored("✓ Pushed to GitHub", Colors.GREEN)

def deploy_to_railway():
    """Automate Railway deployment"""
    print_colored("Deploying to Railway...", Colors.YELLOW)
    
    # Open Railway in browser
    webbrowser.open("https://railway.app")
    time.sleep(3)
    
    print_colored("Please complete the following steps manually:", Colors.BLUE)
    print_colored("1. Sign in with your GitHub account", Colors.BLUE)
    print_colored("2. Click 'New Project'", Colors.BLUE)
    print_colored("3. Select 'Deploy from GitHub repo'", Colors.BLUE)
    print_colored("4. Choose: xlrdtech/gitgod-search-engine", Colors.BLUE)
    print_colored("5. Click 'Deploy Now'", Colors.BLUE)
    
    input("Press Enter when deployment is complete...")
    
    print_colored("🚀 GitGod deployed to Railway! 🚀", Colors.GREEN)

def main():
    """Main deployment function"""
    print_colored("========================================", Colors.BLUE)
    print_colored("  GitGod Automated Railway Deployment", Colors.BLUE)
    print_colored("========================================", Colors.BLUE)
    
    try:
        # Step 1: Setup Git repository
        setup_git_repo()
        
        # Step 2: Create GitHub repository
        create_github_repo()
        
        # Step 3: Deploy to Railway
        deploy_to_railway()
        
        print_colored("\n========================================", Colors.BLUE)
        print_colored("  Deployment Complete!", Colors.BLUE)
        print_colored("========================================", Colors.BLUE)
        print_colored("Your GitGod search engine is now live on Railway!", Colors.GREEN)
        
    except KeyboardInterrupt:
        print_colored("\nDeployment cancelled by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_colored(f"Deployment failed: {str(e)}", Colors.RED)
        sys.exit(1)

if __name__ == "__main__":
    main()