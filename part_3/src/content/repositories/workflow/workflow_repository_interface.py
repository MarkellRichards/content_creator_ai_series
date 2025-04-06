from abc import ABC, abstractmethod
from src.content.schemas.workflow import Workflow, WorkflowCreate, WorkflowUpdate

class IWorklflowRepository(ABC):
    @abstractmethod
    async def create_workflow(self, workflow_data: WorkflowCreate) -> Workflow:
        pass

    @abstractmethod
    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Workflow:
        pass

    @abstractmethod
    async def get_workflow(self, workflow_id: int) -> Workflow:
        pass