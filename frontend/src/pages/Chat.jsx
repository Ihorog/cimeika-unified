/**
 * Chat Page - Ci Chat Interface with OpenAI GPT
 * Interactive chat with conversational AI
 * Supports voice input from Android WebView
 * Supports Participant API integration
 */
import React, { useState, useRef, useEffect } from 'react';
import { useVoiceIntegration } from '../hooks/useVoiceIntegration';
import { participantClient } from '../services/participantClient';

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
  const [participantMode, setParticipantMode] = useState('analysis');
  const [participantTopic, setParticipantTopic] = useState('');
  const [showParticipantControls, setShowParticipantControls] = useState(false);
  const [conversationId] = useState(() => `conv-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const formRef = useRef(null);

  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5000';

  // Small delay to ensure state is updated before form submission
  const VOICE_AUTO_SUBMIT_DELAY = 100; // milliseconds

  // Voice integration
  const { isAndroid, startVoice, speak } = useVoiceIntegration({
    onVoiceText: (text) => {
      console.log('Voice text received:', text);
      setInputMessage(text);
      // Auto-submit the voice text using form ref
      setTimeout(() => {
        if (formRef.current) {
          const event = new Event('submit', { bubbles: true, cancelable: true });
          formRef.current.dispatchEvent(event);
        }
      }, VOICE_AUTO_SUBMIT_DELAY);
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

  const handleParticipantMessage = async () => {
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
      const response = await participantClient.sendMessage({
        conversation_id: conversationId,
        mode: participantMode,
        topic: participantTopic || undefined,
        input: {
          text: userMessage,
          metadata: {
            source: 'ci',
            repo: 'Ihorog/cimeika-unified'
          }
        }
      });

      // Add participant response to chat
      const participantMessage = {
        role: 'participant',
        participant: response.participant,
        content: response.message,
        severity: response.severity,
        outputs: response.outputs,
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, participantMessage]);
    } catch (error) {
      console.error('Participant API error:', error);
      
      // Add error message with participant format
      const errorMessage = {
        role: 'participant',
        participant: 'system',
        content: 'API unavailable: Unable to connect to the participant service.',
        severity: 'warn',
        outputs: { actions: [] },
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      console.log('Copied to clipboard');
    }).catch((error) => {
      console.error('Failed to copy:', error);
    });
  };

  const downloadPatch = (patchContent) => {
    const blob = new Blob([patchContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `patch-${Date.now()}.diff`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(e);
    }
  };

  const renderMessage = (message, index) => {
    if (message.role === 'participant') {
      return (
        <div key={index} className="flex justify-start">
          <div className="max-w-[80%] rounded-lg px-4 py-2 bg-blue-50 border border-blue-200">
            <div className="flex items-center gap-2 mb-1">
              <span className="font-semibold text-blue-900">
                🤖 API ({message.participant})
              </span>
              {message.severity === 'warn' && <span className="text-yellow-600">⚠️</span>}
              {message.severity === 'error' && <span className="text-red-600">❌</span>}
            </div>
            <p className="whitespace-pre-wrap text-gray-900">{message.content}</p>
            
            {/* Patch display */}
            {message.outputs?.patch_unified_diff && (
              <div className="mt-2 p-2 bg-gray-800 rounded text-xs">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-300 font-semibold">Patch:</span>
                  <div className="flex gap-2">
                    <button
                      onClick={() => copyToClipboard(message.outputs.patch_unified_diff)}
                      className="px-2 py-1 bg-blue-600 text-white rounded text-xs hover:bg-blue-700"
                    >
                      📋 Copy
                    </button>
                    <button
                      onClick={() => downloadPatch(message.outputs.patch_unified_diff)}
                      className="px-2 py-1 bg-green-600 text-white rounded text-xs hover:bg-green-700"
                    >
                      💾 Download
                    </button>
                  </div>
                </div>
                <pre className="text-green-400 overflow-x-auto max-h-48">
                  {message.outputs.patch_unified_diff}
                </pre>
              </div>
            )}
            
            {/* Actions display */}
            {message.outputs?.actions && message.outputs.actions.length > 0 && (
              <div className="mt-2 space-y-1">
                <span className="text-sm font-semibold text-blue-900">Actions:</span>
                {message.outputs.actions.map((action, idx) => (
                  <div key={idx} className="p-2 bg-white rounded border border-blue-200 text-sm">
                    <div className="flex items-start gap-2">
                      <span className="font-semibold text-blue-800">
                        {action.type === 'suggest' && '💡'}
                        {action.type === 'check' && '✅'}
                        {action.type === 'patch' && '🔧'}
                        {action.title}:
                      </span>
                    </div>
                    <p className="text-gray-700 mt-1">{action.details}</p>
                  </div>
                ))}
              </div>
            )}
            
            <p className="text-xs mt-1 text-blue-500">
              {new Date(message.timestamp).toLocaleTimeString('uk-UA', {
                hour: '2-digit',
                minute: '2-digit'
              })}
            </p>
          </div>
        </div>
      );
    }

    return (
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
    );
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
          {messages.map((message, index) => renderMessage(message, index))}
          
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

      {/* Participant Controls Toggle */}
      <div className="mb-2">
        <button
          onClick={() => setShowParticipantControls(!showParticipantControls)}
          className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-2"
        >
          🤖 {showParticipantControls ? 'Сховати' : 'Показати'} контроль API Participant
          <span>{showParticipantControls ? '▼' : '▶'}</span>
        </button>
      </div>

      {/* Participant Controls */}
      {showParticipantControls && (
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex gap-3 items-center flex-wrap">
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Режим:
              </label>
              <select
                value={participantMode}
                onChange={(e) => setParticipantMode(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="analysis">Analysis</option>
                <option value="autofix">Autofix</option>
                <option value="logger">Logger</option>
              </select>
            </div>
            <div className="flex-1">
              <label className="block text-xs font-semibold text-gray-700 mb-1">
                Тема (опціонально):
              </label>
              <input
                type="text"
                value={participantTopic}
                onChange={(e) => setParticipantTopic(e.target.value)}
                placeholder="Введіть тему..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>
      )}

      {/* Input Form */}
      <form ref={formRef} onSubmit={handleSendMessage} className="flex gap-2">
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

        {/* Participant API button */}
        {showParticipantControls && (
          <button
            type="button"
            onClick={handleParticipantMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? '...' : '🤖 API'}
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
          {showParticipantControls && ' • 🤖 для API Participant'}
        </p>
      </div>
    </div>
  );
}
