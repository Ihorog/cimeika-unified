# Logo Replacement Instructions

## Current Status

✅ **Code Updated**: The application code has been updated to use PNG logo files.  
⚠️ **Placeholders Active**: Temporary 1x1 pixel transparent PNG files are in place.  
📋 **Action Required**: Replace placeholders with original logo images.

## What Was Changed

### Files Modified:
1. **frontend/src/layouts/MainLayout.jsx**  
   - Changed import from `logo-cimeika.svg` → `logo-cimeika.png`
   
2. **frontend/src/components/CiFAB/CiFAB.tsx**  
   - Changed import from `icon-ci.svg` → `icon-ci.png`

### Files Added:
1. **frontend/src/assets/logo-cimeika.png**  
   - Placeholder: 1x1px transparent PNG  
   - Needs replacement with actual Cimeika logo
   
2. **frontend/src/assets/icon-ci.png**  
   - Placeholder: 1x1px transparent PNG  
   - Needs replacement with actual Ci icon

3. **frontend/src/assets/ADD_LOGOS_HERE.md**  
   - Detailed instructions for logo replacement

4. **scripts/download-original-logos.sh**  
   - Automated download script (requires network access to GitHub CDN)

## Original Logo Sources

The original logos were provided in PR #7, comment #3677365624:

1. **Cimeika Logo**: https://github.com/user-attachments/assets/85cb4090-480a-465e-b2e3-5924996ed602
2. **Ci Icon**: https://github.com/user-attachments/assets/aa61382b-4288-4631-b116-19df35dba9bb

## How to Complete the Setup

### Option A: Manual Download and Upload (Recommended)

1. **Download the logos**:
   - Visit the URLs above in your browser
   - Save images to your computer

2. **Upload to GitHub**:
   - Navigate to `frontend/src/assets` directory in your branch on GitHub
   - For each placeholder file (`logo-cimeika.png` and `icon-ci.png`):
     - Click the filename
     - Click the trash icon to delete it
     - Click "Add file" → "Upload files"
     - Upload the corresponding original logo
     - Commit changes

### Option B: Using Git Locally

```bash
# 1. Download the images from the GitHub URLs
# 2. Navigate to the assets directory
cd frontend/src/assets

# 3. Replace the placeholder files
cp /path/to/downloaded/cimeika-logo.png logo-cimeika.png
cp /path/to/downloaded/ci-icon.png icon-ci.png

# 4. Commit and push
git add logo-cimeika.png icon-ci.png
git commit -m "Replace logo placeholders with original images"
git push
```

### Option C: Using the Download Script

```bash
# From repository root (requires network access to GitHub CDN)
chmod +x scripts/download-original-logos.sh
./scripts/download-original-logos.sh
```

**Note**: The download script may not work in restricted network environments.

## After Replacement

Once you replace the placeholders:

1. **Verify the logos appear correctly**:
   ```bash
   cd frontend
   npm run dev
   ```
   - Cimeika logo should appear in the header
   - Ci icon should appear in the floating action button (bottom-right)

2. **Optional: Remove old SVG files**:
   ```bash
   git rm frontend/src/assets/logo-cimeika.svg
   git rm frontend/src/assets/icon-ci.svg
   git commit -m "Remove SVG logo placeholders"
   ```

3. **Test on different screen sizes**:
   - Desktop: Full logo should be visible
   - Mobile: Logo should scale appropriately

## Technical Details

- **Framework**: React with Vite
- **Import Method**: ES6 imports (Vite handles asset bundling)
- **Build Status**: ✅ Frontend builds successfully with placeholder PNGs
- **File Sizes**: 
  - Current placeholders: 70 bytes each
  - Expected original images: ~10-100 KB each (depending on resolution)

## Troubleshooting

**If logos don't appear after replacement:**
1. Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
2. Restart the dev server
3. Check browser console for errors
4. Verify file names are exactly: `logo-cimeika.png` and `icon-ci.png`

**If build fails:**
1. Ensure PNG files are valid images
2. Run `npm run build` to check for errors
3. Check that imports match filenames

## Questions?

See `frontend/src/assets/ADD_LOGOS_HERE.md` for more detailed instructions.
