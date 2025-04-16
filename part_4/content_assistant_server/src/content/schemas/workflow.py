import uuid
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional

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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class WorkflowList(BaseModel):
    total: int
    workflows: list[Workflow]
    
class WorkflowQuery(BaseModel):
    offset: int = 0
    limit: int = 10
    filter_criteria: Optional[dict] = None
    sort_field: Optional[str] = None
    sort_order: Optional[str] = 'asc'