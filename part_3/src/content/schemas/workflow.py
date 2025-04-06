from pydantic import BaseModel, Field
import uuid
from enum import Enum

class WorkflowStatusType(str, Enum):
    INPROGRESS = "INPROGRESS"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class WorkflowCreate(BaseModel):
    status: WorkflowStatusType

class WorkflowUpdate(BaseModel):
    id: int
    status: WorkflowStatusType

class Workflow(BaseModel):
    id: int
    guid: uuid.UUID
    status: WorkflowStatusType

    class Config:
        from_attributes = True