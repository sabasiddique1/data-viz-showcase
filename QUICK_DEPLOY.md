# 🚀 Quick Deployment Guide

## Fastest Way: Deploy to Render (5 minutes)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:
   - **Name**: `data-viz-showcase`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click **"Create Web Service"**
6. Wait 5-10 minutes
7. Your app is live! 🎉

---

## Alternative: Railway (Even Easier)

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your repo
5. Railway auto-detects Flask - just wait!
6. Get your URL from the dashboard

---

## Files Created for You

✅ `requirements.txt` - All dependencies
✅ `Procfile` - For Heroku/Render
✅ `.gitignore` - Git exclusions
✅ `DEPLOYMENT_GUIDE.md` - Full detailed guide

---

## Need Help?

Check `DEPLOYMENT_GUIDE.md` for detailed instructions for all platforms!

