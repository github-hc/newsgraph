from typing import TypedDict


class NewsletterState(TypedDict):
    topic: str
    urls: list[str]      # URLs to crawl, supplied at invocation time
    chunks: list[dict]   # Raw chunks returned by the crawl node
    research: str
    newsletter: str