FROM astral/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv pip install --no-cache-dir --system '.[test]'
RUN uv sync --extra test
   
COPY app ./app
COPY tests ./tests
RUN uv run ruff check
RUN uv run pyrefly check
RUN uv run pytest

FROM astral/uv:python3.12-bookworm-slim
WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY app ./app

RUN uv pip install --no-cache-dir --system .

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=5)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
