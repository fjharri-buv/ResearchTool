# Research Assistant (Local-Only)

This repo now includes:
- `backend/`: FastAPI + SQLAlchemy + Alembic + SQLite (Milestone 1 complete)
- `frontend/`: React + Vite scaffold (future milestones)
- `data/`: SQLite DB location (`data/app.db`)

## Milestone 1 status
Completed:
- Backend skeleton and project structure
- Initial migration for `papers`
- Core papers CRUD API (create/list/detail/update)
- DOI metadata enrichment (Crossref, best effort)
- Graceful fallback to manual entry when metadata fetch fails

## Quickstart

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
