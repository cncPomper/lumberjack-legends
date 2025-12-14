# Deploying to Render

This guide walks you through deploying Lumberjack Legends to Render.

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com - free tier available)
- Code pushed to GitHub repository

## Deployment Options

### Option 1: Blueprint (Recommended) - Infrastructure as Code

This method uses the `render.yaml` file for automatic setup.

#### Steps:

1. **Push code to GitHub**
   ```bash
   git push origin main
   ```

2. **Go to Render Dashboard**
   - Visit https://dashboard.render.com
   - Click **"New"** → **"Blueprint"**

3. **Connect Repository**
   - Connect your GitHub account if not already connected
   - Select the `lumberjack-legends` repository
   - Click **"Connect"**

4. **Review and Deploy**
   - Render will read `render.yaml` and show you what will be created:
     - PostgreSQL Database (Free plan - expires after 90 days)
     - Web Service (Free plan - spins down after 15 min inactivity)
   - You can upgrade plans later if needed
   - Click **"Apply"** to create services

5. **Wait for Deployment**
   - Database creation: ~2-5 minutes
   - App build and deploy: ~5-10 minutes
   - Watch the logs for any errors

6. **Access Your App**
   - Once deployed, Render provides a URL like:
     `https://lumberjack-app.onrender.com`
   - Your app is now live! 🎉

#### Environment Variables

The `render.yaml` file automatically sets up:
- ✅ `DATABASE_URL` - Connected to PostgreSQL
- ✅ `SECRET_KEY` - Auto-generated secure key
- ✅ `PORT` - Set to 80 (Render will map this to HTTPS)

### Option 2: Manual Setup (More Control)

If you prefer manual configuration:

#### 1. Create PostgreSQL Database

1. Click **"New"** → **"PostgreSQL"**
2. Settings:
   - Name: `lumberjack-db`
   - Database: `lumberjack_legends`
   - User: `lumberjack`
   - Plan: Free (expires after 90 days) or Standard ($7/month)
3. Click **"Create Database"**
4. Note the **Internal Database URL** (starts with `postgresql://`)

#### 2. Create Web Service

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Settings:
   - Name: `lumberjack-app`
   - Environment: **Docker**
   - Branch: `main`
   - Dockerfile Path: `./Dockerfile`
   - Plan: Free (spins down after 15 min) or Standard ($7/month)
4. Add Environment Variables:
   - `DATABASE_URL`: Paste the Internal Database URL from step 1
   - `SECRET_KEY`: Generate with: `openssl rand -hex 32`
   - `PORT`: `80`
5. Advanced Settings:
   - Health Check Path: `/api/health`
   - Auto-Deploy: Yes (deploy on git push)
6. Click **"Create Web Service"**

## Post-Deployment

### Initialize Database

The database will be automatically initialized on first startup through the FastAPI startup event.

To manually seed data or run migrations:

```bash
# Install Render CLI (optional)
brew install render  # or download from render.com/docs/cli

# Connect to your service
render shell lumberjack-app

# Inside the container
cd /app/backend
uv run python -m app.seed
```

### Custom Domain (Optional)

1. In your web service settings, go to **"Settings"** → **"Custom Domains"**
2. Add your domain (e.g., `lumberjackslegends.com`)
3. Update your DNS records as instructed by Render
4. Render automatically provisions SSL certificate

### Update CORS Settings

For production, update the backend CORS settings:

Edit `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://lumberjack-app.onrender.com",  # Your Render URL
        "https://yourdomain.com"  # Your custom domain if any
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-deploy.

## Monitoring

### View Logs

1. In Render Dashboard, select your service
2. Click **"Logs"** tab
3. View real-time logs from your application

### Metrics

- **Events** tab: Deployment history
- **Metrics** tab: CPU, Memory, Request stats
- **Shell** tab: SSH into your container

## Troubleshooting

### Build Failed

Check the logs for errors. Common issues:
- Missing dependencies in `package.json` or `pyproject.toml`
- Docker build errors (check `Dockerfile`)

### Database Connection Failed

- Verify `DATABASE_URL` environment variable is set correctly
- Ensure internal database URL is used (not external)
- Check if database is fully initialized

### App Not Responding

- Check if health check endpoint is working: `/api/health`
- Review logs for Python/Node errors
- Verify port 80 is exposed in Dockerfile

### Slow Response Times (Free Tier)

Free tier services spin down after 15 minutes of inactivity:
- First request after spin-down takes 30-60 seconds
- Upgrade to Standard plan ($7/month) for always-on service
- Or accept cold start delays on free tier

## Updating Your App

With auto-deploy enabled:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render automatically detects the push and redeploys (~5 min).

## Costs

### Free Tier
- Web Service: Free (spins down after 15 min inactivity, 750 hrs/month)
- PostgreSQL: Free (expires after 90 days, 1GB storage)
- **Total**: $0 (database expires after 90 days)

### Standard Plan (Recommended)
- Web Service: $7/month (always on, 0.5 CPU, 512 MB RAM)
- PostgreSQL: $7/month (1GB storage, 97 connections)
- **Total**: $14/month

### Pro Plan (Scale up later)
- Web Service: $19+/month (more CPU/RAM options)
- PostgreSQL: $20+/month (10GB+ storage, better performance)
- **Total**: $39+/month

## Backup Database

### Manual Backup

```bash
# Download from Render
render postgres backup lumberjack-db

# Or use pg_dump
pg_dump $DATABASE_URL > backup.sql
```

### Automatic Backups

Available on Pro PostgreSQL plan ($20/month):
- Daily automatic backups
- 7-day retention
- Point-in-time recovery

## Scaling

### Horizontal Scaling
In web service settings:
- Increase **"Instance Count"** to run multiple containers
- Built-in load balancing

### Vertical Scaling
- Upgrade plan for more CPU/RAM
- Starter → Pro → Pro Plus

## Alternative: Manual Deployment

If you don't want to use render.yaml:

1. Go to render.com and create services manually
2. Use the Docker environment
3. Point to your GitHub repository
4. Configure environment variables manually

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Status Page: https://status.render.com

## Summary

✅ Push code to GitHub
✅ Connect repository to Render via Blueprint
✅ Wait ~10 minutes for deployment
✅ Access your app at provided URL
✅ Optional: Add custom domain

Your app is now deployed and accessible worldwide! 🚀
