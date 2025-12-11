import React from 'react';

function AgentStatus({ status }) {
    const progress = Math.round((status.progress || 0) * 100);

    const agents = [
        { name: 'Market Researcher', icon: '🔍', stage: 0.4, description: 'MCP News Server' },
        { name: 'Data Analyst', icon: '📊', stage: 0.7, description: 'MCP Financial Server' },
        { name: 'Report Writer', icon: '📝', stage: 1.0, description: 'Google ADK Synthesis' }
    ];

    return (
        <div className="agent-status">
            <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }}>
                    {progress}%
                </div>
            </div>

            <div className="agents">
                {agents.map((agent) => (
                    <div
                        key={agent.name}
                        className={`agent ${status.current_agent === agent.name ? 'active' : ''
                            } ${status.progress >= agent.stage ? 'completed' : ''}`}
                    >
                        <span className="agent-icon">{agent.icon}</span>
                        <span className="agent-name">{agent.name}</span>
                        <span className="agent-description">{agent.description}</span>
                        {status.current_agent === agent.name && (
                            <span className="agent-working">🔄 Working...</span>
                        )}
                        {status.progress >= agent.stage && status.current_agent !== agent.name && (
                            <span className="agent-done">✅</span>
                        )}
                    </div>
                ))}
            </div>

            {status.status === 'processing' && (
                <div className="status-message">
                    <strong>Current Agent:</strong> {status.current_agent}
                    <br />
                    <small>Using MCP protocol for context sharing</small>
                </div>
            )}
        </div>
    );
}

export default AgentStatus;
