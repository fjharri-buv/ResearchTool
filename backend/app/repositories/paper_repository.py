"""Paper repository primitives."""

from __future__ import annotations

from dataclasses import dataclass

from backend.app.utils.doi import normalize_doi


@dataclass
class Paper:
    id: int | None = None
    title: str = ""
    doi: str | None = None


class PaperRepository:
    """Simple in-memory repository used by the service layer."""

    def __init__(self) -> None:
        self._papers: dict[int, Paper] = {}
        self._next_id = 1

    def get_by_doi(self, doi: str) -> Paper | None:
        normalized_doi = normalize_doi(doi)
        return next(
            (paper for paper in self._papers.values() if paper.doi == normalized_doi),
            None,
        )

    def create(self, paper: Paper) -> Paper:
        paper.id = self._next_id
        self._next_id += 1
        paper.doi = normalize_doi(paper.doi)
        self._papers[paper.id] = paper
        return paper

    def update(self, paper: Paper) -> Paper:
        if paper.id is None or paper.id not in self._papers:
            raise ValueError("Paper does not exist")

        paper.doi = normalize_doi(paper.doi)
        self._papers[paper.id] = paper
        return paper
