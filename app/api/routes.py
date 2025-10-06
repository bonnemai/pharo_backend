from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from app.models.schemas import Instrument
from app.services.crud import get_instruments, sse_stream

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

@router.get("/instruments/realtime")
async def stream_realtime_updates(request: Request):
    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Retry-After": "1000",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    return StreamingResponse(sse_stream(request), media_type="text/event-stream", headers=headers)
