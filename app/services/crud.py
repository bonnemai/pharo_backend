import json
import os
from importlib.resources import files

import aiofiles

from app.models.schemas import Instrument

_DATA_PATH = files("app.resources").joinpath("instruments.json")

async def get_instruments(skip: int = 0, limit: int = 10, symbol: str | None = None, sort_by_pnl: bool = False) -> list[Instrument]:
    async with aiofiles.open(os.fspath(_DATA_PATH), 'r') as f:
        content = await f.read()
        mock_db = json.loads(content)

    filtered_instruments = mock_db
    if symbol:
        filtered_instruments = [instrument for instrument in filtered_instruments if instrument["symbol"] == symbol]
    
    if sort_by_pnl:
        filtered_instruments.sort(key=lambda x: x["pnl"], reverse=True)
    
    return filtered_instruments[skip: skip + limit]

async def get_instrument_by_symbol(symbol: str) -> Instrument | None:
    instruments = await get_instruments()
    for instrument in instruments:
        if instrument['symbol'] == symbol:
            return instrument
    return None

async def get_realtime_updates(symbol: str) -> Instrument | None:
    return await get_instrument_by_symbol(symbol)
