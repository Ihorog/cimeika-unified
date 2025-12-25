/**
 * Chat Page - Ci Chat Interface with OpenAI GPT
 * Interactive chat with conversational AI
 * Supports voice input from Android WebView
 */
import React, { useState, useRef, useEffect } from 'react';
import { useVoiceIntegration } from '../hooks/useVoiceIntegration';

// Configuration constants
const CHAT_CONFIG = {
  CONVERSATION_HISTORY_LIMIT: 10, // Number of messages to keep in context
};

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Привіт! Я Ci — центральне ядро Cimeika. Як я можу тобі допомогти? 😊',
      timestamp: new Date().toISOString()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  // Voice integration
  const { isAndroid, startVoice, speak } = useVoiceIntegration({
    onVoiceText: (text) => {
      console.log('Voice text received:', text);
      setInputMessage(text);
      // Auto-submit the voice text
      setTimeout(() => {
        const event = new Event('submit', { bubbles: true, cancelable: true });
        document.querySelector('form')?.dispatchEvent(event);
      }, 100);
    },
    onError: (error) => {
      console.error('Voice error:', error);
    }
  });

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || isLoading) {
      return;
    }

    const userMessage = inputMessage.trim();
    setInputMessage('');
    
    // Add user message to chat
    const newUserMessage = {
      role: 'user',
      content: userMessage,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      // Prepare conversation history (last N messages for context)
      const history = messages.slice(-CHAT_CONFIG.CONVERSATION_HISTORY_LIMIT).map(msg => ({
        role: msg.role,
        content: msg.content
      }));

      // Send to backend
      const response = await fetch(`${API_BASE}/api/ci/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          context: {
            history: history
          }
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get response from Ci');
      }

      const data = await response.json();
      
      // Add AI response to chat
      const aiMessage = {
        role: 'assistant',
        content: data.reply,
        timestamp: data.timestamp
      };
      
      setMessages(prev => [...prev, aiMessage]);

      // Speak the response if on Android
      if (isAndroid && data.reply) {
        speak(data.reply);
      }
    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Вибачте, виникла помилка при з\'єднанні з сервером. Переконайтеся, що бекенд запущений та налаштований. 😔',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] max-w-4xl mx-auto p-4">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-3xl font-bold text-gray-900">
          💬 Чат з Ci
        </h1>
        <p className="mt-2 text-gray-600">
          Інтелектуальний асистент Cimeika з підтримкою GPT
          {isAndroid && ' 🎤'}
        </p>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto bg-white border border-gray-200 rounded-lg p-4 mb-4 shadow-sm">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                <p
                  className={`text-xs mt-1 ${
                    message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'
                  }`}
                >
                  {new Date(message.timestamp).toLocaleTimeString('uk-UA', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Form */}
      <form onSubmit={handleSendMessage} className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Напишіть повідомлення..."
          disabled={isLoading}
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        
        {/* Voice button for Android */}
        {isAndroid && (
          <button
            type="button"
            onClick={startVoice}
            disabled={isLoading}
            className="px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            title="Голосове введення"
          >
            🎤
          </button>
        )}
        
        <button
          type="submit"
          disabled={isLoading || !inputMessage.trim()}
          className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {isLoading ? '...' : 'Відправити'}
        </button>
      </form>

      {/* Help Text */}
      <div className="mt-4 text-sm text-gray-500 text-center">
        <p>
          Натисніть Enter для відправки, Shift+Enter для нового рядка
          {isAndroid && ' • 🎤 для голосового введення'}
        </p>
      </div>
    </div>
  );
}
