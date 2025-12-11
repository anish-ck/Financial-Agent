"""
Data Analyst Agent
Uses Google ADK and MCP Financial Server to analyze stock data and calculate KPIs
"""
import logging
from typing import Dict, Any
from google import genai

logger = logging.getLogger(__name__)

class DataAnalystAgent:
    """Agent specialized in financial data analysis"""
    
    def __init__(self, client: genai.Client, financial_server):
        self.client = client
        self.financial_server = financial_server
        self.name = "Data Analyst"
        logger.info(f"{self.name} Agent initialized")
    
    async def analyze(self, ticker: str, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform financial data analysis using MCP financial server
        Returns price data, KPIs, and technical analysis
        """
        logger.info(f"{self.name} starting analysis for {ticker}")
        
        try:
            # Step 1: Get current price via MCP
            price_data = self.financial_server.get_current_price(ticker)
            
            # Step 2: Get historical data via MCP
            historical_data = self.financial_server.get_historical_data(ticker, period="1y")
            
            # Step 3: Get company info via MCP
            company_info = self.financial_server.get_company_info(ticker)
            
            # Step 4: Calculate KPIs via MCP
            kpis = self.financial_server.calculate_kpis(ticker)
            
            # Step 5: Use ADK agent to generate technical analysis
            prompt = f"""You are a quantitative financial analyst. Analyze {ticker} based on this data:

Company: {company_info.get('company_name', ticker)}
Sector: {company_info.get('sector', 'N/A')}
Industry: {company_info.get('industry', 'N/A')}

Current Metrics:
- Current Price: ${price_data.get('current_price', 0):.2f}
- Market Cap: ${price_data.get('market_cap', 0):,.0f}
- Volume: {price_data.get('volume', 0):,}

Key Performance Indicators:
- P/E Ratio: {kpis.get('pe_ratio', 'N/A')}
- Price-to-Book: {kpis.get('price_to_book', 'N/A')}
- ROI (1Y): {kpis.get('roi_1y', 0)}%
- Volatility: {kpis.get('volatility', 0)}
- Beta: {kpis.get('beta', 'N/A')}
- Dividend Yield: {kpis.get('dividend_yield', 0)}

Historical Performance:
- Period: {historical_data.get('summary', {}).get('start_date')} to {historical_data.get('summary', {}).get('end_date')}
- Average Price: ${historical_data.get('summary', {}).get('avg_price', 0):.2f}
- 52-Week High: ${kpis.get('52_week_high', 0):.2f}
- 52-Week Low: ${kpis.get('52_week_low', 0):.2f}

Provide a technical analysis summary (2-3 paragraphs) covering:
1. Valuation assessment (overvalued/undervalued based on P/E, P/B)
2. Risk analysis (volatility, beta)
3. Performance trends and price momentum
"""
            
            # Use Gemini via ADK to generate insights
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            technical_analysis = response.text if hasattr(response, 'text') else "Analysis completed"
            
            result = {
                "agent": self.name,
                "ticker": ticker,
                "price": price_data,
                "historical": historical_data,
                "company": company_info,
                "kpis": kpis,
                "technical_analysis": technical_analysis,
                "status": "completed"
            }
            
            logger.info(f"{self.name} completed analysis for {ticker}")
            return result
            
        except Exception as e:
            logger.error(f"{self.name} error: {str(e)}", exc_info=True)
            return {
                "agent": self.name,
                "ticker": ticker,
                "status": "error",
                "error": str(e)
            }
