# Deployment Guide for Data Viz Showcase

This guide will help you deploy your Flask web application to various platforms.

## 🚀 Recommended Platforms

### 1. **Render** (Recommended - Free Tier Available)
- ✅ Easy setup
- ✅ Free tier with limitations
- ✅ Automatic deployments from GitHub
- ✅ HTTPS included

### 2. **Railway** (Recommended - Free Tier Available)
- ✅ Very easy setup
- ✅ $5 free credit monthly
- ✅ Automatic deployments
- ✅ Great for beginners

### 3. **PythonAnywhere** (Good for Beginners)
- ✅ Free tier available
- ✅ Simple setup
- ✅ Good for learning

### 4. **Heroku** (Paid Only Now)
- ⚠️ No longer has free tier
- ✅ Very reliable
- ✅ Easy setup

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

1. ✅ All dependencies are in `requirements.txt`
2. ✅ `Procfile` exists (for Heroku/Render)
3. ✅ `.gitignore` is set up
4. ✅ Your code is committed to Git
5. ✅ Data files are included (or use external storage)

---

## 🎯 Option 1: Deploy to Render (Recommended)

### Step 1: Prepare Your Repository

1. Make sure all files are committed:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Verify your email

### Step 3: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Select your repository: `python_megaproject` (or your repo name)

### Step 4: Configure Settings

**Basic Settings:**
- **Name**: `data-viz-showcase` (or your choice)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty (or `./` if needed)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

**Advanced Settings (optional):**
- **Environment**: `Python 3`
- **Python Version**: `3.11.0`

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

### Step 6: Update App Configuration (if needed)

If your app uses port 8080, update `app.py`:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
```

---

## 🎯 Option 2: Deploy to Railway

### Step 1: Prepare Repository

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Verify your email

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository

### Step 4: Configure Deployment

Railway auto-detects Flask apps, but you can verify:

1. Go to **Settings** → **Deploy**
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Step 5: Set Environment Variables (if needed)

Go to **Variables** tab and add:
- `PORT` (usually auto-set)
- Any other environment variables your app needs

### Step 6: Deploy

1. Railway will automatically deploy
2. Click on your service → **Settings** → **Generate Domain**
3. Your app will be live at: `https://your-app-name.up.railway.app`

---

## 🎯 Option 3: Deploy to PythonAnywhere

### Step 1: Create Account

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for free account
3. Verify your email

### Step 2: Upload Your Files

**Option A: Using Git (Recommended)**
1. Go to **Consoles** → **Bash**
2. Clone your repository:
```bash
cd ~
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

**Option B: Using Web Interface**
1. Go to **Files** tab
2. Upload your files manually

### Step 3: Install Dependencies

1. Open **Consoles** → **Bash**
2. Create virtual environment:
```bash
cd ~/your-repo
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to **Web** tab
2. Click **"Add a new web app"**
3. Choose **Flask** → **Python 3.10**
4. Set **Source code**: `/home/yourusername/your-repo`
5. Set **Working directory**: `/home/yourusername/your-repo`

### Step 5: Configure WSGI File

1. Click on the WSGI file link
2. Update it to point to your app:
```python
import sys
path = '/home/yourusername/your-repo'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 6: Reload Web App

1. Go back to **Web** tab
2. Click **"Reload"** button
3. Your app will be live at: `https://yourusername.pythonanywhere.com`

---

## 🔧 Important Configuration Updates

### Update app.py for Production

Make sure your `app.py` has this at the end:

```python
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
```

**Changes:**
- `debug=False` (security - don't run debug mode in production)
- `host='0.0.0.0'` (allows external connections)
- `port` from environment variable (platforms set this automatically)

### Static Files Configuration

Your static files should work automatically, but verify:
- CSS files in `static/css/`
- Templates in `templates/`
- Data files in `data/`

---

## 📦 Data Files Consideration

### Option 1: Include in Repository (Small files)
- ✅ Simple
- ✅ Works for files < 100MB
- ⚠️ Increases repo size

### Option 2: External Storage (Large files)
For large datasets, consider:
- **AWS S3**
- **Google Cloud Storage**
- **Database** (PostgreSQL, MongoDB)

---

## 🐛 Troubleshooting

### Common Issues:

1. **"Module not found"**
   - Check `requirements.txt` has all dependencies
   - Verify imports in your code

2. **"Port already in use"**
   - Use `$PORT` environment variable
   - Don't hardcode port numbers

3. **"Static files not loading"**
   - Check file paths are relative
   - Verify `static/` folder structure

4. **"Data files not found"**
   - Ensure data files are committed to Git
   - Check file paths in code

5. **"App crashes on startup"**
   - Check logs in platform dashboard
   - Verify all dependencies installed
   - Test locally first

---

## 🔒 Security Checklist

Before deploying:

- [ ] Set `debug=False` in production
- [ ] Don't commit API keys or secrets
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Review error messages (don't expose sensitive info)

---

## 📊 Platform Comparison

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ | General use |
| **Railway** | ✅ $5 credit | ⭐⭐⭐⭐⭐ | Beginners |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐⭐ | Learning |
| **Heroku** | ❌ No | ⭐⭐⭐⭐ | Production |
| **AWS** | ⚠️ Limited | ⭐⭐ | Advanced |

---

## 🎉 After Deployment

1. **Test your app**: Visit the provided URL
2. **Share the link**: Your app is now live!
3. **Monitor logs**: Check platform dashboard for errors
4. **Set up custom domain** (optional): Most platforms support this

---

## 📝 Quick Start Commands

```bash
# 1. Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Test locally first
python3 app.py

# 3. Check requirements
pip freeze > requirements.txt

# 4. Deploy to your chosen platform
# Follow platform-specific steps above
```

---

## 💡 Pro Tips

1. **Start with Render or Railway** - easiest for beginners
2. **Test locally first** - fix issues before deploying
3. **Check logs regularly** - helps debug issues
4. **Use environment variables** - for configuration
5. **Monitor usage** - free tiers have limits

---

## 🆘 Need Help?

- Check platform documentation
- Review error logs in dashboard
- Test locally to isolate issues
- Verify all dependencies are listed

Good luck with your deployment! 🚀

