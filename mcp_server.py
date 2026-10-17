import os
import uvicorn
from mcp.server.fastmcp import FastMCP

# Inicializa el servidor MCP
mcp = FastMCP("REA-Unblob")

@mcp.tool()
def analyze_firmware(file_path: str) -> str:
    """Herramienta para analizar archivos de firmware o binarios."""
    return f"Analizando archivo {file_path} con la suite de REA/Unblob..."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Ejecuta el servidor expuesto en el puerto de Render
    uvicorn.run(mcp.sse_app(), host="0.0.0.0", port=port)
