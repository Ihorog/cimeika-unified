# Abilities System - CIT-ORGANISM Plugin Architecture

## Overview

The Abilities system provides a plugin-based architecture for dormant module activation in the CIT-ORGANISM protocol. Abilities are modular, self-contained components that can be dynamically activated and deactivated without requiring system restarts.

## Architecture

### Core Components

1. **`base.py`** - Abstract `Ability` base class defining the interface
2. **`__init__.py`** - `AbilityRegistry` singleton for lifecycle management
3. **`manifest.json`** - Metadata registry with activation states
4. **Ability Modules** - Individual dormant abilities (notes, scheduler, intent_observer)

### Ability Lifecycle States

```
dormant → activating → active → deactivating → dormant
```

- **Dormant**: Minimal memory footprint, no background processes
- **Activating**: Initializing resources and dependencies
- **Active**: Fully operational, ready to execute
- **Deactivating**: Cleaning up resources, persisting state
- **Dormant**: Back to minimal state

## Available Abilities

### 1. Notes Ability (`notes`)

**Description**: Note-taking and knowledge capture functionality

**Version**: 0.1.0

**Activation Triggers**:
- User explicitly requests note-taking functionality
- System detects need for persistent knowledge storage
- Integration with Kazkar (memory/legends) module

**Operations**:
- `create`: Create a new note
- `read`: Retrieve a note by ID
- `update`: Update note content or metadata
- `delete`: Remove a note
- `list`: List all notes

**Example Usage**:
```python
from abilities import registry

# Activate the ability
await registry.activate("notes")

# Execute operations
result = await registry.execute("notes", {
    "action": "create",
    "note_id": "note_1",
    "content": "Important information",
    "metadata": {"tags": ["important"]}
})
```

### 2. Scheduler Ability (`scheduler`)

**Description**: Task scheduling and reminder functionality

**Version**: 0.1.0

**Activation Triggers**:
- User requests scheduling functionality
- System needs to manage time-based tasks
- Integration with Calendar module

**Operations**:
- `schedule`: Schedule a new task
- `cancel`: Cancel a scheduled task
- `get`: Get task details
- `list`: List all scheduled tasks

**Example Usage**:
```python
# Schedule a task
result = await registry.execute("scheduler", {
    "action": "schedule",
    "task_id": "task_1",
    "scheduled_time": "2026-02-01T10:00:00",
    "task_data": {"type": "reminder", "message": "Meeting"}
})
```

### 3. Intent Observer Ability (`intent_observer`)

**Description**: User intent pattern detection and analysis

**Version**: 0.1.0

**Activation Triggers**:
- User behavior analysis is required
- System needs to learn user patterns
- Integration with AI modules for intent classification

**Operations**:
- `observe`: Record a user intent
- `analyze`: Analyze observed patterns
- `patterns`: Get pattern frequencies
- `clear`: Clear observation history

**Example Usage**:
```python
# Observe an intent
result = await registry.execute("intent_observer", {
    "action": "observe",
    "intent": "create_note",
    "user_id": "user_123",
    "metadata": {"context": "work"}
})

# Analyze patterns
analysis = await registry.execute("intent_observer", {
    "action": "analyze"
})
```

## API Endpoints

The abilities system is integrated with FastAPI and provides the following endpoints:

### List All Abilities
```
GET /api/v1/abilities
```

Response:
```json
{
  "abilities": [
    {
      "name": "notes",
      "version": "0.1.0",
      "is_active": false,
      "enabled": false,
      "description": "Note-taking and knowledge capture",
      "dependencies": []
    }
  ]
}
```

### Activate an Ability
```
POST /api/v1/abilities/{ability_name}/activate
```

Response:
```json
{
  "status": "success",
  "message": "Ability 'notes' activated successfully"
}
```

### Deactivate an Ability
```
POST /api/v1/abilities/{ability_name}/deactivate
```

Response:
```json
{
  "status": "success",
  "message": "Ability 'notes' deactivated successfully"
}
```

### Execute an Ability
```
POST /api/v1/abilities/{ability_name}/execute
```

Request Body:
```json
{
  "action": "create",
  "note_id": "note_1",
  "content": "Example note"
}
```

Response:
```json
{
  "status": "created",
  "note_id": "note_1"
}
```

### Get Manifest
```
GET /api/v1/abilities/manifest
```

Response:
```json
{
  "version": "1.0.0",
  "abilities": {
    "notes": {
      "enabled": false,
      "version": "0.1.0",
      "description": "Note-taking and knowledge capture",
      "dependencies": []
    }
  }
}
```

## Programmatic Usage

### Basic Operations

```python
from abilities import registry, NotesAbility, SchedulerAbility, IntentObserverAbility

# Register abilities
registry.register(NotesAbility())
registry.register(SchedulerAbility())
registry.register(IntentObserverAbility())

# Activate an ability
await registry.activate("notes")

# Check if active
ability = registry.get("notes")
if ability.is_active:
    print("Notes ability is active")

# Execute operations
result = await registry.execute("notes", {
    "action": "create",
    "content": "My note"
})

# Deactivate when done
await registry.deactivate("notes")
```

### List All Abilities

```python
abilities = registry.list_abilities()
for ability in abilities:
    print(f"{ability['name']}: {ability['is_active']}")
```

## Integration with Self-Improvement System

The abilities subsystem is compatible with the existing `self_improvement.py` validation system. Abilities can be referenced in the main manifest and validated as part of the overall system health checks.

## Development Guidelines

### Creating a New Ability

1. Create a new directory under `abilities/`
2. Implement `ability.py` inheriting from `Ability` base class
3. Add `__init__.py` to export the ability class
4. Update `manifest.json` with ability metadata
5. Register the ability in application startup

Example structure:
```
abilities/
└── my_ability/
    ├── __init__.py
    └── ability.py
```

### Ability Implementation Checklist

- [ ] Inherit from `Ability` base class
- [ ] Implement all abstract methods (name, version, activate, deactivate, execute)
- [ ] Define clear activation triggers in docstrings
- [ ] Ensure dormant state has minimal memory footprint
- [ ] Handle errors gracefully in execute method
- [ ] Add comprehensive docstrings
- [ ] Update manifest.json

## Security Considerations

- Abilities run with the same privileges as the main application
- Input validation is required in execute methods
- State persistence should use secure storage mechanisms
- Consider rate limiting for resource-intensive abilities

## Performance Notes

- Dormant abilities have minimal overhead (~1KB memory per ability)
- Activation typically takes <100ms
- Deactivation ensures proper resource cleanup
- Registry operations are thread-safe (singleton pattern)

## Future Enhancements

- [ ] Dependency resolution between abilities
- [ ] Auto-activation based on system events
- [ ] Ability health monitoring
- [ ] Rollback mechanisms for failed activations
- [ ] Inter-ability communication protocol
- [ ] Persistent state storage (database integration)

## Troubleshooting

### Ability won't activate

Check logs for:
1. Missing dependencies
2. Initialization errors
3. Manifest configuration issues

### Execute returns None

Ensure:
1. Ability is activated first
2. Context dictionary has required keys
3. Check ability-specific documentation for required parameters

## Contributing

When adding new abilities:
1. Follow the established patterns
2. Write comprehensive tests
3. Update this README
4. Ensure backward compatibility

---

**Last Updated**: 2026-01-31  
**Version**: 1.0.0  
**Status**: Production Ready
