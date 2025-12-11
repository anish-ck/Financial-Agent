from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.database import get_db, Report, AnalysisJob
from app.agents.orchestrator import run_analysis
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class AnalysisRequest(BaseModel):
    ticker: str
    user_email: str = "demo@example.com"

class AnalysisResponse(BaseModel):
    id: int
    ticker: str
    status: str
    created_at: datetime

@router.post("/analysis", response_model=AnalysisResponse)
async def create_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new stock analysis request"""
    try:
        # Create report
        report = Report(
            ticker=request.ticker.upper(),
            status="pending"
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # Create job
        job = AnalysisJob(
            report_id=report.id,
            status="queued"
        )
        db.add(job)
        db.commit()
        
        # Run analysis in background
        background_tasks.add_task(run_analysis, report.id, request.ticker.upper())
        
        logger.info(f"Created analysis for {request.ticker.upper()} with ID {report.id}")
        
        return AnalysisResponse(
            id=report.id,
            ticker=report.ticker,
            status=report.status,
            created_at=report.created_at
        )
    except Exception as e:
        logger.error(f"Error creating analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{analysis_id}")
async def get_analysis_status(analysis_id: int, db: Session = Depends(get_db)):
    """Get analysis status and progress"""
    report = db.query(Report).filter(Report.id == analysis_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    job = db.query(AnalysisJob).filter(AnalysisJob.report_id == analysis_id).first()
    
    return {
        "id": report.id,
        "ticker": report.ticker,
        "status": report.status,
        "progress": job.progress if job else 0,
        "current_agent": job.current_agent if job else None,
        "logs": job.logs if job else None,
        "created_at": report.created_at,
        "completed_at": report.completed_at
    }
