import axios, { AxiosResponse } from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Types
export interface ChatRequest {
  message: string;
  lang: string;
}

export interface ChatResponse {
  answer: string;
  status: "SAFE" | "FLAGGED" | "DENIED";
  audit_id?: string;
}

export interface HealthResponse {
  ok: boolean;
  status: string;
  mode: string;
  timestamp: string;
  services: Record<string, string>;
}

export interface ModeResponse {
  ok: boolean;
  mode: string;
  message?: string;
}

export interface ShutdownResponse {
  ok: boolean;
  message: string;
  audit_id: string;
}

// API Functions
export const chatApi = {
  // Send chat message
  async sendMessage(
    message: string,
    lang: string = "en"
  ): Promise<ChatResponse> {
    try {
      const response: AxiosResponse<ChatResponse> = await api.post(
        "/api/chat",
        {
          message,
          lang,
        }
      );
      return response.data;
    } catch (error: any) {
      console.error("Chat API error:", error);

      // If we get a response from the backend, use it
      if (error.response?.data?.answer) {
        return {
          answer: error.response.data.answer,
          status: error.response.data.status || "SAFE",
        };
      }

      // Fallback error response that matches Klein's voice
      return {
        answer:
          "Klein: I apologize, but I'm having some technical difficulties right now. Let me still try to help you - what specific information are you looking for?",
        status: "SAFE",
      };
    }
  },

  // Get system health
  async getHealth(): Promise<HealthResponse> {
    try {
      const response: AxiosResponse<HealthResponse> = await api.get(
        "/api/health"
      );
      return response.data;
    } catch (error) {
      console.error("Health API error:", error);
      throw new Error("Failed to get system health.");
    }
  },

  // Set energy mode
  async setMode(mode: "normal" | "peak"): Promise<ModeResponse> {
    try {
      const response: AxiosResponse<ModeResponse> = await api.post(
        "/api/mode",
        {
          mode,
        }
      );
      return response.data;
    } catch (error) {
      console.error("Mode API error:", error);
      throw new Error("Failed to set energy mode.");
    }
  },

  // Shutdown system
  async shutdown(): Promise<ShutdownResponse> {
    try {
      const response: AxiosResponse<ShutdownResponse> = await api.post(
        "/api/shutdown"
      );
      return response.data;
    } catch (error) {
      console.error("Shutdown API error:", error);
      throw new Error("Failed to shutdown system.");
    }
  },
};

// Helper function to get status color
export const getStatusColor = (status: string): string => {
  switch (status.toUpperCase()) {
    case "SAFE":
      return "text-green-600";
    case "FLAGGED":
      return "text-amber-600";
    case "DENIED":
      return "text-red-600";
    default:
      return "text-gray-600";
  }
};

// Helper function to format timestamp
export const formatTimestamp = (timestamp: string): string => {
  return new Date(timestamp).toLocaleTimeString();
};

export default api;
