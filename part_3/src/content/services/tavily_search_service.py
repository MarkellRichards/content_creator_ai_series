from tavily import TavilyClient
from typing import Annotated
from src.content.schemas.tavily_search import TavilySearchInput

async def tavily_search(query: Annotated[TavilySearchInput, "Input for Tavily search"], api_key):
    tavily_client = TavilyClient(api_key=api_key)
    response = tavily_client.search(
        query=query.query,
        max_results=query.max_results,
        search_depth=query.search_depth,
    )

    formatted_results = []
    for result in response.get("results", []):
        formatted_results.append(
            f"Title: {result['title']}\\nURL: {result['url']}\\nContent: {result['content']}\\n"
        )

    return "\\n".join(formatted_results)