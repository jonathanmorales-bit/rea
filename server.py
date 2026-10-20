import os
import sys
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# Inicializar servidor MCP oficial
mcp = FastMCP("REA-MCP-Server")

@mcp.tool()
def analyze_code(query: str) -> str:
    """Herramienta de análisis e ingeniería inversa para REA."""
    return f"Procesando solicitud REA: {query}"

# Inicializar la aplicación FastAPI
app = FastAPI(title="REA MCP Server")

@app.get("/")
def root():
    return {
        "status": "online",
        "mcp_status": "Active",
        "mcp_endpoint": "/mcp"
    }

# Montar el transporte de MCP (compatible con la versión 2.x mediante sse_app)
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando servidor REA MCP en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
