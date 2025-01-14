from langchain_community.tools.tavily_search import TavilySearchResults # Search API optimized for LLMs

def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res