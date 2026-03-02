from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.pipeline import PipelineStatus, ErrorCategory, FixStatus

class PipelineResponse(BaseModel):
    id: int
    platform: str
    repository: str
    branch: str
    commit_sha: str
    pipeline_id: str
    status: PipelineStatus
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class FailureAnalysisResponse(BaseModel):
    id: int
    pipeline_id: int
    error_category: ErrorCategory
    error_message: str
    root_cause: Optional[str]
    confidence_score: int
    analyzed_at: datetime
    
    class Config:
        from_attributes = True

class FixResponse(BaseModel):
    id: int
    analysis_id: int
    fix_type: str
    description: str
    commit_sha: Optional[str]
    status: FixStatus
    success: bool
    applied_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    total_pipelines: int
    total_failures: int
    total_fixes: int
    successful_fixes: int
    success_rate: float
