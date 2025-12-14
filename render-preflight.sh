#!/bin/bash
# Pre-deployment checklist for Render

echo "🔍 Render Deployment Pre-flight Checklist"
echo "=========================================="
echo ""

# Check if code is committed
if [[ -n $(git status -s) ]]; then
    echo "⚠️  You have uncommitted changes:"
    git status -s
    echo ""
    read -p "Commit changes now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
    fi
fi

# Check if remote exists
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No git remote 'origin' found"
    echo "   Add remote: git remote add origin <your-repo-url>"
    exit 1
else
    echo "✅ Git remote configured"
fi

# Check if branch is pushed
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null)

if [ "$LOCAL" != "$REMOTE" ]; then
    echo "⚠️  Local branch is ahead of remote"
    read -p "Push to GitHub now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin $(git branch --show-current)
    else
        echo "❌ Please push your code before deploying"
        exit 1
    fi
else
    echo "✅ Code is up to date with remote"
fi

# Check required files
echo ""
echo "📁 Checking required files..."

required_files=(
    "Dockerfile"
    "render.yaml"
    "backend/pyproject.toml"
    "frontend/package.json"
)

all_files_exist=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (missing)"
        all_files_exist=false
    fi
done

if [ "$all_files_exist" = false ]; then
    echo ""
    echo "❌ Some required files are missing"
    exit 1
fi

# Generate SECRET_KEY suggestion
echo ""
echo "🔐 Secret Key"
echo "   For production, generate a secure key:"
SECRET_KEY=$(openssl rand -hex 32 2>/dev/null || echo "run: openssl rand -hex 32")
echo "   $SECRET_KEY"
echo "   (Render will auto-generate this for you)"

echo ""
echo "✅ Pre-flight checks passed!"
echo ""
echo "📋 Next Steps:"
echo "   1. Go to https://dashboard.render.com"
echo "   2. Click 'New' → 'Blueprint'"
echo "   3. Select your GitHub repository"
echo "   4. Click 'Apply' to deploy"
echo ""
echo "📖 Full guide: See DEPLOY_RENDER.md"
echo ""
echo "🚀 Ready to deploy!"
