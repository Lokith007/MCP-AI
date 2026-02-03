"""Scrape movie list from the Tamil 2025 movies listing page."""

from typing import Generator

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://moviesda16.com"
LISTING_PATH = "/tamil-2025-movies/"
MAX_PAGES = 26  # from site: "Showing Page 1 of 26"
USER_AGENT = "MCP-Moviesda-Server/1.0 (compatible; Python)"


def _fetch_page(path: str, page: int | None = None) -> str:
    url = BASE_URL + path
    if page and page > 1:
        url += f"?page={page}"
    resp = httpx.get(
        url,
        follow_redirects=True,
        timeout=30.0,
        headers={"User-Agent": USER_AGENT},
    )
    resp.raise_for_status()
    return resp.text


def _parse_listing(html: str) -> Generator[tuple[str, str], None, None]:
    """Parse HTML and yield (title, href) for each movie in div.f > a."""
    soup = BeautifulSoup(html, "html.parser")
    for div in soup.select("div.f"):
        a = div.find("a", href=True)
        if not a:
            continue
        href = (a.get("href") or "").strip()
        title = (a.get_text() or "").strip()
        if not href or not title:
            continue
        if not href.startswith("/"):
            continue
        yield title, href


def scrape_all_pages(max_pages: int = MAX_PAGES) -> list[tuple[str, str]]:
    """Scrape listing pages and return list of (title, href)."""
    result: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for page in range(1, max_pages + 1):
        try:
            html = _fetch_page(LISTING_PATH, page if page > 1 else None)
            for title, href in _parse_listing(html):
                key = (title, href)
                if key not in seen:
                    seen.add(key)
                    result.append((title, href))
        except Exception:
            break
    return result
