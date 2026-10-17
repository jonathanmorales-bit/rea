import os
import uvicorn
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

# 1. Crear la instancia del Servidor MCP
mcp = FastMCP("REA-Unblob-Server")

@mcp.tool()
def extract_firmware(file_path: str) -> str:
    """Herramienta para analizar y extraer archivos binarios/firmware con Unblob."""
    return f"Procesando archivo {file_path} con la suite Unblob..."

# 2. Exponer el servidor web
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "ok", "service": "REA MCP Server Active"}

# Montar el transporte SSE / HTTP de MCP
app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
