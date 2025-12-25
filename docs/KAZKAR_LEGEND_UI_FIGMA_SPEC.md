# KAZKAR LEGEND UI FIGMA SPECIFICATION

## Overview

This document specifies the Figma design integration for the Kazkar Legends module, ensuring visual continuity between design and implementation. It defines design tokens, component frames, and synchronization protocols.

---

## Figma Project

**Project Name:** Ihor Hlushchuk's team library  
**File URL:** https://www.figma.com/file/D2eFTza3H8PAEJrW1BnMQp/Ihor-Hlushchuk-s-team-library  
**Access:** Team shared (read-only for automation)

---

## Design Tokens

### Color Tokens

#### Kazkar Night Theme

| Token Name | Value | Usage |
|------------|-------|-------|
| `kazkar-bg-start` | `#000000` | Gradient start |
| `kazkar-bg-mid` | `#0f172a` | Gradient middle |
| `kazkar-bg-end` | `#312e81` | Gradient end |
| `kazkar-card-bg` | `rgba(30, 27, 75, 0.6)` | Card background |
| `kazkar-text-primary` | `#e0e7ff` | Main text |
| `kazkar-text-secondary` | `#c7d2fe` | Secondary text |
| `kazkar-text-muted` | `#a5b4fc` | Muted/label text |
| `kazkar-accent-start` | `#6366f1` | Accent gradient start |
| `kazkar-accent-end` | `#8b5cf6` | Accent gradient end |
| `kazkar-border` | `rgba(139, 92, 246, 0.3)` | Border color |
| `kazkar-shadow` | `rgba(99, 102, 241, 0.4)` | Shadow color |
| `kazkar-error` | `#fca5a5` | Error messages |

### Typography Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| `kazkar-heading-size` | `48px / 3rem` | Legend titles |
| `kazkar-heading-weight` | `700` | Title weight |
| `kazkar-heading-height` | `1.2` | Title line height |
| `kazkar-body-size` | `20px / 1.25rem` | Body text |
| `kazkar-body-weight` | `400` | Body weight |
| `kazkar-body-height` | `1.8` | Body line height |
| `kazkar-label-size` | `14px / 0.875rem` | Labels/tags |
| `kazkar-label-weight` | `600` | Label weight |
| `kazkar-label-spacing` | `0.1em` | Letter spacing |

### Spacing Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| `kazkar-space-xs` | `0.5rem / 8px` | Tiny gaps |
| `kazkar-space-sm` | `1rem / 16px` | Small gaps |
| `kazkar-space-md` | `1.5rem / 24px` | Medium gaps |
| `kazkar-space-lg` | `2rem / 32px` | Large gaps |
| `kazkar-space-xl` | `3rem / 48px` | Extra large gaps |

### Border Radius Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| `kazkar-radius-sm` | `12px` | Buttons, small cards |
| `kazkar-radius-md` | `20px` | Sense nodes |
| `kazkar-radius-lg` | `32px` | Main content cards |

### Shadow Tokens

| Token Name | Value | Usage |
|------------|-------|-------|
| `kazkar-shadow-sm` | `0 4px 12px rgba(99, 102, 241, 0.3)` | Sense nodes |
| `kazkar-shadow-md` | `0 8px 20px rgba(99, 102, 241, 0.4)` | Buttons |
| `kazkar-shadow-lg` | `0 20px 60px rgba(99, 102, 241, 0.4)` | Main cards |
| `kazkar-shadow-glow` | `0 0 100px rgba(139, 92, 246, 0.2)` | Card glow effect |

---

## Component Frames

### 1. Legend Scene Frame

**Frame Name:** `Kazkar/LegendScene`  
**Size:** 1440 x 1024 (desktop)  
**Variants:**
- `default` - Normal view
- `loading` - Loading state
- `error` - Error state
- `ritual` - Ritual mode

**Layers:**
1. Background gradient
2. Content card
3. Title (with gradient text)
4. Body text
5. Sense nodes container
6. Control buttons

### 2. Sense Node Frame

**Frame Name:** `Kazkar/SenseNode`  
**Size:** Auto (fits content)  
**Variants:**
- `default` - Normal state
- `hover` - Hover state
- `active` - Active/selected state

**Layers:**
1. Background pill
2. Border
3. Emoji/icon (left)
4. Label text (right)

### 3. Control Button Frame

**Frame Name:** `Kazkar/Button`  
**Variants:**
- `primary` - Voice button
- `secondary` - Ritual mode button
- `disabled` - Disabled state

**Layers:**
1. Background (gradient or semi-transparent)
2. Border (if secondary)
3. Icon/emoji (left)
4. Button text (right)
5. Shadow effect

### 4. Ritual Mode Frame

**Frame Name:** `Kazkar/RitualMode`  
**Size:** 1440 x 1024 (desktop)  
**Variants:**
- `default` - Normal ritual view
- `with-audio` - With volume controls

**Layers:**
1. Darkened overlay
2. Blurred background
3. Centered content
4. Ambient visualization (optional)
5. Return button

---

## Figma Variables Export

### Export Format

**File:** `/docs/figma_tokens.json`

```json
{
  "kazkar": {
    "colors": {
      "bg-start": "#000000",
      "bg-mid": "#0f172a",
      "bg-end": "#312e81",
      "card-bg": "rgba(30, 27, 75, 0.6)",
      "text-primary": "#e0e7ff",
      "text-secondary": "#c7d2fe",
      "text-muted": "#a5b4fc",
      "accent-start": "#6366f1",
      "accent-end": "#8b5cf6",
      "border": "rgba(139, 92, 246, 0.3)",
      "shadow": "rgba(99, 102, 241, 0.4)",
      "error": "#fca5a5"
    },
    "typography": {
      "heading-size": "3rem",
      "heading-weight": "700",
      "heading-height": "1.2",
      "body-size": "1.25rem",
      "body-weight": "400",
      "body-height": "1.8",
      "label-size": "0.875rem",
      "label-weight": "600",
      "label-spacing": "0.1em"
    },
    "spacing": {
      "xs": "0.5rem",
      "sm": "1rem",
      "md": "1.5rem",
      "lg": "2rem",
      "xl": "3rem"
    },
    "radius": {
      "sm": "12px",
      "md": "20px",
      "lg": "32px"
    },
    "shadows": {
      "sm": "0 4px 12px rgba(99, 102, 241, 0.3)",
      "md": "0 8px 20px rgba(99, 102, 241, 0.4)",
      "lg": "0 20px 60px rgba(99, 102, 241, 0.4)",
      "glow": "0 0 100px rgba(139, 92, 246, 0.2)"
    }
  }
}
```

---

## Synchronization Protocol

### Manual Sync (Designer → Developer)

1. **Designer Updates Figma:**
   - Modify colors, typography, or spacing in Figma
   - Update component frames
   - Add comment: "Ready for sync"

2. **Developer Exports Variables:**
   - Use Figma Variables Export plugin
   - Save to `/docs/figma_tokens.json`
   - Commit to repository

3. **Developer Updates CSS:**
   - Import tokens into CSS variables
   - Update component styles
   - Test visual consistency

4. **Visual QA:**
   - Compare Figma frames with live UI
   - Screenshot comparison
   - Pixel-perfect adjustments

### Automated Sync (Future)

**Planned Integration:**
- Figma Webhooks → GitHub Actions
- Auto-generate CSS variables from Figma API
- Visual regression testing (Percy/Chromatic)
- Automatic PR creation on design updates

---

## Sync Configuration

**File:** `/docs/figma_sync.json`

```json
{
  "source": "https://github.com/Ihorog/cimeika-unified/tree/main/docs/KAZKAR_LEGEND_UI_FIGMA_SPEC.md",
  "target": "https://www.figma.com/file/D2eFTza3H8PAEJrW1BnMQp/Ihor-Hlushchuk-s-team-library",
  "sync": ["colors", "tokens", "frames", "text"],
  "automation": {
    "enabled": false,
    "webhook_url": null,
    "github_action": ".github/workflows/figma-sync.yml"
  },
  "mapping": {
    "figma_page": "Kazkar Legends",
    "token_file": "docs/figma_tokens.json",
    "css_output": "frontend/src/modules/Kazkar/legends/legends.css"
  }
}
```

---

## Design Guidelines

### Gradient Usage

**Background gradients:**
- Always use 3+ color stops
- Direction: `to bottom` (top to bottom)
- Smooth transitions between colors

**Text gradients:**
- Direction: `135deg` (diagonal)
- Use for headings only
- Ensure readability on all backgrounds

### Animation Guidelines

**Micro-interactions:**
- Hover effects: 200ms ease
- Button presses: 150ms ease-out
- Loading spinners: 1s linear infinite

**Page transitions:**
- Entry: 600-800ms ease-out
- Exit: 400ms ease-in
- Stagger children: +100ms per item

### Accessibility Standards

**Color Contrast:**
- Minimum ratio: 4.5:1 (text)
- Large text: 3:1
- Interactive elements: 3:1

**Focus States:**
- Visible outline: 2px solid
- Offset: 2px
- Color: `#8b5cf6`

---

## Component Specifications

### LegendScene Component

**Figma Frame:** `Kazkar/LegendScene/default`

**Spacing:**
- Container padding: `2rem` (all sides)
- Card max-width: `900px`
- Card padding: `3rem`
- Title margin-bottom: `2rem`
- Content margin-bottom: `3rem`
- Sense nodes margin-bottom: `2rem`
- Control buttons margin-top: `2rem`

**Responsive Breakpoints:**
- Desktop: >1024px (as specified)
- Tablet: 768px - 1024px (card full width)
- Mobile: <768px (reduced padding)

### Sense Node Component

**Figma Frame:** `Kazkar/SenseNode/default`

**Dimensions:**
- Auto width (fits content)
- Min-width: `120px`
- Height: `auto`
- Padding: `0.75rem 1.5rem`

**Content:**
- Emoji size: `1.5rem`
- Label size: `1rem`
- Gap: `0.5rem`

---

## Visual Regression Testing

### Screenshot Locations

Store reference screenshots in `/docs/figma_reference/`:

```
/docs/figma_reference/
├── kazkar-legend-scene-default.png
├── kazkar-legend-scene-loading.png
├── kazkar-legend-scene-error.png
├── kazkar-legend-scene-ritual.png
├── kazkar-sense-node-default.png
├── kazkar-sense-node-hover.png
├── kazkar-button-primary.png
└── kazkar-button-secondary.png
```

### Comparison Process

1. **Capture Figma Screenshot:**
   - Export frame at 2x resolution
   - PNG format, no background

2. **Capture Live UI Screenshot:**
   - Use Playwright/Puppeteer
   - Same viewport size as Figma
   - Same content/data

3. **Compare:**
   - Pixel-diff threshold: 0.1% (allow for anti-aliasing)
   - Highlight differences in red overlay
   - Generate report

---

## Maintenance Schedule

**Weekly:**
- Check for Figma updates
- Review designer comments
- Update token JSON if needed

**Monthly:**
- Full visual audit
- Screenshot comparison
- Performance check

**Quarterly:**
- Design system review
- Token cleanup
- Documentation update

---

## Contact & Resources

**Design Team:** design@cimeika.com.ua  
**Figma Access:** Request via GitHub issue  
**Sync Issues:** Tag `figma-sync` in repository

**Tools:**
- Figma Variables Export Plugin
- Figma Tokens Studio (optional)
- Percy.io (visual testing)
- Chromatic (Storybook integration)

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-25  
**Maintained by:** Cimeika Design & Dev Team
