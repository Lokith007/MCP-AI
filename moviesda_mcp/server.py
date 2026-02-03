"""MCP server for searching Tamil 2025 movies and returning movie links."""

import json
from mcp.server import Server

from db import count_movies, init_db, search_by_name, upsert_movies
from scraper import scrape_all_pages

server = Server("moviesda")


@server.method()
async def search_movie(movie_name: str, refresh_cache: bool = False) -> str:
    """
    Search for a Tamil 2025 movie by name and return matching movie links.
    """
    init_db()

    if refresh_cache or count_movies() == 0:
        try:
            entries = scrape_all_pages()
            upsert_movies(entries)
        except Exception as e:
            return json.dumps({
                "error": "Failed to refresh cache from site",
                "detail": str(e),
                "matches": []
            })

    matches = search_by_name(movie_name, limit=15)
    return json.dumps([
        {"title": m["title"], "full_url": m["full_url"]}
        for m in matches
    ])


if __name__ == "__main__":
    server.run()
