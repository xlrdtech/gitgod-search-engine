# 🚀 Quick Deploy GitGod to Railway

## One-Command Setup

```bash
cd /Volumes/selfexec_/dev_/New\ Installs/gitgod
./deploy.sh
```

## Manual Steps (if needed)

### 1. GitHub Setup
```bash
# Initialize and push to GitHub
git init
git add .
git commit -m "Initial commit: FastAPI search engine"
git remote add origin https://github.com/xlrdtech/gitgod-search-engine.git
git branch -M main
git push -u origin main
```

### 2. Railway Deployment
1. Go to [Railway.app](https://railway.app)
2. Sign in with GitHub account
3. New Project → Deploy from GitHub repo
4. Select: `xlrdtech/gitgod-search-engine`
5. Deploy Now

### 3. Optimize for Railway (Important!)
```bash
# Use optimized requirements
cp requirements-railway.txt requirements.txt
git add requirements.txt
git commit -m "Optimize dependencies for Railway"
git push
```

## 🎯 Your App URLs

After deployment:
- **App**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`
- **Search**: `https://your-app.railway.app/search/gg?q=python`

## 🔧 Troubleshooting

**Build fails?** → Use `requirements-railway.txt` (removes desktop dependencies)

**App won't start?** → Check Procfile: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`

---

**Need help?** See detailed guide: `RAILWAY_DEPLOYMENT.md`