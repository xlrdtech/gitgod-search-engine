#!/bin/bash

# GitGod Railway Deployment Script
# For GitHub account: xlrdtech

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  GitGod Railway Deployment Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if we're in the right directory
if [ ! -f "main.py" ] || [ ! -f "Procfile" ]; then
    echo -e "${RED}Error: Please run this script from the gitgod directory${NC}"
    echo -e "${YELLOW}Expected files: main.py, Procfile${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Found required files${NC}"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing Git repository...${NC}"
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
else
    echo -e "${GREEN}✓ Git repository already exists${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}Creating .gitignore...${NC}"
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
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
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi

# Optimize requirements for Railway
echo -e "${YELLOW}Optimizing requirements for Railway deployment...${NC}"
if [ -f "requirements-railway.txt" ]; then
    cp requirements-railway.txt requirements.txt.railway
    echo -e "${GREEN}✓ Railway-optimized requirements ready${NC}"
    echo -e "${BLUE}Note: Use requirements.txt.railway for Railway deployment${NC}"
fi

# Add all files to git
echo -e "${YELLOW}Adding files to git...${NC}"
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    echo -e "${YELLOW}Committing changes...${NC}"
    git commit -m "Prepare for Railway deployment
    
- Add deployment documentation
- Optimize requirements for web deployment
- Add deployment scripts and configuration"
    echo -e "${GREEN}✓ Changes committed${NC}"
fi

# Check if remote origin exists
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Git remote already configured${NC}"
    REMOTE_URL=$(git remote get-url origin)
    echo -e "${BLUE}Remote URL: $REMOTE_URL${NC}"
else
    echo -e "${YELLOW}Setting up GitHub remote...${NC}"
    echo -e "${BLUE}Please create a repository on GitHub first:${NC}"
    echo -e "${BLUE}1. Go to https://github.com/xlrdtech${NC}"
    echo -e "${BLUE}2. Click 'New repository'${NC}"
    echo -e "${BLUE}3. Name it 'gitgod-search-engine'${NC}"
    echo -e "${BLUE}4. Make it Public${NC}"
    echo -e "${BLUE}5. Don't initialize with README${NC}"
    echo ""
    read -p "Enter your GitHub repository URL (e.g., https://github.com/xlrdtech/gitgod-search-engine.git): " REPO_URL
    
    if [ -n "$REPO_URL" ]; then
        git remote add origin "$REPO_URL"
        echo -e "${GREEN}✓ Remote origin added${NC}"
    else
        echo -e "${YELLOW}Skipping remote setup${NC}"
    fi
fi

# Push to GitHub
echo -e "${YELLOW}Ready to push to GitHub...${NC}"
read -p "Push to GitHub now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    git branch -M main
    git push -u origin main
    echo -e "${GREEN}✓ Pushed to GitHub${NC}"
else
    echo -e "${YELLOW}Skipping GitHub push${NC}"
    echo -e "${BLUE}To push later, run: git push -u origin main${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Next Steps for Railway Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}1. Go to https://railway.app${NC}"
echo -e "${GREEN}2. Sign in with your GitHub account${NC}"
echo -e "${GREEN}3. Click 'New Project'${NC}"
echo -e "${GREEN}4. Select 'Deploy from GitHub repo'${NC}"
echo -e "${GREEN}5. Choose: xlrdtech/gitgod-search-engine${NC}"
echo -e "${GREEN}6. Click 'Deploy Now'${NC}"
echo ""
echo -e "${BLUE}For detailed instructions, see: RAILWAY_DEPLOYMENT.md${NC}"
echo ""
echo -e "${YELLOW}Important: Use requirements.txt.railway for Railway deployment${NC}"
echo -e "${YELLOW}It has optimized dependencies for web deployment${NC}"
echo ""
echo -e "${GREEN}🚀 Your FastAPI search engine is ready for Railway! 🚀${NC}"