import React, { useState } from 'react';
import AnalysisForm from './components/AnalysisForm';
import ReportViewer from './components/ReportViewer';
import './App.css';

function App() {
    const [currentAnalysisId, setCurrentAnalysisId] = useState(null);
    const [showReport, setShowReport] = useState(false);

    const handleAnalysisCreated = (analysisId) => {
        setCurrentAnalysisId(analysisId);
        setShowReport(true);
    };

    return (
        <div className="App">
            <header className="header">
                <h1>🤖 Financial Analysis Agent Crew</h1>
                <p>AI-Powered Multi-Agent Stock Analysis System</p>
                <p className="tech-stack">Google ADK • Vertex AI • MCP • React • FastAPI</p>
            </header>

            <main className="container">
                {!showReport ? (
                    <AnalysisForm onAnalysisCreated={handleAnalysisCreated} />
                ) : (
                    <div>
                        <button
                            onClick={() => setShowReport(false)}
                            className="back-button"
                        >
                            ← New Analysis
                        </button>
                        <ReportViewer analysisId={currentAnalysisId} />
                    </div>
                )}
            </main>

            <footer className="footer">
                <p>Agent-to-Agent Communication via Model Context Protocol (MCP)</p>
            </footer>
        </div>
    );
}

export default App;
