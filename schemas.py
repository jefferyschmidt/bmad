"""
Pydantic schemas for BMAD Pipeline API
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AIProviderBase(BaseModel):
    name: str
    display_name: str
    model_name: str
    max_tokens: int = 4000
    is_active: bool = True

class AIProviderCreate(AIProviderBase):
    api_key: str

class AIProviderUpdate(BaseModel):
    display_name: Optional[str] = None
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    max_tokens: Optional[int] = None
    is_active: Optional[bool] = None

class AIProviderResponse(AIProviderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    requirements: str
    application_type: Optional[str] = None
    ai_provider: str = "anthropic"  # anthropic, openai

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    application_type: Optional[str] = None
    ai_provider: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    requirements: str
    refined_requirements: Optional[str] = None
    user_stories: Optional[str] = None
    ux_design: Optional[str] = None
    system_architecture: Optional[str] = None
    application_type: Optional[str] = None
    tech_stack: Optional[str] = None
    status: str
    archived: bool
    ai_provider: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RequirementsAnalysisRequest(BaseModel):
    pass  # No additional data needed for analysis

class ArchiveProjectRequest(BaseModel):
    archived: bool

class RequirementsAnalysisResponse(BaseModel):
    success: bool
    refined_requirements: Optional[str] = None
    user_stories: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class UXDesignResponse(BaseModel):
    success: bool
    ux_design: Optional[str] = None
    error: Optional[str] = None

class SystemArchitectureResponse(BaseModel):
    success: bool
    system_architecture: Optional[str] = None
    error: Optional[str] = None

class ProjectGenerationResponse(BaseModel):
    success: bool
    project_path: Optional[str] = None
    tech_stack: Optional[Dict[str, Any]] = None
    code_generation: Optional[Dict[str, Any]] = None
    documentation: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    error: Optional[str] = None

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
