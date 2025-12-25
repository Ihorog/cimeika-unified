# Scripts

Utility scripts for Cimeika project management.

## Available Scripts

### Kazkar Legends Sync

#### `sync_legends_to_api.js`
Synchronizes legend markdown files from `/docs/legends/` to the Cimeika API.

**Usage:**
```bash
# Normal sync
node scripts/sync_legends_to_api.js

# Dry run (no API calls)
DRY_RUN=true node scripts/sync_legends_to_api.js

# Custom API URL
API_URL=https://api.cimeika.com.ua node scripts/sync_legends_to_api.js
```

**Environment Variables:**
- `API_URL` - Base URL for the API (default: http://localhost:8000)
- `DRY_RUN` - Set to 'true' to preview without sending (default: false)

**Features:**
- Parses structured markdown legends
- Extracts metadata (type, participants, location, tags)
- Deduplicates by source_trace
- Batch import with error handling
- Progress reporting

---

#### `verify_kazkar_pipeline.js`
Comprehensive verification of the Kazkar Legends Sync Pipeline.

**Usage:**
```bash
# Default (localhost)
node scripts/verify_kazkar_pipeline.js

# Production
API_URL=https://api.cimeika.com.ua node scripts/verify_kazkar_pipeline.js
```

**Environment Variables:**
- `API_URL` - Base URL for the API (default: http://localhost:8000)
- `FRONTEND_URL` - Frontend URL (default: http://localhost:3000)

**Tests:**
1. ✅ Legends directory exists
2. ✅ Sync script exists
3. ✅ API health check
4. ✅ Kazkar module endpoint
5. ✅ Legends endpoint
6. ✅ Import endpoint
7. ✅ WebSocket endpoint
8. ✅ Specification files
9. ✅ GitHub Action workflow
10. ✅ Frontend files

**Exit Codes:**
- `0` - All tests passed
- `1` - One or more tests failed

---

### SEO Health Check

#### `seo/seo_health_report.mjs`
Generates SEO health report for the Cimeika SEO matrix.

**Usage:**
```bash
npm run seo:health
```

See `seo/` directory for more details.

---

### Deployment Verification

#### `verify-deployment.sh`
Shell script to verify deployment status across services.

**Usage:**
```bash
bash scripts/verify-deployment.sh
```

---

#### `verify-modules.sh`
Verifies all 7 Cimeika modules are properly configured.

**Usage:**
```bash
bash scripts/verify-modules.sh
```

---

## Contributing

When adding new scripts:

1. **Use descriptive names** - `verb_noun.js` or `noun_action.sh`
2. **Add documentation** - Update this README with usage examples
3. **Make executable** - `chmod +x scripts/new_script.js`
4. **Add error handling** - Exit codes and meaningful messages
5. **Environment variables** - Document all required/optional vars
6. **Test locally** - Before committing, test in dev environment

---

## See Also

- [Kazkar Sync Pipeline Guide](../docs/KAZKAR_SYNC_PIPELINE_GUIDE.md)
- [GitHub Actions Workflows](../.github/workflows/README.md)
- [API Documentation](../docs/API_DOCUMENTATION.md)
