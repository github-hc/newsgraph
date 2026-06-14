"""
Utility for cleaning and chunking raw markdown produced by web crawls.

Uses the `unstructured` library to:
- Strip common footer/reference noise
- Fix whitespace and broken paragraphs
- Partition the document into semantic elements
- Chunk elements for downstream embedding / RAG pipelines
"""

import re
from unstructured.partition.md import partition_md
from unstructured.chunking.title import chunk_by_title
from unstructured.cleaners.core import clean_extra_whitespace, group_broken_paragraphs


# Markers that typically signal the start of low-value boilerplate
_NOISE_MARKERS = [
    "\n  1. [\"",
    "\nReferences\n",
    "\n## References",
    "\n## See also",
    "\n## External links",
]


def clean_markdown(raw_markdown: str) -> str:
    """
    Strip trailing noise sections and fix whitespace/paragraph issues.

    Args:
        raw_markdown: Raw markdown string from a web crawl.

    Returns:
        Cleaned markdown string.
    """
    for marker in _NOISE_MARKERS:
        if marker in raw_markdown:
            raw_markdown = raw_markdown.split(marker)[0]

    cleaned = clean_extra_whitespace(raw_markdown)
    cleaned = group_broken_paragraphs(cleaned)
    return cleaned


def chunk_markdown(
    raw_markdown: str,
    source_url: str = "",
    combine_under_n_chars: int = 250,
    max_characters: int = 1200,
    new_after_n_chars: int = 1000,
) -> list[dict]:
    """
    Clean, partition, and chunk a raw markdown string into embed-ready dicts.

    Args:
        raw_markdown:        Raw markdown content from a web crawl.
        source_url:          The originating URL, stored in chunk metadata.
        combine_under_n_chars: Merge short consecutive elements to preserve meaning.
        max_characters:      Hard cap on chunk size (~300-400 tokens at 3 chars/token).
        new_after_n_chars:   Soft target boundary before starting a new chunk.

    Returns:
        List of dicts with keys ``text_to_embed`` and ``metadata``.
    """
    cleaned = clean_markdown(raw_markdown)

    elements = partition_md(text=cleaned)

    chunks = chunk_by_title(
        elements,
        combine_text_under_n_chars=combine_under_n_chars,
        max_characters=max_characters,
        new_after_n_chars=new_after_n_chars,
    )

    processed: list[dict] = []

    for index, chunk in enumerate(chunks):
        text = chunk.text

        # Drop bare markdown table fragments with no real content
        if text.startswith("|") and "---" in text:
            continue

        enriched = (
            f"Source: {source_url}\n"
            f"Section: {index + 1}\n"
            f"Content: {text}"
        )

        processed.append({
            "text_to_embed": enriched,
            "metadata": {
                "source": source_url,
                "chunk_id": index,
                "element_type": chunk.category,
            },
        })

    return processed
