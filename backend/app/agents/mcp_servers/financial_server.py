"""
MCP Server for Financial Data
Provides stock prices, historical data, and company information via MCP protocol
"""
import yfinance as yf
import pandas as pd
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FinancialDataServer:
    """MCP Server that provides financial data as resources and tools"""
    
    def __init__(self):
        self.name = "financial-data-server"
        logger.info("Financial Data MCP Server initialized")
    
    def get_current_price(self, ticker: str) -> Dict[str, Any]:
        """MCP Tool: Get current stock price"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
                "previous_close": info.get("previousClose"),
                "market_cap": info.get("marketCap"),
                "volume": info.get("volume"),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting current price for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> Dict[str, Any]:
        """MCP Tool: Get historical stock data"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            return {
                "ticker": ticker,
                "period": period,
                "data": {
                    "dates": hist.index.strftime('%Y-%m-%d').tolist(),
                    "close": hist['Close'].tolist(),
                    "open": hist['Open'].tolist(),
                    "high": hist['High'].tolist(),
                    "low": hist['Low'].tolist(),
                    "volume": hist['Volume'].tolist()
                },
                "summary": {
                    "start_date": hist.index[0].strftime('%Y-%m-%d'),
                    "end_date": hist.index[-1].strftime('%Y-%m-%d'),
                    "total_days": len(hist),
                    "avg_price": float(hist['Close'].mean()),
                    "min_price": float(hist['Close'].min()),
                    "max_price": float(hist['Close'].max())
                }
            }
        except Exception as e:
            logger.error(f"Error getting historical data for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    def get_company_info(self, ticker: str) -> Dict[str, Any]:
        """MCP Tool: Get company information"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                "ticker": ticker,
                "company_name": info.get("longName", info.get("shortName")),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "description": info.get("longBusinessSummary", "")[:500],
                "website": info.get("website"),
                "employees": info.get("fullTimeEmployees"),
                "country": info.get("country"),
                "exchange": info.get("exchange"),
                "currency": info.get("currency")
            }
        except Exception as e:
            logger.error(f"Error getting company info for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    def calculate_kpis(self, ticker: str) -> Dict[str, Any]:
        """MCP Tool: Calculate key performance indicators"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
            
            # Calculate volatility
            returns = hist['Close'].pct_change()
            volatility = float(returns.std() * (252 ** 0.5))  # Annualized
            
            # Calculate ROI (1 year)
            if len(hist) > 0:
                roi = ((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100
            else:
                roi = 0
            
            return {
                "ticker": ticker,
                "pe_ratio": info.get("trailingPE"),
                "forward_pe": info.get("forwardPE"),
                "peg_ratio": info.get("pegRatio"),
                "price_to_book": info.get("priceToBook"),
                "dividend_yield": info.get("dividendYield"),
                "volatility": round(volatility, 4),
                "roi_1y": round(float(roi), 2),
                "beta": info.get("beta"),
                "52_week_high": info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow")
            }
        except Exception as e:
            logger.error(f"Error calculating KPIs for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    # MCP Resource methods (for context provision)
    def get_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Get resource by URI (MCP protocol)"""
        # Parse URI: stock://{ticker}/{resource_type}
        parts = resource_uri.replace("stock://", "").split("/")
        if len(parts) < 2:
            return {"error": "Invalid resource URI"}
        
        ticker = parts[0]
        resource_type = parts[1]
        
        if resource_type == "price":
            return self.get_current_price(ticker)
        elif resource_type == "history":
            return self.get_historical_data(ticker)
        elif resource_type == "info":
            return self.get_company_info(ticker)
        else:
            return {"error": f"Unknown resource type: {resource_type}"}
