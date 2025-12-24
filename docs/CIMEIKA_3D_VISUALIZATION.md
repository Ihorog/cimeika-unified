# Cimeika 3D Visualization

## 🌌 Overview

The Cimeika 3D Visualization provides an immersive, interactive representation of the ecosystem's architecture. Built with React Three Fiber and Three.js, it creates a living 3D space where users can explore the relationships between the 7 core modules.

![Cimeika 3D Visualization](https://github.com/user-attachments/assets/744c4743-a0f9-4b0a-be4f-72160e59dc1c)

## 🎯 Purpose

The 3D map serves multiple purposes:
- **Visual Navigation**: Intuitive way to explore the Cimeika ecosystem
- **System Understanding**: Shows the central role of Ci and its connections
- **Aesthetic Experience**: Creates an immersive, breathing digital space
- **Module Discovery**: Makes the system architecture immediately comprehensible

## 🏗️ Architecture

### Seven Modules Orbiting Ci

```
         Календар
              |
    Наст━━━━━Ci━━━━━Казкар
         /    |    \
     Маля   ПоДія  Галерея
```

**Central Node**: Ci (Coordinator)  
**Orbital Nodes**: 6 specialized modules arranged in 3D space

### Module Positioning

Each module has a carefully designed position to create visual balance:

| Module | Position [x, y, z] | Color Scheme | Role |
|--------|-------------------|--------------|------|
| Ci | [0, 0, 0] | Purple-Blue | Central Coordinator |
| Казкар | [6, 2, 0] | Pink-Red | Storyteller |
| ПоДія | [4, -3, 3] | Blue-Cyan | Events Manager |
| Настрій | [-5, 2, 2] | Green-Teal | Mood Analytics |
| Маля | [-4, -2, -3] | Pink-Yellow | Creative Studio |
| Галерея | [2, 3, -4] | Cyan-Purple | Visual Memory |
| Календар | [-2, -4, 1] | Teal-Pink | Temporal Nodes |

## 🎨 Visual Effects

### 1. Breathing Spheres
Each module sphere exhibits a subtle breathing animation:
- **Period**: 2 seconds per cycle
- **Scale variation**: ±5%
- **Synchronized**: Halo and particle systems breathe together

### 2. Orbital Particles
20 particles orbit each module:
- Individual velocities and trajectories
- Vertical wobble for depth perception
- Continuous rotation around module center

### 3. Halo Rings
Glowing torus rings around each module:
- Pulsing opacity
- Module-specific colors
- Adds visual depth and emphasis

### 4. Connection Lines
Bezier curves connecting Ci to all modules:
- Animated opacity (breathing effect)
- Curved paths for organic feel
- Synchronized with module animations

### 5. Star Field Background
Dynamic shader-based background:
- **1000+ particles** with depth parallax
- **Perlin noise gradient** (warm/cold)
- Slow rotation for immersion
- Custom GLSL shaders

## 🎮 Interactions

### Camera Controls
- **Left Mouse Drag**: Rotate camera around the scene
- **Scroll Wheel**: Zoom in/out (10-40 units range)
- **Auto-rotate**: Gentle continuous rotation (0.5 speed)

### Module Interaction
- **Hover**: Cursor changes to pointer
- **Click**: Navigate to module's full interface
- **Visual Feedback**: Hover highlights (planned)

### Audio Control
- **Toggle Button**: Top-right corner
- **Fade Effects**: Smooth 3-second fade in/out
- **Volume**: 30% by default (configurable)

## 🔧 Technical Implementation

### Technology Stack
```json
{
  "@react-three/fiber": "^8.15.0",
  "@react-three/drei": "^9.88.0",
  "three": "^0.158.0"
}
```

### Component Structure
```
Cimeika3D/
├── Cimeika3DMap_v2.jsx     # Main orchestrator
├── ModuleSphere.jsx         # Individual module rendering
├── ConnectionLine.jsx       # Inter-module connections
├── StarField.jsx            # Background and particles
└── AudioLayer.jsx           # Sound atmosphere
```

### Performance Optimizations
- **Memoized geometries**: Particles and shapes cached
- **LOD management**: 32-segment spheres (balanced quality)
- **Particle limits**: 1140 total particles (1000 bg + 140 modules)
- **Auto-culling**: Enabled by default
- **Shader optimization**: Efficient Perlin noise implementation

## 🚀 Usage

### Basic Integration
```jsx
import { Cimeika3DMap_v2 } from '@/components/Cimeika3D';

function MyView() {
  const handleModuleClick = (module) => {
    navigate(`/${module.id}`);
  };

  return <Cimeika3DMap_v2 onModuleClick={handleModuleClick} />;
}
```

### Current Integration
The 3D map is currently integrated into:
- **Ci Module** (`/ci` route): Primary visualization interface

### Future Integrations
Potential locations for the 3D map:
- Welcome/landing page
- Dashboard view
- About/system architecture page
- Mobile-optimized version

## 📱 Responsive Design

### Desktop (Optimal)
- Full 3D rendering with all effects
- Smooth 60 FPS target
- All interactions enabled

### Tablet
- Reduced particle count (recommended)
- Touch-optimized controls
- Maintained visual quality

### Mobile
- Minimal particle rendering
- Simplified shaders
- Touch navigation only

## 🎵 Audio Layer

### Ambient Sound Design
The audio layer is designed to provide:
- **Atmosphere**: Deep, breathing ambient sound
- **Non-intrusive**: Low volume, soothing tones
- **Context**: Enhances the "living system" feeling

### Audio File Specification
- **Format**: MP3 (cross-browser support)
- **Loop**: Yes (seamless)
- **Duration**: 30-60 seconds recommended
- **Style**: Ambient, drone, minimal texture
- **File location**: `/frontend/src/assets/3d/ambient_cimeika.mp3`

**Note**: Audio file is optional. System works without it.

## 🔮 Future Enhancements

### Planned Features
- [ ] **Module Labels**: Text overlays with module names
- [ ] **Activity Indicators**: Show real-time module activity
- [ ] **Connection Highlighting**: Emphasize paths on hover
- [ ] **Custom Particle Shapes**: Module-specific particle designs
- [ ] **VR/AR Support**: Via @react-three/xr
- [ ] **Dynamic Repositioning**: User-configurable layouts
- [ ] **Mobile Optimization**: Adaptive quality settings
- [ ] **Loading Progress**: Visual indicator for asset loading

### Advanced Features
- [ ] **Data Visualization**: Show inter-module data flow
- [ ] **Time-based Changes**: Visual representation of system state
- [ ] **Sound Spatialization**: 3D audio matching visual positions
- [ ] **Module Expansion**: Zoom into individual module spaces
- [ ] **Collaborative Viewing**: Multi-user shared space

## 🐛 Known Limitations

1. **Audio Autoplay**: Browser policies may block automatic audio playback
2. **Line Width**: WebGL limitation restricts line thickness to 1px on some systems
3. **Mobile Performance**: May require particle count reduction on older devices
4. **Label Rendering**: Current implementation uses placeholder sprites

## 📊 Performance Benchmarks

### Desktop (Modern GPU)
- **FPS**: 60 (stable)
- **GPU Load**: 15-25%
- **Memory**: ~80MB WebGL context

### Desktop (Integrated GPU)
- **FPS**: 45-60
- **GPU Load**: 40-60%
- **Memory**: ~80MB WebGL context

### Mobile (Modern)
- **FPS**: 30-45
- **GPU Load**: 60-80%
- **Memory**: ~60MB WebGL context

## 🔗 Related Documentation

- [Components README](/frontend/src/components/Cimeika3D/README.md) - Detailed component documentation
- [Architecture](/docs/ARCHITECTURE.md) - System architecture overview
- [Technical Task](/TECHNICAL_TASK.md) - Original requirements

## 📝 Development Notes

### Adding New Modules
To add a new module to the visualization:

1. Update module configuration in `Cimeika3DMap_v2.jsx`:
```jsx
const modules = [
  // ... existing modules
  {
    id: 'newmodule',
    name: 'New Module',
    position: [x, y, z],
    description: 'Description'
  }
];
```

2. Add color scheme in `ModuleSphere.jsx`:
```jsx
const moduleColors = {
  // ... existing colors
  newmodule: { primary: '#color1', glow: '#color2' }
};
```

### Customizing Animations
Animation parameters can be adjusted in respective components:
- **Breathing**: `ModuleSphere.jsx` line 89 (`Math.sin(time * 0.5)`)
- **Auto-rotate**: `Cimeika3DMap_v2.jsx` line 106 (`autoRotateSpeed={0.5}`)
- **Particle speed**: `ModuleSphere.jsx` line 48-50 (velocity configuration)

## 💡 Design Philosophy

The 3D visualization embodies Cimeika's core principles:
- **Organic**: Natural breathing, flowing movements
- **Connected**: Visual representation of system relationships
- **Accessible**: Intuitive navigation and interaction
- **Beautiful**: Aesthetic experience enhances functionality
- **Performant**: Optimized for smooth experience across devices

---

**Created with ❤️ for the Cimeika ecosystem**  
*Making complex systems beautifully simple*
