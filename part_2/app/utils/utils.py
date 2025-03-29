import os
import asyncio
from typing import Annotated
from pydantic import BaseModel, Field

class TavilySearchInput(BaseModel):
    query: Annotated[str, Field(description="The search query string")]
    max_results: Annotated[
        int, Field(description="Maximum number of results to return", ge=1, le=10)
    ] = 5
    search_depth: Annotated[
        str,
        Field(
            description="Search depth: 'basic' or 'advanced'",
            choices=["basic", "advanced"],
        ),
    ] = "basic"

def tavily_search(query: Annotated[TavilySearchInput, "Input for Tavily search"], api_key):
    tavily_client = TavilyClient(api_key=tavily_api_key)
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

def save_file(content, uuid, type="Blog"):
        directory = f'./posts/{uuid}'
        file_name = f"{type}_{uuid}.md"
        file_path = os.path.join(directory, file_name)
    
        try:
            os.makedirs(directory, exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(f"# {content}")
            print(f"{type} post saved to {file_path}.")
        except Exception as e:
            print("An error occurred while saving the blog post:", e)

async def generate_image_with_retries(client, prompt, max_retries=3, delay=2):
    attempt = 0
    while attempt < max_retries:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            return response
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                await asyncio.sleep(delay)
                print(f"Retrying after {delay} seconds...")
            else:
                print("Exceeded maximum retries.")
                raise