import os
import sys
import uvicorn
from fastapi import FastAPI

# Importación oficial compatible con MCP 2.x
try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    # Respaldar sintaxis por si acaso
    from mcp.server.fastmcp import FastMCP as MCPServer

# Inicializar servidor MCP con la nueva API
mcp = MCPServer("REA-MCP-Server")

@mcp.tool()
def analyze_code(query: str) -> str:
    """Herramienta de prueba para REA en Gemini Enterprise."""
    return f"Procesando solicitud REA: {query}"

# Aplicación FastAPI
app = FastAPI(title="REA MCP Server")

@app.get("/")
def root():
    return {"status": "online", "mcp_endpoint": "/mcp"}

# Montar el endpoint MCP SSE
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Iniciando servidor REA MCP v2 en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
