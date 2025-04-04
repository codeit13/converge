import axios from "axios";

import { BACKEND_URL } from "@/utils/constants";

// Helper function to create an EventSource with authorization header
const createEventSourceWithAuth = (url, token) => {
  const eventSource = new EventSource(url, {
    withCredentials: true,
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  return eventSource;
};

export default {
  // Test streaming functionality with a simple endpoint
  async testStream({ state, commit }, { onMessage, onError, onComplete }) {
    console.log('Starting test stream request');
    try {
      // Create a fetch request with proper headers for streaming
      const controller = new AbortController();
      const signal = controller.signal;
      
      // Start the streaming request to the test endpoint
      console.log('Sending POST request to test stream endpoint');
      fetch(`${BACKEND_URL}/api/test-stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.JWT_TOKEN}`,
          'Accept': 'text/event-stream',
        },
        credentials: 'include',
        signal: signal
      })
      .then(response => {
        console.log('Test stream response received:', response.status, response.statusText);
        console.log('Response headers:', [...response.headers.entries()]);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Get the reader from the response body stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        console.log('Test stream reader and decoder created');
        
        // Function to process the stream
        function processStream() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              console.log('Test stream complete - done flag received');
              if (onComplete && typeof onComplete === 'function') {
                onComplete();
              }
              return;
            }
            
            // Decode the chunk and add it to our buffer
            const chunk = decoder.decode(value, { stream: true });
            console.log('Received test chunk:', chunk);
            buffer += chunk;
            
            // Process each complete SSE message (format: "data: {...}\n\n")
            const messages = buffer.split('\n\n');
            buffer = messages.pop() || ''; // Keep the last incomplete chunk in the buffer
            console.log('Processed test messages count:', messages.length, 'Remaining buffer:', buffer ? buffer.length : 0);
            
            for (const message of messages) {
              console.log('Processing test message:', message);
              if (message.startsWith('data: ')) {
                try {
                  const jsonStr = message.substring(6); // Remove 'data: ' prefix
                  console.log('Parsing test JSON:', jsonStr);
                  const data = JSON.parse(jsonStr);
                  console.log('Parsed test data:', data);
                  if (onMessage && typeof onMessage === 'function') {
                    onMessage(data);
                  }
                } catch (err) {
                  console.error('Error parsing test SSE message:', err, message);
                }
              } else {
                console.log('Test message does not start with "data: ":', message);
              }
            }
            
            // Continue reading
            return processStream();
          }).catch(error => {
            console.error('Test stream reading error:', error);
            if (onError && typeof onError === 'function') {
              onError(error);
            }
          });
        }
        
        // Start processing the stream
        console.log('Starting test stream processing');
        processStream();
      })
      .catch(error => {
        console.error('Test fetch error:', error);
        if (onError && typeof onError === 'function') {
          onError(error);
        }
      });
      
      // Return an object with a close method to abort the fetch
      return {
        close: () => {
          controller.abort();
          if (onComplete && typeof onComplete === 'function') {
            onComplete();
          }
        }
      };
    } catch (error) {
      console.error('Error setting up test stream:', error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Test Streaming Error",
        description: "Failed to connect to the test streaming service."
      });
      if (onError && typeof onError === 'function') {
        onError(error);
      }
      return { close: () => {} }; // Return a dummy close function
    }
  },
  
  // Run an agent
  async runAgent({ state, commit }, userMessage) {
    try {
      const response = await axios.post(`${BACKEND_URL}/api/run`, {
        message: userMessage
      }, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${state.JWT_TOKEN}`,
        },
      });
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
  streamAgent({ state, commit }, { userPrompt, onMessage, onError, onComplete }) {
    try {
      // Create a fetch request with proper headers for streaming
      const controller = new AbortController();
      const signal = controller.signal;
      
      // Start the streaming request
      fetch(`${BACKEND_URL}/api/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.JWT_TOKEN}`,
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({ prompt: userPrompt }),
        credentials: 'include',
        signal: signal
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        // Get the reader from the response body stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        // Function to process the stream
        function processStream() {
          return reader.read().then(({ done, value }) => {
            if (done) {
              if (onComplete && typeof onComplete === 'function') {
                onComplete();
              }
              return;
            }
            
            // Decode the chunk and add it to our buffer
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;
            
            // Process each complete SSE message (format: "data: {...}\n\n")
            const messages = buffer.split('\n\n');
            buffer = messages.pop() || ''; // Keep the last incomplete chunk in the buffer
            
            for (const message of messages) {
              if (message.startsWith('data: ')) {
                try {
                  const jsonStr = message.substring(6); // Remove 'data: ' prefix
                  const data = JSON.parse(jsonStr);
                  if (onMessage && typeof onMessage === 'function') {
                    onMessage(data);
                  }
                } catch (err) {
                  console.error('Error parsing SSE message:', err);
                }
              }
            }
            
            // Continue reading
            return processStream();
          }).catch(error => {
            console.error('Stream reading error:', error);
            if (onError && typeof onError === 'function') {
              onError(error);
            }
          });
        }
        
        // Start processing the stream
        console.log('Starting stream processing');
        processStream();
      })
      .catch(error => {
        console.error('Fetch error:', error);
        if (onError && typeof onError === 'function') {
          onError(error);
        }
      });
      
      // Return an object with a close method to abort the fetch
      return {
        close: () => {
          controller.abort();
          if (onComplete && typeof onComplete === 'function') {
            onComplete();
          }
        }
      };
    } catch (error) {
      console.error('Error setting up stream:', error);
      commit("SET_TOASTER_DATA", {
        type: "error",
        message: "Streaming Error",
        description: "Failed to connect to the streaming service."
      });
      if (onError && typeof onError === 'function') {
        onError(error);
      }
      return { close: () => {} }; // Return a dummy close function
    }
  },

  async getHistory({ state, commit }, agentId) {
    try {
      const response = await axios.get(
        `${BACKEND_URL}/api/history/${agentId}`,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${state.JWT_TOKEN}`,
          },
        }
      );
      return response;
    } catch (error) {
      // You can add additional error handling here
      throw error;
    }
  },
};
