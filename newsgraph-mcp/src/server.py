import sys
from mcp.server.fastmcp import FastMCP

from src.tools.web_crawl_tool import web_crawl

mcp = FastMCP(
    name="NewsGraph MCP",
    instructions="""
    This server provides tools for researching, collecting,
    processing, and generating newsletter content.

    The available tools help gather information from external
    sources that can later be transformed into newsletter-ready
    content.
    """
)

mcp.tool()(web_crawl)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", "8000"))
    mcp.settings.port = port

    print("=" * 50)
    print("🚀 NewsGraph MCP Server Starting...")
    print("=" * 50)
    print(f"Server Name: NewsGraph MCP")
    print(f"Available Tools: web_crawl")
    print(f"Status: Listening for SSE connections on http://localhost:{port}/sse")
    print("=" * 50)
    sys.stdout.flush()
    
    mcp.run(transport="sse")