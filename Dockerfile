FROM astral/uv:python3.12-bookworm-slim
WORKDIR /app

COPY pyproject.toml README.md ./
COPY app ./app

RUN uv pip install --no-cache-dir --system .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
