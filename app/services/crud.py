import asyncio
import json
import logging
import aiofiles
from pathlib import Path
from random import random
from typing import Any
from fastapi import Request

_DATA_PATH = Path(__file__).resolve().parent.parent / "resources" / "instruments.json"
logger = logging.getLogger(__name__)

async def get_instruments(
    skip: int = 0,
    limit: int = 10,
    symbol: str | None = None,
    sort_by_pnl: bool = False,
) -> list[dict[str, Any]]:
    async with aiofiles.open(_DATA_PATH, 'r') as f:
        content = await f.read()
        mock_db = json.loads(content)
        logger.debug("Loaded %s instruments from %s", len(mock_db), _DATA_PATH)

    filtered_instruments = mock_db
    if symbol:
        filtered_instruments = [instrument for instrument in filtered_instruments if instrument["symbol"] == symbol]
        logger.debug("Filtered instruments by symbol '%s': %s matched", symbol, len(filtered_instruments))
    
    if sort_by_pnl:
        filtered_instruments.sort(key=lambda x: x["pnl"], reverse=True)
        logger.debug("Sorted instruments by pnl descending")
    
    return filtered_instruments[skip: skip + limit]

async def get_instrument_by_symbol(symbol: str) -> dict[str, Any] | None:
    instruments = await get_instruments()
    for instrument in instruments:
        if instrument['symbol'] == symbol:
            logger.debug("Found instrument for symbol '%s'", symbol)
            return instrument
    logger.debug("No instrument found for symbol '%s'", symbol)
    return None

# async def get_realtime_updates(symbol: str) -> Instrument | None:
#     return await get_instrument_by_symbol(symbol)

def sse_pack(event: str | None, data: dict) -> str:
    """Format one SSE message with optional event name."""
    payload = f"data: {json.dumps(data)}\n"
    if event:
        payload = f"event: {event}\n" + payload
    return payload + "\n"

async def sse_stream(request: Request):
    """Continuously push random upserts/deletes and heartbeats."""
    try:
        while True:
            if await request.is_disconnected():
                logger.info("SSE client disconnected")
                break

            # heartbeat every 10s (helps load balancers / keep-alive)
            yield "event: ping\ndata: {}\n\n"

            dice = random()

            # random demo mutation
            await asyncio.sleep(dice)

            instruments = await get_instruments()

            for instrument in instruments: 
                instrument['price']*=2*dice-1
                instrument['pnl']*=2*dice-1
            
            yield sse_pack("upsert", {"rows": instruments})
            logger.debug("Pushed SSE update with dice=%.3f", dice)
    except asyncio.CancelledError:
        logger.info("SSE stream cancelled by server")
