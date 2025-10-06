from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.schemas import Instrument
from app.services.crud import get_instruments

router = APIRouter()

@router.get("/instruments", response_model=List[Instrument])
async def read_instruments(
    symbol: Optional[str] = None,
    sort_by_pnl: bool = Query(default=False),
):
    instruments = await get_instruments(symbol=symbol, sort_by_pnl=sort_by_pnl)
    if instruments is None:
        raise HTTPException(status_code=404, detail="Instruments not found")
    return instruments
