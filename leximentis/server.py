import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
import uvicorn
from mcp_agent.mcp.mcp_aggregator import MCPAggregator
from mcp_agent.context import initialize_context

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP context and aggregator
context = None
aggregator = None


@app.on_event("startup")
async def startup_event():
    global context, aggregator
    context = await initialize_context()
    # Connect to both vector database and optional file system
    aggregator = MCPAggregator(
        server_names=["qdrant", "filesystem"],
        connection_persistence=True,
        context=context,
        name="workers_comp_assistant",
    )
    await aggregator.__aenter__()


@app.on_event("shutdown")
async def shutdown_event():
    if aggregator:
        await aggregator.__aexit__(None, None, None)


@app.post("/query")
async def query(request: Request):
    data = await request.json()
    user_query = data.get("query")

    # Call the vector database search tool
    result = await aggregator.call_tool(
        "qdrant/search", {"query": user_query, "top_k": 5}
    )

    # Get relevant context from the vector database
    context_data = result.result

    # You can process the context and return it directly or
    # use it to generate a response with an LLM
    return {"result": context_data}


# SSE endpoint for streaming responses
@app.get("/sse")
async def sse_endpoint(request: Request):
    async def event_generator():
        # Example implementation - adapt to your needs
        while True:
            if await request.is_disconnected():
                break
            # Process any pending messages from clients
            await asyncio.sleep(0.1)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
