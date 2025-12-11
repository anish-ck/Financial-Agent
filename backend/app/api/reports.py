from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.models.database import get_db, Report
import json

router = APIRouter()

@router.get("/reports")
async def list_reports(db: Session = Depends(get_db)):
    """List all reports"""
    reports = db.query(Report).order_by(Report.created_at.desc()).limit(50).all()
    return [
        {
            "id": r.id,
            "ticker": r.ticker,
            "status": r.status,
            "created_at": r.created_at,
            "completed_at": r.completed_at
        }
        for r in reports
    ]

@router.get("/reports/{report_id}")
async def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get specific report data"""
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    result_data = json.loads(report.result_json) if report.result_json else {}
    
    return {
        "id": report.id,
        "ticker": report.ticker,
        "status": report.status,
        "pdf_url": report.pdf_url,
        "data": result_data,
        "created_at": report.created_at,
        "completed_at": report.completed_at
    }

@router.get("/reports/{report_id}/download")
async def download_report(report_id: int, db: Session = Depends(get_db)):
    """Download PDF report"""
    import os
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    if not report.pdf_url or not os.path.exists(report.pdf_url):
        raise HTTPException(status_code=404, detail="Report PDF not found or not yet generated")
    
    return FileResponse(
        report.pdf_url,
        media_type="application/pdf",
        filename=f"report_{report.ticker}_{report.id}.pdf"
    )
