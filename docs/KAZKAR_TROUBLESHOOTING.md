# Kazkar Sync Pipeline - Troubleshooting Guide

Quick reference for common issues and solutions.

---

## Table of Contents

1. [Sync Script Issues](#sync-script-issues)
2. [API Connection Problems](#api-connection-problems)
3. [WebSocket Issues](#websocket-issues)
4. [GitHub Action Failures](#github-action-failures)
5. [Frontend Display Issues](#frontend-display-issues)
6. [Database Issues](#database-issues)

---

## Sync Script Issues

### Error: "Legends directory not found"

**Symptoms:**
```
❌ Legends directory not found: /path/to/docs/legends
```

**Solutions:**
1. Create the directory: `mkdir -p docs/legends`
2. Verify you're running from repository root
3. Check file path in script matches your structure

### Error: "Failed to parse legend"

**Symptoms:**
```
❌ my_legend.md: Parse error
```

**Solutions:**
1. Verify markdown structure matches template:
   ```markdown
   # Title
   **Тип**: legend
   **Учасники**: Name1, Name2
   **Локація**: Location
   **Теги**: tag1, tag2
   
   ## Зміст
   Content here...
   ```
2. Check for missing sections
3. Ensure Ukrainian metadata keys are spelled correctly

### Error: "API connection failed"

**Symptoms:**
```
❌ Legend Title: ECONNREFUSED
```

**Solutions:**
1. Verify API is running: `curl http://localhost:8000/health`
2. Check `API_URL` environment variable
3. Ensure no firewall blocking
4. For production, verify DNS resolves: `nslookup api.cimeika.com.ua`

---

## API Connection Problems

### Error: "Connection refused"

**Cause:** Backend not running or wrong URL

**Solutions:**
1. Start backend: `cd backend && python main.py`
2. Check port: Default is 8000, verify in `.env`
3. Test health endpoint: `curl http://localhost:8000/health`

### Error: "422 Unprocessable Entity"

**Cause:** Request body doesn't match schema

**Solutions:**
1. Check required fields:
   - `title` (string, required)
   - `content` (string, required)
   - `story_type` (string, optional)
   - `tags` (array, optional)
2. Validate JSON structure
3. Review API docs: `/api/docs`

### Error: "CORS error"

**Cause:** Frontend origin not allowed

**Solutions:**
1. Add frontend URL to `CORS_ORIGINS` in `.env`:
   ```
   CORS_ORIGINS=http://localhost:3000,https://cimeika.com.ua
   ```
2. Restart backend
3. Clear browser cache

---

## WebSocket Issues

### Error: "WebSocket connection failed"

**Symptoms:**
- Frontend shows "disconnected" status
- Console: `WebSocket connection to 'ws://...' failed`

**Solutions:**
1. Check WebSocket URL format:
   - HTTP → `ws://`
   - HTTPS → `wss://`
2. Verify backend WebSocket endpoint: `/ws/kazkar`
3. Test manually:
   ```javascript
   const ws = new WebSocket('ws://localhost:8000/ws/kazkar');
   ws.onopen = () => console.log('Connected');
   ```
4. Check proxy/reverse proxy WebSocket support

### Error: "Connection drops immediately"

**Cause:** Backend not handling WebSocket properly

**Solutions:**
1. Check backend logs for errors
2. Verify WebSocket manager initialized
3. Ensure no middleware blocking WebSocket upgrade
4. Test with Postman or wscat:
   ```bash
   npm install -g wscat
   wscat -c ws://localhost:8000/ws/kazkar
   ```

### Error: "Events not received"

**Cause:** Events not being broadcast

**Solutions:**
1. Verify broadcast function called:
   ```python
   await kazkar_ws_manager.broadcast(event)
   ```
2. Check active connections:
   ```python
   print(len(kazkar_ws_manager.active_connections))
   ```
3. Test broadcast endpoint:
   ```bash
   curl -X POST http://localhost:8000/api/v1/kazkar/broadcast \
     -H "Content-Type: application/json" \
     -d '{"event": "test", "data": "hello"}'
   ```

---

## GitHub Action Failures

### Error: "Sync script failed"

**Symptoms:**
- GitHub Action shows red X
- Job "sync-legends" failed

**Solutions:**
1. Check Action logs for specific error
2. Run sync script locally to reproduce
3. Verify `API_URL` secret is set in repository
4. Test with dry run:
   ```yaml
   workflow_dispatch:
     inputs:
       dry_run: 'true'
   ```

### Error: "API not reachable"

**Cause:** Production API down or blocked

**Solutions:**
1. Verify API is deployed and running
2. Check DNS: `nslookup api.cimeika.com.ua`
3. Test endpoint: `curl https://api.cimeika.com.ua/health`
4. Review firewall rules (GitHub IPs must be allowed)

### Error: "WebSocket notification failed"

**Cause:** Broadcast endpoint not accessible

**Solutions:**
1. Check if error is blocking deployment (it shouldn't)
2. Verify broadcast endpoint exists: `/api/v1/kazkar/broadcast`
3. Test manually:
   ```bash
   curl -X POST https://api.cimeika.com.ua/api/v1/kazkar/broadcast \
     -H "Content-Type: application/json" \
     -d '{"event": "test"}'
   ```

---

## Frontend Display Issues

### Error: "Legend not found"

**Symptoms:**
- Empty legend list
- "Legend not found" message

**Solutions:**
1. Verify legends synced to database:
   ```bash
   curl http://localhost:8000/api/v1/kazkar/legends
   ```
2. Check API URL in frontend `.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```
3. Inspect network tab for API errors
4. Clear frontend cache

### Error: "WebSocket not connecting"

**Symptoms:**
- No green indicator on audio button
- Status shows "disconnected"

**Solutions:**
1. Check `useKazkarRealtime` hook configuration
2. Verify API URL format (http → ws, https → wss)
3. Enable debug mode:
   ```tsx
   const { status } = useKazkarRealtime({ debug: true });
   ```
4. Check browser console for WebSocket errors

### Error: "Audio not playing"

**Symptoms:**
- Clicking audio button does nothing
- Console shows audio load error

**Solutions:**
1. Audio file missing (this is expected if placeholder used)
2. Add real audio file: `/frontend/public/audio/kazkar_ambient.mp3`
3. Check file format (MP3 or OGG)
4. Verify file size <5MB for fast loading
5. Test audio URL directly: `http://localhost:3000/audio/kazkar_ambient.mp3`

---

## Database Issues

### Error: "Table does not exist"

**Cause:** Database not initialized

**Solutions:**
1. Run database initialization:
   ```bash
   cd backend
   python init_db.py
   ```
2. Check database connection in `.env`
3. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

### Error: "Duplicate key error"

**Cause:** Trying to create legend with existing source_trace

**Solutions:**
1. This is handled automatically (upsert logic)
2. If manual import, check source_trace uniqueness
3. Review import endpoint logic

---

## Quick Diagnostic Commands

### Check all services status
```bash
# Backend
curl http://localhost:8000/health

# Kazkar module
curl http://localhost:8000/api/v1/kazkar/

# Legends
curl http://localhost:8000/api/v1/kazkar/legends

# WebSocket (requires wscat)
wscat -c ws://localhost:8000/ws/kazkar

# Frontend
curl http://localhost:3000
```

### Run full verification
```bash
node scripts/verify_kazkar_pipeline.js
```

### Test sync manually
```bash
# Dry run first
DRY_RUN=true node scripts/sync_legends_to_api.js

# Real sync
node scripts/sync_legends_to_api.js
```

### Check logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Python logs
tail -f backend/app.log

# Frontend console
# Open browser dev tools (F12) → Console tab
```

---

## Getting Help

If issues persist:

1. **Check documentation:**
   - [Sync Pipeline Guide](./KAZKAR_SYNC_PIPELINE_GUIDE.md)
   - [UI Specification](./KAZKAR_LEGEND_UI_SPEC.md)
   - [API Documentation](./API_DOCUMENTATION.md)

2. **Run diagnostics:**
   ```bash
   node scripts/verify_kazkar_pipeline.js
   ```

3. **Enable debug mode:**
   - Backend: Set log level to DEBUG
   - Frontend: Use `debug: true` in hooks
   - Sync script: Add `console.log` statements

4. **Create GitHub issue:**
   - Include error messages
   - Describe steps to reproduce
   - Share relevant logs
   - Tag with `kazkar` label

5. **Contact team:**
   - Discord: #cimeika-dev
   - Email: dev@cimeika.com.ua

---

## Common Quick Fixes

### "Just make it work"

```bash
# 1. Reset everything
docker-compose down -v
docker-compose up -d

# 2. Initialize database
cd backend && python init_db.py

# 3. Sync legends
cd .. && node scripts/sync_legends_to_api.js

# 4. Verify
node scripts/verify_kazkar_pipeline.js
```

### "WebSocket immediately"

```bash
# Backend must be running first
cd backend && python main.py &

# Then test
wscat -c ws://localhost:8000/ws/kazkar
# Should see: {"event": "connected", ...}
```

### "Sync one legend"

```bash
# Manual curl
curl -X POST http://localhost:8000/api/v1/kazkar/import \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Legend",
    "content": "This is a test",
    "story_type": "legend",
    "tags": ["test"]
  }'
```

---

**Last Updated:** 2025-12-25  
**Maintained by:** Cimeika Core Team
