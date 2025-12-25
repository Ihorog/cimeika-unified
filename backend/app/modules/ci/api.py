"""
Ci module API routes
CANON v1.0.0 - ci.capture() flow implementation
+ Legend ci interactive endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Optional
from app.config.seo import seo_service
from app.modules.ci.schema import CiCaptureRequest, CiCaptureResponse, CiChatRequest, CiChatResponse
from app.modules.ci.legend_ci_content import LEGEND_CI_NODES, LEGEND_CI_METADATA, SYMBOLIC_LIBRARY
from app.modules.ci.legend_duality_full import DUALITY_LEGEND_FULL
from services.openai_service import openai_service
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


@router.post("/chat", response_model=CiChatResponse)
async def ci_chat(request: CiChatRequest):
    """
    Chat with Ci using OpenAI GPT
    
    Args:
        request: Chat request with message and optional context
        
    Returns:
        AI response with timestamp
    """
    if not openai_service or not openai_service.is_available():
        raise HTTPException(
            status_code=503,
            detail="Chat service is unavailable. Please configure OPENAI_API_KEY."
        )
    
    try:
        # Extract conversation history from context
        conversation_history = []
        if request.context and "history" in request.context:
            conversation_history = request.context["history"]
        
        # Get AI response
        reply = openai_service.chat(
            user_message=request.message,
            conversation_history=conversation_history
        )
        
        # Return response with timestamp
        return CiChatResponse(
            reply=reply,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat message: {str(e)}"
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


# ========================================
# Legend ci Interactive Endpoints
# ========================================

@router.get("/legend")
async def get_legend_metadata():
    """Get Legend ci metadata and structure"""
    return LEGEND_CI_METADATA


@router.get("/legend/nodes")
async def get_legend_nodes(tags: Optional[str] = None):
    """
    Get all Legend ci nodes or filter by tags
    
    Args:
        tags: Comma-separated list of tags to filter by
        
    Returns:
        List of legend nodes
    """
    nodes = LEGEND_CI_NODES
    
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        nodes = [
            node for node in nodes
            if any(tag in node.get("tags", []) for tag in tag_list)
        ]
    
    return {
        "total": len(nodes),
        "nodes": nodes
    }


@router.get("/legend/nodes/{node_id}")
async def get_legend_node(node_id: int):
    """
    Get specific Legend ci node by ID
    
    Args:
        node_id: Node ID (1-20)
        
    Returns:
        Complete node data including connections
    """
    node = next((n for n in LEGEND_CI_NODES if n["id"] == node_id), None)
    
    if not node:
        raise HTTPException(
            status_code=404,
            detail=f"Node {node_id} not found"
        )
    
    # Enrich with connected nodes info
    connected_nodes = []
    for conn_id in node.get("connections", []):
        conn_node = next((n for n in LEGEND_CI_NODES if n["id"] == conn_id), None)
        if conn_node:
            connected_nodes.append({
                "id": conn_node["id"],
                "title": conn_node["title"],
                "icon": conn_node["icon"]
            })
    
    return {
        **node,
        "connected_nodes": connected_nodes
    }


@router.get("/legend/duality")
async def get_duality_legend():
    """
    Get the complete Duality Legend (full narrative)
    
    Returns:
        Complete duality legend with all 10 sections
    """
    return DUALITY_LEGEND_FULL


@router.get("/legend/duality/sections/{section_id}")
async def get_duality_section(section_id: str):
    """
    Get specific section of the Duality Legend
    
    Args:
        section_id: Section identifier (section_1 through section_10)
        
    Returns:
        Specific section content
    """
    section = next(
        (s for s in DUALITY_LEGEND_FULL["sections"] if s["id"] == section_id),
        None
    )
    
    if not section:
        raise HTTPException(
            status_code=404,
            detail=f"Section {section_id} not found"
        )
    
    return section


@router.get("/legend/symbols")
async def get_symbolic_library():
    """
    Get the symbolic library for Legend ci visualization
    
    Returns:
        Symbolic meanings for numbers, geometry, and elements
    """
    return SYMBOLIC_LIBRARY


@router.get("/legend/navigation/{current_node_id}")
async def get_navigation_options(current_node_id: int, state: str = "overview"):
    """
    Get navigation options from current node
    
    Args:
        current_node_id: Current node ID
        state: User state (overview, immersion, integration)
        
    Returns:
        Available navigation paths and recommendations
    """
    current = next((n for n in LEGEND_CI_NODES if n["id"] == current_node_id), None)
    
    if not current:
        raise HTTPException(
            status_code=404,
            detail=f"Node {current_node_id} not found"
        )
    
    # Get connected nodes
    connections = []
    for conn_id in current.get("connections", []):
        conn_node = next((n for n in LEGEND_CI_NODES if n["id"] == conn_id), None)
        if conn_node:
            connections.append({
                "id": conn_node["id"],
                "title": conn_node["title"],
                "icon": conn_node["icon"],
                "short_text": conn_node["short_text"]
            })
    
    # State-based recommendations
    recommendations = []
    if state == "overview":
        # Suggest starting points
        recommendations = [n for n in LEGEND_CI_NODES if n["id"] in [1, 2, 8]]
    elif state == "immersion":
        # Suggest related by tags
        current_tags = set(current.get("tags", []))
        recommendations = [
            n for n in LEGEND_CI_NODES
            if n["id"] != current_node_id and
            len(set(n.get("tags", [])) & current_tags) >= 2
        ][:3]
    elif state == "integration":
        # Suggest synthesis nodes
        recommendations = [n for n in LEGEND_CI_NODES if n["id"] in [17, 19, 20]]
    
    return {
        "current_node": {
            "id": current["id"],
            "title": current["title"],
            "icon": current["icon"]
        },
        "state": state,
        "direct_connections": connections,
        "recommendations": recommendations
    }

