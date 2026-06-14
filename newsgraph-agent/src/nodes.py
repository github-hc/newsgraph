from state import NewsletterState
from llm import llm

def research_node(state: NewsletterState):
    topic = state["topic"]

    prompt = f"""
    Create a research summary about:

    {topic}

    Give 5 key points.
    """

    response = llm.invoke(prompt)

    return {
        "research": response.content
    }


def writer_node(state: NewsletterState):
    research = state["research"]

    prompt = f"""
    Write a newsletter based on this research:

    {research}
    """

    response = llm.invoke(prompt)

    return {
        "newsletter": response.content
    }