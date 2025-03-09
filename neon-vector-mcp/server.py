import os
from typing import Dict, Any, List
import asyncio
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.mcp.mcp_aggregator import MCPAggregator
from mcp_agent.context import Context

app = FastAPI()

# Configure CORS to allow requests from your website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your website URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
mcp_app = None
agent = None
llm = None
aggregator = None


class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []


@app.on_event("startup")
async def startup_event():
    global mcp_app, agent, llm, aggregator

    # Initialize the MCP application
    mcp_app = MCPApp(name="neon_vector_mcp")
    await mcp_app.initialize()

    # Create the agent with access to the neon_vector server
    agent = Agent(
        name="neon_knowledge_agent",
        instruction="""You are an assistant with access to a knowledge base stored in a Neon Vector Database.
        When asked questions, you'll use the 'search' tool to find relevant information 
        from this database before answering. Always provide helpful, accurate responses
        based on the information retrieved from the database.""",
        server_names=["neon_vector"],
    )
    await agent.initialize()

    # Attach the LLM to the agent
    llm = await agent.attach_llm(OpenAIAugmentedLLM)

    # Set up aggregator for direct tool access
    aggregator = MCPAggregator(
        server_names=["neon_vector"],
        connection_persistence=True,
        context=mcp_app.context,
        name="neon_vector_assistant",
    )
    await aggregator.__aenter__()

    print("MCP Server initialized and ready!")


@app.on_event("shutdown")
async def shutdown_event():
    if aggregator:
        await aggregator.__aexit__(None, None, None)
    print("MCP Server shut down.")


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Convert history to the format LLM expects if needed
        history = request.history if request.history else []

        # Generate response using the LLM with RAG capabilities
        response = await llm.generate_str(message=request.message, history=history)

        return {"response": response}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"An error occurred: {str(e)}"}
        )


@app.post("/vector-search")
async def vector_search(request: Request):
    data = await request.json()
    query = data.get("query")
    top_k = data.get("top_k", 5)

    try:
        # Direct access to the vector database search tool
        result = await aggregator.call_tool(
            "neon_vector/search", {"query": query, "top_k": top_k}
        )

        return {"results": result.result}
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"An error occurred: {str(e)}"}
        )


# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message")
            history = data.get("history", [])

            response = await llm.generate_str(message=message, history=history)

            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        await websocket.send_json({"error": str(e)})


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
