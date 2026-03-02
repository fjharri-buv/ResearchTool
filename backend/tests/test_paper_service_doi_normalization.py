from backend.app.repositories.paper_repository import PaperRepository
from backend.app.services.paper_service import PaperService


def test_create_paper_normalizes_doi_for_lookup_and_persistence() -> None:
    repository = PaperRepository()
    service = PaperService(repository)

    created = service.create_paper(
        title="A Paper",
        doi="  HTTPS://DOI.ORG/10.1000/XYZ  ",
    )

    assert created.doi == "10.1000/xyz"
    fetched = repository.get_by_doi("doi:10.1000/XYZ")
    assert fetched is not None
    assert fetched.id == created.id


def test_create_paper_rejects_duplicate_after_normalization() -> None:
    repository = PaperRepository()
    service = PaperService(repository)

    service.create_paper(title="A Paper", doi="doi:10.1000/xyz")

    try:
        service.create_paper(title="Duplicate", doi=" https://doi.org/10.1000/XYZ ")
    except ValueError as exc:
        assert str(exc) == "Paper with DOI already exists"
    else:
        raise AssertionError("Expected duplicate DOI error")


def test_update_paper_normalizes_doi_before_persist() -> None:
    repository = PaperRepository()
    service = PaperService(repository)

    created = service.create_paper(title="A Paper", doi=None)
    updated = service.update_paper(
        paper_id=created.id,
        title="A Paper Revised",
        doi="  DOI:10.1000/ABC  ",
    )

    assert updated.doi == "10.1000/abc"
    fetched = repository.get_by_doi("https://doi.org/10.1000/abc")
    assert fetched is not None
    assert fetched.id == created.id
