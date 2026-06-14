import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

async def web_crawl(url: str) -> str:
    """
    Crawl and extract content from a web page.

    Use this tool when the user wants to:
    - Retrieve content from a website
    - Analyze a webpage
    - Extract information from a URL
    - Summarize a webpage
    - Search within a specific webpage

    Do not use this tool when:
    - The user is asking a general knowledge question
    - No URL is provided or implied
    - The information is already available in the conversation

    Args:
        url:
            The URL of the webpage to crawl.

    Returns:
        Extracted webpage content as text.
    """
    # Step 1: Create a pruning filter
    prune_filter = PruningContentFilter(
        # Lower → more content retained, higher → more content pruned
        threshold=0.45,           
        # "fixed" or "dynamic"
        threshold_type="dynamic",  
        # Ignore nodes with <5 words
        min_word_threshold=5      
    )

    # Step 2: Insert it into a Markdown Generator
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

    # Step 3: Pass it to CrawlerRunConfig
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url, 
            config=config
        )

        if result.success:
            # 'fit_markdown' is your pruned content, focusing on "denser" text
            print("Raw Markdown length:", len(result.markdown.raw_markdown))
            print("Fit Markdown length:", len(result.markdown.fit_markdown))
            return result.markdown.fit_markdown
        else:
            print("Error:", result.error_message)
            return result.error_message