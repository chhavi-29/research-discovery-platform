
from fastapi import APIRouter, Query

from app.services import semantic_scholar
from app.schemas.paper import PaperSearchResponse, PaperCard, Author

router = APIRouter(prefix="/papers", tags=["papers"])


def _map_raw_paper_to_card(raw: dict) -> PaperCard:
    open_access_pdf = raw.get("openAccessPdf") or {}
    authors = [
        Author(name=a.get("name", "Unknown"), authorId=a.get("authorId"))
        for a in (raw.get("authors") or [])
    ]

    return PaperCard(
        paperId=raw.get("paperId"),
        title=raw.get("title") or "Untitled",
        abstract=raw.get("abstract"),
        year=raw.get("year"),
        authors=authors,
        citationCount=raw.get("citationCount") or 0,
        referenceCount=raw.get("referenceCount") or 0,
        isOpenAccess=raw.get("isOpenAccess") or False,
        openAccessPdfUrl=open_access_pdf.get("url"),
        url=raw.get("url"),
        venue=raw.get("venue"),
        publicationTypes=raw.get("publicationTypes") or [],
    )


@router.get("/search", response_model=PaperSearchResponse)
async def search_papers(
    query: str = Query(..., min_length=2, description="Research topic or keywords"),
    limit: int = Query(10, ge=1, le=100, description="Results per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
):
    raw_data = await semantic_scholar.search_papers(query=query, limit=limit, offset=offset)

    papers = [_map_raw_paper_to_card(p) for p in raw_data.get("data", [])]

    return PaperSearchResponse(
        query=query,
        total=raw_data.get("total", len(papers)),
        offset=offset,
        limit=limit,
        papers=papers,
    )