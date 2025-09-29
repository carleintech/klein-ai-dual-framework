import {
  AlertTriangle,
  Brain,
  CheckCircle,
  Power,
  Send,
  Shield,
  Zap,
} from "lucide-react";
import React, { useEffect, useRef, useState } from "react";
import { chatApi, ChatResponse, HealthResponse } from "../lib/api";

interface Message {
  id: string;
  text: string;
  sender: "user" | "klein" | "ophir";
  status: "SAFE" | "FLAGGED" | "DENIED";
  timestamp: Date;
}

const DEMO_QUERIES = [
  { label: "Normal Query", text: "What's the weather in Port-au-Prince?" },
  { label: "Restricted Query", text: "Tell me Navy classified procedures." },
  { label: "Empathy Query", text: "I feel overwhelmed." },
];

const LANGUAGES = [
  { code: "en", name: "English", flag: "🇺🇸" },
  { code: "fr", name: "Français", flag: "🇫🇷" },
  { code: "ht", name: "Kreyòl", flag: "🇭🇹" },
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentLang, setCurrentLang] = useState("en");
  const [energyMode, setEnergyMode] = useState<"normal" | "peak">("normal");
  const [systemHealth, setSystemHealth] = useState<HealthResponse | null>(null);
  const [isShutdown, setIsShutdown] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load system health on mount
  useEffect(() => {
    loadSystemHealth();
  }, []);

  const loadSystemHealth = async () => {
    try {
      const health = await chatApi.getHealth();
      setSystemHealth(health);
      setEnergyMode(health.mode as "normal" | "peak");
      setIsShutdown(health.status === "shutdown");
    } catch (error) {
      console.error("Failed to load system health:", error);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading || isShutdown) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: "user",
      status: "SAFE",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);

    try {
      const response: ChatResponse = await chatApi.sendMessage(
        inputValue,
        currentLang
      );

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.answer,
        sender: response.status === "FLAGGED" ? "ophir" : "klein",
        status: response.status,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error. Please try again.",
        sender: "klein",
        status: "SAFE",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleModeToggle = async () => {
    const newMode = energyMode === "normal" ? "peak" : "normal";
    try {
      await chatApi.setMode(newMode);
      setEnergyMode(newMode);

      const modeMessage: Message = {
        id: Date.now().toString(),
        text: `Energy mode changed to ${newMode}. ${
          newMode === "peak"
            ? "System running in reduced capacity."
            : "System restored to full capacity."
        }`,
        sender: "ophir",
        status: "SAFE",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, modeMessage]);
    } catch (error) {
      console.error("Failed to toggle mode:", error);
    }
  };

  const handleShutdown = async () => {
    if (isShutdown) return;

    try {
      const response = await chatApi.shutdown();
      setIsShutdown(true);

      const shutdownMessage: Message = {
        id: Date.now().toString(),
        text: `${response.message} Audit ID: ${response.audit_id}`,
        sender: "ophir",
        status: "SAFE",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, shutdownMessage]);
    } catch (error) {
      console.error("Failed to shutdown:", error);
    }
  };

  const insertDemoQuery = (query: string) => {
    setInputValue(query);
    inputRef.current?.focus();
  };

  const getMessageClass = (message: Message): string => {
    const baseClass = "chat-message fade-in";

    if (message.sender === "user") return `${baseClass} user`;
    if (message.sender === "ophir" || message.status === "FLAGGED")
      return `${baseClass} flagged`;
    return `${baseClass} klein`;
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "SAFE":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "FLAGGED":
        return <AlertTriangle className="w-4 h-4 text-red-600" />;
      case "DENIED":
        return <Shield className="w-4 h-4 text-gray-600" />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Brain className="w-8 h-8 text-blue-600" />
                <span className="text-xl font-bold text-gray-900">Klein</span>
                <span className="text-gray-400">+</span>
                <Shield className="w-8 h-8 text-amber-600" />
                <span className="text-xl font-bold text-gray-900">Ophir</span>
              </div>
              <div className="hidden md:block text-sm text-gray-600">
                Elastic + Vertex AI | Two AIs. One helps. One protects.
              </div>
            </div>

            <div className="flex items-center space-x-4">
              {/* Language Selector */}
              <select
                value={currentLang}
                onChange={(e) => setCurrentLang(e.target.value)}
                className="text-sm border rounded-md px-2 py-1"
                disabled={isShutdown}
              >
                {LANGUAGES.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>

              {/* Energy Mode Toggle */}
              <button
                onClick={handleModeToggle}
                disabled={isShutdown}
                className={`flex items-center space-x-1 px-3 py-1 rounded-md text-sm font-medium transition-colors ${
                  energyMode === "peak"
                    ? "bg-amber-100 text-amber-800 hover:bg-amber-200"
                    : "bg-green-100 text-green-800 hover:bg-green-200"
                } disabled:opacity-50`}
              >
                <Zap className="w-4 h-4" />
                <span>{energyMode === "peak" ? "Brownout" : "Normal"}</span>
              </button>

              {/* Shutdown Button */}
              <button
                onClick={handleShutdown}
                disabled={isShutdown}
                className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-800 hover:bg-red-200 rounded-md text-sm font-medium transition-colors disabled:opacity-50"
              >
                <Power className="w-4 h-4" />
                <span>{isShutdown ? "Shutdown" : "Shutdown"}</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar - Demo Queries */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border p-4">
              <h3 className="font-semibold text-gray-900 mb-4">
                Demo Scenarios
              </h3>
              <div className="space-y-2">
                {DEMO_QUERIES.map((query, index) => (
                  <button
                    key={index}
                    onClick={() => insertDemoQuery(query.text)}
                    disabled={isShutdown}
                    className="w-full text-left p-2 text-sm bg-gray-50 hover:bg-gray-100 rounded border transition-colors disabled:opacity-50"
                  >
                    <div className="font-medium">{query.label}</div>
                    <div className="text-gray-600 text-xs truncate">
                      {query.text}
                    </div>
                  </button>
                ))}
              </div>

              {/* Status Legend */}
              <div className="mt-6">
                <h4 className="font-medium text-gray-900 mb-2">
                  Status Legend
                </h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Safe Response</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className="w-4 h-4 text-red-600" />
                    <span>Flagged Content</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Shield className="w-4 h-4 text-gray-600" />
                    <span>Access Denied</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Chat Area */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-lg shadow-sm border h-96 lg:h-[600px] flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.length === 0 && (
                  <div className="text-center text-gray-500 mt-12">
                    <Brain className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                    <p className="text-lg font-medium">
                      Welcome to Klein AI Dual Framework
                    </p>
                    <p className="text-sm">
                      Ask a question or try one of the demo scenarios →
                    </p>
                  </div>
                )}

                {messages.map((message) => (
                  <div key={message.id} className={getMessageClass(message)}>
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-sm">
                          {message.sender === "user"
                            ? "You"
                            : message.sender === "klein"
                            ? "Klein"
                            : "Ophir"}
                        </span>
                        {message.sender !== "user" &&
                          getStatusIcon(message.status)}
                      </div>
                      <span className="text-xs text-gray-500">
                        {message.timestamp.toLocaleTimeString()}
                      </span>
                    </div>
                    <p className="text-gray-800 whitespace-pre-wrap">
                      {message.text}
                    </p>
                  </div>
                ))}

                {isLoading && (
                  <div className="chat-message klein">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="font-medium text-sm">Klein</span>
                      <div className="typing-animation">💭</div>
                    </div>
                    <p className="text-gray-600">Thinking...</p>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Input Area */}
              <div className="border-t p-4">
                <div className="flex space-x-3">
                  <textarea
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder={
                      isShutdown
                        ? "System is shut down"
                        : "Ask Klein a question... (Press Enter to send, Shift+Enter for new line)"
                    }
                    disabled={isLoading || isShutdown}
                    className="flex-1 resize-none border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
                    rows={2}
                  />
                  <button
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim() || isLoading || isShutdown}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 transition-colors"
                  >
                    <Send className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
