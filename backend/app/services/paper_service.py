"""Business logic for papers."""

from __future__ import annotations

from backend.app.repositories.paper_repository import Paper, PaperRepository
from backend.app.utils.doi import normalize_doi


class PaperService:
    def __init__(self, repository: PaperRepository) -> None:
        self.repository = repository

    def create_paper(self, title: str, doi: str | None) -> Paper:
        normalized_doi = normalize_doi(doi)
        if normalized_doi and self.repository.get_by_doi(normalized_doi):
            raise ValueError("Paper with DOI already exists")

        paper = Paper(title=title, doi=normalized_doi)
        return self.repository.create(paper)

    def update_paper(self, paper_id: int, title: str, doi: str | None) -> Paper:
        normalized_doi = normalize_doi(doi)
        if normalized_doi:
            existing = self.repository.get_by_doi(normalized_doi)
            if existing is not None and existing.id != paper_id:
                raise ValueError("Paper with DOI already exists")

        paper = Paper(id=paper_id, title=title, doi=normalized_doi)
        return self.repository.update(paper)
