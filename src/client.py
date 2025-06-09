from typing import Any, TypedDict
import httpx

ANKICONNECT_URL = "http://127.0.0.1:8765"

class AnkiConnectResponse(TypedDict):
    result: Any | None
    error: str | None

def SuccessResponse(result: Any) -> AnkiConnectResponse:
    return {
        "result": result,
        "error": None,
    }

def ErrorResponse(error: str) -> AnkiConnectResponse:
    return {
        "result": None,
        "error": error,
    }

async def invoke(
        action: str,
        params: dict[str, Any] | None = None,
) -> AnkiConnectResponse:
    payload = {
        "action": action,
        "version": 6,
    }
    if params:
        payload["params"] = params

    async with httpx.AsyncClient() as client:
        response = await client.post(ANKICONNECT_URL, json=payload)
        return response.json()
