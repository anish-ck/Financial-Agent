import React, { useState, useEffect } from 'react';
import axios from 'axios';
import AgentStatus from './AgentStatus';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function ReportViewer({ analysisId }) {
    const [status, setStatus] = useState(null);
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);
    const [viewMode, setViewMode] = useState('formatted'); // 'formatted', 'pdf', 'json'

    useEffect(() => {
        const pollStatus = setInterval(async () => {
            try {
                const response = await axios.get(`${API_URL}/api/analysis/${analysisId}`);
                setStatus(response.data);

                if (response.data.status === 'completed') {
                    clearInterval(pollStatus);
                    fetchReport();
                } else if (response.data.status === 'failed') {
                    clearInterval(pollStatus);
                    setLoading(false);
                }
            } catch (error) {
                console.error('Error polling status:', error);
            }
        }, 2000);

        return () => clearInterval(pollStatus);
    }, [analysisId]);

    const fetchReport = async () => {
        try {
            const response = await axios.get(`${API_URL}/api/reports/${analysisId}`);
            setReport(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching report:', error);
            setLoading(false);
        }
    };

    if (!status) return <div className="loading">Loading...</div>;

    return (
        <div className="report-viewer">
            <h2>Analysis Report: {status.ticker}</h2>

            <AgentStatus status={status} />

            {loading && status.status !== 'failed' && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Agents are collaborating on your analysis...</p>
                    <p className="loading-detail">Using MCP for agent-to-agent communication</p>
                </div>
            )}

            {status.status === 'failed' && (
                <div className="error">
                    ❌ Analysis failed. Please try again.
                </div>
            )}

            {report && (
                <div className="report-content">
                    <div className="report-header">
                        <h3>✅ Analysis Complete</h3>
                        <div className="report-actions">
                            <button className="download-btn" onClick={() => window.open(`${API_URL}/api/reports/${analysisId}/download`, '_blank')}>
                                📄 Download PDF
                            </button>
                        </div>
                    </div>

                    {/* View Mode Toggle */}
                    <div className="view-toggle">
                        <button
                            className={`toggle-btn ${viewMode === 'formatted' ? 'active' : ''}`}
                            onClick={() => setViewMode('formatted')}
                        >
                            📊 Formatted View
                        </button>
                        <button
                            className={`toggle-btn ${viewMode === 'pdf' ? 'active' : ''}`}
                            onClick={() => setViewMode('pdf')}
                        >
                            📋 PDF Preview
                        </button>
                        <button
                            className={`toggle-btn ${viewMode === 'json' ? 'active' : ''}`}
                            onClick={() => setViewMode('json')}
                        >
                            🔧 Raw Data
                        </button>
                    </div>

                    {/* Formatted View */}
                    {viewMode === 'formatted' && (
                        <div className="report-sections">
                            <div className="report-section sentiment-section">
                                <h4>📊 Market Sentiment Analysis</h4>
                                <div className="sentiment-grid">
                                    <div className="metric-card">
                                        <span className="metric-label">Sentiment</span>
                                        <span className={`metric-value sentiment-${report.data?.data_sources?.market_research?.sentiment_label || 'neutral'}`}>
                                            {report.data?.data_sources?.market_research?.sentiment_label?.toUpperCase() || 'NEUTRAL'}
                                        </span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="metric-label">Sentiment Score</span>
                                        <span className="metric-value">
                                            {report.data?.data_sources?.market_research?.sentiment_score?.toFixed(4) || 'N/A'}
                                        </span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="metric-label">Articles Analyzed</span>
                                        <span className="metric-value">
                                            {report.data?.data_sources?.market_research?.articles_analyzed || 0}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="report-section financial-section">
                                <h4>💰 Financial Metrics</h4>
                                <div className="metrics-grid">
                                    <div className="metric-card">
                                        <span className="metric-label">Current Price</span>
                                        <span className="metric-value">
                                            ${report.data?.data_sources?.financial_analysis?.current_price?.toFixed(2) || 'N/A'}
                                        </span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="metric-label">P/E Ratio</span>
                                        <span className="metric-value">
                                            {typeof report.data?.data_sources?.financial_analysis?.pe_ratio === 'number'
                                                ? report.data.data_sources.financial_analysis.pe_ratio.toFixed(2)
                                                : report.data?.data_sources?.financial_analysis?.pe_ratio || 'N/A'}
                                        </span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="metric-label">ROI (1Y)</span>
                                        <span className="metric-value">
                                            {report.data?.data_sources?.financial_analysis?.roi_1y?.toFixed(2) || 0}%
                                        </span>
                                    </div>
                                    <div className="metric-card">
                                        <span className="metric-label">Volatility</span>
                                        <span className="metric-value">
                                            {report.data?.data_sources?.financial_analysis?.volatility?.toFixed(4) || 'N/A'}
                                        </span>
                                    </div>
                                </div>
                            </div>

                            <div className="report-section analysis-section">
                                <h4>📝 Comprehensive Investment Analysis</h4>
                                <div className="report-text">
                                    {report.data?.report?.full_text ? (
                                        <div className="analysis-content">
                                            {report.data.report.full_text}
                                        </div>
                                    ) : (
                                        <p>Full report generated successfully.</p>
                                    )}
                                </div>
                            </div>
                        </div>
                    )}

                    {/* PDF Preview */}
                    {viewMode === 'pdf' && (
                        <div className="pdf-preview">
                            <iframe
                                src={`${API_URL}/api/reports/${analysisId}/download`}
                                className="pdf-frame"
                                title="PDF Report Preview"
                            />
                        </div>
                    )}

                    {/* Raw JSON Data */}
                    {viewMode === 'json' && (
                        <div className="json-view">
                            <pre>{JSON.stringify(report.data, null, 2)}</pre>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ReportViewer;
