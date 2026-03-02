import httpx


class MetadataService:
    CROSSREF_URL = "https://api.crossref.org/works/"

    async def fetch_by_doi(self, doi: str) -> dict | None:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(f"{self.CROSSREF_URL}{doi}")
                resp.raise_for_status()
            data = resp.json().get("message", {})
            title = (data.get("title") or [None])[0]
            issued = data.get("issued", {}).get("date-parts", [[None]])[0][0]
            venue = (data.get("container-title") or [None])[0]
            abstract = data.get("abstract")
            url = data.get("URL")
            return {
                "doi": doi,
                "title": title,
                "year": issued,
                "venue": venue,
                "abstract": abstract,
                "url": url,
            }
        except Exception:
            return None
