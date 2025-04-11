from typing import Any, Optional
import httpx
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("saos-mcp-server")

API_BASE = "https://www.saos.org.pl/api"
USER_AGENT = "saos-mcp-server/1.0"


async def make_request(url: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any] | None:
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
async def search_judgments(
    judge_name: Optional[str] = None,
    case_number: Optional[str] = None,
    court_type: Optional[str] = None,
    judgment_date_from: Optional[str] = None,
    judgment_date_to: Optional[str] = None,
    sort_field: str = "JUDGMENT_DATE",
    sort_direction: str = "DESC",
    page_number: int = 0,
    page_size: int = 10,
) -> dict[str, Any] | None:
    """Search for judgments in the SAOS API.

    Args:
        judge_name: Filter by judge's name.
        case_number: Filter by case number.
        court_type: Filter by court type.
        judgment_date_from: Start of judgment date range (YYYY-MM-DD).
        judgment_date_to: End of judgment date range (YYYY-MM-DD).
        sort_field: Field to sort by (default: 'JUDGMENT_DATE').
        sort_direction: Sort direction ('ASC' or 'DESC').
        page_number: Page number starting from 0.
        page_size: Number of results per page (10–100).
    """
    params: dict[str, Any] = {
        "judgeName": judge_name,
        "caseNumber": case_number,
        "courtType": court_type,
        "judgmentDateFrom": judgment_date_from,
        "judgmentDateTo": judgment_date_to,
        "sortingField": sort_field,
        "sortingDirection": sort_direction,
        "pageNumber": page_number,
        "pageSize": page_size,
    }

    # Remove keys with None values
    filtered_params = {k: v for k, v in params.items() if v is not None}
    results = await make_request(f"{API_BASE}/search/judgments", params=filtered_params)
    if results is None:
        return None

    # for item in results['items']:
    #     item['id'] = int(item['id'])
    return results

@mcp.tool()
async def get_judgment(id: int) -> dict[str, Any] | None:
    """Get a specific judgment from SAOS API.

    Args:
        id: ID of the judgment
    """
    results = await make_request(f"{API_BASE}/judgments/{id}")
    return results



if __name__ == "__main__":
    # Initialize and run the server
    print('Starting SAOS MCP server...')
    mcp.run(transport='stdio')
