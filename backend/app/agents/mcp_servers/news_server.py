"""
MCP Server for News and Sentiment Analysis
Provides financial news and sentiment analysis via MCP protocol
"""
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import yfinance as yf

logger = logging.getLogger(__name__)

class NewsServer:
    """MCP Server that provides news and sentiment analysis"""
    
    def __init__(self):
        self.name = "news-server"
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        logger.info("News MCP Server initialized")
    
    def fetch_news(self, ticker: str, limit: int = 10) -> Dict[str, Any]:
        """MCP Tool: Fetch latest news for a ticker"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            articles = []
            for item in news[:limit]:
                articles.append({
                    "title": item.get("title", ""),
                    "publisher": item.get("publisher", ""),
                    "link": item.get("link", ""),
                    "published": datetime.fromtimestamp(item.get("providerPublishTime", 0)).isoformat(),
                    "type": item.get("type", "")
                })
            
            return {
                "ticker": ticker,
                "total_articles": len(articles),
                "articles": articles,
                "fetched_at": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching news for {ticker}: {str(e)}")
            return {
                "ticker": ticker,
                "total_articles": 0,
                "articles": [],
                "error": str(e)
            }
    
    def analyze_sentiment(self, ticker: str) -> Dict[str, Any]:
        """MCP Tool: Analyze sentiment from news headlines"""
        try:
            # Fetch news first
            news_data = self.fetch_news(ticker, limit=20)
            articles = news_data.get("articles", [])
            
            if not articles:
                return {
                    "ticker": ticker,
                    "sentiment_score": 0,
                    "sentiment_label": "neutral",
                    "analyzed_articles": 0,
                    "message": "No articles to analyze"
                }
            
            # Analyze sentiment for each title
            sentiments = []
            for article in articles:
                title = article.get("title", "")
                if title:
                    scores = self.sentiment_analyzer.polarity_scores(title)
                    sentiments.append(scores['compound'])
            
            # Calculate average sentiment
            if sentiments:
                avg_sentiment = sum(sentiments) / len(sentiments)
                
                # Classify sentiment
                if avg_sentiment >= 0.05:
                    label = "positive"
                elif avg_sentiment <= -0.05:
                    label = "negative"
                else:
                    label = "neutral"
                
                return {
                    "ticker": ticker,
                    "sentiment_score": round(avg_sentiment, 4),
                    "sentiment_label": label,
                    "analyzed_articles": len(sentiments),
                    "score_range": {
                        "min": round(min(sentiments), 4),
                        "max": round(max(sentiments), 4)
                    },
                    "distribution": {
                        "positive": sum(1 for s in sentiments if s >= 0.05),
                        "neutral": sum(1 for s in sentiments if -0.05 < s < 0.05),
                        "negative": sum(1 for s in sentiments if s <= -0.05)
                    }
                }
            else:
                return {
                    "ticker": ticker,
                    "sentiment_score": 0,
                    "sentiment_label": "neutral",
                    "analyzed_articles": 0
                }
        except Exception as e:
            logger.error(f"Error analyzing sentiment for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    def get_trending_topics(self, ticker: str) -> Dict[str, Any]:
        """MCP Tool: Extract trending topics from news"""
        try:
            news_data = self.fetch_news(ticker, limit=20)
            articles = news_data.get("articles", [])
            
            # Simple keyword extraction from titles
            all_titles = " ".join([a.get("title", "") for a in articles])
            
            # Common financial keywords
            keywords = ["earnings", "revenue", "profit", "growth", "decline", 
                       "stock", "shares", "market", "investor", "CEO", "merger",
                       "acquisition", "launch", "product", "sales"]
            
            found_keywords = {}
            for keyword in keywords:
                count = all_titles.lower().count(keyword.lower())
                if count > 0:
                    found_keywords[keyword] = count
            
            # Sort by frequency
            trending = sorted(found_keywords.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "ticker": ticker,
                "trending_topics": [{"topic": k, "mentions": v} for k, v in trending],
                "total_articles_analyzed": len(articles)
            }
        except Exception as e:
            logger.error(f"Error getting trending topics for {ticker}: {str(e)}")
            return {"error": str(e)}
    
    # MCP Resource methods
    def get_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Get resource by URI (MCP protocol)"""
        # Parse URI: news://{ticker}/{resource_type}
        if resource_uri.startswith("news://"):
            parts = resource_uri.replace("news://", "").split("/")
            ticker = parts[0]
            resource_type = parts[1] if len(parts) > 1 else "latest"
            
            if resource_type == "latest":
                return self.fetch_news(ticker)
        elif resource_uri.startswith("sentiment://"):
            parts = resource_uri.replace("sentiment://", "").split("/")
            ticker = parts[0]
            return self.analyze_sentiment(ticker)
        
        return {"error": "Invalid resource URI"}
