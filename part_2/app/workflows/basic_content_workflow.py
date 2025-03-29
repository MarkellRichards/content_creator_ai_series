from llama_index.core.workflow import Event, Workflow, step, StartEvent, Context, StopEvent
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI
import os
import uuid
from app.utils.utils import TavilySearchInput, tavily_search, save_file, generate_image_with_retries
from app.prompts.prompts import *
from PIL import Image
import requests
from io import BytesIO
from app.config.settings import Settings

class ResearchEvent(Event):
    query: str

class BlogEvent(Event):
    query: str
    research: str

class BlogWithoutResearchEvent(Event):
    query: str

class SocialMediaEvent(Event):
    blog: str

class SocialMediaCompleteEvent(Event):
    result: str

class IllustratorEvent(Event):
    blog: str

class IllustratorCompleteEvent(Event):
    result: str
    
blog_template = BLOG_TEMPLATE
blog_and_research_template = BLOG_AND_RESEARCH_TEMPLATE
image_prompt_instructions = IMAGE_GENERATION_TEMPLATE
linked_in_template = LINKED_IN_TEMPLATE


class ContentCreationWorkflow(Workflow):
    
    def __init__(self, settings, timeout=None, verbose=False):
        super().__init__(timeout, verbose)
        self.settings = settings
    
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> ResearchEvent | BlogWithoutResearchEvent:
        print("Starting content creation", ev.query)
        id = str(uuid.uuid4())
        if (ev.research) is False:
            return BlogWithoutResearchEvent(query=ev.query, uuid=id)
        return ResearchEvent(query=ev.query, uuid=id)

    @step
    async def step_research(self, ctx: Context, ev: ResearchEvent) -> BlogEvent:
        print("Researching users query")
        search_input = TavilySearchInput(
            query=ev.query,
            max_results=3,
            search_depth="basic")
        research = tavily_search(search_input, api_key=self.settings.TAVILY_SEARCH_API_KEY)
        return BlogEvent(query=ev.query, research=research, uuid=ev.uuid)

    @step
    async def step_blog_without_research(self, ctx: Context, ev: BlogWithoutResearchEvent) -> SocialMediaEvent | IllustratorEvent:
        print("Writing blog post without research")
        print("uuid", ev.uuid)
        llm = LlamaOpenAI(model="gpt-4o-mini", api_key=self.settings.OPENAI_API_KEY)
        prompt = blog_template.format(query_str=ev.query)
        result = await llm.acomplete(prompt, formatted=True)
        save_file(result.text, ev.uuid)
        print(result)
        ctx.send_event(SocialMediaEvent(blog=result.text, uuid=ev.uuid))
        ctx.send_event(IllustratorEvent(blog=result.text, uuid=ev.uuid))
                        
    @step
    async def step_blog(self, ctx: Context, ev: BlogEvent) -> SocialMediaEvent | IllustratorEvent:
        print("Writing blog post")

        llm = LlamaOpenAI(model="gpt-4o-mini", api_key=self.settings.OPENAI_API_KEY)
        prompt = blog_and_research_template.format(query_str=ev.query, research=ev.research)
        result = await llm.acomplete(prompt, formatted=True)

        save_file(result.text, ev.uuid)
        ctx.send_event(SocialMediaEvent(blog=result.text, uuid=ev.uuid))
        ctx.send_event(IllustratorEvent(blog=result.text, uuid=ev.uuid))

    @step
    async def step_social_media(self, ctx: Context, ev: SocialMediaEvent) -> SocialMediaCompleteEvent:
        print("Writing social media post")
        llm = LlamaOpenAI(model="gpt-4o-mini", api_key=self.settings.OPENAI_API_KEY)
        prompt = linked_in_template.format(blog_content=ev.blog)
        results = await llm.acomplete(prompt, formatted=True)
        save_file(results.text, ev.uuid, type="LinkedIn")
        return SocialMediaCompleteEvent(result="LinkedIn post written")

    @step
    async def step_illustrator(self, ctx: Context, ev:IllustratorEvent) -> IllustratorCompleteEvent:
        print("Generating image")
        llm = LlamaOpenAI(model="gpt-4o-mini", api_key=self.settings.OPENAI_API_KEY)
        image_prompt_instruction_generator = image_prompt_instructions.format(blog_post=ev.blog)
        image_prompt = await llm.acomplete(image_prompt_instruction_generator, formatted=True)
        
        client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        response = await generate_image_with_retries(client, image_prompt.text)
        image_url = response.data[0].url
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        directory = f'./posts/{ev.uuid}'
        os.makedirs(directory, exist_ok=True)
        image.save(f'{directory}/generated_image.png')
        
        return IllustratorCompleteEvent(result="Images drawn")

    @step
    async def step_collection(self, ctx: Context, ev: SocialMediaCompleteEvent | IllustratorCompleteEvent) -> StopEvent:
        if (
            ctx.collect_events(
                ev,
                [SocialMediaCompleteEvent, IllustratorCompleteEvent]
            ) is None
        ) : return None
        return StopEvent(result="Done")