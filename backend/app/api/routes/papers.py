from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.paper import PaperCreate, PaperListResponse, PaperQueryParams, PaperRead, PaperStatus, PaperUpdate
from app.services.paper_service import PaperService

router = APIRouter(prefix="/api/papers", tags=["papers"])


@router.post("", response_model=PaperRead)
async def create_paper(payload: PaperCreate, db: Session = Depends(get_db)):
    service = PaperService(db)
    paper = await service.create_paper(payload)
    return paper


@router.get("", response_model=PaperListResponse)
def list_papers(
    db: Session = Depends(get_db),
    search: str | None = None,
    status: PaperStatus | None = None,
    year_from: int | None = Query(default=None, ge=0),
    year_to: int | None = Query(default=None, ge=0),
    sort_by: str = "added_at",
    sort_dir: str = "desc",
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = PaperService(db)
    params = PaperQueryParams(
        search=search,
        status=status,
        year_from=year_from,
        year_to=year_to,
        sort_by=sort_by,
        sort_dir=sort_dir,
        limit=limit,
        offset=offset,
    )
    items, total = service.list_papers(params)
    return PaperListResponse(items=items, total=total)


@router.get("/{paper_id}", response_model=PaperRead)
def get_paper(paper_id: int, db: Session = Depends(get_db)):
    service = PaperService(db)
    return service.get_paper(paper_id)


@router.patch("/{paper_id}", response_model=PaperRead)
def update_paper(paper_id: int, payload: PaperUpdate, db: Session = Depends(get_db)):
    service = PaperService(db)
    return service.update_paper(paper_id, payload)
