# GitHub Actions CI/CD Setup

This document explains how to set up the GitHub Actions CI/CD pipeline for automatic testing and deployment to Render.

## Pipeline Overview

The CI/CD pipeline consists of three jobs:

1. **Test Backend** - Runs Python tests with PostgreSQL
2. **Test Frontend** - Runs TypeScript/React tests
3. **Deploy to Render** - Triggers deployment (only on main branch pushes after tests pass)

## Setup Instructions

### 1. Get Render Deploy Hook URL

1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Navigate to your `lumberjack-app` web service
3. Click on **Settings** in the left sidebar
4. Scroll down to the **Deploy Hook** section
5. Copy the Deploy Hook URL (it looks like: `https://api.render.com/deploy/srv-xxxxx?key=yyyyy`)

### 2. Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

   - **Name:** `RENDER_DEPLOY_HOOK_URL`
     - **Value:** The deploy hook URL from step 1

### 4. Test the Pipeline

1. Commit and push to a branch:
   ```bash
   git add .
   git commit -m "Add CI/CD pipeline"
   git push origin your-branch
   ```

2. Open a Pull Request - this will:
   - ✅ Run backend tests
   - ✅ Run frontend tests
   - ❌ NOT deploy (only PRs trigger tests, not deployment)

3. Merge to main - this will:
   - ✅ Run backend tests
   - ✅ Run frontend tests
   - ✅ Deploy to Render (if tests pass)

## Pipeline Behavior

### On Pull Requests
- Runs all tests
- Does NOT deploy
- Must pass before merging

### On Push to Main
- Runs all tests
- Deploys to Render if tests pass
- Fails deployment if any test fails

## Monitoring

### GitHub Actions
- View workflow runs: Go to your repo → **Actions** tab
- See detailed logs for each job
- Get notifications on failures

### Render Deployment
- View deployment status: [Render Dashboard](https://dashboard.render.com)
- Check deployment logs in Render
- The workflow triggers a deployment, but Render handles the actual build

## Troubleshooting

### Tests fail in CI but pass locally
- Check environment variables
- Verify Node.js/Python versions match
- Check database connection settings

### Deployment doesn't trigger
- Verify secrets are set correctly
- Check that you pushed to `main` branch
- Ensure tests passed first

### Deployment API call fails
- Verify `RENDER_DEPLOY_HOOK_URL` is correct and complete
- Make sure the URL includes the service ID and key parameter
- Check Render API status

## Manual Deployment

If you need to deploy manually without waiting for CI/CD:

```bash
curl -X POST "YOUR_RENDER_DEPLOY_HOOK_URL"
```

Or use the Render Dashboard:
1. Go to your service
2. Click **Manual Deploy** → **Deploy latest commit**

## Customization

### Change test commands
Edit `.github/workflows/ci-cd.yml`:
- Backend tests: Modify the `uv run pytest` command
- Frontend tests: Modify the `npm test` command

### Add integration tests
Add a new job in the workflow file before the deploy step.

### Deploy to staging first
Create a separate workflow for staging deployments with a different `RENDER_SERVICE_ID`.

## Security Notes

- Never commit API keys or secrets to the repository
- Use GitHub Secrets for all sensitive values
- Rotate API keys periodically
- Review the Actions logs to ensure no secrets are exposed
