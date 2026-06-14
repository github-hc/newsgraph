"""
Test: end-to-end web crawl → markdown cleaning → chunking pipeline.

Run from the project root:
    uv run python -m tests.test_web_crawl
    uv run python -m tests.test_web_crawl --url https://example.com

Output is saved to tests/output/chunks_<domain>.txt
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path
from urllib.parse import urlparse

# Ensure src is importable when running as a module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.tools.web_crawl_tool import web_crawl

OUTPUT_DIR = Path(__file__).parent / "output"
DEFAULT_URL = "https://en.wikipedia.org/wiki/Shark_Tank_India"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test the web_crawl → chunk pipeline.")
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"URL to crawl (default: {DEFAULT_URL})",
    )
    return parser.parse_args()


async def run(url: str) -> None:
    print(f"Crawling: {url}")
    raw_result = await web_crawl(url)

    # web_crawl returns a JSON string of chunks
    chunks: list[dict] = json.loads(raw_result)
    print(f"Total chunks produced: {len(chunks)}")

    # Build output path
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    domain = urlparse(url).netloc.replace("www.", "").replace(".", "_")
    out_path = OUTPUT_DIR / f"chunks_{domain}.txt"

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Total chunks: {len(chunks)}\n")
        f.write("=" * 70 + "\n\n")

        for chunk in chunks:
            f.write(chunk["text_to_embed"])
            f.write(f"\nMetadata: {json.dumps(chunk['metadata'])}\n")
            f.write("-" * 70 + "\n\n")

    print(f"Output saved to: {out_path}")


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run(args.url))
