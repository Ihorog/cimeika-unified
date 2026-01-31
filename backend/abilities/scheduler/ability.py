"""
Scheduler Ability Module
Provides task scheduling and reminder functionality.
"""
from typing import Any, Dict, List
from datetime import datetime
from ..base import Ability


class SchedulerAbility(Ability):
    """
    Task scheduling and reminders ability.
    
    Activation Triggers:
    - User requests scheduling functionality
    - System needs to manage time-based tasks
    - Integration with Calendar module for event management
    
    States:
    - Dormant: No timers running, minimal memory footprint
    - Active: Timers active, can schedule and trigger tasks
    """
    
    def __init__(self):
        """Initialize scheduler ability in dormant state."""
        self._active = False
        self._scheduled_tasks: Dict[str, Dict[str, Any]] = {}
    
    @property
    def name(self) -> str:
        """Unique ability identifier."""
        return "scheduler"
    
    @property
    def version(self) -> str:
        """Semantic version."""
        return "0.1.0"
    
    async def activate(self) -> None:
        """
        Transition from dormant to active state.
        Initialize scheduling engine and task queue.
        """
        if not self._active:
            # Initialize scheduling structures
            self._scheduled_tasks = {}
            self._active = True
    
    async def deactivate(self) -> None:
        """
        Return to dormant state.
        Cancel all pending tasks and clean up timers.
        """
        if self._active:
            # Could cancel all pending tasks here
            self._scheduled_tasks.clear()
            self._active = False
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute scheduling operations.
        
        Args:
            context: Operation context with keys:
                - action: "schedule", "cancel", "list", "get"
                - task_id: Task identifier
                - scheduled_time: ISO format datetime string
                - task_data: Task payload
                - repeat: Optional repeat configuration
        
        Returns:
            Result dict with operation status and data
        """
        if not self._active:
            return {"error": "Scheduler ability is not active"}
        
        action = context.get("action", "list")
        
        if action == "schedule":
            task_id = context.get("task_id", f"task_{len(self._scheduled_tasks) + 1}")
            scheduled_time = context.get("scheduled_time")
            
            if not scheduled_time:
                return {"error": "scheduled_time is required"}
            
            self._scheduled_tasks[task_id] = {
                "scheduled_time": scheduled_time,
                "task_data": context.get("task_data", {}),
                "repeat": context.get("repeat"),
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            return {"status": "scheduled", "task_id": task_id}
        
        elif action == "cancel":
            task_id = context.get("task_id")
            if task_id in self._scheduled_tasks:
                self._scheduled_tasks[task_id]["status"] = "cancelled"
                return {"status": "cancelled", "task_id": task_id}
            return {"error": "Task not found"}
        
        elif action == "get":
            task_id = context.get("task_id")
            if task_id in self._scheduled_tasks:
                return {"status": "success", "task": self._scheduled_tasks[task_id]}
            return {"error": "Task not found"}
        
        elif action == "list":
            # Filter by status if provided
            status_filter = context.get("status")
            tasks = self._scheduled_tasks
            
            if status_filter:
                tasks = {
                    tid: task for tid, task in tasks.items()
                    if task.get("status") == status_filter
                }
            
            return {
                "status": "success",
                "tasks": tasks,
                "count": len(tasks)
            }
        
        return {"error": f"Unknown action: {action}"}
