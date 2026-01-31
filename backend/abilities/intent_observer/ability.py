"""
Intent Observer Ability Module
Provides user intent pattern detection functionality.
"""
from typing import Any, Dict, List
from datetime import datetime
from ..base import Ability


class IntentObserverAbility(Ability):
    """
    User intent pattern detection ability.
    
    Activation Triggers:
    - User behavior analysis is required
    - System needs to learn user patterns
    - Integration with AI modules for intent classification
    
    States:
    - Dormant: No observation, minimal memory footprint
    - Active: Observing and analyzing user interactions
    """
    
    def __init__(self):
        """Initialize intent observer ability in dormant state."""
        self._active = False
        self._observed_intents: List[Dict[str, Any]] = []
        self._intent_patterns: Dict[str, int] = {}
    
    @property
    def name(self) -> str:
        """Unique ability identifier."""
        return "intent_observer"
    
    @property
    def version(self) -> str:
        """Semantic version."""
        return "0.1.0"
    
    async def activate(self) -> None:
        """
        Transition from dormant to active state.
        Initialize observation buffers and pattern recognition.
        """
        if not self._active:
            # Initialize observation structures
            self._observed_intents = []
            self._intent_patterns = {}
            self._active = True
    
    async def deactivate(self) -> None:
        """
        Return to dormant state.
        Persist learned patterns and clean up observation buffers.
        """
        if self._active:
            # Could persist patterns to database here
            self._active = False
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute intent observation operations.
        
        Args:
            context: Operation context with keys:
                - action: "observe", "analyze", "patterns", "clear"
                - intent: Intent to observe (for "observe" action)
                - user_id: Optional user identifier
                - metadata: Optional observation metadata
                - threshold: Minimum pattern frequency (for "patterns" action)
        
        Returns:
            Result dict with operation status and data
        """
        if not self._active:
            return {"error": "Intent observer ability is not active"}
        
        action = context.get("action", "patterns")
        
        if action == "observe":
            intent = context.get("intent")
            if not intent:
                return {"error": "intent is required"}
            
            # Record the observation
            observation = {
                "intent": intent,
                "timestamp": datetime.now().isoformat(),
                "user_id": context.get("user_id"),
                "metadata": context.get("metadata", {})
            }
            self._observed_intents.append(observation)
            
            # Update pattern count
            self._intent_patterns[intent] = self._intent_patterns.get(intent, 0) + 1
            
            return {
                "status": "observed",
                "intent": intent,
                "total_observations": len(self._observed_intents)
            }
        
        elif action == "analyze":
            # Analyze recent intent patterns
            if not self._observed_intents:
                return {"status": "success", "analysis": "No intents observed yet"}
            
            # Simple frequency analysis
            most_common = max(self._intent_patterns.items(), key=lambda x: x[1])
            
            return {
                "status": "success",
                "analysis": {
                    "total_observations": len(self._observed_intents),
                    "unique_intents": len(self._intent_patterns),
                    "most_common_intent": most_common[0],
                    "most_common_count": most_common[1],
                    "all_patterns": self._intent_patterns
                }
            }
        
        elif action == "patterns":
            # Return patterns above threshold
            threshold = context.get("threshold", 1)
            filtered_patterns = {
                intent: count for intent, count in self._intent_patterns.items()
                if count >= threshold
            }
            
            return {
                "status": "success",
                "patterns": filtered_patterns,
                "count": len(filtered_patterns)
            }
        
        elif action == "clear":
            # Clear observation history
            self._observed_intents.clear()
            self._intent_patterns.clear()
            
            return {
                "status": "cleared",
                "message": "All observations and patterns cleared"
            }
        
        return {"error": f"Unknown action: {action}"}
