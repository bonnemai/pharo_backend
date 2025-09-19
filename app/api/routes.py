from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models.schemas import Instrument
from services.crud import get_instruments, get_realtime_updates

router = APIRouter()

@router.get("/api/instruments", response_model=List[Instrument])
async def read_instruments(symbol: Optional[str] = None, sort_by_pnl: Optional[str] = None):
    instruments = await get_instruments(symbol=symbol, sort_by_pnl=sort_by_pnl)
    if instruments is None:
        raise HTTPException(status_code=404, detail="Instruments not found")
    return instruments

@router.get("/api/instruments/realtime")
async def stream_realtime_updates(symbol: str):
    return await get_realtime_updates(symbol=symbol)