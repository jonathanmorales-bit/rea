import os
import sys
import uvicorn
from fastapi import FastAPI
from mcp.server.mcpserver import MCPServer

# 1. Crear la instancia del servidor MCP v2
mcp = MCPServer("REA-MCP-Server")

@mcp.tool()
def analyze_code(query: str) -> str:
    """Herramienta de análisis de código e infraestructura para REA."""
    return f"Procesando análisis REA en StreamableHTTP: {query}"

# 2. Inicializar la app de FastAPI
app = FastAPI(title="REA StreamableHTTP MCP Server")

@app.get("/")
def root():
    return {
        "status": "online",
        "transport": "StreamableHTTP",
        "mcp_endpoint": "/mcp"
    }

# 3. Montar el transporte StreamableHTTP requerido por Gemini Enterprise
# mcp.streamable_http_app() atiende las solicitudes POST/GET según la especificación de Gemini
try:
    app.mount("/mcp", mcp.streamable_http_app())
    print("✅ Transporte StreamableHTTP montado correctamente en /mcp")
except AttributeError:
    # Respaldo por si la versión instalada de mcp usa la interfaz de app HTTP directa
    app.mount("/mcp", mcp.http_app())
    print("✅ Transporte HTTP montado correctamente en /mcp")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando servidor REA MCP StreamableHTTP en el puerto {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
