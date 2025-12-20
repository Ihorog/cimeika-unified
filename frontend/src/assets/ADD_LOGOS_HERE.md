# Original Logo Files - Replace Placeholders

⚠️ **IMPORTANT**: The PNG files in this directory are placeholders (1x1 transparent pixels).

## What You Need to Do

Replace these placeholder files with the actual logo images:

1. **logo-cimeika.png** - Full Cimeika wordmark logo  
   - Replace with: https://github.com/user-attachments/assets/85cb4090-480a-465e-b2e3-5924996ed602
   - Current: 1x1px placeholder
   - Recommended: ~400x120px or similar aspect ratio

2. **icon-ci.png** - Ci icon for floating action button  
   - Replace with: https://github.com/user-attachments/assets/aa61382b-4288-4631-b116-19df35dba9bb
   - Current: 1x1px placeholder  
   - Recommended: 48x48px to 128x128px (square)

## How to Replace (Choose One Method)

### Method 1: GitHub Web Interface (Easiest)
1. Download the images from the URLs above
2. Navigate to this directory on GitHub (frontend/src/assets)
3. Click on `logo-cimeika.png` → Click the pencil icon (Edit) → Click "Delete this file"
4. Click "Add file" → "Upload files" → Upload your downloaded Cimeika logo
5. Repeat for `icon-ci.png` with the Ci icon
6. Commit changes

### Method 2: Local Git
```bash
# Download images from the GitHub comment and save them locally, then:
cd frontend/src/assets

# Replace the placeholder files with your actual images
cp /path/to/your/cimeika-logo.png logo-cimeika.png
cp /path/to/your/ci-icon.png icon-ci.png

# Commit and push
git add logo-cimeika.png icon-ci.png
git commit -m "Replace logo placeholders with original images"
git push
```

### Method 3: Using the Download Script
```bash
# From the repository root (requires network access to GitHub CDN)
./scripts/download-original-logos.sh
```

## Code Changes Already Made

✅ The following files have been updated to use PNG instead of SVG:
- `frontend/src/layouts/MainLayout.jsx` - imports `logo-cimeika.png`
- `frontend/src/components/CiFAB/CiFAB.tsx` - imports `icon-ci.png`

## File Format Requirements

- **Format**: PNG with transparency (RGBA)
- **Cimeika Logo**: Wide aspect ratio (e.g., 4:1 or 3:1)
- **Ci Icon**: Square aspect ratio (1:1)
- **Quality**: High resolution for retina displays (2x recommended)
- **Background**: Transparent

## After Replacement

Once you replace the placeholders:
1. The logos will automatically appear in the application
2. You can optionally delete the old SVG files:
   ```bash
   git rm frontend/src/assets/logo-cimeika.svg
   git rm frontend/src/assets/icon-ci.svg
   ```

## Testing

After replacing the files, test the application:
```bash
cd frontend
npm run dev
```

Then check:
- ✓ Cimeika logo appears in the header
- ✓ Ci icon appears in the floating action button (bottom-right)
- ✓ Logos scale properly on different screen sizes

