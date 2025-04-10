import axios from "axios";

import { BACKEND_URL } from "@/utils/constants";

// Helper function to create an EventSource with authorization header
const createEventSourceWithAuth = (url, token) => {
  const eventSource = new EventSource(url, {
    withCredentials: true,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return eventSource;
};

export default {
  // Create a new chat session
  async createChat({ state }, payload) {
    try {
      // If payload is provided, use the user_id from it, otherwise get from state
      const userId = payload?.user_id || state.auth?.user?._id;
      if (!userId) {
        throw new Error('User not authenticated');
      }
      console.log('Creating chat with user_id:', userId);
      const response = await axios.post(`${BACKEND_URL}/api/chats`, {
        user_id: userId
      });
      return { data: response.data };
    } catch (error) {
      console.error('Error creating chat:', error);
      throw error;
    }
  },

  // Run an agent
  async runAgent({ state, commit }, userMessage) {
    try {
      const response = await axios.post(
        `${BACKEND_URL}/api/run`,
        {
          message: userMessage,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.JWT_TOKEN}`,
            "user-id": state?.auth?.user?._id,
          },
        }
      );
      return response;
    } catch (error) {
      console.log(error);

      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description:
          error?.response?.data?.detail[0]?.msg || "Failed to run agent.",
      });
    }
  },

  // Stream agent responses
  streamAgent(
    { state, commit },
    { userPrompt, chatId = null, onMessage, onError, onComplete }
  ) {
    try {
      // Create a fetch request with proper headers for streaming
      const controller = new AbortController();
      const signal = controller.signal;

      // Start the streaming request
      fetch(`${BACKEND_URL}/api/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "user-id": state?.auth?.user?._id || "", // Ensure it's never undefined
          Accept: "text/event-stream",
        },
        body: JSON.stringify({ prompt: userPrompt }),
        credentials: "include",
        signal: signal,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          // Get the reader from the response body stream
          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = "";

          // Function to process the stream
          function processStream() {
            return reader
              .read()
              .then(({ done, value }) => {
                if (done) {
                  if (onComplete && typeof onComplete === "function") {
                    onComplete();
                  }
                  return;
                }

                // Decode the chunk and add it to our buffer
                const chunk = decoder.decode(value, { stream: true });
                buffer += chunk;

                // Process each complete SSE message (format: "data: {...}\n\n")
                const messages = buffer.split("\n\n");
                buffer = messages.pop() || ""; // Keep the last incomplete chunk in the buffer

                for (const message of messages) {
                  if (message.startsWith("data: ")) {
                    try {
                      const jsonStr = message.substring(6); // Remove 'data: ' prefix
                      const data = JSON.parse(jsonStr);
                      if (onMessage && typeof onMessage === "function") {
                        onMessage(data);
                      }
                    } catch (err) {
                      console.error("Error parsing SSE message:", err);
                    }
                  }
                }

                // Continue reading
                return processStream();
              })
              .catch((error) => {
                console.error("Stream reading error:", error);
                if (onError && typeof onError === "function") {
                  onError(error);
                }
              });
          }

          // Start processing the stream
          console.log("Starting stream processing");
          processStream();
        })
        .catch((error) => {
          console.error("Fetch error:", error);
          if (onError && typeof onError === "function") {
            onError(error);
          }
        });

      // Return an object with a close method to abort the fetch
      return {
        close: () => {
          controller.abort();
          if (onComplete && typeof onComplete === "function") {
            onComplete();
          }
        },
      };
    } catch (error) {
      console.error("Error setting up stream:", error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Streaming Error",
        description: "Failed to connect to the streaming service.",
      });
      if (onError && typeof onError === "function") {
        onError(error);
      }
      return { close: () => {} }; // Return a dummy close function
    }
  },

  async getHistory({ state, commit }, agentId) {
    try {
      const { data } = await axios.get(`${BACKEND_URL}/api/history`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${state.JWT_TOKEN}`,
        },
      });
      commit("SET_AVAILABLE_TOOLS", data);
    } catch (error) {
      console.log(error);

      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description:
          error?.response?.data?.detail[0]?.msg || "Failed to run agent.",
      });
    }
  },

  async getAvailableTools({ state, commit }) {
    try {
      const { data } = await axios.get(
        `${BACKEND_URL}/api/get-available-tools`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.JWT_TOKEN}`,
          },
        }
      );
      commit("SET_HISTORY", data);
    } catch (error) {
      console.log(error);

      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description:
          error?.response?.data?.detail[0]?.msg || "Failed to get tools.",
      });
    }
  },

  // Get all chat sessions for the current user
  async getChatSessions({ state, commit }) {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/chats`, {
        headers: {
          "Content-Type": "application/json",
          "user-id": state?.auth?.user?._id,
        },
      });
      commit("SET_CHAT_SESSIONS", response.data);
      return response.data;
    } catch (error) {
      console.log(error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description:
          error?.response?.data?.detail || "Failed to load chat sessions.",
      });
    }
  },

  // Get messages for a specific chat session
  async getChatMessages({ state, commit }, chatId) {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/chats/${chatId}`, {
        headers: {
          "Content-Type": "application/json",
          "user-id": state?.auth?.user?._id,
        },
      });
      commit("SET_CURRENT_CHAT_MESSAGES", response.data);
      return response.data;
    } catch (error) {
      console.log(error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description:
          error?.response?.data?.detail || "Failed to load chat messages.",
      });
    }
  },

  // Delete a chat session
  async deleteChat({ state, commit }, chatId) {
    try {
      await axios.delete(`${BACKEND_URL}/api/chats/${chatId}`, {
        headers: {
          "Content-Type": "application/json",
          "user-id": state?.auth?.user?._id,
        },
      });
      // Remove the chat from the local state
      commit("REMOVE_CHAT_SESSION", chatId);
      commit("SET_TOASTER_DATA", {
        type: "success",
        message: "Success",
        description: "Chat deleted successfully.",
      });
    } catch (error) {
      console.log(error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Error",
        description: error?.response?.data?.detail || "Failed to delete chat.",
      });
    }
  },

  // Analytics actions
  async getAnalyticsSummary({ state, commit }) {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/analytics/summary`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.JWT_TOKEN}`,
            "user-id": state?.auth?.user?._id,
          },
        }
      );
      commit("SET_ANALYTICS_SUMMARY", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching analytics summary:", error);
      throw error;
    }
  },

  async getChatDistribution({ state, commit }) {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/analytics/chat-distribution`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.JWT_TOKEN}`,
            "user-id": state?.auth?.user?._id,
          },
        }
      );
      commit("SET_CHAT_DISTRIBUTION", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching chat distribution:", error);
      throw error;
    }
  },
};
