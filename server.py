import os
import sys
import uvicorn
from fastapi import FastAPI

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as e:
    print(f"Error importando MCP: {e}", file=sys.stderr)
    sys.exit(1)

# Inicializar servidor MCP
mcp = FastMCP("REA-MCP-Server")

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
    print(f"Iniciando servidor REA MCP en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
