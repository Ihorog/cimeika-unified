# Cimeika 3D Visualization System

## 🌌 Overview

Interactive 3D visualization of the Cimeika ecosystem, featuring 7 modules orbiting around the central Ci core.

## 📁 Structure

```
components/Cimeika3D/
├── Cimeika3DMap_v2.jsx        ← Main 3D scene orchestrator
├── ModuleSphere.jsx            ← Module visualization with breathing, particles, halo
├── ConnectionLine.jsx          ← Animated connections between nodes
├── StarField.jsx               ← Background with Perlin noise + particles
├── AudioLayer.jsx              ← Ambient sound atmosphere
└── index.js                    ← Exports
```

## 🎨 Features

### Cimeika3DMap_v2.jsx
- Main Canvas with module animation and background
- Orbital camera controls (auto-rotate, zoom, rotate)
- Module positioning and layout
- Click handling for module navigation
- Audio control toggle

### ModuleSphere.jsx
- Natural breathing animation (subtle scale pulse)
- Orbital particle system (20 particles per module)
- Halo ring with glow effect
- Module-specific color schemes
- Interactive hover states
- Smooth transitions

### StarField.jsx
- Dynamic shader-based background
- Warm-cold gradient with Perlin noise
- 1000 particle stars with depth
- Slow rotation for depth perception

### ConnectionLine.jsx
- Bezier curve connections between modules
- Animated opacity with breathing effect
- Transparent, living lines
- Synchronized with module animations

### AudioLayer.jsx
- Smooth fade-in/out transitions
- Volume control
- Loop functionality
- User-initiated playback (browser autoplay policy)

## 🎯 Module Configuration

Seven modules with distinct positions and colors:

| Module | ID | Position | Color | Description |
|--------|-------|----------|-------|-------------|
| Ci | `ci` | [0, 0, 0] | Purple-Blue | Central coordinator |
| Казкар | `kazkar` | [6, 2, 0] | Pink-Red | Storyteller |
| ПоДія | `podija` | [4, -3, 3] | Blue-Cyan | Events |
| Настрій | `nastrij` | [-5, 2, 2] | Green-Teal | Mood |
| Маля | `malya` | [-4, -2, -3] | Pink-Yellow | Creative |
| Галерея | `gallery` | [2, 3, -4] | Cyan-Purple | Gallery |
| Календар | `calendar` | [-2, -4, 1] | Teal-Pink | Calendar |

## 🔧 Dependencies

```json
{
  "@react-three/fiber": "^9.x",
  "@react-three/drei": "^9.x",
  "three": "^0.x",
  "framer-motion": "^10.x"
}
```

Install with:
```bash
npm install --legacy-peer-deps @react-three/fiber @react-three/drei three framer-motion
```

## 🚀 Usage

```jsx
import { Cimeika3DMap_v2 } from './components/Cimeika3D';

function App() {
  const handleModuleClick = (module) => {
    console.log('Clicked:', module.id);
    // Navigate to module
  };

  return (
    <Cimeika3DMap_v2 onModuleClick={handleModuleClick} />
  );
}
```

## 🎬 Animations

### Module Breathing
- Period: 0.5 Hz (2 seconds per cycle)
- Scale variation: ±5%
- Synchronized across sphere and halo

### Particle Orbits
- 20 particles per module
- Individual velocities
- Vertical wobble for depth
- Continuous rotation

### Background
- Shader-based Perlin noise
- Time-animated gradient
- Slow particle rotation
- Depth parallax effect

## 🎨 Visual Effects

1. **Glow System**: Three-layer depth
   - Outer glow (BackSide rendering)
   - Halo ring (transparent torus)
   - Inner sphere (emissive material)

2. **Lighting**:
   - Ambient light (30% intensity)
   - Two point lights (white + blue)
   - Module-specific emissive colors

3. **Materials**:
   - Standard material with metalness
   - Emissive properties for glow
   - Transparent overlays
   - Color-coded per module

## 🔊 Audio Layer

The AudioLayer component provides ambient atmosphere:
- Fade-in: 3 seconds
- Fade-out: 2 seconds  
- Volume: 30% (configurable)
- Loop: Enabled

**Note**: Add audio file to `/assets/3d/ambient_cimeika.mp3`

## ⚙️ Performance

- LOD: Sphere geometry at 32 segments
- Particle count: 1000 (background) + 140 (modules)
- Auto-culling enabled
- Optimized shader calculations

## 🎮 Controls

- **Left Mouse**: Rotate camera
- **Scroll**: Zoom in/out
- **Auto-rotate**: Enabled (0.5 speed)
- **Module Click**: Navigate to module
- **Audio Toggle**: Top-right button

## 🖼️ Assets Directory

```
assets/3d/
├── ambient_cimeika.mp3         ← Background ambient track (loop)
└── backgroundOverlay.png       ← Optional texture overlay (not implemented)
```

## 🔮 Future Enhancements

- [ ] Module-specific particle shapes
- [ ] Interactive connection highlighting
- [ ] Module activity indicators
- [ ] VR/AR support via @react-three/xr
- [ ] Dynamic module repositioning
- [ ] Text labels with HTML overlay
- [ ] Loading progress indicator
- [ ] Mobile touch controls optimization

## 📖 Integration

Currently integrated in:
- **Ci Module** (`/frontend/src/modules/ci/CiView.jsx`)

Can be integrated anywhere:
```jsx
import { Cimeika3DMap_v2 } from '@/components/Cimeika3D';
```

## 🐛 Known Issues

- Audio autoplay may be blocked by browser policy (user interaction required)
- Line width limited to 1px on some WebGL implementations
- Mobile performance may require particle count reduction

## 📝 Technical Notes

- Built with React Three Fiber (R3F)
- Uses declarative 3D rendering
- Hooks-based animation (`useFrame`)
- Memoized geometries for performance
- Suspense boundaries for loading states

---

**Created with ❤️ for Cimeika ecosystem visualization**
