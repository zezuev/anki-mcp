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

async def get_deck_names() -> AnkiConnectResponse:
    response = await invoke("deckNames")
    return response

async def get_cards_in_deck(
        deck: str,
) -> AnkiConnectResponse:
    response = await invoke(
        action="findCards",
        params={
            "query": f"deck:\"{deck.lower()}\"",
        },
    )
    return response

async def change_deck(
        card_ids: list[int],
        target_deck: str,
) -> AnkiConnectResponse:
    response = await invoke(
        action="changeDeck",
        params={
            "cards": card_ids,
            "deck": target_deck,
        },
    )
    return response

async def delete_deck(
        deck: str,
) -> AnkiConnectResponse:
    response = await invoke(
        action="deleteDecks",
        params={
            "decks": [deck],
            "cardsToo": True,
        },
    )
    return response

async def create_deck(
        deck: str,
) -> AnkiConnectResponse:
    response = await invoke(
        action="createDeck",
        params={
            "deck": deck,
        },
    )
    return response

async def migrate_deck(
        source_prefix: str,
        target_prefix: str,
) -> AnkiConnectResponse:
    # Fetch all deck names
    response = await get_deck_names()
    if response["result"] is None:
        return response
    all_decks: list[str] = response["result"]

    # Find decks to migrate
    decks_to_migrate = [
        deck
        for deck in all_decks
        if deck == source_prefix
        or deck.startswith(source_prefix + "::")
    ]
    if not decks_to_migrate:
        return ErrorResponse(
            f"No decks found starting with '{source_prefix!r}'."
        )

    # Migrate each deck
    for old_deck in decks_to_migrate:
        # Determine new deck name
        if old_deck == source_prefix:
            new_deck = target_prefix
        else:
            subdeck_part = old_deck[len(source_prefix):]
            new_deck = target_prefix + subdeck_part

        # Find all cards in the old deck
        response = await get_cards_in_deck(old_deck)
        if response["result"] is None:
            return response
        card_ids: list[int] = response["result"]

        # Migrate cards to new deck
        await create_deck(new_deck)
        if card_ids:
            await change_deck(card_ids, new_deck)

        # Delete old deck
        await delete_deck(old_deck)

    return SuccessResponse(
        f"Successfully migrated {source_prefix!r} to {target_prefix!r}.",
    )
