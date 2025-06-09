from mcp.server.fastmcp import FastMCP

from src.client import invoke

mcp = FastMCP("AnkiMCP")

@mcp.tool()
async def get_deck_names():
    response = await invoke("deckNames")
    return response
