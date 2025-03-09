class MCPChatClient {
  constructor(serverUrl) {
    this.serverUrl = serverUrl || "http://localhost:8000";
    this.history = [];
    this.useWebSocket = false;
    this.ws = null;
    this.onMessageCallback = null;
  }

  // Initialize websocket connection
  connectWebSocket() {
    if (this.useWebSocket) {
      this.ws = new WebSocket(
        `ws://${this.serverUrl.replace(/^https?:\/\//, "")}/ws`
      );

      this.ws.onopen = () => {
        console.log("WebSocket connected");
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
          console.error("WebSocket error:", data.error);
          if (this.onMessageCallback) {
            this.onMessageCallback({ error: data.error });
          }
        } else if (data.response && this.onMessageCallback) {
          this.history.push({ role: "assistant", content: data.response });
          this.onMessageCallback({
            message: data.response,
            history: this.history,
          });
        }
      };

      this.ws.onclose = () => {
        console.log("WebSocket disconnected");
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    }
  }

  // Switch between WebSocket and HTTP modes
  setUseWebSocket(value) {
    this.useWebSocket = value;
    if (value && !this.ws) {
      this.connectWebSocket();
    }
  }

  // Set callback for receiving messages
  onMessage(callback) {
    this.onMessageCallback = callback;
  }

  // Send a message to the MCP server
  async sendMessage(message) {
    if (!message.trim()) return;

    // Add user message to history
    this.history.push({ role: "user", content: message });

    if (this.useWebSocket && this.ws && this.ws.readyState === WebSocket.OPEN) {
      // Use WebSocket for real-time communication
      this.ws.send(
        JSON.stringify({
          message: message,
          history: this.history,
        })
      );
    } else {
      // Use HTTP API
      try {
        const response = await fetch(`${this.serverUrl}/chat`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: message,
            history: this.history,
          }),
        });

        const data = await response.json();

        if (data.error) {
          console.error("Error:", data.error);
          if (this.onMessageCallback) {
            this.onMessageCallback({ error: data.error });
          }
        } else {
          this.history.push({ role: "assistant", content: data.response });
          if (this.onMessageCallback) {
            this.onMessageCallback({
              message: data.response,
              history: this.history,
            });
          }
        }
      } catch (error) {
        console.error("Error:", error);
        if (this.onMessageCallback) {
          this.onMessageCallback({ error: error.message });
        }
      }
    }
  }

  // Clear chat history
  clearHistory() {
    this.history = [];
  }

  // Direct vector search (bypass chat)
  async searchVector(query, topK = 5) {
    try {
      const response = await fetch(`${this.serverUrl}/vector-search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
          top_k: topK,
        }),
      });

      return await response.json();
    } catch (error) {
      console.error("Vector search error:", error);
      return { error: error.message };
    }
  }
}
