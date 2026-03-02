from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.paper import PaperStatus


class PaperCreate(BaseModel):
    doi: str | None = None
    title: str | None = None
    year: int | None = None
    venue: str | None = None
    abstract: str | None = None
    url: str | None = None
    pdf_path: str | None = None
    status: PaperStatus = PaperStatus.TO_READ


class PaperUpdate(BaseModel):
    title: str | None = None
    year: int | None = None
    venue: str | None = None
    abstract: str | None = None
    url: str | None = None
    pdf_path: str | None = None
    status: PaperStatus | None = None


class PaperRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    doi: str | None
    title: str
    year: int | None
    venue: str | None
    abstract: str | None
    url: str | None
    pdf_path: str | None
    status: str
    is_stub: int
    added_at: datetime
    updated_at: datetime


class PaperListResponse(BaseModel):
    items: list[PaperRead]
    total: int


class PaperQueryParams(BaseModel):
    search: str | None = None
    status: PaperStatus | None = None
    year_from: int | None = Field(default=None, ge=0)
    year_to: int | None = Field(default=None, ge=0)
    sort_by: str = "added_at"
    sort_dir: str = "desc"
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
