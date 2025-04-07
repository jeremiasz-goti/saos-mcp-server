from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("saos-mcp-server")

API_BASE = "https://www.saos.org.pl/api"
USER_AGENT = "saos-mcp-server/1.0"


async def make_request(url: str) -> dict[str, Any] | None:
    """Make a request to the SAOS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


@mcp.tool()
async def get_judgments() -> dict[str, Any] | None:
    results = await make_request(f"{API_BASE}/search/judgments")
    return results

@mcp.tool()
async def get_judgment(id: str) -> dict[str, Any] | None:
    results = await make_request(f"{API_BASE}/search/judgments/{id}")
    return results



if __name__ == "__main__":
    # Initialize and run the server
    print('Starting SAOS MCP server...')
    mcp.run(transport='stdio')
