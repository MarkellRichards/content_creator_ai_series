from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.content.schemas.workflow import Workflow, WorkflowCreate, WorkflowUpdate, WorkflowList
from src.content.models.workflows import Workflow as DatabaseWorkflow
from src.content.models.blog_posts import BlogPosts
from src.content.models.social_media_post import SocialMediaPosts
from src.content.repositories.workflow.workflow_repository_interface import IWorklflowRepository
from sqlalchemy import func, desc, asc
from sqlalchemy.orm import joinedload
from typing import Optional
from fastapi import HTTPException, status
from src.core.logs import logger

class WorkflowRepository(IWorklflowRepository):
    def __init__(self, async_db_session: AsyncSession):
        self.db = async_db_session

    async def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        if not isinstance(workflow_data, WorkflowCreate):
            raise ValueError("Expected a WorkflowCreate instance")
        try: 
            new_workflow = DatabaseWorkflow(status=workflow_data.status)
            self.db.add(new_workflow)
            await self.db.commit()
            await self.db.refresh(new_workflow)
            return Workflow(
                id=new_workflow.id,
                guid=new_workflow.guid,
                status=new_workflow.status,
                created_at=new_workflow.created_at,
                updated_at=new_workflow.updated_at
            )
        except:
            await self.db.rollback()
            raise

    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Workflow:
        try:
            query = select(DatabaseWorkflow).where(DatabaseWorkflow.id == workflow_id)
            result = await self.db.execute(query)
            workflow = result.scalars().first()

            if workflow is None:
                raise HTTPException(status_code=404, detail="Workflow not found")

            for key, value in workflow_data.model_dump().items():
                setattr(workflow, key, value)

            await self.db.commit()
            await self.db.refresh(workflow)
            return workflow
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error") 

    async def get_workflow_details(self, workflow_guid: str) -> dict:
        try:
            query = (
                select(DatabaseWorkflow)
                .options(
                    joinedload(DatabaseWorkflow.blog_posts).joinedload(BlogPosts.image),
                    joinedload(DatabaseWorkflow.social_media_posts).joinedload(SocialMediaPosts.image)
                )
                .where(DatabaseWorkflow.guid == workflow_guid)
            )
            result = await self.db.execute(query)
            workflow = result.scalars().first()

            if not workflow:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="workflow not found")

            blog_posts_data = [
                {
                    "id": post.id,
                    "guid": post.guid,
                    "title": post.title,
                    "content": post.content,
                    "created_at": post.created_at,
                    "image_url": post.image.url if post.image else None
                }
                for post in workflow.blog_posts
            ]

            social_media_posts_data = [
                {
                    "id": post.id,
                    "guid": post.guid,
                    "content": post.content,
                    "platform_type": post.platform_type.value,
                    "created_at": post.created_at,
                    "image_url": post.image.url if post.image else None
                }
                for post in workflow.social_media_posts
            ]

            return {
                "workflow": {
                    "id": workflow.id,
                    "guid": workflow.guid,
                    "status": workflow.status.value,
                    "created_at": workflow.created_at,
                },
                "blog_posts": blog_posts_data,
                "social_media_posts": social_media_posts_data,
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    
    async def get_workflows(self, offset, limit, filter_criteria: Optional[dict] = None, sort_field: Optional[str] = None, sort_order: Optional[str] = 'desc') -> WorkflowList:
        try: 
            
            base_query = select(DatabaseWorkflow)

            if filter_criteria:
                for key, value in filter_criteria.items():
                    base_query = base_query.where(getattr(DatabaseWorkflow, key) == value)
                    
            if sort_field:
                sort_column = getattr(DatabaseWorkflow, sort_field)
                if sort_order == "desc":
                    base_query = base_query.order_by(desc(sort_column))
                else:
                    base_query = base_query.order_by(asc(sort_column))

            total_result = await self.db.execute(select(func.count()).select_from(base_query.subquery()))
            total = total_result.scalar_one()

            result = await self.db.scalars(base_query.offset(offset).limit(limit))
            workflows = result.all()
            return {
                "total": total,
                "workflows": [Workflow.model_validate(wf) for wf in workflows]
            }
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        