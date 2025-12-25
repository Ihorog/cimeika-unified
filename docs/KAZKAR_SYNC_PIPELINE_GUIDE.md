# Kazkar Legends Sync Pipeline - Complete Guide

## Overview

The Kazkar Legends Sync Pipeline is a comprehensive system for managing, syncing, and displaying interactive storytelling content in the Cimeika platform. It enables automatic synchronization from markdown files to the database and live UI updates via WebSocket.

---

## Architecture

```
┌─────────────────┐
│  GitHub Repo    │
│  /docs/legends/ │
│  *.md files     │
└────────┬────────┘
         │
         │ Push to main
         ▼
┌─────────────────┐
│ GitHub Action   │
│ kazkar-sync.yml │
└────────┬────────┘
         │
         │ Run sync script
         ▼
┌─────────────────┐
│  Sync Script    │
│  Node.js        │
└────────┬────────┘
         │
         │ POST to API
         ▼
┌─────────────────┐
│  Backend API    │
│  /api/v1/kazkar │
│  /import        │
└────────┬────────┘
         │
         │ Broadcast event
         ▼
┌─────────────────┐
│  WebSocket      │
│  /ws/kazkar     │
└────────┬────────┘
         │
         │ Real-time update
         ▼
┌─────────────────┐
│  Frontend UI    │
│  LegendScene    │
└─────────────────┘
```

---

## Components

### 1. Legend Markdown Files (`/docs/legends/*.md`)

**Location:** `docs/legends/`  
**Format:** Markdown with structured metadata

**Template:**
```markdown
# Legend Title

**Тип**: legend  
**Учасники**: Participant1, Participant2  
**Локація**: Location Name  
**Теги**: tag1, tag2, tag3  

---

## Зміст

Legend content goes here...
Multiple paragraphs supported.

---

## Відчуття

- ✦ **Sense Name** — Description
- 🔥 **Another Sense** — Description
```

**Fields:**
- `title` (# heading) - Legend title
- `Тип` - Story type (usually "legend")
- `Учасники` - Comma-separated list of participants
- `Локація` - Location/setting
- `Теги` - Comma-separated tags
- `## Зміст` - Main legend text
- `## Відчуття` - Optional sense nodes

### 2. Sync Script (`scripts/sync_legends_to_api.js`)

**Purpose:** Parse markdown files and POST to API  
**Language:** Node.js (ES modules)  
**Dependencies:** Built-in (fs, path, fetch)

**Usage:**
```bash
# Normal sync
node scripts/sync_legends_to_api.js

# Dry run (no API calls)
DRY_RUN=true node scripts/sync_legends_to_api.js

# Custom API URL
API_URL=https://api.cimeika.com.ua node scripts/sync_legends_to_api.js
```

**Features:**
- Parses structured markdown
- Extracts metadata and content
- Deduplicates by `source_trace`
- Error handling and reporting
- Parallel-safe execution

### 3. Backend API Endpoints

#### GET `/api/v1/kazkar/`
Module status and info

#### GET `/api/v1/kazkar/legends`
List all legends with pagination
- Query params: `skip`, `limit`

#### GET `/api/v1/kazkar/stories/{id}`
Get single legend by ID

#### POST `/api/v1/kazkar/import`
Import/update legend from sync pipeline
- Body: `KazkarStoryCreate` schema
- Returns: `KazkarStorySchema`
- Broadcasts: `legend_created` or `legend_updated` event

#### POST `/api/v1/kazkar/broadcast`
Manually broadcast event to WebSocket clients
- Body: `{"event": "event_name", "data": {...}}`

#### WebSocket `/ws/kazkar`
Real-time updates channel
- Events: `legend_created`, `legend_updated`, `legends_synced`, `legend_sense_activated`

### 4. GitHub Action (`.github/workflows/kazkar-sync.yml`)

**Triggers:**
- Push to `main` branch affecting:
  - `docs/legends/**.md`
  - `frontend/src/modules/Kazkar/legends/**`
  - `scripts/sync_legends_to_api.js`
- Manual dispatch with `dry_run` option

**Jobs:**
1. **sync-legends** - Run sync script
2. **notify-websocket** - Broadcast sync completion
3. **verify-deployment** - Health checks

**Secrets Required:**
- `CIMEIKA_API_URL` (optional, defaults to https://api.cimeika.com.ua)

### 5. Frontend Components

#### `LegendScene.tsx`
Main immersive legend display
- Props: `title`, `content`, `senses`, `onPlayVoice`
- Features:
  - Framer Motion animations
  - Ambient audio playback
  - Volume controls
  - WebSocket status indicator
  - Ritual mode toggle

#### `LegendPage.tsx`
Data fetching wrapper
- Fetches legend by ID from API
- Handles loading/error states
- TTS voice playback integration

#### `useKazkarRealtime.ts`
React hook for WebSocket
- Auto-connect/reconnect
- Event listening
- Status tracking
- Options: `autoReconnect`, `maxReconnectAttempts`, `debug`

---

## API Reference

### Import Endpoint

**POST** `/api/v1/kazkar/import`

**Request Body:**
```json
{
  "title": "Legend Title",
  "content": "Legend content...",
  "story_type": "legend",
  "participants": ["Participant1", "Participant2"],
  "location": "Location Name",
  "tags": ["tag1", "tag2"],
  "source_trace": "docs/legends/01_legend.md"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Legend Title",
  "content": "Legend content...",
  "story_type": "legend",
  "participants": ["Participant1", "Participant2"],
  "location": "Location Name",
  "tags": ["tag1", "tag2"],
  "source_trace": "docs/legends/01_legend.md",
  "module": "kazkar",
  "time": "2025-12-25T02:00:00",
  "canon_bundle_id": "cimeika_2024_v1"
}
```

### WebSocket Events

**Connection:**
```javascript
const ws = new WebSocket('wss://api.cimeika.com.ua/ws/kazkar');
```

**Event Format:**
```json
{
  "event": "legend_updated",
  "legend_id": 1,
  "sense": "Spark",
  "timestamp": 1735123802,
  "data": {
    "title": "Updated Legend",
    "action": "updated"
  }
}
```

**Event Types:**
- `connected` - Initial connection confirmation
- `legend_created` - New legend added
- `legend_updated` - Existing legend modified
- `legends_synced` - Batch sync completed
- `legend_sense_activated` - Sense node activated (future)
- `echo` - Server echo response

---

## Workflow Examples

### Adding a New Legend

1. **Create markdown file:**
   ```bash
   # Create docs/legends/06_new_legend.md
   vi docs/legends/06_new_legend.md
   ```

2. **Commit and push:**
   ```bash
   git add docs/legends/06_new_legend.md
   git commit -m "Add new legend: The Cosmic Dance"
   git push origin main
   ```

3. **GitHub Action automatically:**
   - Triggers on push
   - Runs sync script
   - POSTs to `/api/v1/kazkar/import`
   - Broadcasts `legend_created` event
   - Verifies API health

4. **Connected clients:**
   - Receive WebSocket event
   - Update UI automatically
   - Show notification (optional)

### Manual Sync (Local Development)

```bash
# 1. Start backend locally
cd backend
python main.py

# 2. Run sync script
cd ..
node scripts/sync_legends_to_api.js

# 3. Check results
curl http://localhost:8000/api/v1/kazkar/legends
```

### Testing WebSocket

```javascript
// Frontend test
const { lastEvent, status } = useKazkarRealtime({ debug: true });

useEffect(() => {
  if (lastEvent) {
    console.log('Received:', lastEvent);
  }
}, [lastEvent]);
```

```bash
# Backend test
curl -X POST http://localhost:8000/api/v1/kazkar/broadcast \
  -H "Content-Type: application/json" \
  -d '{"event": "test", "message": "Hello WebSocket"}'
```

---

## Troubleshooting

### Sync Script Issues

**Problem:** "Legends directory not found"  
**Solution:** Ensure `docs/legends/` exists and contains `.md` files

**Problem:** "API connection failed"  
**Solution:** Check `API_URL` environment variable and network connectivity

**Problem:** "Import returned 422 error"  
**Solution:** Validate markdown structure matches schema

### WebSocket Issues

**Problem:** WebSocket won't connect  
**Solution:** 
- Check API URL uses `wss://` for HTTPS or `ws://` for HTTP
- Verify CORS settings allow WebSocket connections
- Check browser console for errors

**Problem:** No events received  
**Solution:**
- Verify connection status is `connected`
- Check backend logs for broadcast activity
- Test with manual broadcast endpoint

### GitHub Action Issues

**Problem:** Workflow doesn't trigger  
**Solution:** 
- Verify file paths match workflow triggers
- Check workflow permissions in repository settings

**Problem:** API returns 404  
**Solution:**
- Verify `CIMEIKA_API_URL` secret is set
- Check API is deployed and accessible
- Test endpoint with curl

---

## Environment Variables

### Backend
```env
# Database
POSTGRES_DB=cimeika
POSTGRES_USER=cimeika_user
POSTGRES_PASSWORD=***
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# CORS (must include frontend URL)
CORS_ORIGINS=http://localhost:3000,https://cimeika.com.ua
```

### Frontend
```env
# API URL (used for WebSocket connection)
VITE_API_URL=https://api.cimeika.com.ua
```

### Sync Script
```env
# Override API URL
API_URL=https://api.cimeika.com.ua

# Enable dry run
DRY_RUN=true
```

---

## Performance

### Metrics
- **Sync time:** <5 seconds for 10 legends
- **WebSocket latency:** <100ms
- **Frontend load:** <200KB bundle size
- **Audio load:** Depends on ambient file size

### Optimization Tips
- Keep legend markdown files under 50KB
- Use WebP for images (future)
- Compress ambient audio to <5MB
- Enable CDN for static assets

---

## Security

### API
- CORS properly configured
- Input validation on all endpoints
- Rate limiting (recommended for production)
- Authentication (future enhancement)

### WebSocket
- Origin validation
- Connection limits
- Timeout handling
- Automatic reconnection with backoff

---

## Future Enhancements

1. **Bi-directional WebSocket** - Client → server events
2. **Legend versioning** - Track changes over time
3. **Collaborative editing** - Multi-user legend creation
4. **AI-generated audio** - TTS for legend narration
5. **Visual sync** - Figma → Code automation
6. **Analytics** - Track legend views and engagement
7. **Search** - Full-text search across legends
8. **Categories** - Organize legends by theme

---

## Support

**Documentation:** [docs/KAZKAR_LEGEND_UI_SPEC.md](./KAZKAR_LEGEND_UI_SPEC.md)  
**Figma Spec:** [docs/KAZKAR_LEGEND_UI_FIGMA_SPEC.md](./KAZKAR_LEGEND_UI_FIGMA_SPEC.md)  
**API Docs:** https://api.cimeika.com.ua/api/docs  
**Issues:** https://github.com/Ihorog/cimeika-unified/issues

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-25  
**Maintained by:** Cimeika Core Team
