# Moviesda MCP Server

Small MCP (Model Context Protocol) server that lets you search Tamil 2025 movies by name and get the movie page link. Uses SQLite to cache scraped listings.

## Setup

```bash
cd moviesda_mcp
pip install -r requirements.txt
```

## Run the server

**stdio (for Cursor / MCP clients):**

```bash
python server.py
``` 

Or with `uv`:

```bash
uv run server.py
```

## Cursor configuration

Add to `.cursor/mcp.json` (or Cursor MCP settings):

```json
{
  "mcpServers": {
    "moviesda": {
      "command": "python",
      "args": ["c:/Users/ASUS VIVOBOOK/Documents/projects and assg/mcp-demo/moviesda_mcp/server.py"],
      "cwd": "c:/Users/ASUS VIVOBOOK/Documents/projects and assg/mcp-demo/moviesda_mcp"
    }
  }
}
```

Use the path that matches your machine. On Windows use forward slashes or escaped backslashes.

**If you see `can't open file '...\server.py': No such file or directory`:** Cursor is running the command from the wrong directory. Either use the **full path to server.py** in `args` (as in the example above), or set `cwd` to the `moviesda_mcp` folder. A project-level config is in `mcp-demo/.cursor/mcp.json` when you open this repo.

## Tools

### `search_movie`

- **movie_name** (required): Full or partial movie name (e.g. `Mark`, `Sirai`, `Bank of Bhagyalakshmi`).
- **refresh_cache** (optional, default `false`): If `true`, re-scrapes the listing site and updates the SQLite cache before searching.

Returns a JSON array of `{ "title": "...", "full_url": "https://..." }`. On first use the DB is empty, so the server will automatically scrape the site and fill the cache before searching.

## Database

- SQLite file: `movies.db` in the same folder as `server.py`.
- Table: `movies` with columns `title`, `href`, `full_url`, `created_at`.
- Search is case-insensitive and supports partial match on title.

## Site structure

The server targets the Tamil 2025 movies listing: `div.f` items with `a[href]` for each movie. Pagination: `/tamil-2025-movies/?page=2`, etc. (up to 26 pages).
