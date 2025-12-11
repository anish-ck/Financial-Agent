"""
Agent Orchestrator - Coordinates multi-agent analysis workflow
Uses Google ADK for agent creation and MCP for context sharing
"""
import logging
import asyncio
import os
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, Report, AnalysisJob
from datetime import datetime
from google import genai
from google.genai import types

# Import MCP servers
from app.agents.mcp_servers.financial_server import FinancialDataServer
from app.agents.mcp_servers.news_server import NewsServer

# Import agents
from app.agents.market_researcher import MarketResearcherAgent
from app.agents.data_analyst import DataAnalystAgent
from app.agents.report_writer import ReportWriterAgent

logger = logging.getLogger(__name__)

# Set Google credentials environment variable explicitly
import os
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    cred_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    if os.path.exists(cred_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    else:
        # Try Windows path
        cred_path = os.path.join(os.getenv("APPDATA", ""), "gcloud", "application_default_credentials.json")
        if os.path.exists(cred_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path

# Initialize Google ADK client
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "blissful-sun-455513-t1")
client = genai.Client(
    vertexai=True,
    project=GOOGLE_CLOUD_PROJECT,
    location="us-central1"
)

async def run_analysis(report_id: int, ticker: str):
    """
    Orchestrate the multi-agent analysis process
    Agent-to-Agent communication pattern:
    1. Market Researcher Agent → collects news & sentiment
    2. Data Analyst Agent → gets financial data & KPIs
    3. Report Writer Agent → synthesizes final report
    
    Agents communicate directly via shared context
    """
    db = SessionLocal()
    
    try:
        # Update job status
        job = db.query(AnalysisJob).filter(AnalysisJob.report_id == report_id).first()
        report = db.query(Report).filter(Report.id == report_id).first()
        
        report.status = "processing"
        job.status = "running"
        db.commit()
        
        logger.info(f"Starting agent-to-agent analysis for {ticker}")
        
        # Initialize MCP servers
        financial_server = FinancialDataServer()
        news_server = NewsServer()
        
        # Shared context between agents
        shared_context = {
            "ticker": ticker,
            "report_id": report_id,
            "data": {}
        }
        
        # ========== AGENT 1: Market Researcher ==========
        job.current_agent = "Market Researcher"
        job.progress = 0.1
        db.commit()
        logger.info(f"🔍 Stage 1: Market Researcher Agent analyzing {ticker}")
        
        market_researcher = MarketResearcherAgent(client, news_server)
        news_analysis = await market_researcher.analyze(ticker, shared_context)
        shared_context["data"]["news"] = news_analysis
        
        job.progress = 0.4
        job.logs = f"Market research completed: {len(news_analysis.get('articles', []))} articles analyzed"
        db.commit()
        logger.info(f"✅ Market Researcher completed for {ticker}")
        
        # ========== AGENT 2: Data Analyst ==========
        job.current_agent = "Data Analyst"
        job.progress = 0.5
        db.commit()
        logger.info(f"📊 Stage 2: Data Analyst Agent analyzing {ticker}")
        
        data_analyst = DataAnalystAgent(client, financial_server)
        financial_analysis = await data_analyst.analyze(ticker, shared_context)
        shared_context["data"]["financial"] = financial_analysis
        
        job.progress = 0.7
        job.logs = f"Financial analysis completed: KPIs calculated, charts generated"
        db.commit()
        logger.info(f"✅ Data Analyst completed for {ticker}")
        
        # ========== AGENT 3: Report Writer ==========
        job.current_agent = "Report Writer"
        job.progress = 0.8
        db.commit()
        logger.info(f"📝 Stage 3: Report Writer Agent synthesizing report for {ticker}")
        
        report_writer = ReportWriterAgent(client)
        final_report = await report_writer.synthesize(ticker, shared_context)
        
        job.progress = 0.95
        db.commit()
        logger.info(f"✅ Report Writer completed for {ticker}")
        
        # Save final report
        import json
        report.result_json = json.dumps(final_report)
        
        # Generate PDF report
        try:
            from app.tools.pdf_generator import generate_pdf_report
            import os
            
            # Create reports directory if it doesn't exist
            reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            # Generate PDF
            pdf_filename = f"report_{ticker}_{report_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
            pdf_path = os.path.join(reports_dir, pdf_filename)
            
            generate_pdf_report(ticker, final_report, pdf_path)
            report.pdf_url = pdf_path
            
            logger.info(f"📄 PDF report generated: {pdf_path}")
        except Exception as pdf_error:
            logger.error(f"Failed to generate PDF: {str(pdf_error)}")
            # Continue even if PDF generation fails
        
        report.status = "completed"
        report.completed_at = datetime.utcnow()
        
        job.progress = 1.0
        job.status = "completed"
        job.current_agent = None
        job.logs = "Analysis completed successfully"
        
        db.commit()
        logger.info(f"🎉 Complete analysis finished for {ticker}")
        
    except Exception as e:
        logger.error(f"❌ Error in analysis: {str(e)}", exc_info=True)
        job.status = "failed"
        job.error_message = str(e)
        report.status = "failed"
        db.commit()
    finally:
        db.close()
