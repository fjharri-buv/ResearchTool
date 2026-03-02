from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.schemas.paper import PaperQueryParams


class PaperRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Paper:
        paper = Paper(**data)
        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)
        return paper

    def get(self, paper_id: int) -> Paper | None:
        return self.db.get(Paper, paper_id)

    def get_by_doi(self, doi: str) -> Paper | None:
        return self.db.scalar(select(Paper).where(Paper.doi == doi))

    def update(self, paper: Paper, updates: dict) -> Paper:
        for key, value in updates.items():
            setattr(paper, key, value)
        self.db.add(paper)
        self.db.commit()
        self.db.refresh(paper)
        return paper

    def list(self, params: PaperQueryParams) -> tuple[list[Paper], int]:
        query: Select[tuple[Paper]] = select(Paper)

        if params.search:
            pattern = f"%{params.search}%"
            query = query.where(or_(Paper.title.ilike(pattern), Paper.doi.ilike(pattern), Paper.venue.ilike(pattern)))
        if params.status:
            query = query.where(Paper.status == params.status.value)
        if params.year_from is not None:
            query = query.where(Paper.year >= params.year_from)
        if params.year_to is not None:
            query = query.where(Paper.year <= params.year_to)

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.scalar(count_query) or 0

        sortable = {
            "title": Paper.title,
            "year": Paper.year,
            "added_at": Paper.added_at,
            "updated_at": Paper.updated_at,
        }
        sort_col = sortable.get(params.sort_by, Paper.added_at)
        query = query.order_by(sort_col.desc() if params.sort_dir.lower() == "desc" else sort_col.asc())
        query = query.offset(params.offset).limit(params.limit)

        return list(self.db.scalars(query).all()), total
