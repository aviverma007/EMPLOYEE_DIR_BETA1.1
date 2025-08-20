import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, Send, X, Minimize2, Maximize2, Trash2 } from 'lucide-react';

const FloatingChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load chat history on first open
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      loadChatHistory();
    }
  }, [isOpen]);

  const loadChatHistory = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/chat/history/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        if (data.messages && data.messages.length > 0) {
          const formattedMessages = [];
          data.messages.forEach(msg => {
            formattedMessages.push({ text: msg.user_message, isUser: true, timestamp: new Date(msg.created_at) });
            formattedMessages.push({ text: msg.bot_response, isUser: false, timestamp: new Date(msg.created_at) });
          });
          setMessages(formattedMessages);
        } else {
          // Add welcome message if no history
          setMessages([{
            text: "Hi! I'm SmartWorld's AI assistant with real-time capabilities! 🚀\n\n💼 **SmartWorld System**: Navigate employee directory, book meeting rooms, access policies\n🌍 **General AI**: Answer any question like ChatGPT\n⚡ **Real-time Data**: Check weather, traffic, news, stocks, currency rates, and more!\n\nTry asking:\n• \"What's the weather in Delhi?\"\n• \"How do I search employees?\"\n• \"Latest news headlines\"\n• \"Current stock market\"\n\nHow can I help you today?",
            isUser: false,
            timestamp: new Date()
          }]);
        }
      }
    } catch (error) {
      console.error('Error loading chat history:', error);
      // Add welcome message on error
      setMessages([{
        text: "Hi! I'm SmartWorld's AI assistant with real-time capabilities! 🚀\n\n💼 **SmartWorld System**: Navigate employee directory, book meeting rooms, access policies\n🌍 **General AI**: Answer any question like ChatGPT\n⚡ **Real-time Data**: Check weather, traffic, news, stocks, currency rates, and more!\n\nTry asking:\n• \"What's the weather in Delhi?\"\n• \"How do I search employees?\"\n• \"Latest news headlines\"\n• \"Current stock market\"\n\nHow can I help you today?",
        isUser: false,
        timestamp: new Date()
      }]);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      text: inputMessage,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: inputMessage
        })
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          text: data.response,
          isUser: false,
          timestamp: new Date(data.created_at)
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        throw new Error('Failed to get response');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
      await fetch(`${backendUrl}/api/chat/history/${sessionId}`, {
        method: 'DELETE'
      });
      setMessages([{
        text: "Chat history cleared! 🔄\n\nI'm ready to help with:\n💼 SmartWorld system guidance\n🌍 General questions & knowledge\n⚡ Real-time data (weather, traffic, news, stocks)\n\nWhat would you like to know?",
        isUser: false,
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error('Error clearing chat:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (timestamp) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(new Date(timestamp));
  };

  return (
    <>
      {/* Floating Chat Button */}
      {!isOpen && (
        <div 
          className="fixed bottom-6 right-6 z-50 cursor-pointer group"
          onClick={() => setIsOpen(true)}
        >
          <div className="relative">
            {/* Chat Button */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-full p-4 shadow-lg hover:shadow-xl transition-all duration-300 transform group-hover:scale-110">
              <MessageCircle className="h-6 w-6" />
            </div>
            
            {/* Company Logo Overlay */}
            <div className="absolute -top-2 -right-2 bg-white rounded-full p-1.5 shadow-md border-2 border-blue-200">
              <img 
                src="https://customer-assets.emergentagent.com/job_fast-modify/artifacts/kwtv62x3_company%20logo.png" 
                alt="SmartWorld Logo" 
                className="h-5 w-5 object-contain"
              />
            </div>
            
            {/* Pulse Animation */}
            <div className="absolute inset-0 bg-blue-600 rounded-full animate-ping opacity-20"></div>
          </div>
          
          {/* Tooltip */}
          <div className="absolute bottom-full right-0 mb-2 px-3 py-1 bg-gray-800 text-white text-sm rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
            AI Assistant • Real-time Data • Weather • Traffic
          </div>
        </div>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={`fixed bottom-6 right-6 z-50 bg-white rounded-lg shadow-2xl border border-gray-200 transition-all duration-300 ${
          isMinimized ? 'h-14 w-80' : 'h-96 w-80'
        }`}>
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-t-lg flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <img 
                src="https://customer-assets.emergentagent.com/job_fast-modify/artifacts/kwtv62x3_company%20logo.png" 
                alt="SmartWorld" 
                className="h-6 w-6 object-contain bg-white rounded-full p-1"
              />
              <div>
                <h3 className="font-semibold text-sm">SmartWorld AI</h3>
                <p className="text-xs opacity-90">Employee Assistant</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-1">
              <button
                onClick={clearChat}
                className="p-1 hover:bg-blue-800 rounded transition-colors"
                title="Clear Chat"
              >
                <Trash2 className="h-4 w-4" />
              </button>
              <button
                onClick={() => setIsMinimized(!isMinimized)}
                className="p-1 hover:bg-blue-800 rounded transition-colors"
              >
                {isMinimized ? <Maximize2 className="h-4 w-4" /> : <Minimize2 className="h-4 w-4" />}
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 hover:bg-blue-800 rounded transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Chat Messages */}
          {!isMinimized && (
            <>
              <div className="h-64 overflow-y-auto p-3 space-y-3 bg-gray-50">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
                  >
                    <div className="flex items-start space-x-2 max-w-[85%]">
                      {!message.isUser && (
                        <img 
                          src="https://customer-assets.emergentagent.com/job_fast-modify/artifacts/kwtv62x3_company%20logo.png" 
                          alt="AI" 
                          className="h-6 w-6 object-contain bg-blue-600 rounded-full p-1 flex-shrink-0 mt-1"
                        />
                      )}
                      <div>
                        <div
                          className={`px-3 py-2 rounded-lg text-sm ${
                            message.isUser
                              ? 'bg-blue-600 text-white rounded-br-sm'
                              : 'bg-white border border-gray-200 text-gray-800 rounded-bl-sm'
                          }`}
                        >
                          <p className="whitespace-pre-wrap">{message.text}</p>
                        </div>
                        <p className="text-xs text-gray-500 mt-1 px-1">
                          {formatTime(message.timestamp)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="flex items-start space-x-2">
                      <img 
                        src="https://customer-assets.emergentagent.com/job_fast-modify/artifacts/kwtv62x3_company%20logo.png" 
                        alt="AI" 
                        className="h-6 w-6 object-contain bg-blue-600 rounded-full p-1 flex-shrink-0 mt-1"
                      />
                      <div className="bg-white border border-gray-200 rounded-lg rounded-bl-sm px-3 py-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="p-3 border-t border-gray-200">
                <div className="flex space-x-2">
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me anything about SmartWorld..."
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                    disabled={isLoading}
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!inputMessage.trim() || isLoading}
                    className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-2 rounded-md transition-colors"
                  >
                    <Send className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
};

export default FloatingChatbot;