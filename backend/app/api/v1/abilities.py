"""
Abilities API Router
Provides HTTP endpoints for managing abilities lifecycle and execution.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
import sys
from pathlib import Path

# Add abilities module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "abilities"))

from abilities import registry, NotesAbility, SchedulerAbility, IntentObserverAbility

# Initialize router
router = APIRouter(prefix="/abilities", tags=["abilities"])

# Initialize and register abilities at module load
try:
    registry.register(NotesAbility())
    registry.register(SchedulerAbility())
    registry.register(IntentObserverAbility())
except Exception as e:
    print(f"Error registering abilities: {e}")


# Pydantic models for request/response
class ExecuteRequest(BaseModel):
    """Request model for ability execution."""
    context: Dict[str, Any] = Field(
        ...,
        description="Execution context with action and parameters"
    )


class AbilityResponse(BaseModel):
    """Response model for ability operations."""
    status: str
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class AbilityInfo(BaseModel):
    """Model for ability information."""
    name: str
    version: str
    is_active: bool
    enabled: bool
    description: str
    dependencies: List[str]


class AbilitiesListResponse(BaseModel):
    """Response model for listing abilities."""
    abilities: List[AbilityInfo]


@router.get("", response_model=AbilitiesListResponse)
async def list_abilities():
    """
    List all registered abilities with their current state.
    
    Returns:
        List of abilities with metadata and activation status
    """
    abilities = registry.list_abilities()
    return {"abilities": abilities}


@router.get("/manifest")
async def get_manifest():
    """
    Get the abilities manifest with metadata.
    
    Returns:
        Manifest dictionary with version and ability metadata
    """
    manifest = registry.get_manifest()
    return manifest


@router.post("/{ability_name}/activate", response_model=AbilityResponse)
async def activate_ability(ability_name: str):
    """
    Activate a dormant ability.
    
    Args:
        ability_name: Name of the ability to activate
    
    Returns:
        Success response with activation status
    
    Raises:
        HTTPException: If ability not found or activation fails
    """
    # Check if ability exists
    ability = registry.get(ability_name)
    if not ability:
        raise HTTPException(
            status_code=404,
            detail=f"Ability '{ability_name}' not found"
        )
    
    # Activate the ability
    success = await registry.activate(ability_name)
    
    if success:
        return {
            "status": "success",
            "message": f"Ability '{ability_name}' activated successfully"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to activate ability '{ability_name}'"
        )


@router.post("/{ability_name}/deactivate", response_model=AbilityResponse)
async def deactivate_ability(ability_name: str):
    """
    Deactivate an active ability.
    
    Args:
        ability_name: Name of the ability to deactivate
    
    Returns:
        Success response with deactivation status
    
    Raises:
        HTTPException: If ability not found or deactivation fails
    """
    # Check if ability exists
    ability = registry.get(ability_name)
    if not ability:
        raise HTTPException(
            status_code=404,
            detail=f"Ability '{ability_name}' not found"
        )
    
    # Deactivate the ability
    success = await registry.deactivate(ability_name)
    
    if success:
        return {
            "status": "success",
            "message": f"Ability '{ability_name}' deactivated successfully"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deactivate ability '{ability_name}'"
        )


@router.post("/{ability_name}/execute", response_model=AbilityResponse)
async def execute_ability(ability_name: str, request: ExecuteRequest):
    """
    Execute an active ability with given context.
    
    Args:
        ability_name: Name of the ability to execute
        request: Execution request with context
    
    Returns:
        Execution result from the ability
    
    Raises:
        HTTPException: If ability not found, not active, or execution fails
    """
    # Check if ability exists
    ability = registry.get(ability_name)
    if not ability:
        raise HTTPException(
            status_code=404,
            detail=f"Ability '{ability_name}' not found"
        )
    
    # Check if ability is active
    if not ability.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"Ability '{ability_name}' is not active. Activate it first."
        )
    
    # Execute the ability
    result = await registry.execute(ability_name, request.context)
    
    if result is None:
        raise HTTPException(
            status_code=500,
            detail=f"Execution failed for ability '{ability_name}'"
        )
    
    # Check if result contains an error
    if "error" in result:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )
    
    return {
        "status": "success",
        "message": f"Ability '{ability_name}' executed successfully",
        "data": result
    }


@router.get("/{ability_name}", response_model=AbilityInfo)
async def get_ability_info(ability_name: str):
    """
    Get detailed information about a specific ability.
    
    Args:
        ability_name: Name of the ability
    
    Returns:
        Ability information with status and metadata
    
    Raises:
        HTTPException: If ability not found
    """
    abilities = registry.list_abilities()
    ability_info = next((a for a in abilities if a["name"] == ability_name), None)
    
    if not ability_info:
        raise HTTPException(
            status_code=404,
            detail=f"Ability '{ability_name}' not found"
        )
    
    return ability_info
