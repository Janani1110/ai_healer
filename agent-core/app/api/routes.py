from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.pipeline import Pipeline, FailureAnalysis, Fix
from app.schemas.pipeline import PipelineResponse, FailureAnalysisResponse, FixResponse, StatsResponse

router = APIRouter()

@router.get("/pipelines", response_model=List[PipelineResponse])
async def get_pipelines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all monitored pipelines"""
    pipelines = db.query(Pipeline).offset(skip).limit(limit).all()
    return pipelines

@router.get("/pipelines/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline(pipeline_id: int, db: Session = Depends(get_db)):
    """Get specific pipeline details"""
    pipeline = db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    return pipeline

@router.get("/failures", response_model=List[FailureAnalysisResponse])
async def get_failures(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all failure analyses"""
    failures = db.query(FailureAnalysis).offset(skip).limit(limit).all()
    return failures

@router.get("/fixes", response_model=List[FixResponse])
async def get_fixes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all applied fixes"""
    fixes = db.query(Fix).offset(skip).limit(limit).all()
    return fixes

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get agent statistics"""
    total_pipelines = db.query(Pipeline).count()
    total_failures = db.query(FailureAnalysis).count()
    total_fixes = db.query(Fix).count()
    successful_fixes = db.query(Fix).filter(Fix.success == True).count()
    
    success_rate = (successful_fixes / total_fixes * 100) if total_fixes > 0 else 0
    
    return {
        "total_pipelines": total_pipelines,
        "total_failures": total_failures,
        "total_fixes": total_fixes,
        "successful_fixes": successful_fixes,
        "success_rate": round(success_rate, 2)
    }
