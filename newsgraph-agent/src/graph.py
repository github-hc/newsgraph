from langgraph.graph import StateGraph, START, END

from state import NewsletterState
from nodes import crawl_node, research_node, writer_node


builder = StateGraph(NewsletterState)

builder.add_node("crawl", crawl_node)
builder.add_node("research", research_node)
builder.add_node("writer", writer_node)

builder.add_edge(START, "crawl")
builder.add_edge("crawl", "research")
builder.add_edge("research", "writer")
builder.add_edge("writer", END)

graph = builder.compile()