from typing import Optional
from pydantic import BaseModel


class Author(BaseModel):
    name: str
    authorId: Optional[str] = None


class PaperCard(BaseModel):
    paperId: str
    title: str
    abstract: Optional[str] = None
    year: Optional[int] = None
    authors: list[Author] = []
    citationCount: Optional[int] = 0
    referenceCount: Optional[int] = 0
    isOpenAccess: Optional[bool] = False
    openAccessPdfUrl: Optional[str] = None
    url: Optional[str] = None
    venue: Optional[str] = None
    publicationTypes: list[str] = []


class PaperSearchResponse(BaseModel):
    query: str
    total: int
    offset: int
    limit: int
    papers: list[PaperCard]