"""DOI normalization helpers."""


DOI_PREFIXES = (
    "doi:",
    "https://doi.org/",
)


def normalize_doi(doi: str | None) -> str | None:
    """Normalize DOI values for canonical lookups and persistence."""
    if doi is None:
        return None

    normalized = doi.strip().lower()
    for prefix in DOI_PREFIXES:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):].strip()
            break

    return normalized
