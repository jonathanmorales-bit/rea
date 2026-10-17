import os
import sys
import traceback
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="REA MCP Server")

# Manejo seguro para importar el SDK de MCP
mcp_status = "Not initialized"
mcp_app = None

try:
    # Intentar importar la sintaxis v2 primero
    try:
        from mcp.server.mcpserver import MCPServer
        mcp = MCPServer("REA-MCP-Server")
    except ImportError:
        # Fallback a la sintaxis v1 si aplica
        from mcp.server.fastmcp import FastMCP
        mcp = FastMCP("REA-MCP-Server")

    @mcp.tool()
    def analyze_code(query: str) -> str:
        """Herramienta de prueba para REA en Gemini Enterprise."""
        return f"Procesando solicitud REA: {query}"

    mcp_app = mcp.sse_app()
    mcp_status = "Active"
    print("✅ Módulo MCP inicializado con éxito.")

except Exception as err:
    print(f"⚠️ Error al inicializar MCP: {err}", file=sys.stderr)
    traceback.print_exc()
    mcp_status = f"Error: {str(err)}"

# Endpoint principal de diagnóstico
@app.get("/")
def root():
    return {
        "status": "online",
        "mcp_status": mcp_status,
        "mcp_endpoint": "/mcp"
    }

# Montar el transporte SSE de MCP si está disponible
if mcp_app:
    app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    # Render asigna dinámicamente la variable PORT
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando servidor web en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
