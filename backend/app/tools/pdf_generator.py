"""
PDF Report Generator
Creates professional PDF reports from analysis data
"""
import os
from datetime import datetime
from fpdf import FPDF
import logging

logger = logging.getLogger(__name__)

class PDFReport(FPDF):
    """Custom PDF class for financial reports"""
    
    def header(self):
        """Add header to each page"""
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Financial Analysis Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(ticker: str, report_data: dict, output_path: str) -> str:
    """
    Generate PDF report from analysis data
    
    Args:
        ticker: Stock ticker symbol
        report_data: Complete analysis data from agents
        output_path: Path where PDF should be saved
        
    Returns:
        Path to generated PDF file
    """
    try:
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Title
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, f'{ticker} Stock Analysis', 0, 1, 'C')
        pdf.ln(5)
        
        # Date
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        pdf.ln(10)
        
        # Market Sentiment Section
        if 'data_sources' in report_data and 'market_research' in report_data['data_sources']:
            pdf.set_font('Arial', 'B', 14)
            pdf.set_fill_color(230, 240, 255)
            pdf.cell(0, 10, 'Market Sentiment Analysis', 0, 1, 'L', True)
            pdf.ln(3)
            
            market = report_data['data_sources']['market_research']
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'Sentiment:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"{market.get('sentiment_label', 'N/A').upper()}", 0, 1)
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'Sentiment Score:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"{market.get('sentiment_score', 0):.4f}", 0, 1)
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'Articles Analyzed:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"{market.get('articles_analyzed', 0)}", 0, 1)
            pdf.ln(8)
        
        # Financial Metrics Section
        if 'data_sources' in report_data and 'financial_analysis' in report_data['data_sources']:
            pdf.set_font('Arial', 'B', 14)
            pdf.set_fill_color(230, 255, 230)
            pdf.cell(0, 10, 'Financial Metrics', 0, 1, 'L', True)
            pdf.ln(3)
            
            financial = report_data['data_sources']['financial_analysis']
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'Current Price:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"${financial.get('current_price', 0):.2f}", 0, 1)
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'P/E Ratio:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pe_ratio = financial.get('pe_ratio', 'N/A')
            pe_text = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else str(pe_ratio)
            pdf.cell(0, 8, pe_text, 0, 1)
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'ROI (1Y):', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"{financial.get('roi_1y', 0):.2f}%", 0, 1)
            
            pdf.set_font('Arial', 'B', 11)
            pdf.cell(60, 8, 'Volatility:', 0, 0)
            pdf.set_font('Arial', '', 11)
            pdf.cell(0, 8, f"{financial.get('volatility', 0):.4f}", 0, 1)
            pdf.ln(8)
        
        # Comprehensive Analysis Section
        if 'report' in report_data and 'full_text' in report_data['report']:
            pdf.set_font('Arial', 'B', 14)
            pdf.set_fill_color(255, 245, 230)
            pdf.cell(0, 10, 'Comprehensive Investment Analysis', 0, 1, 'L', True)
            pdf.ln(5)
            
            pdf.set_font('Arial', '', 10)
            full_text = report_data['report']['full_text']
            
            # Clean and format text for PDF
            full_text = full_text.replace('\u2019', "'").replace('\u2018', "'")
            full_text = full_text.replace('\u201c', '"').replace('\u201d', '"')
            full_text = full_text.replace('\u2013', '-').replace('\u2014', '-')
            full_text = full_text.replace('\u2026', '...')
            
            # Handle any remaining encoding issues
            try:
                full_text = full_text.encode('latin-1', 'replace').decode('latin-1')
            except:
                pass
            
            # Add text with proper formatting
            pdf.multi_cell(0, 6, full_text)
        
        # Footer info
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 8)
        pdf.set_text_color(128, 128, 128)
        pdf.multi_cell(0, 5, 'Generated by Financial Analysis Agent Crew\nPowered by Google ADK, Vertex AI, and MCP')
        
        # Save PDF
        pdf.output(output_path)
        logger.info(f"PDF report generated successfully: {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}", exc_info=True)
        raise
