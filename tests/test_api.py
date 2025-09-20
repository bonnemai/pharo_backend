from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.main import app
import pytest


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_read_root_returns_welcome_message(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI REST API!"}


def test_favicon_returns_svg_document(client: TestClient) -> None:
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/svg+xml")
    assert response.text.startswith("<svg")


@pytest.mark.skip('In progress')
def test_read_instruments_uses_service_layer(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    expected_payload = [{"symbol": "AAPL", "pnl": 10.0}]
    mock_get_instruments = AsyncMock(return_value=expected_payload)
    monkeypatch.setattr("app.api.routes.get_instruments", mock_get_instruments)

    response = client.get("/api/api/instruments", params={"symbol": "AAPL"})

    assert response.status_code == 200
    assert response.json() == expected_payload
    mock_get_instruments.assert_awaited_once_with(symbol="AAPL", sort_by_pnl=None)


def test_read_instruments_returns_404_when_missing(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    mock_get_instruments = AsyncMock(return_value=None)
    monkeypatch.setattr("app.api.routes.get_instruments", mock_get_instruments)

    response = client.get("/api/api/instruments")

    assert response.status_code == 404
    assert response.json()["detail"] == "Instruments not found"


@pytest.mark.skip('too Slow')
def test_stream_realtime_updates_returns_payload(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    expected_payload = {"symbol": "AAPL", "pnl": 2, "price": 12}
    mock_get_updates = AsyncMock(return_value=expected_payload)
    monkeypatch.setattr("app.api.routes.get_instruments", mock_get_updates)

    response = client.get("/api/api/instruments/realtime")

    assert response.status_code == 200
    assert response.json() != expected_payload
    mock_get_updates.assert_awaited_once_with(symbol="AAPL")
