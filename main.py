from mcp.server.fastmcp import FastMCP

import src.client as client

mcp = FastMCP("AnkiMCP")

@mcp.tool()
async def get_deck_names():
    return await client.get_deck_names()

@mcp.tool()
async def create_deck(
        deck: str,
):
    return await client.create_deck(deck)

@mcp.tool()
async def migrate_deck(
        source_prefix: str,
        target_prefix: str,
):
    return await client.migrate_deck(source_prefix, target_prefix)
