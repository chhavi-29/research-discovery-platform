import httpx
from fastapi import HTTPException

from app.core.config import settings

PAPER_FIELDS = (
    "paperId,title,abstract,year,authors,citationCount,referenceCount,"
    "isOpenAccess,openAccessPdf,url,venue,publicationTypes"
)


def _headers() -> dict:
    headers = {}
    if settings.SEMANTIC_SCHOLAR_API_KEY:
        headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
    return headers


async def search_papers(query: str, limit: int = 10, offset: int = 0) -> dict:
    url = f"{settings.SEMANTIC_SCHOLAR_BASE_URL}/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "fields": PAPER_FIELDS,
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(url, params=params, headers=_headers())
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Could not reach Semantic Scholar: {exc}",
            )

    if response.status_code == 429:
        raise HTTPException(
            status_code=429,
            detail="Semantic Scholar rate limit hit. Try again shortly, "
                   "or add an API key to increase your limit.",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Semantic Scholar error: {response.text}",
        )

    return response.json()