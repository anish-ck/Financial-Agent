"""
Market Researcher Agent
Uses Google ADK and MCP News Server to gather and analyze market sentiment
"""
import logging
from typing import Dict, Any
from google import genai

logger = logging.getLogger(__name__)

class MarketResearcherAgent:
    """Agent specialized in market research and sentiment analysis"""
    
    def __init__(self, client: genai.Client, news_server):
        self.client = client
        self.news_server = news_server
        self.name = "Market Researcher"
        logger.info(f"{self.name} Agent initialized")
    
    async def analyze(self, ticker: str, shared_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform market research using MCP news server
        Returns news summary and sentiment analysis
        """
        logger.info(f"{self.name} starting analysis for {ticker}")
        
        try:
            # Step 1: Fetch news via MCP
            news_data = self.news_server.fetch_news(ticker, limit=15)
            
            # Step 2: Analyze sentiment via MCP
            sentiment_data = self.news_server.analyze_sentiment(ticker)
            
            # Step 3: Get trending topics via MCP
            trending_data = self.news_server.get_trending_topics(ticker)
            
            # Step 4: Use ADK agent to synthesize insights
            articles_text = "\n".join([
                f"- {article['title']} ({article['publisher']})"
                for article in news_data.get('articles', [])[:10]
            ])
            
            prompt = f"""You are a market research analyst. Analyze the following news about {ticker}:

Recent News Headlines:
{articles_text}

Sentiment Analysis:
- Overall Sentiment: {sentiment_data.get('sentiment_label', 'neutral')}
- Sentiment Score: {sentiment_data.get('sentiment_score', 0)}
- Articles Analyzed: {sentiment_data.get('analyzed_articles', 0)}

Trending Topics:
{', '.join([t['topic'] for t in trending_data.get('trending_topics', [])[:5]])}

Provide a brief market sentiment summary (2-3 paragraphs) highlighting:
1. Overall market sentiment towards {ticker}
2. Key themes and topics in recent news
3. Potential impact on stock performance
"""
            
            # Use Gemini via ADK to generate insights
            response = self.client.models.generate_content(
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            
            summary = response.text if hasattr(response, 'text') else "Analysis completed"
            
            result = {
                "agent": self.name,
                "ticker": ticker,
                "news": news_data,
                "sentiment": sentiment_data,
                "trending": trending_data,
                "summary": summary,
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
