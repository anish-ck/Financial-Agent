import React, { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function AnalysisForm({ onAnalysisCreated }) {
    const [ticker, setTicker] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API_URL}/api/analysis`, {
                ticker: ticker.toUpperCase(),
                user_email: 'demo@example.com'
            });

            onAnalysisCreated(response.data.id);
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create analysis');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="analysis-form">
            <h2>Start New Stock Analysis</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="ticker">Stock Ticker Symbol</label>
                    <input
                        type="text"
                        id="ticker"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        placeholder="e.g., AAPL, TSLA, GOOGL"
                        required
                        maxLength="10"
                    />
                </div>

                {error && <div className="error">{error}</div>}

                <button type="submit" disabled={loading || !ticker}>
                    {loading ? 'Creating Analysis...' : 'Analyze Stock'}
                </button>
            </form>

            <div className="info-box">
                <h3>🔄 Agent-to-Agent Workflow:</h3>
                <ol>
                    <li>
                        <strong>🔍 Market Researcher Agent</strong><br />
                        Uses MCP News Server to gather latest news and analyze sentiment
                    </li>
                    <li>
                        <strong>📊 Data Analyst Agent</strong><br />
                        Uses MCP Financial Server to pull price data and calculate KPIs
                    </li>
                    <li>
                        <strong>📝 Report Writer Agent</strong><br />
                        Synthesizes insights from both agents into comprehensive report
                    </li>
                </ol>
                <p className="info-note">
                    <strong>Powered by:</strong> Google ADK (Agent Developer Kit) with Vertex AI Gemini models
                </p>
            </div>
        </div>
    );
}

export default AnalysisForm;
