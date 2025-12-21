"""
Ci module API routes
CANON v1.0.0 - ci.capture() flow implementation
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.config.seo import seo_service
from app.modules.ci.schema import CiCaptureRequest, CiCaptureResponse
import uuid

router = APIRouter(prefix="/ci", tags=["ci"])


@router.get("/")
async def get_ci_status():
    """Get Ci module status"""
    return {
        "module": "ci",
        "name": "Ci",
        "description": "Центральне ядро, оркестрація",
        "status": "active"
    }


@router.post("/capture", response_model=CiCaptureResponse)
async def ci_capture(request: CiCaptureRequest):
    """
    CANON v1.0.0: ci.capture() - The single entry point action
    
    Step 0: Contact - raw_event capture
    Step 1: Structure - classify (podija/stan/time), attach_context
    Step 2: Reveal - return event, time_position, related_traces
    
    No login required, stateless action, emits event
    """
    # Step 0: Receive raw event
    raw_event = {
        "type": request.type,
        "content": request.content,
        "metadata": request.metadata or {}
    }
    
    # Step 1: Structure - classify and attach context
    # 🔧 Simplified classification for initial implementation
    event_id = str(uuid.uuid4())
    now = datetime.now()
    
    classified_event = {
        "id": event_id,
        "content": request.content,
        "type": request.type,
        "captured_at": now.isoformat(),
        "classification": {
            "podija": "moment",  # Event layer classification
            "stan": "neutral",    # State layer classification
            "time": now.isoformat()
        }
    }
    
    # Step 2: Reveal - prepare response
    time_position = f"Зафіксовано: {now.strftime('%d.%m.%Y %H:%M')}"
    
    # 🔧 Related traces - placeholder, will be implemented with proper DB queries
    related_traces = []
    
    # Step 3 options defined in schema
    return CiCaptureResponse(
        event_id=event_id,
        event=classified_event,
        time_position=time_position,
        related_traces=related_traces
    )


@router.get("/seo/states")
async def get_seo_states():
    """Get list of canonical emotional states"""
    return {"states": seo_service.get_states()}


@router.get("/seo/intents")
async def get_seo_intents():
    """Get list of canonical intents"""
    return {"intents": seo_service.get_intents()}


@router.get("/seo/languages")
async def get_seo_languages():
    """Get list of supported languages"""
    return {"languages": seo_service.get_languages()}


@router.get("/seo/entry/{lang}/{state}/{intent}")
async def get_seo_entry(lang: str, state: str, intent: str):
    """
    Get complete SEO entry for given language, state, and intent
    
    Args:
        lang: Language code (en, uk)
        state: Emotional state
        intent: User intent
        
    Returns:
        Complete SEO entry with title, description, url, module, writes_policy
    """
    entry = seo_service.get_entry(lang, state, intent)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail=f"SEO entry not found for {lang}/{state}/{intent}"
        )
    return entry


@router.get("/seo/entries/{lang}")
async def get_all_seo_entries(lang: str):
    """
    Get all SEO entries for a given language
    
    Args:
        lang: Language code (en, uk)
        
    Returns:
        List of all SEO entries
    """
    if lang not in seo_service.get_languages():
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {lang}"
        )
    entries = seo_service.get_all_entries(lang)
    return {"lang": lang, "entries": entries, "count": len(entries)}


@router.get("/seo/sitemap")
async def get_sitemap_entries(base_url: str = ""):
    """
    Generate sitemap entries for all SEO routes
    
    Args:
        base_url: Optional base URL for the site
        
    Returns:
        List of sitemap entries with hreflang alternates
    """
    entries = seo_service.generate_sitemap_entries(base_url)
    return {"sitemap": entries, "count": len(entries)}


@router.get("/seo/seeds")
async def get_seo_seeds(lang: str = None):
    """
    Get semantic research seeds
    
    Args:
        lang: Optional language filter (en, uk)
        
    Returns:
        Semantic research seeds data
    """
    seeds = seo_service.get_seeds(lang)
    return {"seeds": seeds}


@router.get("/seo/module/{state}")
async def get_module_for_state(state: str):
    """
    Get module mapping for a given emotional state
    
    Args:
        state: Emotional state
        
    Returns:
        Module name and writes policy
    """
    if state not in seo_service.get_states():
        raise HTTPException(
            status_code=400,
            detail=f"Invalid state: {state}"
        )
    
    module = seo_service.get_module(state)
    writes_policy = seo_service.get_writes_policy(module)
    
    return {
        "state": state,
        "module": module,
        "writes_policy": writes_policy
    }
