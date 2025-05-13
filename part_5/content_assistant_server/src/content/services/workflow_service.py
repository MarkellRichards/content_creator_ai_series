from src.content.repositories.workflow.workflow_repository import WorkflowRepository
from src.content.schemas.workflow import WorkflowCreate, WorkflowUpdate, Workflow
from typing import Optional

class WorkflowService:
    def __init__(self, repository: WorkflowRepository):
        self.repository = repository

    async def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        workflow = await self.repository.create_workflow(workflow_data)
        return Workflow.model_validate(workflow)

    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Workflow:
        workflow = await self.repository.update_workflow(workflow_id, workflow_data)
        return Workflow.model_validate(workflow)
    
    async def get_workflow_details(self, workflow_guid: str) -> Workflow:
        return await self.repository.get_workflow_details(workflow_guid)

    async def get_workflows(self, offset: int, limit: int, filter_criteria: Optional[dict], sort_field: Optional[str], sort_order: Optional[str]) -> list[Workflow]:
        return await self.repository.get_workflows(offset, limit, filter_criteria, sort_field, sort_order)
    
         