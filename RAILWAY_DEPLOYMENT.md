# 🚀 Deploy GitGod to Railway

This guide will help you deploy your FastAPI search engine to Railway using your GitHub account `/xlrdtech`.

## 📋 Prerequisites

- GitHub account: `/xlrdtech`
- Railway account (free tier available)
- Git installed on your machine

## 🔧 Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository
```bash
cd /Volumes/selfexec_/dev_/New\ Installs/gitgod
git init
git add .
git commit -m "Initial commit: FastAPI search engine"
```

### 1.2 Create GitHub Repository
1. Go to [GitHub](https://github.com/xlrdtech)
2. Click "New repository"
3. Name it `gitgod-search-engine` (or your preferred name)
4. Make it **Public** (required for Railway free tier)
5. Don't initialize with README (we already have files)
6. Click "Create repository"

### 1.3 Push to GitHub
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/xlrdtech/gitgod-search-engine.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🚂 Step 2: Deploy to Railway

### 2.1 Create Railway Account
1. Go to [Railway.app](https://railway.app)
2. Click "Login" and sign in with your GitHub account
3. Authorize Railway to access your repositories

### 2.2 Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `xlrdtech/gitgod-search-engine`
4. Click "Deploy Now"

### 2.3 Configure Deployment
Railway will automatically:
- ✅ Detect it's a Python project
- ✅ Install dependencies from `requirements.txt`
- ✅ Use the `Procfile` for startup command
- ✅ Assign a public URL

## ⚙️ Step 3: Environment Configuration

### 3.1 Set Environment Variables (if needed)
If your app needs environment variables:
1. Go to your Railway project dashboard
2. Click "Variables" tab
3. Add any required variables:
   ```
   ENVIRONMENT=production
   DEBUG=false
   ```

### 3.2 Custom Domain (Optional)
1. In Railway dashboard, go to "Settings"
2. Click "Domains"
3. Add your custom domain if you have one

## 🔍 Step 4: Verify Deployment

### 4.1 Check Deployment Status
1. In Railway dashboard, check the "Deployments" tab
2. Wait for build to complete (usually 2-3 minutes)
3. Look for green "Success" status

### 4.2 Test Your Application
1. Click on the generated URL (e.g., `https://your-app.railway.app`)
2. Test the search functionality:
   ```
   GET https://your-app.railway.app/search/gg?q=fastapi
   GET https://your-app.railway.app/docs  # API documentation
   ```

## 📊 Step 5: Monitor and Manage

### 5.1 View Logs
```bash
# In Railway dashboard
1. Go to "Deployments" tab
2. Click on latest deployment
3. View real-time logs
```

### 5.2 Auto-Deploy Setup
Railway automatically redeploys when you push to GitHub:
```bash
# Make changes to your code
git add .
git commit -m "Update search engines"
git push origin main
# Railway will automatically redeploy!
```

## 🛠️ Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for incompatible versions
   - Ensure `Procfile` is correct
   - View build logs in Railway dashboard

2. **App Won't Start**
   - Verify Procfile command: `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Check that `main.py` has `app = FastAPI()` instance

3. **Dependencies Issues**
   - Remove unnecessary packages from `requirements.txt`:
     ```txt
     # Remove these if not needed for web deployment:
     pyautogui==0.9.54
     pywinauto==0.6.8
     opencv-python==4.8.1.78
     ```

### Optimized requirements.txt for Railway
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
beautifulsoup4==4.12.2
lxml==4.9.3
python-multipart==0.0.6
```

## 🎯 Your Deployed URLs

Once deployed, your search engine will be available at:

- **Main App**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`
- **Search Examples**:
  - `https://your-app.railway.app/search/gg?q=python`
  - `https://your-app.railway.app/search/gh?q=fastapi`
  - `https://your-app.railway.app/multi-search?engines=gg,gh&q=machine+learning`

## 💡 Pro Tips

1. **Free Tier Limits**:
   - 500 hours/month execution time
   - $5 credit monthly
   - Perfect for personal projects

2. **Performance Optimization**:
   - Remove unused dependencies
   - Add caching for frequent searches
   - Use async/await for better performance

3. **Monitoring**:
   - Set up Railway's built-in metrics
   - Monitor response times and errors
   - Use Railway's logging for debugging

## 🚀 Next Steps

1. **Custom Features**:
   - Add authentication
   - Implement rate limiting
   - Add search result caching

2. **Scaling**:
   - Upgrade to Railway Pro for more resources
   - Add database for search history
   - Implement search analytics

---

## 🎉 Congratulations!

Your GitGod search engine is now live on Railway! 🎊

**Quick Commands Summary**:
```bash
# Deploy updates
git add .
git commit -m "Your update message"
git push origin main

# View live app
open https://your-app.railway.app
```

Enjoy your deployed search engine! 🔍✨