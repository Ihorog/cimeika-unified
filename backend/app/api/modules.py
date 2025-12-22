"""
Core API routes for module management and orchestration
"""
from fastapi import APIRouter, HTTPException
from app.core import registry
from typing import Dict, Any

router = APIRouter(prefix="/modules", tags=["modules"])


@router.get("/")
async def list_modules():
    """
    List all registered modules
    
    Returns:
        List of module names
    """
    return {
        "status": "success",
        "modules": registry.list_modules()
    }


@router.get("/status")
async def get_all_modules_status():
    """
    Get status of all registered modules
    
    Returns:
        Dict mapping module names to their status information
    """
    try:
        statuses = registry.get_all_statuses()
        return {
            "status": "success",
            "modules": statuses
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get module statuses: {str(e)}"
        )


@router.get("/{module_name}/status")
async def get_module_status(module_name: str):
    """
    Get status of a specific module
    
    Args:
        module_name: Name of the module
        
    Returns:
        Module status information
    """
    module = registry.get(module_name)
    
    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module '{module_name}' not found"
        )
    
    try:
        status = module.get_status()
        return {
            "status": "success",
            "module": module_name,
            "data": status
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get status for module '{module_name}': {str(e)}"
        )


@router.get("/{module_name}/metadata")
async def get_module_metadata(module_name: str):
    """
    Get metadata for a specific module
    
    Args:
        module_name: Name of the module
        
    Returns:
        Module metadata
    """
    module = registry.get(module_name)
    
    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module '{module_name}' not found"
        )
    
    try:
        metadata = module.get_metadata()
        return {
            "status": "success",
            "module": module_name,
            "data": metadata
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get metadata for module '{module_name}': {str(e)}"
        )


@router.post("/{module_name}/initialize")
async def initialize_module(module_name: str):
    """
    Initialize a specific module
    
    Args:
        module_name: Name of the module
        
    Returns:
        Initialization result
    """
    module = registry.get(module_name)
    
    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module '{module_name}' not found"
        )
    
    try:
        result = module.initialize()
        return {
            "status": "success",
            "module": module_name,
            "initialized": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize module '{module_name}': {str(e)}"
        )


@router.post("/{module_name}/shutdown")
async def shutdown_module(module_name: str):
    """
    Shutdown a specific module
    
    Args:
        module_name: Name of the module
        
    Returns:
        Shutdown result
    """
    module = registry.get(module_name)
    
    if not module:
        raise HTTPException(
            status_code=404,
            detail=f"Module '{module_name}' not found"
        )
    
    try:
        result = module.shutdown()
        return {
            "status": "success",
            "module": module_name,
            "shutdown": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to shutdown module '{module_name}': {str(e)}"
        )
