# Module Orchestration System

## Overview

The Cimeika Unified project implements a comprehensive module orchestration system that provides centralized management, initialization, and monitoring of all 7 core modules across both backend (Python/FastAPI) and frontend (TypeScript/React).

## Architecture

### Core Components

1. **Interfaces** - Define contracts that all modules must implement
2. **Module Registry** - Central registry for module registration and access
3. **Startup System** - Handles initialization and lifecycle management
4. **API Layer** - Exposes module management through HTTP endpoints
5. **React Hooks** - Provides easy access to modules in UI components

## Backend Implementation

### File Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── interfaces.py      # Base interfaces
│   │   └── orchestrator.py    # Module registry
│   ├── startup.py              # Module initialization
│   ├── api/
│   │   └── modules.py          # Module management API
│   └── modules/
│       ├── ci/
│       ├── kazkar/
│       ├── podija/
│       ├── nastrij/
│       ├── malya/
│       ├── gallery/
│       └── calendar/
```

### ModuleInterface (Backend)

All backend modules implement `ModuleInterface` and `ServiceInterface`:

```python
from app.core.interfaces import ModuleInterface, ServiceInterface

class MyModuleService(ModuleInterface, ServiceInterface):
    def get_name(self) -> str:
        return "my_module"
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "active",
            "name": self._name,
            "initialized": self._initialized
        }
    
    def initialize(self) -> bool:
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Business logic here
        pass
```

### Module Registration (Backend)

Modules are registered in `app/startup.py`:

```python
from app.core import registry
from app.modules.ci.service import CiService
from app.modules.kazkar.service import KazkarService
# ... other imports

# Create service instances
ci_service = CiService()
kazkar_service = KazkarService()

def setup_modules():
    """Register and initialize all modules"""
    registry.register('ci', ci_service)
    registry.register('kazkar', kazkar_service)
    # ... register other modules
    
    # Initialize all
    results = registry.initialize_all()
    return results
```

The modules are automatically initialized when the FastAPI app starts via the lifespan context in `fastapi_app.py`.

### API Endpoints

Module management is exposed through REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/modules/` | GET | List all registered modules |
| `/api/v1/modules/status` | GET | Get status of all modules |
| `/api/v1/modules/{name}/status` | GET | Get status of specific module |
| `/api/v1/modules/{name}/metadata` | GET | Get module metadata |
| `/api/v1/modules/{name}/initialize` | POST | Initialize a module |
| `/api/v1/modules/{name}/shutdown` | POST | Shutdown a module |

#### Example API Response

```json
{
  "status": "success",
  "modules": {
    "ci": {
      "status": "active",
      "name": "ci",
      "initialized": true,
      "seo_enabled": true
    },
    "kazkar": {
      "status": "active",
      "name": "kazkar",
      "initialized": true
    }
  }
}
```

## Frontend Implementation

### File Structure

```
frontend/
├── src/
│   ├── types/
│   │   └── interfaces.ts       # TypeScript interfaces
│   ├── core/
│   │   └── orchestrator.ts     # Module registry
│   ├── app/
│   │   └── modules.ts          # Module registration
│   ├── hooks/
│   │   └── useModules.ts       # React hooks
│   └── modules/
│       ├── Ci/
│       │   └── module.ts
│       ├── Kazkar/
│       │   └── module.ts
│       └── ...
```

### ModuleInterface (Frontend)

All frontend modules implement `ModuleInterface`:

```typescript
import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../types';

export class MyModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'my_module';

  getName(): string {
    return this.name;
  }

  async getStatus(): Promise<ModuleStatus> {
    return {
      status: 'active',
      name: this.name,
      initialized: this.initialized
    };
  }

  async initialize(): Promise<boolean> {
    this.initialized = true;
    return true;
  }

  async shutdown(): Promise<boolean> {
    this.initialized = false;
    return true;
  }

  getMetadata(): ModuleMetadata {
    return {
      name: this.name,
      version: '0.1.0',
      description: 'Module description'
    };
  }

  isInitialized(): boolean {
    return this.initialized;
  }
}
```

### Module Registration (Frontend)

Modules are registered in `app/modules.ts` and initialized in `main.jsx`:

```typescript
// app/modules.ts
import { registry } from '../core';
import { ciModule } from '../modules/Ci';
import { kazkarModule } from '../modules/Kazkar';

export function registerModules(): void {
  registry.register('ci', ciModule);
  registry.register('kazkar', kazkarModule);
  // ... register other modules
}

export async function setupModules() {
  registerModules();
  const results = await registry.initializeAll();
  return results;
}
```

```javascript
// main.jsx
import { setupModules } from './app/modules';

setupModules().then(results => {
  console.log('Cimeika modules initialized:', results);
});
```

### React Hooks

The system provides several React hooks for easy module access:

```typescript
import { 
  useModulesStatus,
  useModuleStatus,
  useModule,
  useModulesList,
  useModuleMetadata,
  useModuleInitialize
} from '../hooks/useModules';

function MyComponent() {
  // Get all module statuses
  const { statuses, loading, error, refresh } = useModulesStatus();
  
  // Get specific module
  const ciModule = useModule('ci');
  
  // Get module status
  const { status } = useModuleStatus('kazkar');
  
  // Initialize a module
  const { initialize, initializing } = useModuleInitialize('podija');
  
  return (
    <div>
      <button onClick={refresh}>Refresh Statuses</button>
      {/* ... render module information */}
    </div>
  );
}
```

### ModuleStatusDashboard Component

A comprehensive dashboard component is provided to visualize module status:

```typescript
import ModuleStatusDashboard from './components/ModuleStatusDashboard';

function App() {
  return (
    <div>
      <ModuleStatusDashboard />
    </div>
  );
}
```

The dashboard displays:
- Total module count
- Active module count
- Error count
- Individual module cards with status, version, and description
- Refresh button to reload statuses

## Module Lifecycle

### Initialization Flow

1. **Application Startup**
   - Backend: `fastapi_app.py` lifespan context calls `setup_modules()`
   - Frontend: `main.jsx` calls `setupModules()`

2. **Module Registration**
   - Each module instance is registered with the global registry
   - Registry validates that module implements required interface

3. **Initialization**
   - `registry.initializeAll()` is called
   - Each module's `initialize()` method is invoked
   - Results are logged and tracked

4. **Ready State**
   - Modules are now active and ready to handle requests
   - Status can be queried via API or hooks

### Shutdown Flow

1. **Shutdown Triggered**
   - Backend: Application shutdown or explicit API call
   - Frontend: `registry.shutdownAll()` or individual module shutdown

2. **Cleanup**
   - Each module's `shutdown()` method is called
   - Resources are released
   - State is cleared

3. **Unregistration** (optional)
   - Modules can be unregistered from the registry
   - Automatic shutdown before removal

## Testing

### Backend Testing

```python
from app.startup import setup_modules, get_modules_status
from app.core import registry

# Setup and test
results = setup_modules()
assert all(results.values()), "All modules should initialize"

# Get status
statuses = get_modules_status()
assert statuses['ci']['status'] == 'active'

# Test API
from fastapi.testclient import TestClient
from fastapi_app import app

client = TestClient(app)
response = client.get('/api/v1/modules/status')
assert response.status_code == 200
```

### Frontend Testing

```typescript
import { registry } from './core';
import { ciModule } from './modules/Ci';

// Register and test
registry.register('ci', ciModule);
const result = await ciModule.initialize();
expect(result).toBe(true);

// Get status
const status = await ciModule.getStatus();
expect(status.status).toBe('active');
```

## Seven Core Modules

All 7 Cimeika modules implement the orchestration system:

1. **Ci** - Central orchestration core
2. **Kazkar** - Memory, stories, legends
3. **Podija** - Events, future, scenarios
4. **Nastrij** - Emotional states, context
5. **Malya** - Ideas, creativity, innovations
6. **Gallery** - Visual archive, media
7. **Calendar** - Time, rhythms, planning

Each module:
- Implements all required interface methods
- Has its own service layer (backend) and module class (frontend)
- Maintains initialization state
- Provides metadata and status information
- Can be independently initialized and shutdown

## Benefits

### Consistency
- All modules follow the same patterns
- Predictable behavior across the system
- Easy to add new modules

### Observability
- Centralized status monitoring
- Easy debugging of initialization issues
- Clear module lifecycle tracking

### Maintainability
- Clear separation of concerns
- Well-defined interfaces
- Easy to extend and modify

### Type Safety
- Full TypeScript support in frontend
- Python type hints in backend
- Compile-time validation

## Best Practices

### Module Implementation

1. **Keep initialization lightweight** - Complex setup should be lazy-loaded
2. **Handle errors gracefully** - Return false from initialize() on failure
3. **Provide meaningful status** - Include relevant diagnostic information
4. **Clean up properly** - Implement shutdown() to release resources
5. **Maintain metadata** - Keep version and description up to date

### Registry Usage

1. **Register early** - Do registration at application startup
2. **Initialize once** - Don't call initialize() multiple times
3. **Check status** - Verify module is initialized before use
4. **Handle failures** - Check initialization results

### API Integration

1. **Use status endpoints** - Monitor module health
2. **Implement retries** - Handle temporary failures
3. **Cache metadata** - Reduce unnecessary API calls
4. **Handle errors** - Provide user feedback on issues

## Future Enhancements

Potential improvements to the orchestration system:

- **Dependency Management** - Track and enforce module dependencies
- **Health Checks** - Periodic health monitoring and auto-recovery
- **Metrics Collection** - Performance and usage statistics
- **Hot Reload** - Dynamic module loading/unloading
- **Configuration Management** - Centralized module configuration
- **Event System** - Inter-module communication via events

## Conclusion

The module orchestration system provides a solid foundation for managing the complexity of the Cimeika Unified project. By enforcing consistent interfaces and providing centralized management, it ensures reliability, maintainability, and observability across all modules.
