"""
Ci module service
Business logic for Ci module
"""
from datetime import datetime
from typing import List, Optional
from ..models.ci_models import CiState, CiChatMessage, CiChatResponse, ModuleInfo, HealthStatus
from .openai_service import openai_service


class CiService:
    """Service for Ci module orchestration"""

    def __init__(self):
        self.modules = [
            ModuleInfo(id="ci", name="Ci", description="Центральне ядро, оркестрація", status="in_development"),
            ModuleInfo(id="podija", name="ПоДія", description="Події, майбутнє, сценарії", status="in_development"),
            ModuleInfo(id="nastrij", name="Настрій", description="Емоційні стани, контекст", status="in_development"),
            ModuleInfo(id="malya", name="Маля", description="Ідеї, творчість, інновації", status="in_development"),
            ModuleInfo(id="kazkar", name="Казкар", description="Пам'ять, історії, легенди", status="in_development"),
            ModuleInfo(id="calendar", name="Календар", description="Час, ритми, планування", status="in_development"),
            ModuleInfo(id="gallery", name="Галерея", description="Візуальний архів, медіа", status="in_development"),
        ]

    def get_state(self) -> CiState:
        """Get current Ci state"""
        return CiState(
            status="ready",
            modules=self.modules,
            health=HealthStatus(
                status="healthy",
                message="Ci module is operational",
                timestamp=datetime.utcnow().isoformat(),
                version="0.1.0"
            )
        )

    def process_chat(self, message: CiChatMessage) -> CiChatResponse:
        """Process chat message with OpenAI GPT"""
        try:
            # Extract conversation history from context if provided
            conversation_history = None
            if message.context and 'history' in message.context:
                conversation_history = message.context['history']
            
            # Use OpenAI service if available
            if openai_service and openai_service.is_available():
                reply = openai_service.chat(
                    user_message=message.message,
                    conversation_history=conversation_history
                )
            else:
                # Fallback response if OpenAI is not available
                reply = f"Ci отримав ваше повідомлення: '{message.message}'. Функціонал у розробці. (OpenAI не налаштовано)"
            
            return CiChatResponse(
                reply=reply,
                timestamp=datetime.utcnow().isoformat(),
                context=message.context
            )
        except Exception as e:
            # Error handling
            return CiChatResponse(
                reply=f"Вибачте, виникла помилка: {str(e)}",
                timestamp=datetime.utcnow().isoformat(),
                context=message.context
            )


# Singleton instance
ci_service = CiService()
