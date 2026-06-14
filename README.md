# NewsGraph

An agentic newsletter pipeline built with LangGraph and local LLMs. Give it a topic and a list of URLs — it crawls the pages, summarises the content, and writes a newsletter. No external API keys needed.

## How it works

```
START
  ↓
Crawl Node      — fetches each URL via the MCP web-crawl tool,
                  prunes noise, and returns semantic text chunks
  ↓
Research Node   — grounds an LLM summary in the crawled content
  ↓
Writer Node     — turns the summary into a newsletter draft
  ↓
END
```

The crawling runs as a separate MCP server (`newsgraph-mcp`) so it can be reused by other agents or inspected independently. The agent (`newsgraph-agent`) connects to it over SSE.

## Project layout

```
newsgraph/
├── newsgraph-mcp/        MCP server — web crawling + markdown chunking
│   └── src/
│       ├── server.py
│       ├── tools/
│       │   └── web_crawl_tool.py
│       └── utils/
│           └── markdown_cleaner.py
├── newsgraph-agent/      LangGraph agent
│   └── src/
│       ├── main.py       entry point — set your topic and URLs here
│       ├── graph.py
│       ├── nodes.py
│       ├── state.py
│       └── llm.py
└── start.sh              starts both services
```

## Requirements

- [uv](https://docs.astral.sh/uv/) — Python package manager
- [Ollama](https://ollama.com) running locally with `phi3:mini` pulled

```bash
ollama pull phi3:mini
```

## Setup

Each sub-project manages its own virtual environment. Run these once:

```bash
# MCP server
cd newsgraph-mcp
uv sync
uv run crawl4ai-setup   # downloads Playwright/Chromium, needed once

# Agent
cd ../newsgraph-agent
uv sync
```

## Running

From the project root:

```bash
./start.sh
```

This starts the MCP server in the background, waits for it to be ready, runs the agent, then shuts everything down when done. Server logs go to `mcp-server.log`.

To change the topic or URLs, edit `newsgraph-agent/src/main.py`:

```python
result = graph.invoke(
    {
        "topic": "Indian Startup Ecosystem",
        "urls": [
            "https://en.wikipedia.org/wiki/Startup_India",
            "https://en.wikipedia.org/wiki/Shark_Tank_India",
        ],
    }
)
```

To run on a different port:

```bash
PORT=9000 ./start.sh
```

## MCP server

The MCP server exposes one tool:

| Tool | Description |
|---|---|
| `web_crawl(url)` | Fetches a page, prunes noise with `crawl4ai`, and returns chunked markdown ready for embedding |

You can inspect it independently with [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
cd newsgraph-mcp
uv run python -m src.server   # terminal 1

npx @modelcontextprotocol/inspector   # terminal 2
```

Open `http://localhost:6274`, set transport to **SSE**, URL to `http://localhost:8000/sse`, and connect.

## Tech stack

| Component | Library |
|---|---|
| Agent graph | [LangGraph](https://github.com/langchain-ai/langgraph) |
| Local LLM | [Ollama](https://ollama.com) via `langchain-ollama` |
| Web crawling | [crawl4ai](https://github.com/unclecode/crawl4ai) |
| Markdown chunking | [unstructured](https://github.com/Unstructured-IO/unstructured) |
| MCP transport | [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) |
