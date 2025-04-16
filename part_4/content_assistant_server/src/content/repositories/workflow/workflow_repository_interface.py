from abc import ABC, abstractmethod
from src.content.schemas.workflow import Workflow, WorkflowCreate, WorkflowUpdate
from typing import Optional

class IWorklflowRepository(ABC):
    @abstractmethod
    async def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        pass

    @abstractmethod
    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Workflow:
        pass

    @abstractmethod
    async def get_workflow_details(self, workflow_id: int) -> Workflow:
        pass
    
    @abstractmethod
    async def get_workflows(self,offset, limit, filter_criteria: Optional[dict], sort_field: Optional[str], sort_order: Optional[str]) -> list[Workflow]:
        pass