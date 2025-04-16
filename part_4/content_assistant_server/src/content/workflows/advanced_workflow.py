from llama_index.core.workflow import Workflow, Event, StartEvent, StopEvent, Context, step
from sqlalchemy.orm import Session
from src.content.services.workflow_service import WorkflowService
from src.content.services.blog_service import BlogService
from src.content.services.social_media_service import SocialMediaService
from src.content.services.image_service import ImageService
from src.content.schemas.workflow import WorkflowStatusType, WorkflowCreate, WorkflowUpdate
from src.content.schemas.blog_posts import BlogCreate, BlogUpdate
from src.content.schemas.social_media_post import SocialMediaCreate, PlatformType, SocialMediaUpdate
from src.content.schemas.tavily_search import TavilySearchInput
from src.content.schemas.images import ImageCreate
from src.content.prompts.prompts import *
from src.content.services.tavily_search_service import tavily_search
from llama_index.llms.openai import OpenAI as LlamaOpenAI
from openai import OpenAI
from src.core.logs import logger

class ResearchEvent(Event):
    topic: str
    research: bool

class BlogEvent(Event):
    topic: str
    research: bool
    research_material: str

class SocialMediaEvent(Event):
    blog: str

class SocialMediaCompleteEvent(Event):
   pass

class IllustratorEvent(Event):
    blog: str

class IllustratorCompleteEvent(Event):
    url: str

class ProgressEvent(Event):
    msg: str

class RetryEvent(Event):
    pass

class WorkflowFailedEvent(Event):
    error: str
class AdvancedWorkflow(Workflow):
    
    def __init__(self, settings, db: Session, workfow_service: WorkflowService, blog_service: BlogService, social_media_service: SocialMediaService, image_service: ImageService, timeout=None, verbose=None):
        super().__init__(timeout, verbose)
        self.settings = settings
        self.db = db
        self.workflow_service = workfow_service
        self.blog_service = blog_service
        self.social_media_service = social_media_service
        self.image_service = image_service
        
    @step
    async def start_event(self, ev: StartEvent, ctx: Context) -> ResearchEvent | BlogEvent | WorkflowFailedEvent:
        ctx.write_event_to_stream(ProgressEvent(msg="Starting content creation workflow"))
        workflow_data = WorkflowCreate(status=WorkflowStatusType.INPROGRESS)
        try: 
            workflow = await self.workflow_service.create_workflow(workflow_data=workflow_data)
            await ctx.set(key="workflow_id", value=workflow.id)
            await ctx.set(key="workflow_guid", value=workflow.guid)
            if ev.research:
                return ResearchEvent(topic=ev.topic, research=ev.research)
            return BlogEvent(topic=ev.topic, research=ev.research, research_material="None")
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")
        
    @step
    async def research_event(self, ev: ResearchEvent, ctx: Context) -> BlogEvent | WorkflowFailedEvent:
        ctx.write_event_to_stream(ProgressEvent(msg=f"Searching internet for information about {ev.topic}"))
        try:
            search_input = TavilySearchInput(
                query=ev.topic,
                max_results=3,
                search_depth="basic"
            )
            research_material = await tavily_search(search_input, api_key=self.settings.TAVILY_SEARCH_API_KEY)
            return BlogEvent(topic=ev.topic, research= ev.research, research_material=research_material)
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")
    
    @step
    async def blog_event(self, ev: BlogEvent, ctx: Context) -> SocialMediaEvent | WorkflowFailedEvent:
        ctx.write_event_to_stream(ProgressEvent(msg="Writing blog post"))
        prompt_template = ""
        workflow_guid = await ctx.get("workflow_guid")
        try:
            if(ev.research):
                prompt_template = BLOG_AND_RESEARCH_TEMPLATE.format(query_str=ev.topic, research=ev.research_material)
            else:
                prompt_template = BLOG_TEMPLATE.format(query_str=ev.topic)
            llm = LlamaOpenAI(model=self.settings.OPENAI_MODEL, api_key=self.settings.OPENAI_API_KEY)
            response = await llm.acomplete(prompt_template)
            blog_data = BlogCreate(title=ev.topic, content=response.text, workflow_guid=workflow_guid)
            blog_post = await self.blog_service.create_blog(blog_data=blog_data)
            await ctx.set(key="blog_id", value=blog_post.id)
            ctx.send_event(SocialMediaEvent(blog=blog_data.content))
    
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")
        
    @step
    async def social_media_event(self, ev: SocialMediaEvent, ctx: Context) -> SocialMediaCompleteEvent | IllustratorEvent | WorkflowFailedEvent:
        ctx.write_event_to_stream(ProgressEvent(msg="Writing social media post"))
        worklflow_guid = await ctx.get("workflow_guid")
        try:
            prompt_template = LINKED_IN_TEMPLATE.format(blog_content=ev.blog)
            llm = LlamaOpenAI(model=self.settings.OPENAI_MODEL, api_key=self.settings.OPENAI_API_KEY)
            response = await llm.acomplete(prompt_template)
            sm_data = SocialMediaCreate(content=response.text, platform_type=PlatformType.LINKEDIN, workflow_guid=worklflow_guid)
            sm_post = await self.social_media_service.create_social_media_post(social_media_data=sm_data)
            await ctx.set(key="sm_id", value=sm_post.id)
            ctx.send_event(IllustratorEvent(blog=ev.blog))
            return SocialMediaCompleteEvent()
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")
    
    @step
    async def illustration_event(self, ev: IllustratorEvent, ctx: Context) -> IllustratorCompleteEvent | WorkflowFailedEvent:
        ctx.write_event_to_stream(ProgressEvent(msg="Drawing illustration for content"))
        try:
            llm = LlamaOpenAI(model=self.settings.OPENAI_MODEL, api_key=self.settings.OPENAI_API_KEY)
            image_prompt_instructions_generator = IMAGE_GENERATION_TEMPLATE.format(blog_post=ev.blog)
            image_prompt = await llm.acomplete(image_prompt_instructions_generator, formatted=True)
            openai_client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
            file_name = await self.image_service.generate_and_upload_image(bucket=self.settings.MINIO_BUCKET_NAME, openai_client=openai_client, image_prompt=image_prompt.text)
            url = f"{self.settings.MINIO_ENDPOINT}/{self.settings.MINIO_BUCKET_NAME}/{file_name}"
            image_data = ImageCreate(url=url)
            image = await self.image_service.create_image(image_data=image_data)
            await ctx.set("image_guid", image.guid)
            return IllustratorCompleteEvent(url=url)
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")

    
    @step
    async def step_workflow_success(self, ev:SocialMediaCompleteEvent | IllustratorCompleteEvent, ctx: Context) -> StopEvent | WorkflowFailedEvent:
        if (
            ctx.collect_events(
                ev,
                [SocialMediaCompleteEvent, IllustratorCompleteEvent]
            ) is None
        ) : return None
        
        workflow_id = await ctx.get("workflow_id")
        workflow_guid = await ctx.get("workflow_guid")
        image_guid = await ctx.get("image_guid")
        blog_id = await ctx.get("blog_id")
        sm_id = await ctx.get("sm_id")
        workflow_update_data = WorkflowUpdate(id=workflow_id, status=WorkflowStatusType.COMPLETE)
        blog_update_data = BlogUpdate(id=blog_id, image_guid=image_guid)
        sm_update_data = SocialMediaUpdate(id=sm_id, image_guid=image_guid)
        
        try: 
            await self.workflow_service.update_workflow(workflow_id, workflow_update_data)
            await self.blog_service.update_blog(blog_id=blog_id, blog_data=blog_update_data)
            await self.social_media_service.update_social_media_post(sm_id=sm_id, sm_data=sm_update_data)
            return StopEvent(result=workflow_guid)
        except Exception as e:
            return WorkflowFailedEvent(error=f"{e}")

    @step
    async def step_workflow_failed(self, ev: WorkflowFailedEvent, ctx: Context) -> StopEvent:
        try:
            workflow_id = await ctx.get("workflow_id")
            workflow_update_data = WorkflowUpdate(id=workflow_id, status=WorkflowStatusType.FAILED)
            await self.workflow_service.update_workflow(workflow_id, workflow_update_data)
            logger.error(ev.error)
            return StopEvent(result="Failed")
        except:
            logger.error(ev.error)
            return StopEvent(result="Failed")
