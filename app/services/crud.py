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
    limit: int = 100,
    symbol: str | None = None,
    sort_by_pnl: bool = False,
) -> list[dict[str, Any]]:
    async with aiofiles.open(_DATA_PATH, 'r') as f:
        content = await f.read()
        filtered_instruments = json.loads(content)
        logger.debug("Loaded %s instruments from %s", len(filtered_instruments), _DATA_PATH)

    # Add random variations to price and pnl for demo purposes
    dice = random()
    for instrument in filtered_instruments:
        instrument['price'] *= 1 + 0.2 * (dice - 0.5)
        instrument['pnl'] *= 1 + 0.2 * (dice - 0.5)

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

