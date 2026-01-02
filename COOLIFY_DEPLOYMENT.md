# TARA Deployment on Coolify

This guide explains how to deploy the TARA application on Coolify with Docker Compose.

## Architecture

- **Frontend**: React + Vite (served via Nginx on port 3000)
- **Backend**: FastAPI + Python (running on port 8000)
- **Database**: PostgreSQL 15

All services run in Docker containers orchestrated by Docker Compose.

---

## Prerequisites

- Coolify instance running on Hetzner (or any server)
- GitHub repository with deploy key configured
- OpenAI API key (or OpenRouter API key)
- PostgreSQL database password

---

## Deployment Steps

### 1. **In Coolify Dashboard**

1. Click "New Resource" → "Application"
2. Select "Private Repository (with Deploy Key)"
3. Configure:
   - **Repository**: `radian-rag-v2`
   - **Branch**: `main`
   - **Build Pack**: `Docker Compose`
   - **Docker Compose Location**: `/docker-compose.yaml`
   - **Base Directory**: `/`

### 2. **Set Environment Variables**

In Coolify, go to your application → Environment Variables and add these:

#### Required Variables:

```bash
# Database Password (IMPORTANT: Change this!)
DATABASE_PASSWORD=your_secure_password_here

# OpenAI API Key (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-...

# Backend URL for frontend (Coolify will provide a domain)
# Format: http://backend:8000/api (internal) or https://your-domain.com/api (external)
VITE_API_BASE_URL=http://backend:8000/api

# Disable mock data
VITE_USE_MOCK_API=false

# CORS - Add your Coolify domain here
CORS_ADDITIONAL_ORIGINS=https://your-coolify-domain.com

# Environment
TARA_ENVIRONMENT=prod
```

#### Optional Variables:

```bash
# OpenRouter (Alternative to OpenAI)
OPENROUTER_API_KEY=sk-or-...
USE_OPENROUTER=true

# PostgreSQL Pool Settings
PG_POOL_MIN_SIZE=2
PG_POOL_MAX_SIZE=10

# CORS (only for development/testing)
CORS_ALLOW_ALL_ORIGINS=false
```

### 3. **Configure Port Mapping**

Coolify will automatically detect ports from docker-compose.yaml:
- **Frontend**: Port 3000 (publicly accessible)
- **Backend**: Port 8000 (internal, accessed via frontend proxy)

Make sure Coolify exposes port **3000** publicly.

### 4. **Deploy**

1. Click "Deploy" in Coolify
2. Wait for build to complete (~5-10 minutes first time)
3. Coolify will:
   - Pull your GitHub repo
   - Build Docker images
   - Start all services (database, backend, frontend)
   - Assign a domain (e.g., `app-xyz.coolify.domain.com`)

### 5. **Post-Deployment Configuration**

After deployment, update the environment variable:

```bash
VITE_API_BASE_URL=https://your-coolify-domain.com/api
CORS_ADDITIONAL_ORIGINS=https://your-coolify-domain.com
```

Then **redeploy** the application.

---

## Service URLs

After deployment, Coolify will provide:

- **Frontend (Public)**: `https://your-app.coolify.domain.com`
- **Backend (Internal)**: `http://backend:8000` (accessed by frontend)
- **Database (Internal)**: `postgresql://database:5432/tara`

---

## Database Management

### Access PostgreSQL

```bash
# Via Coolify shell (exec into database container)
psql -U tara_user -d tara
```

### Database Connection String

```
postgresql://tara_user:your_password@database:5432/tara
```

### Backup Database

```bash
# From Coolify server
docker exec -t <database_container> pg_dump -U tara_user tara > backup.sql

# Restore
docker exec -i <database_container> psql -U tara_user tara < backup.sql
```

---

## Monitoring & Logs

### View Logs in Coolify

1. Go to your application dashboard
2. Click on each service (frontend, backend, database)
3. View real-time logs

### Health Checks

- **Backend**: `https://your-domain.com/api/healthz`
- **Frontend**: `https://your-domain.com/`
- **Database**: Automatically monitored by Docker health check

---

## Scaling

### Increase Backend Workers

Edit `docker-compose.yaml`:

```yaml
backend:
  command: uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4  # Increase workers
```

### Increase Database Connections

Add to environment variables:

```bash
PG_POOL_MAX_SIZE=20
```

---

## Troubleshooting

### Build Fails

- Check Coolify build logs
- Verify all files are committed to GitHub
- Ensure `docker-compose.yaml` is at repository root

### Frontend Shows Mock Data

- Check `VITE_USE_MOCK_API=false` is set
- Verify `VITE_API_BASE_URL` is correct
- Redeploy after changing environment variables

### Backend Can't Connect to Database

- Verify `DATABASE_PASSWORD` matches in both backend and database service
- Check database health check is passing
- Ensure backend waits for database (defined in `depends_on`)

### CORS Errors

- Add your Coolify domain to `CORS_ADDITIONAL_ORIGINS`
- Format: `https://your-domain.com` (no trailing slash)
- Restart backend service

### 500 Errors on API Calls

- Check backend logs in Coolify
- Verify `OPENAI_API_KEY` is set correctly
- Ensure database migrations ran successfully

---

## Production Checklist

Before going live:

- [ ] Change `DATABASE_PASSWORD` from default
- [ ] Set `TARA_ENVIRONMENT=prod`
- [ ] Set `CORS_ALLOW_ALL_ORIGINS=false`
- [ ] Add specific domains to `CORS_ADDITIONAL_ORIGINS`
- [ ] Configure custom domain in Coolify
- [ ] Set up automatic backups for PostgreSQL
- [ ] Enable SSL/HTTPS (Coolify handles this automatically)
- [ ] Test all features (chat, transcription, streaming)
- [ ] Monitor resource usage (CPU, RAM, disk)

---

## Updating the Application

### Deploy New Version

1. Push changes to GitHub `main` branch
2. Coolify auto-deploys (if enabled)
3. Or manually click "Redeploy" in Coolify

### Zero-Downtime Deployment

Docker Compose will:
1. Pull new images
2. Start new containers
3. Stop old containers (after new ones are healthy)

---

## Cost Estimates

**Hetzner Server (Coolify Host)**:
- CPX11: €4.15/month (2 vCPU, 2GB RAM) - Minimum
- CPX21: €8.50/month (3 vCPU, 4GB RAM) - Recommended
- CPX31: €15.50/month (4 vCPU, 8GB RAM) - For production

**Additional Costs**:
- OpenAI API: ~$0.002-0.01 per request
- Bandwidth: Usually included in server cost

---

## Support

- **Coolify Docs**: https://coolify.io/docs
- **Docker Compose**: https://docs.docker.com/compose/
- **Issue Tracker**: Check application logs in Coolify

---

## Advanced Configuration

### Custom Domain

1. In Coolify, go to your app → Domains
2. Add custom domain (e.g., `app.yourdomain.com`)
3. Update DNS records as instructed
4. Coolify will auto-provision SSL certificate

### Environment-Specific Configs

For staging/production splits, create separate Coolify applications pointing to different branches:

- `main` → Production
- `staging` → Staging environment

### Backup Strategy

Set up automated PostgreSQL backups:

```bash
# Cron job on Coolify server
0 2 * * * docker exec <db_container> pg_dump -U tara_user tara | gzip > /backups/tara-$(date +\%Y\%m\%d).sql.gz
```

---

Good luck with your deployment! 🚀
