import boto3
from fastapi import APIRouter, WebSocket, Depends, HTTPException, WebSocketDisconnect
from sqlalchemy.orm import Session
from src.core.logs import logger
from src.core.database import get_db
from src.content.workflows.advanced_workflow import AdvancedWorkflow
from src.settings.config import get_settings, Settings
from llama_index.core.workflow.handler import WorkflowHandler
from src.content.workflows.advanced_workflow import ProgressEvent

from src.content.repositories.workflow.workflow_repository import WorkflowRepository
from src.content.services.workflow_service import WorkflowService
from src.content.repositories.blogs.blog_repository import BlogRepository
from src.content.services.blog_service import BlogService
from src.content.repositories.social_media.social_media_repository import SocialMediaRepository
from src.content.services.social_media_service import SocialMediaService
from src.content.repositories.images.images_repository import ImageRepository
from src.content.services.image_service import ImageService
import time

from src.content.schemas.workflow import WorkflowQuery

router = APIRouter(tags=["Content Endpoints"])

def get_workflow_service(db: Session = Depends(get_db)):
    repository = WorkflowRepository(db)
    return WorkflowService(repository)

def get_blog_service(db: Session = Depends(get_db)):
    repository = BlogRepository(db)
    return BlogService(repository)

def get_social_media_Service(db: Session = Depends(get_db)):
    repository = SocialMediaRepository(db)
    return SocialMediaService(repository)

@router.get("/social_media_posts")
async def fetchSocialMediaPosts(offset: int = 0, limit: int = 10, service: SocialMediaService = Depends(get_social_media_Service)):
    try:
        return await service.get_all_social_media_posts(offset=offset, limit=limit)
    except Exception as e:
        raise Exception(f"{e}")
    
@router.get("/social_media_post")
async def fetchSocialMediaPost(sm_guid, service: SocialMediaService = Depends(get_social_media_Service)):
    try:
        return await service.get_social_media_post(social_media_guid=sm_guid)
    except Exception as e:
        raise Exception(f"{e}")

@router.post("/workflows")
async def fetchWorkflows(query: WorkflowQuery, service: WorkflowService = Depends(get_workflow_service)):
    try:
        return await service.get_workflows(query.offset, query.limit, query.filter_criteria, query.sort_field, query.sort_order)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/workflow")
async def fetchWorkflow(workflow_guid: str, service: WorkflowService = Depends(get_workflow_service)):
    try:
        return await service.get_workflow_details(workflow_guid)
    except Exception as e:
        raise Exception(f"{e}")
    
@router.get("/blogs")
async def fetchBlogs(offset: int = 0, limit: int = 10, service: BlogService = Depends(get_blog_service)):
    try:
        return await service.get_blogs(offset, limit)
    except Exception as e:
        raise Exception(f"{e}")
    
@router.get("/blog")
async def fetchBlog(blog_guid: str, service: BlogService = Depends(get_blog_service)):
    try:
        return await service.get_blog_details(blog_guid)
    except Exception as e:
        raise Exception(f"{e}")
    
@router.websocket("/content")
async def advancedContentFlow(websocket: WebSocket, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    await websocket.accept()
    
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.MINIO_ENDPOINT,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1',
        # Disable SSL verification if using HTTP
        config=boto3.session.Config(signature_version='s3v4')
    )
    
    workflow_repository = WorkflowRepository(db)
    blog_repository = BlogRepository(db)
    social_media_repository = SocialMediaRepository(db)
    image_repository = ImageRepository(db)
    
    
    workfow_service = WorkflowService(workflow_repository)
    blog_service = BlogService(blog_repository)
    social_media_service = SocialMediaService(social_media_repository)
    image_service = ImageService(image_repository=image_repository, s3_client=s3_client)
    
    workflow = AdvancedWorkflow(settings, db, workfow_service=workfow_service, blog_service=blog_service, 
                                social_media_service=social_media_service, image_service=image_service)
    try:
        data = await websocket.receive_json() 
        logger.info(data)
        handler: WorkflowHandler = workflow.run(topic=data["topic"], research=data["research"])
        
        async for event in handler.stream_events():
            if isinstance(event, ProgressEvent):
                await websocket.send_json({
                    "type": "progress_event",
                    "payload": str(event.msg)
                })
        
        result = await handler        
        await websocket.send_json({
            "type": "results",
            "payload": str(result)
        })
        await websocket.close()
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed by the client")
    except Exception as e: 
        await db.rollback()
        await websocket.send_json({
            "type": "error",
            "payload": "Something went wrong"
        }) 
        logger.error(e)
        await websocket.close()