from state import NewsletterState


def research_node(state: NewsletterState):
    topic = state["topic"]

    return {
        "research": f"Research completed for {topic}"
    }


def writer_node(state: NewsletterState):
    research = state["research"]

    return {
        "newsletter": f"Newsletter generated from: {research}"
    }