from pydantic import BaseModel


class PaperBase(BaseModel):
    is_stub: bool = False


class PaperCreate(PaperBase):
    pass


class PaperUpdate(BaseModel):
    is_stub: bool | None = None


class PaperResponse(PaperBase):
    id: int

    class Config:
        orm_mode = True
