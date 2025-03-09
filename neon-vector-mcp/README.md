# Neon Vector MCP Server

This project sets up an MCP (Model Context Protocol) server that connects to a Neon Vector Database and exposes a chat interface for web applications.

## Overview

The MCP server acts as a bridge between your web chat interface and an LLM (Large Language Model), with the ability to retrieve information from your Neon Vector Database using RAG (Retrieval Augmented Generation).

## Prerequisites

- Python 3.10 or higher
- A Neon Vector Database instance
- Embeddings already stored in your Neon database
- An OpenAI API key (or other LLM provider)

## Setup Instructions

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure your MCP server**

Edit `mcp_agent.config.yaml` and update:

- Your Neon connection string
- Your embedding table name
- Your preferred embedding model
- Your LLM configuration

3. **Create a secrets file**

Create `mcp_agent.secrets.yaml` in the same directory with your API keys:

```yaml
openai:
  api_key: "your-openai-api-key"
```

4. **Start the server**

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

5. **Integrate with your website**

Include `client.js` in your website and instantiate the client:

```javascript
const chatClient = new MCPChatClient("http://your-server:8000");

// Send a message
chatClient.sendMessage("What information do you have about X?");

// Receive responses
chatClient.onMessage((data) => {
  if (data.message) {
    console.log("Bot response:", data.message);
  }
});
```

## Database Setup Requirements

Your Neon Vector Database should have a table with:

- A text column containing the content
- A vector column containing embeddings
- Any metadata columns needed

Example schema:

```sql
CREATE TABLE your_embeddings_table (
  id SERIAL PRIMARY KEY,
  content TEXT,
  embedding vector(768), -- Size depends on your model
  source_url TEXT,
  category TEXT
);
```

## API Endpoints

- `POST /chat` - Send a message to the chat interface
- `POST /vector-search` - Directly search the vector database
- `WebSocket /ws` - Real-time chat communication

## Testing

You can test your setup using the included `example.html` file by opening it in a browser while the server is running.

## Customization

You can customize the agent's behavior by modifying:

1. The instruction in `server.py` to change how the agent responds
2. The MCP server configuration in `mcp_agent.config.yaml`
3. The client interface in `client.js` and `example.html`
