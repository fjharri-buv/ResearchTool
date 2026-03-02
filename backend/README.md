# Backend (Milestone 1)

## Run

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Implemented endpoints
- `POST /api/papers`
- `GET /api/papers`
- `GET /api/papers/{id}`
- `PATCH /api/papers/{id}`
- `GET /api/health`

`POST /api/papers` supports DOI metadata enrichment via Crossref (best effort). If network fails, manual fields still work.
