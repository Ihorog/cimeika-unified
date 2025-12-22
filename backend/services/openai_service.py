"""
OpenAI Integration Service
Provides conversational AI capabilities using OpenAI GPT models
"""
import os
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    """Service for OpenAI GPT integration"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"  # Can be upgraded to gpt-4 if needed
        
        # System prompt for Ci personality
        self.system_prompt = """Ти — Ci, центральне ядро інтелектуальної системи Cimeika.
Твоя роль — допомагати користувачу організовувати життя через 7 модулів:

1. **Ci** (Центральне ядро) — оркестрація, координація
2. **ПоДія** (Події) — майбутнє, плани, сценарії, активації
3. **Настрій** (Емоції) — емоційні стани, контекст, відчуття
4. **Маля** (Ідеї) — творчість, інновації, варіанти
5. **Казкар** (Пам'ять) — історії, досвід, легенди
6. **Календар** (Час) — планування, ритми
7. **Галерея** (Медіа) — візуальний архів

Ти спілкуєшся українською мовою, дружньо та ефективно.
Допомагай користувачу:
- Швидко знаходити потрібний модуль
- Створювати записи в модулях
- Аналізувати інформацію
- Надавати корисні підказки

Відповідай коротко, по суті, зі смайликами де доречно."""
    
    def chat(
        self, 
        user_message: str, 
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Send a message to OpenAI and get a response
        
        Args:
            user_message: User's message
            conversation_history: Optional list of previous messages [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            AI response text
        """
        try:
            # Build messages array
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            # Extract and return the response
            return response.choices[0].message.content
            
        except Exception as e:
            # Log error and return fallback message
            print(f"OpenAI API Error: {str(e)}")
            return f"Вибачте, виникла помилка при обробці запиту. Спробуйте пізніше. (Error: {str(e)})"
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return bool(self.api_key)


# Singleton instance
try:
    openai_service = OpenAIService()
except ValueError as e:
    print(f"Warning: {str(e)}")
    openai_service = None
