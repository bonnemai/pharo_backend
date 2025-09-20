import asyncio
import json
from importlib.resources import files

from app.services import crud

_DATA_PATH = files("app.resources").joinpath("instruments.json")


def _load_raw_data() -> list[dict]:
    with _DATA_PATH.open() as handle:
        return json.load(handle)


def test_get_instruments_respects_skip_and_limit() -> None:
    result = asyncio.run(crud.get_instruments(skip=1, limit=2))

    expected = _load_raw_data()[1:3]
    assert result == expected


def test_get_instruments_filters_by_symbol() -> None:
    symbol = _load_raw_data()[3]["symbol"]

    result = asyncio.run(crud.get_instruments(symbol=symbol))

    assert len(result) == 10
    assert result[0]["symbol"] == symbol


def test_get_instruments_sorts_descending_by_pnl() -> None:
    result = asyncio.run(crud.get_instruments(sort_by_pnl=True))

    pnls = [item["pnl"] for item in result]
    assert pnls == sorted(pnls, reverse=True)


def test_get_instrument_by_symbol_returns_match() -> None:
    reference = _load_raw_data()[0]

    result = asyncio.run(crud.get_instrument_by_symbol(reference["symbol"]))

    assert result == reference


def test_get_instrument_by_symbol_returns_none_when_missing() -> None:
    result = asyncio.run(crud.get_instrument_by_symbol("UNKNOWN"))

    assert result is None


def test_get_realtime_updates_delegates_to_lookup() -> None:
    reference = _load_raw_data()[0]

    result = asyncio.run(crud.get_realtime_updates(reference["symbol"]))

    assert result == reference
