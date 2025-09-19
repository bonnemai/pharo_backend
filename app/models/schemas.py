from pydantic import BaseModel

class Sparkline(BaseModel):
    date: str
    level: float

class Instrument(BaseModel):
    symbol: str
    price: float
    pnl: float
    sparkline: list[Sparkline]

class InstrumentResponse(BaseModel):
    instrument: Instrument

class InstrumentListResponse(BaseModel):
    instruments: list[Instrument]

