"""FastAPI server — POST /ci endpoint and GET /health for Ci Agent System v1."""

from __future__ import annotations

import os

from fastapi import FastAPI
from pydantic import BaseModel

from ci.intent_classifier import IntentClassifier
from ci.orchestrator import Orchestrator
from grok.engine import GrokEngine
from memory.active import ActiveMemory
from modules.calendar_module import CalendarModule
from modules.gallery import GalleryModule
from modules.kazkar import KazkarModule
from modules.malya import MalyaModule
from modules.nastrij import NastrijModule
from modules.podija import PodijaModule

app = FastAPI(title="Ci Agent System", version="1.0.0")

# --- Wiring -----------------------------------------------------------
_grok = GrokEngine()  # uses OPENAI_API_KEY from env if present, else stub
_memory = ActiveMemory()
_classifier = IntentClassifier()
_modules = {
    "kazkar": KazkarModule(),
    "podija": PodijaModule(),
    "nastrij": NastrijModule(),
    "malya": MalyaModule(),
    "calendar": CalendarModule(),
    "gallery": GalleryModule(),
}
_orchestrator = Orchestrator(
    memory_store=_memory,
    intent_classifier=_classifier,
    grok_engine=_grok,
    modules=_modules,
)


# --- Schemas ----------------------------------------------------------
class CiRequest(BaseModel):
    input: str


class CiResponse(BaseModel):
    intent: str
    source: str
    status: str
    result: str
    next_action: str | None = None


# --- Endpoints --------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok", "system": "ci-agent-v1"}


@app.post("/ci", response_model=CiResponse)
async def ci_endpoint(req: CiRequest) -> CiResponse:
    response = await _orchestrator.handle_request(req.input)
    return CiResponse(**response)
