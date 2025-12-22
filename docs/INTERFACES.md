# Interface Guidelines for Cimeika Modules

This document describes the interface pattern used throughout the Cimeika Unified project.

## Overview

All modules in Cimeika (both backend and frontend) implement standard interfaces to ensure:
- **Consistency**: All modules behave predictably
- **Type Safety**: Compile-time validation of implementations
- **Maintainability**: Clear contracts between components
- **Testability**: Easy to mock and test

## Backend Interfaces (Python)

### ModuleInterface

The base interface that all module services must implement:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ModuleInterface(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Get the module name"""
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get the current status"""
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the module"""
        pass
    
    def shutdown(self) -> bool:
        """Gracefully shutdown"""
        return True
```

### ServiceInterface

Interface for service layer operations:

```python
class ServiceInterface(ABC):
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data according to service logic"""
        pass
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return True
```

### Implementation Example

```python
from app.core.interfaces import ModuleInterface, ServiceInterface
from typing import Dict, Any

class MyModuleService(ModuleInterface, ServiceInterface):
    def __init__(self):
        self._initialized = False
        self._name = "my_module"
    
    def get_name(self) -> str:
        return self._name
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "active" if self._initialized else "inactive",
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
        if not self._initialized:
            return {"error": "Module not initialized"}
        
        # Your business logic here
        return {
            "status": "success",
            "module": self._name,
            "data": data
        }
    
    def validate(self, data: Dict[str, Any]) -> bool:
        return isinstance(data, dict)
```

## Frontend Interfaces (TypeScript)

### ModuleInterface

The base interface that all frontend modules must implement:

```typescript
export interface ModuleInterface {
  /**
   * Get the module name
   */
  getName(): string;
  
  /**
   * Get the current status of the module
   */
  getStatus(): Promise<ModuleStatus>;
  
  /**
   * Initialize the module
   */
  initialize(): Promise<boolean>;
  
  /**
   * Get module metadata
   */
  getMetadata(): ModuleMetadata;
}
```

### ServiceInterface

Interface for service layer (API/data operations):

```typescript
export interface ServiceInterface {
  getStatus(): Promise<any>;
  process?(data: any): Promise<any>;
  validate?(data: any): boolean;
}
```

### ApiResponse

Standard response format:

```typescript
export interface ApiResponse<T = any> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
  message?: string;
}
```

### Implementation Example

Service implementation:

```typescript
import type { ServiceInterface, ApiResponse } from '../../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export const myModuleService: ServiceInterface = {
  async getStatus(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/my_module`);
      const data = await response.json();
      return {
        status: 'success',
        data
      };
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  },
  
  async process(data: any): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/v1/my_module/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      return {
        status: 'success',
        data: result
      };
    } catch (error) {
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  },
  
  validate(data: any): boolean {
    return typeof data === 'object' && data !== null;
  }
};
```

Module implementation:

```typescript
import type { ModuleInterface, ModuleStatus, ModuleMetadata } from '../../types';
import { myModuleService } from './service';

export class MyModule implements ModuleInterface {
  private initialized: boolean = false;
  private readonly name: string = 'my_module';

  getName(): string {
    return this.name;
  }

  async getStatus(): Promise<ModuleStatus> {
    try {
      const result = await myModuleService.getStatus();
      
      if (result.status === 'success' && result.data) {
        return {
          status: 'active',
          name: this.name,
          initialized: this.initialized,
          ...result.data
        };
      }
      
      return {
        status: 'error',
        name: this.name,
        initialized: this.initialized,
        error: result.error || 'Failed to get status'
      };
    } catch (error) {
      return {
        status: 'error',
        name: this.name,
        initialized: this.initialized,
        error: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }

  async initialize(): Promise<boolean> {
    try {
      const result = await myModuleService.getStatus();
      this.initialized = result.status === 'success';
      return this.initialized;
    } catch (error) {
      console.error(`Failed to initialize ${this.name}:`, error);
      this.initialized = false;
      return false;
    }
  }

  getMetadata(): ModuleMetadata {
    return {
      name: this.name,
      version: '0.1.0',
      description: 'My module description'
    };
  }
}

export const myModule = new MyModule();
```

## Module Registration

### Backend

```python
from app.core import registry
from app.modules.my_module.service import MyModuleService

# Create module instance
my_module = MyModuleService()

# Register with orchestrator
registry.register("my_module", my_module)

# Initialize all modules
results = registry.initialize_all()

# Get all statuses
statuses = registry.get_all_statuses()
```

### Frontend

```typescript
import { registry } from './core';
import { myModule } from './modules/MyModule';

// Register module
registry.register('my_module', myModule);

// Initialize all modules
const results = await registry.initializeAll();

// Get all statuses
const statuses = await registry.getAllStatuses();

// Or use the convenience functions
import { setupModules, getModulesStatus } from './app/modules';

// Setup and initialize all modules at app startup
await setupModules();

// Get status later
const status = await getModulesStatus();
```

### Using Modules

Backend:
```python
# Get a specific module
module = registry.get("my_module")

# Use the module
if module:
    status = module.get_status()
    result = module.process({"key": "value"})
```

Frontend:
```typescript
// Get a specific module
const module = registry.get('my_module');

// Use the module
if (module) {
  const status = await module.getStatus();
  const metadata = module.getMetadata();
}
```

## Best Practices

1. **Always implement required methods**: All abstract methods must be implemented
2. **Handle errors gracefully**: Return error states instead of raising exceptions when appropriate
3. **Validate inputs**: Use the `validate` method before processing
4. **Initialize properly**: Ensure `initialize()` sets up all required resources
5. **Clean up on shutdown**: Release resources in `shutdown()`
6. **Type hints**: Always use type hints for better IDE support and validation
7. **Documentation**: Document what each method does in your implementation
8. **Testing**: Write tests for each interface method

## Testing Interfaces

### Backend Test Example

```python
import pytest
from app.modules.my_module.service import MyModuleService

def test_module_interface():
    service = MyModuleService()
    
    # Test initialization
    assert service.initialize() is True
    
    # Test status
    status = service.get_status()
    assert status['status'] == 'active'
    assert status['name'] == 'my_module'
    
    # Test processing
    result = service.process({"test": "data"})
    assert result['status'] == 'success'
    
    # Test shutdown
    assert service.shutdown() is True
```

### Frontend Test Example

```typescript
import { describe, it, expect, vi } from 'vitest';
import { myModuleService } from './service';

describe('MyModuleService', () => {
  it('should get status', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve({ status: 'active' }),
      })
    );
    
    const result = await myModuleService.getStatus();
    expect(result.status).toBe('success');
  });
  
  it('should validate data', () => {
    expect(myModuleService.validate({ key: 'value' })).toBe(true);
    expect(myModuleService.validate(null)).toBe(false);
  });
});
```

## See Also

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Overall system architecture
- [Backend interfaces](../backend/app/core/interfaces.py) - Python interface definitions
- [Frontend interfaces](../frontend/src/types/interfaces.ts) - TypeScript interface definitions
- [Backend orchestrator](../backend/app/core/orchestrator.py) - Python module registry
- [Frontend orchestrator](../frontend/src/core/orchestrator.ts) - TypeScript module registry

## Frontend Orchestrator Pattern

The frontend module orchestrator mirrors the backend pattern and provides centralized module management.

### Key Features

1. **Module Registry**: Central registry for all modules
2. **Lifecycle Management**: Initialize and manage module states
3. **Status Monitoring**: Query status of all modules
4. **Metadata Access**: Get module information
5. **Type Safety**: Full TypeScript support with interfaces

### Usage in App

```typescript
// In your main.tsx or App.tsx
import { setupModules } from './app/modules';

async function initializeApp() {
  try {
    const results = await setupModules();
    console.log('Modules initialized:', results);
  } catch (error) {
    console.error('Failed to initialize modules:', error);
  }
}

initializeApp();
```

### Module Structure

Each frontend module follows this structure:

```
Module/
├── module.ts       # ModuleInterface implementation
├── service.ts      # ServiceInterface implementation  
├── store.ts        # State management
├── api.ts          # API client
├── types.ts        # Type definitions
├── hooks/          # React hooks
├── views/          # View components
└── index.ts        # Module exports
```

The `module.ts` file implements `ModuleInterface` and coordinates with the service layer, providing a clean separation between module orchestration and business logic.
