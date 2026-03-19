interface ModelAnalysisDetailProps {
    modelAnalysis: any[];
}

function getStatusClass(status: string): string {
    if (status === "Good Fit") return "good";
    if (status === "Overfitting") return "overfit";
    return "underfit";
}

function getSeverityColor(severity: string): string {
    const s = severity?.toLowerCase();
    if (s?.includes("minimal") || s?.includes("none") || s?.includes("low")) return "var(--accent-green)";
    if (s?.includes("moderate") || s?.includes("medium")) return "var(--accent-amber)";
    return "var(--accent-red)";
}

export default function ModelAnalysisDetail({ modelAnalysis }: ModelAnalysisDetailProps) {
    if (!modelAnalysis || modelAnalysis.length === 0) return null;

    return (
        <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
            <div className="section-title">
                <div className="section-icon blue">🔬</div>
                <h2>Detailed Model Analysis</h2>
            </div>

            <div className="stagger-children">
                {modelAnalysis.map((model: any, idx: number) => (
                    <div
                        key={idx}
                        className={`model-card ${getStatusClass(model.fit_diagnosis?.status)}`}
                        style={{ marginBottom: '1.25rem' }}
                    >
                        {/* Header */}
                        <div className="model-card-header">
                            <h3 className="model-card-name">{model.model_name}</h3>
                            <span className={`status-badge ${getStatusClass(model.fit_diagnosis?.status)}`}>
                                {model.fit_diagnosis?.status}
                            </span>
                        </div>

                        {/* Performance Metrics */}
                        <div className="metric-grid" style={{ marginBottom: '1rem' }}>
                            <div className="metric-card">
                                <div className="metric-label">Training</div>
                                <div className="metric-value cyan" style={{ fontSize: '1.2rem' }}>
                                    {model.performance?.train_score}
                                </div>
                            </div>
                            <div className="metric-card">
                                <div className="metric-label">Validation</div>
                                <div className="metric-value green" style={{ fontSize: '1.2rem' }}>
                                    {model.performance?.val_score}
                                </div>
                            </div>
                            <div className="metric-card">
                                <div className="metric-label">Gap</div>
                                <div className="metric-value amber" style={{ fontSize: '1.2rem' }}>
                                    {model.performance?.gap}
                                </div>
                            </div>
                            <div className="metric-card">
                                <div className="metric-label">CV Confidence</div>
                                <div className="metric-value purple" style={{ fontSize: '1rem' }}>
                                    {model.performance?.cv_confidence}
                                </div>
                            </div>
                        </div>

                        {/* Fit Diagnosis */}
                        {model.fit_diagnosis && (
                            <div className="info-box cyan">
                                <p style={{ marginBottom: '0.4rem' }}>
                                    <strong style={{ color: 'var(--text-primary)' }}>Summary:</strong>{' '}
                                    <span style={{ color: 'var(--text-secondary)' }}>{model.fit_diagnosis.summary}</span>
                                </p>
                                <p style={{ marginBottom: '0.4rem' }}>
                                    <strong style={{ color: 'var(--text-primary)' }}>Signal:</strong>{' '}
                                    <span style={{ color: 'var(--text-secondary)' }}>{model.fit_diagnosis.signal}</span>
                                </p>
                                <p>
                                    <strong style={{ color: 'var(--text-primary)' }}>Severity:</strong>{' '}
                                    <span style={{ color: getSeverityColor(model.fit_diagnosis.severity) }}>
                                        {model.fit_diagnosis.severity}
                                    </span>
                                </p>
                            </div>
                        )}

                        {/* Next Steps */}
                        {model.fit_diagnosis?.next_steps && model.fit_diagnosis.next_steps.length > 0 && (
                            <div style={{ marginTop: '1rem' }}>
                                <p style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                                    Recommended Next Steps:
                                </p>
                                <ul className="next-steps-list">
                                    {model.fit_diagnosis.next_steps.map((step: string, i: number) => (
                                        <li key={i}>{step}</li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}
