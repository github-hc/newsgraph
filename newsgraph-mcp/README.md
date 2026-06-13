# NewsGraph MCP Server

A Model Context Protocol (MCP) server that provides tools for researching, collecting, and processing content for the NewsGraph newsletter agent.

## Tools

*   `web_crawl`: Crawls and retrieves content from a specified URL.

## Development

The server runs on SSE (Server-Sent Events) HTTP transport by default.

### 1. Setup

Ensure you have `uv` installed, then install dependencies and download Playwright browsers:

```bash
uv sync
uv run crawl4ai-setup
```

> `crawl4ai-setup` downloads Chromium and sets up the crawl4ai database. Only needed once after install or Python version changes.

### 2. Start the Server

Start the server on the default port (`8000`):

```bash
uv run python -m src.server
```

To run on a custom port, set the `PORT` environment variable:

```bash
PORT=8080 uv run python -m src.server
```

### 3. Debug with MCP Inspector

1. Start the server (e.g., on port 8000).
2. In a separate terminal, launch the inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```
3. Open `http://localhost:6274` in your browser.
4. Set the **Transport Type** to `SSE` and connection URL to `http://localhost:8000/sse` (or `http://localhost:8000/mcp`), then click **Connect**.
