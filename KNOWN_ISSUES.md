# Known Issues and Future Improvements

## Critical Issues to Address

### 1. Delete Operation Index Bug (PARTIALLY FIXED)
- **Status**: Fixed in podiya.html
- **Remaining**: kazkar, nastriy, malya, gallery modules
- **Issue**: Delete operations use sorted array indices which can cause wrong item deletion
- **Solution**: Use item IDs instead of indices for deletion (implemented in podiya.html)

### 2. Accessibility Issues
- **Issue**: Using native `prompt()` for data input
- **Impact**: Poor UX, not screen-reader friendly, blocks main thread
- **Solution**: Implement custom modal dialogs with proper ARIA labels

### 3. Performance - Large Image Storage
- **Issue**: Storing base64 images in CRDT causes memory/sync issues
- **Solution**: Use separate blob storage with references in CRDT

### 4. Security
- **Issue**: CORS headers too permissive (`Access-Control-Allow-Origin: *`)
- **Solution**: Restrict to specific origins or remove if not needed

### 5. Device ID Generation
- **Issue**: Using `Math.random()` which is not cryptographically secure
- **Solution**: Use `crypto.randomUUID()` for collision-free IDs

## Non-Critical Issues

### 6. Focus Indicators
- Missing :focus styles for keyboard navigation
- Add focus-visible styles to all interactive elements

### 7. Service Worker Updates
- No user notification for available updates
- Consider implementing update prompt

### 8. Migration Logic
- Only migrates if CRDT is empty (data loss risk)
- Use per-device migration flag

### 9. Semantic HTML
- Interactive cards use divs instead of buttons
- Add proper ARIA roles and keyboard handlers

### 10. Event Listener Memory Leaks
- Breadcrumb creates new listeners on each render
- Use event delegation or cleanup old listeners

## Recommendations

1. **Immediate**: Fix delete operations in remaining modules
2. **High Priority**: Replace prompts with modal dialogs
3. **High Priority**: Implement image optimization/compression
4. **Medium Priority**: Add accessibility improvements
5. **Medium Priority**: Implement update notifications
6. **Low Priority**: UI polish and animations
