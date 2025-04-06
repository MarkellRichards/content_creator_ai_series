from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.content.schemas.workflow import Workflow, WorkflowCreate, WorkflowUpdate
from src.content.models.workflows import Workflow as DatabaseWorkflow
from src.content.repositories.workflow.workflow_repository_interface import IWorklflowRepository

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
                status=new_workflow.status
            )
        except:
            await self.db.rollback()
            raise

    async def update_workflow(self, workflow_id: int, workflow_data: WorkflowUpdate) -> Workflow:
        query = select(DatabaseWorkflow).where(DatabaseWorkflow.id == workflow_id)
        result = await self.db.execute(query)
        workflow = result.scalars().first()

        if workflow is None:
            raise Exception("Workflow not found")

        for key, value in workflow_data.model_dump().items():
            setattr(workflow, key, value)

        await self.db.commit()
        await self.db.refresh(workflow)
        return workflow

    async def get_workflow(self, workflow_id: int) -> Workflow:
        query = select(DatabaseWorkflow).where(DatabaseWorkflow.id == workflow_id)
        result = await self.db.execute(query)
        workflow = result.scalars().first()

        if workflow is None:
            raise Exception("Workflow not found")

        return workflow