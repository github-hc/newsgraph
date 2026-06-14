import asyncio
import json

from mcp import ClientSession
from mcp.client.sse import sse_client

from state import NewsletterState
from llm import llm

MCP_SERVER_URL = "http://localhost:8000/sse"


# ---------------------------------------------------------------------------
# Crawl Node
# ---------------------------------------------------------------------------

def crawl_node(state: NewsletterState) -> dict:
    """
    Calls the web_crawl MCP tool for every URL in state["urls"].
    Aggregates all returned chunks into state["chunks"].
    """
    urls = state["urls"]
    all_chunks: list[dict] = []

    async def _crawl_all() -> list[dict]:
        async with sse_client(MCP_SERVER_URL) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                for url in urls:
                    print(f"[crawl_node] Crawling: {url}")
                    result = await session.call_tool("web_crawl", {"url": url})
                    # The tool returns a JSON string of chunk dicts
                    raw = result.content[0].text
                    chunks = json.loads(raw)
                    all_chunks.extend(chunks)
        return all_chunks

    chunks = asyncio.run(_crawl_all())
    print(f"[crawl_node] Total chunks: {len(chunks)}")
    return {"chunks": chunks}


# ---------------------------------------------------------------------------
# Research Node
# ---------------------------------------------------------------------------

def research_node(state: NewsletterState) -> dict:
    """
    Summarises the crawled chunks into a research brief.
    """
    topic = state["topic"]
    chunks = state["chunks"]

    # Build context from chunk text
    context = "\n\n".join(c["text_to_embed"] for c in chunks)

    prompt = f"""You are a research analyst. Based on the following web content, 
write a concise research summary about: {topic}

Give 5 key points grounded in the content below.

--- CONTENT ---
{context}
--- END CONTENT ---
"""

    response = llm.invoke(prompt)
    return {"research": response.content}


# ---------------------------------------------------------------------------
# Writer Node
# ---------------------------------------------------------------------------

def writer_node(state: NewsletterState) -> dict:
    """
    Turns the research summary into a polished newsletter.
    """
    topic = state["topic"]
    research = state["research"]

    prompt = f"""You are a newsletter writer. Write an engaging, well-structured 
newsletter about "{topic}" based on the research below.

Include: a hook opening, key insights, and a closing takeaway.

--- RESEARCH ---
{research}
--- END RESEARCH ---
"""

    response = llm.invoke(prompt)
    return {"newsletter": response.content}