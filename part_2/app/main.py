from fastapi import FastAPI, status, Depends
from typing import Annotated
from pydantic import BaseModel, Field
from app.workflows.basic_content_workflow import ContentCreationWorkflow
from pydantic_settings import BaseSettings
from functools import lru_cache
from app.config.settings import Settings

class Topic(BaseModel):
    topic: str
    research: bool = False
        
@lru_cache
def get_settings():
    return Settings()
    
app = FastAPI()

@app.post("/basic", status_code=status.HTTP_201_CREATED)
async def basic_content_workflow(data: Topic, settings: Annotated[Settings, Depends(get_settings)]) -> str:
    print(data)
    workflow = ContentCreationWorkflow(settings=settings, timeout=None, verbose=False)
    result = await workflow.run(query=data.topic, research=data.research)
    return "workflow complete"