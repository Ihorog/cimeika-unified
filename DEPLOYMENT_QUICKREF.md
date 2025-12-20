# CIMEIKA Deployment Quick Reference

## 🚀 Quick Commands

### Start All Services
```bash
./start.sh
# OR
docker compose up -d
```

### Stop All Services
```bash
./stop.sh
# OR
docker compose down
```

### Verify Deployment
```bash
./scripts/verify-deployment.sh
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

### Check Service Status
```bash
docker compose ps
```

---

## 🔗 Access Points

| Service | Local URL | Production URL |
|---------|-----------|----------------|
| Frontend | http://localhost:3000 | https://your-app.vercel.app |
| Backend | http://localhost:5000 | Your backend deployment |
| Backend Health | http://localhost:5000/health | - |
| Backend API | http://localhost:5000/api/v1/modules | - |

---

## ✅ Health Check Endpoints

### Backend Root
```bash
curl http://localhost:5000/
```
Expected: `{"status": "success", "message": "CIMEIKA Backend API is running", ...}`

### Backend Health
```bash
curl http://localhost:5000/health
```
Expected: `{"status": "healthy", "message": "Backend is running", ...}`

### Modules API
```bash
curl http://localhost:5000/api/v1/modules
```
Expected: List of 7 modules (Ci, Казкар, Подія, Настрій, Маля, Галерея, Календар)

---

## 🐳 Docker Container Status

Expected containers (all should be "Up"):
- `cimeika-postgres` (healthy)
- `cimeika-redis` (healthy)
- `cimeika-backend`
- `cimeika-frontend`
- `cimeika-celery-worker`

Check with:
```bash
docker compose ps
```

---

## 🔧 Common Troubleshooting

### Container not starting?
```bash
docker compose logs <container-name>
docker compose restart <container-name>
```

### Need to rebuild?
```bash
docker compose up -d --build
```

### Clean restart?
```bash
docker compose down -v  # WARNING: Removes volumes/data
docker compose up -d
```

### Database issues?
```bash
docker compose exec postgres psql -U cimeika_user -d cimeika
```

### Redis issues?
```bash
docker compose exec redis redis-cli -a your_password ping
```

---

## 📦 Vercel Deployment

### Check GitHub Actions
```bash
# Visit: https://github.com/Ihorog/cimeika-unified/actions
# Look for: "Vercel Deployment" workflow
# Status should be: ✅ Success
```

### Check Vercel Dashboard
```bash
# Visit: https://vercel.com/dashboard
# Find your project
# Latest deployment should be: Ready ✅
```

### Environment Variables (Vercel)
Required in Vercel Dashboard → Settings → Environment Variables:
- `VITE_API_URL` - Backend URL (required)
- `VITE_APP_NAME` - App name (optional, default: CIMEIKA)

### GitHub Secrets (for CI/CD)
Required in GitHub → Settings → Secrets and variables → Actions:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

---

## 📝 Pre-deployment Checklist

### Local Deployment
- [ ] `.env` file created from `.env.template`
- [ ] Docker and Docker Compose installed
- [ ] All environment variables configured
- [ ] Ports 3000, 5000, 5432, 6379 available

### Vercel Deployment
- [ ] Repository connected to Vercel
- [ ] Vercel environment variables set
- [ ] GitHub secrets configured
- [ ] Backend deployed and accessible
- [ ] `vercel.json` configured correctly

---

## 📊 Expected Results

### ✅ Healthy Deployment
```
Backend Health:    ✅ HEALTHY (3/3 checks passed)
Frontend Health:   ✅ HEALTHY (1/1 checks passed)
```

### ❌ Unhealthy Deployment
If checks fail:
1. Check Docker containers: `docker compose ps`
2. Check logs: `docker compose logs`
3. Restart services: `docker compose restart`
4. Rebuild if needed: `docker compose up -d --build`
5. Run verification again: `./scripts/verify-deployment.sh`

---

## 🔗 Documentation

- Full verification guide: [docs/DEPLOYMENT_VERIFICATION.md](../docs/DEPLOYMENT_VERIFICATION.md)
- Vercel deployment: [docs/VERCEL_DEPLOYMENT.md](../docs/VERCEL_DEPLOYMENT.md)
- GitHub Actions: [docs/GITHUB_ACTIONS_VERCEL.md](../docs/GITHUB_ACTIONS_VERCEL.md)
- Getting started: [docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md)

---

**Quick Help:**
- Start: `./start.sh`
- Stop: `./stop.sh`
- Verify: `./scripts/verify-deployment.sh`
- Logs: `docker compose logs -f`
