# TARA Deployment Guide

This guide explains how to deploy the TARA application with the frontend on Vercel and backend on a separate platform.

## Architecture

- **Frontend**: React + Vite (deployed on Vercel)
- **Backend**: FastAPI + Python (deploy on Render, Railway, or Fly.io)

## Frontend Deployment (Vercel)

### 1. Deploy to Vercel

Click the button below or push to your connected GitHub repository:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

### 2. Configure Environment Variables

In your Vercel project settings, add these environment variables:

```
VITE_API_BASE_URL=https://your-backend-url.com/api
VITE_USE_MOCK_API=false
```

**Important**: Replace `https://your-backend-url.com/api` with your actual backend URL after deploying the backend (see below).

### 3. Deploy

Vercel will automatically:
- Install dependencies (`npm install`)
- Build the frontend (`npm run build`)
- Serve the static files from `dist/`

## Backend Deployment Options

Choose one of these platforms to deploy your FastAPI backend:

### Option 1: Render (Recommended - Free Tier Available)

1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `tara-backend`
   - **Root Directory**: Leave empty (or `backend/` if you want)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (see Backend Environment Variables below)
6. Click "Create Web Service"
7. Copy the deployed URL (e.g., `https://tara-backend.onrender.com`)
8. Update `VITE_API_BASE_URL` in Vercel to `https://tara-backend.onrender.com/api`

### Option 2: Railway

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python
5. Add environment variables
6. Deploy
7. Copy the URL and update Vercel's `VITE_API_BASE_URL`

### Option 3: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run `fly launch` in your project directory
3. Follow the prompts
4. Deploy with `fly deploy`
5. Get the URL with `fly info`
6. Update Vercel's `VITE_API_BASE_URL`

## Backend Environment Variables

Set these in your backend deployment platform:

```bash
# Database (Required)
DATABASE_URL=postgresql://user:password@host:port/database

# OpenAI API (Required)
OPENAI_API_KEY=sk-...

# OpenRouter API (Optional - for Gemini models)
OPENROUTER_API_KEY=sk-or-...
USE_OPENROUTER=true

# CORS (Required)
CORS_ALLOW_ALL_ORIGINS=false
CORS_ADDITIONAL_ORIGINS=https://your-app.vercel.app

# Environment
TARA_ENVIRONMENT=prod
```

**Important**:
- Get `DATABASE_URL` from your Supabase project
- Get `OPENAI_API_KEY` from https://platform.openai.com/api-keys
- Add your Vercel frontend URL to `CORS_ADDITIONAL_ORIGINS`

## Local Development

### Frontend
```bash
npm install
npm run dev
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
uvicorn app.main:app --reload --port 8000
```

Set `VITE_API_BASE_URL=http://localhost:8000/api` in your `.env.local` file.

## Testing the Deployment

1. Visit your Vercel URL
2. Open browser DevTools → Network tab
3. Try loading a patient summary
4. Check that API calls are going to your backend URL
5. Verify responses are successful (200 status)

## Troubleshooting

### CORS Errors
- Make sure `CORS_ADDITIONAL_ORIGINS` in backend includes your Vercel URL
- Check that the URL doesn't have a trailing slash

### 404 Errors
- Verify `VITE_API_BASE_URL` ends with `/api` (no trailing slash)
- Check that backend is running and accessible

### Mock Data Showing
- Set `VITE_USE_MOCK_API=false` in Vercel environment variables
- Redeploy the frontend

## Cost Estimates

- **Vercel (Frontend)**: Free tier (100GB bandwidth/month)
- **Render (Backend)**: Free tier with limitations, $7/month for always-on
- **Railway (Backend)**: $5/month usage-based
- **Supabase (Database)**: Free tier (500MB, 2GB bandwidth)
- **OpenAI API**: Pay-per-use (~$0.002 per request)

## Need Help?

- Check [Vercel Docs](https://vercel.com/docs)
- Check [Render Docs](https://render.com/docs)
- Review API logs in your backend platform dashboard
