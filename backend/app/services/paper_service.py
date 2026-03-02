from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.paper import PaperStatus
from app.repositories.paper_repository import PaperRepository
from app.schemas.paper import PaperCreate, PaperQueryParams, PaperUpdate
from app.services.metadata_service import MetadataService


class PaperService:
    def __init__(self, db: Session):
        self.repo = PaperRepository(db)
        self.metadata_service = MetadataService()

    async def create_paper(self, payload: PaperCreate):
        data = payload.model_dump(exclude_none=True)

        if payload.doi:
            existing = self.repo.get_by_doi(payload.doi)
            if existing:
                raise HTTPException(status_code=409, detail="Paper with DOI already exists")
            enriched = await self.metadata_service.fetch_by_doi(payload.doi)
            if enriched:
                data = {**enriched, **data}

        if not data.get("title"):
            raise HTTPException(status_code=400, detail="Title is required (manual or DOI metadata)")

        if "status" not in data:
            data["status"] = PaperStatus.TO_READ.value
        elif isinstance(data["status"], PaperStatus):
            data["status"] = data["status"].value

        return self.repo.create(data)

    def get_paper(self, paper_id: int):
        paper = self.repo.get(paper_id)
        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")
        return paper

    def list_papers(self, params: PaperQueryParams):
        return self.repo.list(params)

    def update_paper(self, paper_id: int, payload: PaperUpdate):
        paper = self.get_paper(paper_id)
        updates = payload.model_dump(exclude_unset=True, exclude_none=True)
        if "status" in updates and isinstance(updates["status"], PaperStatus):
            updates["status"] = updates["status"].value
        return self.repo.update(paper, updates)
