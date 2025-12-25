# KAZKAR LEGEND UI SPECIFICATION

## Overview

This document defines the user interface specifications for the Kazkar Legends interactive storytelling system. The UI is designed to create an immersive, atmospheric experience that transforms text-based legends into multi-sensory journeys.

---

## Design Philosophy

> "Every legend breathes. From silence to spark to rhythm — the system tells its own story."

The Kazkar Legends UI embodies:
- **Immersion**: Deep engagement through animations, sound, and visual design
- **Atmosphere**: Night theme with gradients that evoke mystery and depth
- **Interaction**: Intuitive controls that enhance rather than distract
- **Accessibility**: Clear hierarchy, readable text, keyboard navigation

---

## Theme & Colors

### Night Theme (Kazkar Exclusive)

**Background Gradients:**
```css
/* Main gradient */
background: linear-gradient(to bottom, #000000, #0f172a, #312e81);

/* Card backgrounds */
background: rgba(30, 27, 75, 0.6);
backdrop-filter: blur(12px);
```

**Text Colors:**
- Primary text: `#e0e7ff` (light indigo)
- Secondary text: `#c7d2fe` (soft indigo)
- Muted text: `#a5b4fc` (light blue-indigo)

**Accent Colors:**
- Primary accent: `#6366f1` to `#8b5cf6` (indigo to purple gradient)
- Borders: `rgba(139, 92, 246, 0.3)`
- Shadows: `rgba(99, 102, 241, 0.4)`

---

## Typography

**Headings:**
- Font size: `3rem` (48px)
- Font weight: `bold` (700)
- Gradient text fill: `linear-gradient(135deg, #818cf8, #c4b5fd)`
- Line height: `1.2`

**Body Text:**
- Font size: `1.25rem` (20px)
- Line height: `1.8`
- Color: `#c7d2fe`
- Whitespace: `pre-wrap` (preserves formatting)

**Labels:**
- Font size: `0.875rem` (14px)
- Text transform: `uppercase`
- Letter spacing: `0.1em`
- Color: `#a5b4fc`

---

## Layout Components

### 1. LegendScene (Main View)

**Container:**
- Min height: `100vh`
- Padding: `2rem`
- Display: `flex`, direction: `column`, align: `center`

**Content Card:**
- Max width: `900px`
- Border radius: `32px`
- Padding: `3rem`
- Shadow: `0 20px 60px rgba(99, 102, 241, 0.4), 0 0 100px rgba(139, 92, 246, 0.2)`
- Border: `1px solid rgba(139, 92, 246, 0.3)`

### 2. Sense Nodes

**Container:**
- Display: `flex`, wrap: `wrap`
- Gap: `1rem`

**Individual Node:**
- Background: `rgba(99, 102, 241, 0.2)`
- Border: `1px solid rgba(139, 92, 246, 0.5)`
- Border radius: `20px`
- Padding: `0.75rem 1.5rem`
- Shadow: `0 4px 12px rgba(99, 102, 241, 0.3)`
- Emoji size: `1.5rem`

### 3. Control Buttons

**Primary Button (Voice):**
- Background: `linear-gradient(135deg, #6366f1, #8b5cf6)`
- Border radius: `12px`
- Padding: `1rem 2rem`
- Font weight: `600`
- Shadow: `0 8px 20px rgba(99, 102, 241, 0.4)`
- Hover: translate up 2px, shadow expands

**Secondary Button (Ritual Mode):**
- Background: `rgba(79, 70, 229, 0.2)`
- Border: `1px solid rgba(139, 92, 246, 0.5)`
- Border radius: `12px`
- Padding: `1rem 2rem`
- Hover: background intensifies to `0.3`

---

## Animations (Framer Motion)

### Entry Animations

**Main Container:**
```javascript
initial: { opacity: 0 }
animate: { opacity: 1 }
transition: { duration: 0.8 }
```

**Content Card:**
```javascript
initial: { y: 20, opacity: 0 }
animate: { y: 0, opacity: 1 }
transition: { delay: 0.3, duration: 0.6 }
```

**Title:**
```javascript
initial: { opacity: 0, y: -10 }
animate: { opacity: 1, y: 0 }
transition: { delay: 0.5, duration: 0.6 }
```

**Content Text:**
```javascript
initial: { opacity: 0 }
animate: { opacity: 1 }
transition: { delay: 0.7, duration: 0.8 }
```

**Sense Nodes (staggered):**
```javascript
initial: { opacity: 0, scale: 0.8 }
animate: { opacity: 1, scale: 1 }
transition: { 
  delay: 1.1 + index * 0.1,
  duration: 0.4,
  type: 'spring',
  stiffness: 200
}
```

### Interaction Animations

**Button Hover:**
- Transform: `translateY(-2px)`
- Shadow expansion
- Transition: `0.2s`

---

## Audio Integration

### Voice Playback (TTS)

**API Endpoint:**
```
GET /api/tts?text={encoded_legend_text}
```

**Trigger:** "Озвучити" button click  
**Content:** Full legend text (title + content)  
**Error handling:** Silent fail with console warning

### Ambient Sound

**File Location:**
```
/public/audio/kazkar_ambient.mp3
```

**Playback:**
- Auto-loop: Yes
- Volume control: User-adjustable (0-100%)
- Start on: Legend scene mount
- Stop on: Scene unmount or user pause

**Controls:**
- Volume slider (0-100%)
- Play/Pause toggle
- Position: Bottom-right corner, semi-transparent

---

## Ritual Mode

**Activation:** Button click "Режим Ритуалу"  
**Visual Changes:**
- Darken background further (add overlay)
- Slow down animations (0.5x speed)
- Increase blur intensity
- Hide non-essential UI elements

**Audio Enhancement:**
- Lower ambient volume to 40%
- Add binaural beats layer (optional)
- TTS voice becomes more deliberate (slower)

**Exit:** "Повернутися" button or ESC key

---

## Responsive Design

### Desktop (>1024px)
- Content card: 900px max width
- Two-column sense nodes layout
- Large font sizes (as specified)

### Tablet (768px - 1024px)
- Content card: 100% width with 2rem padding
- Single-column sense nodes
- Font sizes: scale to 90%

### Mobile (<768px)
- Content card: Full width, 1rem padding
- Stack buttons vertically
- Font sizes: scale to 80%
- Reduce animations complexity

---

## Accessibility

**Keyboard Navigation:**
- Tab order: Title → Content → Sense Nodes → Buttons
- Enter/Space: Activate buttons
- ESC: Exit Ritual Mode

**Screen Readers:**
- All buttons have `aria-label`
- Sense nodes have readable labels
- Loading/Error states announced

**Focus States:**
- Visible focus ring: `2px solid #8b5cf6`
- Offset: `2px`

---

## Loading & Error States

### Loading
- Centered spinner or "✦" symbol
- Text: "Завантаження легенди..."
- Background: Same night gradient
- Animation: gentle pulse

### Error
- Centered ⚠️ emoji
- Error message in red-ish tone (`#fca5a5`)
- Background: Same night gradient
- Retry option (future enhancement)

### Not Found
- Text: "Легенду не знайдено"
- Background: Same night gradient
- Link to browse all legends

---

## Performance Targets

- **First paint:** <1s
- **Animation FPS:** 60fps consistently
- **Audio load:** <500ms
- **Image optimization:** WebP with fallback
- **Bundle size:** <200KB (excluding audio)

---

## Future Enhancements

1. **Interactive Sense Map:** Click sense nodes to filter/navigate
2. **Reading Progress:** Track scroll position
3. **Bookmarks:** Save reading position
4. **Social Sharing:** Generate legend preview cards
5. **Multiple Voices:** Choose TTS voice and language
6. **Background Customization:** User-selectable themes
7. **Export:** Save legend as PDF or audio file

---

## Implementation Checklist

- [x] LegendScene.tsx component with animations
- [x] LegendRitualMode.tsx immersive view
- [x] LegendPage.tsx data fetching wrapper
- [x] legends.css custom styles
- [ ] Ambient audio playback
- [ ] Volume controls
- [ ] WebSocket real-time updates
- [ ] Keyboard navigation
- [ ] Screen reader optimization
- [ ] Performance monitoring

---

**Version:** 1.0.0  
**Last Updated:** 2025-12-25  
**Maintained by:** Cimeika Core Team
