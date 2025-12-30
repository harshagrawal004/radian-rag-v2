# Vercel Deployment Checklist

This checklist ensures your TARA application deploys successfully to Vercel with zero errors.

## ✅ Pre-Deployment Checklist

### 1. Repository Setup
- [ ] Code is pushed to a GitHub/GitLab/Bitbucket repository
- [ ] All sensitive files are in `.gitignore` (`.env`, `backend/.env`)
- [ ] `.vercelignore` is present (excludes unnecessary files from deployment)

### 2. Environment Variables Configuration

**In Vercel Project Settings → Environment Variables**, add the following:

#### Required Variables:
- [ ] `DATABASE_URL` - Your Supabase PostgreSQL connection string
- [ ] `OPENAI_API_KEY` - Your OpenAI API key
- [ ] `VITE_API_BASE_URL` - Set to `/api` for same-domain deployment
- [ ] `VITE_USE_MOCK_API` - Set to `false` to use real API

#### Optional Variables:
- [ ] `OPENROUTER_API_KEY` - If using OpenRouter for alternative models
- [ ] `USE_OPENROUTER` - Set to `true` if using OpenRouter
- [ ] `CORS_ALLOW_ALL_ORIGINS` - Set to `false` for production (recommended)
- [ ] `CORS_ADDITIONAL_ORIGINS` - Comma-separated list of allowed domains
- [ ] `TARA_ENVIRONMENT` - Set to `prod` for production

### 3. Database Setup
- [ ] Supabase project is created and running
- [ ] Database tables are created (see `backend/migrations/`)
- [ ] `pgvector` extension is enabled in Supabase
- [ ] Database connection string is correctly formatted with SSL parameters
- [ ] Connection pooling is configured (recommended for serverless)

### 4. API Keys
- [ ] OpenAI API key is valid and has credits
- [ ] OpenRouter API key is valid (if using)
- [ ] Test API keys locally before deploying

### 5. Build Verification
- [ ] Run `npm install` locally - completes without errors
- [ ] Run `npm run build` locally - builds successfully
- [ ] Check `dist/` folder is created with compiled files
- [ ] All Python dependencies are listed in `requirements.txt`

## 🚀 Deployment Steps

### Step 1: Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Import your Git repository
4. Vercel will auto-detect the framework (Vite)

### Step 2: Configure Build Settings
Vercel should auto-configure these, but verify:
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Step 3: Add Environment Variables
1. Go to project Settings → Environment Variables
2. Add all required variables from the checklist above
3. Set variables for all environments (Production, Preview, Development)

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build to complete (2-5 minutes)
3. Verify deployment succeeds

## 🧪 Post-Deployment Verification

### Test Backend Health
Visit: `https://your-app.vercel.app/api/healthz`

**Expected Response:**
```json
{"status": "ok"}
```

### Test Frontend
1. Visit `https://your-app.vercel.app`
2. Open browser DevTools → Network tab
3. Verify API requests go to `/api/*` (not `localhost`)
4. Check for CORS errors in console
5. Test key features:
   - [ ] Patient list loads
   - [ ] Patient summary displays
   - [ ] Chat functionality works
   - [ ] No "failing to fetch" errors

### Check Logs
1. Go to Vercel project → Deployments → Latest deployment
2. Click "Functions" tab
3. Check for any runtime errors
4. Verify `/api` function is running

## 🐛 Common Issues & Solutions

### Issue: "Failing to fetch" error
**Cause**: Frontend can't reach backend
**Solution**:
- Verify `VITE_API_BASE_URL=/api` in Vercel env variables
- Check `/api/healthz` endpoint is accessible
- Ensure `VITE_USE_MOCK_API=false`

### Issue: Database connection timeout
**Cause**: Serverless cold starts or connection limits
**Solution**:
- Use Supabase connection pooling (recommended)
- Increase `maxDuration` in `vercel.json` (max 60s)
- Verify `DATABASE_URL` includes SSL parameters

### Issue: CORS errors
**Cause**: Backend rejecting requests from frontend domain
**Solution**:
- Add Vercel domain to `CORS_ADDITIONAL_ORIGINS`
- Or temporarily set `CORS_ALLOW_ALL_ORIGINS=true` for testing
- Check browser console for specific CORS error

### Issue: Function timeout
**Cause**: RAG queries taking too long
**Solution**:
- Optimize database queries
- Check `maxDuration: 60` in `vercel.json`
- Consider upgrading Vercel plan for longer timeouts

### Issue: Module not found errors
**Cause**: Missing Python dependencies
**Solution**:
- Verify all imports are in `requirements.txt`
- Check `backend/` folder structure is correct
- Ensure `api/index.py` path mapping is correct

### Issue: Python version mismatch
**Cause**: Local Python version differs from Vercel
**Solution**:
- Vercel uses Python 3.11 (as specified in `vercel.json`)
- Ensure code is compatible with Python 3.11
- Test locally with Python 3.11 if possible

## 📊 Performance Optimization

### Recommended Settings
- Enable Vercel Edge Network (automatic)
- Use Supabase connection pooler
- Configure appropriate cache headers
- Monitor function execution time in Vercel dashboard

### Database Connection Pooling
For production, use Supabase's connection pooler:
```
DATABASE_URL=postgres://[user]:[password]@[host]:6543/postgres?pgbouncer=true
```

## 🔒 Security Best Practices

- [ ] Never commit `.env` files
- [ ] Set `CORS_ALLOW_ALL_ORIGINS=false` in production
- [ ] Use specific CORS origins in `CORS_ADDITIONAL_ORIGINS`
- [ ] Rotate API keys regularly
- [ ] Monitor Vercel logs for suspicious activity
- [ ] Enable Vercel deployment protection for production
- [ ] Use environment-specific variables (prod vs preview)

## 📝 Maintenance

### Regular Tasks
- Monitor Vercel function logs for errors
- Check API usage and costs (OpenAI/OpenRouter)
- Update dependencies: `npm update` and rebuild
- Review Vercel analytics for performance issues
- Test critical paths after each deployment

### Rollback Procedure
If a deployment fails:
1. Go to Vercel project → Deployments
2. Find last working deployment
3. Click three dots → "Promote to Production"

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ `/api/healthz` returns `{"status": "ok"}`
- ✅ Frontend loads without errors
- ✅ Patient data displays correctly
- ✅ Chat functionality works
- ✅ No CORS errors in browser console
- ✅ All API requests go to `/api/*` (not localhost)
- ✅ No "failing to fetch" messages
- ✅ Vercel function logs show no errors

## 📞 Support Resources

- Vercel Documentation: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- FastAPI Docs: https://fastapi.tiangolo.com/
- Supabase Docs: https://supabase.com/docs

---

**Last Updated**: 2025-12-31
**Vercel Runtime**: Python 3.11, Node.js (auto)
**Build Tool**: Vite 5.x
