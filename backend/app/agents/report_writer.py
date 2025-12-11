"""
Report Writer Agent
Uses Google ADK to synthesize comprehensive financial report from other agents' outputs
"""
import logging
from typing import Dict, Any
from google import genai

logger = logging.getLogger(__name__)

class ReportWriterAgent:
    """Agent specialized in synthesizing comprehensive financial reports"""
    
    def __init__(self, client: genai.Client):
        self.client = client
        self.name = "Report Writer"
        logger.info(f"{self.name} Agent initialized")
    
    async def synthesize(self, ticker: str, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize comprehensive report from Market Researcher and Data Analyst outputs
        Uses agent-to-agent context sharing
        """
        logger.info(f"{self.name} starting report synthesis for {ticker}")
        
        try:
            # Extract data from previous agents via shared context
            news_data = shared_context.get("data", {}).get("news", {})
            financial_data = shared_context.get("data", {}).get("financial", {})
            
            # Build comprehensive prompt with all agent insights
            prompt = f"""You are a senior financial analyst writing a comprehensive stock analysis report.

STOCK: {ticker}

=== MARKET RESEARCH (from Market Researcher Agent) ===
{news_data.get('summary', 'No market research data available')}

Sentiment: {news_data.get('sentiment', {}).get('sentiment_label', 'N/A')} 
(Score: {news_data.get('sentiment', {}).get('sentiment_score', 0)})

Articles Analyzed: {news_data.get('sentiment', {}).get('analyzed_articles', 0)}

Trending Topics: {', '.join([t.get('topic', '') for t in news_data.get('trending', {}).get('trending_topics', [])[:5]])}

=== FINANCIAL ANALYSIS (from Data Analyst Agent) ===
{financial_data.get('technical_analysis', 'No financial analysis available')}

Company: {financial_data.get('company', {}).get('company_name', ticker)}
Sector: {financial_data.get('company', {}).get('sector', 'N/A')}
Current Price: ${financial_data.get('price', {}).get('current_price', 0):.2f}

Key Metrics:
- P/E Ratio: {financial_data.get('kpis', {}).get('pe_ratio', 'N/A')}
- ROI (1Y): {financial_data.get('kpis', {}).get('roi_1y', 0)}%
- Volatility: {financial_data.get('kpis', {}).get('volatility', 0)}
- Beta: {financial_data.get('kpis', {}).get('beta', 'N/A')}

=== YOUR TASK ===
Synthesize a comprehensive investment analysis report with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. COMPANY OVERVIEW (1 paragraph)
3. MARKET SENTIMENT ANALYSIS (1 paragraph - integrate news insights)
4. FINANCIAL PERFORMANCE (1 paragraph - integrate technical analysis)
5. RISK ASSESSMENT (1 paragraph)
6. INVESTMENT RECOMMENDATION (BUY/HOLD/SELL with justification, 1 paragraph)
7. KEY TAKEAWAYS (3-5 bullet points)

Write in a professional, objective tone suitable for investors.
"""
            
            # Use Gemini via ADK to generate final report
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            final_report_text = response.text if hasattr(response, 'text') else "Report generation completed"
            
            # Compile complete report
            result = {
                "agent": self.name,
                "ticker": ticker,
                "report": {
                    "full_text": final_report_text,
                    "sections": {
                        "market_sentiment": news_data.get('summary', ''),
                        "technical_analysis": financial_data.get('technical_analysis', ''),
                        "synthesis": final_report_text
                    }
                },
                "data_sources": {
                    "market_research": {
                        "articles_analyzed": news_data.get('sentiment', {}).get('analyzed_articles', 0),
                        "sentiment_score": news_data.get('sentiment', {}).get('sentiment_score', 0),
                        "sentiment_label": news_data.get('sentiment', {}).get('sentiment_label', 'neutral')
                    },
                    "financial_analysis": {
                        "current_price": financial_data.get('price', {}).get('current_price', 0),
                        "pe_ratio": financial_data.get('kpis', {}).get('pe_ratio'),
                        "roi_1y": financial_data.get('kpis', {}).get('roi_1y', 0),
                        "volatility": financial_data.get('kpis', {}).get('volatility', 0)
                    }
                },
                "status": "completed"
            }
            
            logger.info(f"{self.name} completed report synthesis for {ticker}")
            return result
            
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}", exc_info=True)
            return {
                "agent": self.name,
                "ticker": ticker,
                "status": "error",
                "error": str(e)
            }
