import os
import sys
import uvicorn
from fastapi import FastAPI

# Importación resiliente según versión de mcp
try:
    from mcp.server import Server as MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        from mcp.server.mcpserver import MCPServer

# Inicializar la app MCP
mcp = MCPServer("REA-MCP-Server")

@mcp.tool()
def analyze_code(query: str) -> str:
    """Herramienta de análisis de código para REA."""
    return f"Procesando solicitud REA: {query}"

app = FastAPI(title="REA StreamableHTTP MCP Server")

@app.get("/")
def root():
    return {
        "status": "online",
        "transport": "StreamableHTTP",
        "mcp_endpoint": "/mcp"
    }

# Intenta montar la aplicación StreamableHTTP/SSE
try:
    if hasattr(mcp, "streamable_http_app"):
        app.mount("/mcp", mcp.streamable_http_app())
    elif hasattr(mcp, "sse_app"):
        app.mount("/mcp", mcp.sse_app())
    else:
        app.mount("/mcp", mcp.http_app())
    print("✅ Transporte MCP montado correctamente en /mcp")
except Exception as err:
    print(f"⚠️ Nota al montar endpoint MCP: {err}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando servidor REA MCP en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
