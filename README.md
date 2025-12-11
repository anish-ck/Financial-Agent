# Financial Analysis Agent Crew

Multi-agent AI system for comprehensive stock analysis using **Google ADK**, **Vertex AI**, **MCP**, **React**, and **FastAPI**.

## 🎯 Architecture

```
React Frontend → FastAPI Backend → ADK Agents (Agent-to-Agent) → PostgreSQL
                                          ↓
                                    MCP Servers
                              (Financial + News Data)
```

## 🚀 Tech Stack

### Backend
- **Google ADK (Agent Developer Kit)** - Agent orchestration
- **Vertex AI (Gemini 2.0 Flash)** - LLM reasoning
- **MCP (Model Context Protocol)** - Agent communication
- **FastAPI** - REST API
- **PostgreSQL** - Data persistence
- **SQLAlchemy** - ORM

### Frontend
- **React 18** + Vite
- **Axios** - API client
- **CSS3** - Responsive styling

### Data Sources
- **Yahoo Finance API** (yfinance)
- **VADER Sentiment** - News analysis

## 🤖 Agent Workflow

**Agent-to-Agent Communication Pattern:**

1. **Market Researcher Agent** 🔍
   - Connects to MCP News Server
   - Fetches latest news articles
   - Performs sentiment analysis
   - Shares context with next agent

2. **Data Analyst Agent** 📊
   - Connects to MCP Financial Server
   - Pulls stock price data
   - Calculates KPIs (P/E, ROI, volatility)
   - Shares financial context

3. **Report Writer Agent** 📝
   - Receives context from both agents via MCP
   - Synthesizes comprehensive report
   - Generates investment recommendations

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Google Cloud SDK (authenticated)
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Option 1: Docker (Recommended)

```powershell
# Start all services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Backend:**
```powershell
cd backend
pip install -r requirements.txt

# Set up PostgreSQL
docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:16

# Run backend
uvicorn app.main:app --reload
```

**Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

## 🔧 Configuration

1. Copy `.env.example` to `.env`:
```powershell
cp .env.example .env
```

2. Update environment variables:
```env
DATABASE_URL=postgresql://admin:password@localhost:5432/financial_agent
GOOGLE_CLOUD_PROJECT=your-project-id
```

3. Authenticate with Google Cloud:
```powershell
gcloud auth application-default login
```

## 📖 API Endpoints

### Analysis
- `POST /api/analysis` - Create new analysis
- `GET /api/analysis/{id}` - Get analysis status

### Reports
- `GET /api/reports` - List all reports
- `GET /api/reports/{id}` - Get specific report
- `GET /api/reports/{id}/download` - Download PDF

## 🏗️ Project Structure

```
Financial-Agent/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── mcp_servers/
│   │   │   │   ├── financial_server.py
│   │   │   │   └── news_server.py
│   │   │   ├── market_researcher.py
│   │   │   ├── data_analyst.py
│   │   │   ├── report_writer.py
│   │   │   └── orchestrator.py
│   │   ├── api/
│   │   │   ├── analysis.py
│   │   │   └── reports.py
│   │   ├── models/
│   │   │   └── database.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisForm.jsx
│   │   │   ├── ReportViewer.jsx
│   │   │   └── AgentStatus.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── docker/
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
└── docker-compose.yml
```

## 🧪 Testing

Try analyzing these stocks:
- AAPL (Apple)
- TSLA (Tesla)
- GOOGL (Google)
- MSFT (Microsoft)
- NVDA (Nvidia)

## 🔍 Features

- ✅ Real-time agent progress tracking
- ✅ Agent-to-agent communication via MCP
- ✅ Sentiment analysis from news
- ✅ Financial KPI calculations
- ✅ AI-powered investment insights
- ✅ PDF report generation
- ✅ Responsive React UI

## 📝 Development

**Add new MCP tools:**

1. Edit `backend/app/agents/mcp_servers/financial_server.py`
2. Add tool method following MCP protocol
3. Update agent to use new tool

**Add new agent:**

1. Create `backend/app/agents/new_agent.py`
2. Implement `analyze()` method
3. Update `orchestrator.py` workflow

## 🚀 Deployment

Deploy to Google Cloud Run:

```powershell
# Build and push images
gcloud builds submit --config cloudbuild.yaml

# Deploy backend
gcloud run deploy financial-agent-backend --image gcr.io/PROJECT_ID/backend

# Deploy frontend
gcloud run deploy financial-agent-frontend --image gcr.io/PROJECT_ID/frontend
```

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

**Powered by Google ADK • Vertex AI • MCP**
