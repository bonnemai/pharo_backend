# FastAPI REST API

This project is a simple REST API built with FastAPI that provides endpoints for managing and retrieving instrument data.

## Project Structure

```
fastapi-rest-api
├── app
│   ├── main.py          # Entry point of the application
│   ├── api
│   │   └── routes.py    # API endpoints
│   ├── models
│   │   └── schemas.py    # Data schemas using Pydantic
│   └── services
│       └── crud.py      # Functions for data interaction
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
└── .env                  # Environment variables
```

## Setup Instructions

1. **Create a virtual environment:**
   ```
   uv venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```
   uv sync
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add your environment variables.

4. **Test & coverage**
   ```
   uv sync --extra test
   uv run pytest
   ```
   Running the suite prints a coverage summary and writes `coverage.xml` (for tooling) while skipping files listed in `.gitignore`.
4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage
Swagger: http://localhost:8000/docs (http://localhost:8001/docs on Docker)
- **Fetch instruments:**
  - `GET /api/instruments` - Retrieve a list of instruments, with optional filtering by symbol and sorting by P&L.
  
- **Real-time updates:**
  - `GET /api/instruments/realtime` - Stream updates for instruments using Server Sent Events.

## TODO
* Migrate to uv, incl. Dockerfile
* GitHub Action? 