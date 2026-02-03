"""SQLite database for caching movie title -> link mappings."""

import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parent / "movies.db"
BASE_URL = "https://moviesda16.com"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                title TEXT PRIMARY KEY,
                href TEXT NOT NULL,
                full_url TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_movies_title_lower ON movies(LOWER(title))"
        )


def upsert_movies(entries: list[tuple[str, str]]) -> int:
    """Insert or replace movies. Each entry is (title, href). Returns count inserted."""
    if not entries:
        return 0
    count = 0
    with get_connection() as conn:
        for title, href in entries:
            full_url = (
                href
                if href.startswith("http")
                else f"{BASE_URL.rstrip('/')}{href}"
                if href.startswith("/")
                else f"{BASE_URL}/{href}"
            )
            conn.execute(
                """
                INSERT OR REPLACE INTO movies (title, href, full_url)
                VALUES (?, ?, ?)
                """,
                (title.strip(), href.strip(), full_url),
            )
            count += 1
        conn.commit()
    return count


def search_by_name(query: str, limit: int = 10) -> list[dict]:
    """Search movies by name (case-insensitive partial match)."""
    init_db()
    pattern = f"%{query.strip().lower()}%"
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT title, href, full_url
            FROM movies
            WHERE LOWER(title) LIKE ?
            ORDER BY title
            LIMIT ?
            """,
            (pattern, limit),
        ).fetchall()
    return [dict(r) for r in rows]


def count_movies() -> int:
    with get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
