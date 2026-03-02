from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    is_stub: bool = Column(Boolean, nullable=False, default=False, server_default="0")
