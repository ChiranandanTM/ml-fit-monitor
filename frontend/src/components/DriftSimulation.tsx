interface DriftSimulationProps {
  driftData: any;
}

function getUrgencyClass(urgency: string): string {
  const u = urgency?.toUpperCase();
  if (u === "IMMEDIATE") return "immediate";
  if (u === "PLANNED") return "planned";
  return "scheduled";
}

export default function DriftSimulation({ driftData }: DriftSimulationProps) {
  if (!driftData) return null;

  // Handle drift data from /drift-simulate endpoint
  if (driftData.simulation_summary) {
    return (
      <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
        <div className="section-title">
          <div className="section-icon pink">📈</div>
          <h2>Data Drift Simulation Report</h2>
        </div>

        <div className="info-box cyan" style={{ marginBottom: '1.25rem' }}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Simulation:</strong> {driftData.simulation_summary}
          </p>
          <p style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem', marginTop: '0.35rem' }}>
            Tested severity levels: {driftData.severity_tested?.map((s: number) => `${(s * 100).toFixed(0)}%`).join(', ')}
          </p>
        </div>

        <div className="stagger-children">
          {driftData.models?.map((m: any, idx: number) => (
            <div key={idx} className="drift-card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <h3 style={{ color: 'var(--text-primary)' }}>{m.model_name}</h3>
                <span className={`urgency-badge ${getUrgencyClass(m.retraining_urgency)}`}>
                  {m.retraining_urgency}
                </span>
              </div>

              <div className="drift-stats">
                <div className="drift-stat">
                  <div className="drift-stat-label">Original Score</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-green)' }}>
                    {m.original_score}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Worst Case</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-red)' }}>
                    {m.worst_case}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Critical At</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-amber)' }}>
                    {m.critical_threshold ? `${(m.critical_threshold * 100).toFixed(0)}%` : 'N/A'}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Monitoring</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-cyan)', fontSize: '0.95rem' }}>
                    {m.monitoring_recommendation || 'daily'}
                  </div>
                </div>
              </div>

              {/* Trigger Events */}
              {m.trigger_events && m.trigger_events.length > 0 && (
                <div style={{ marginTop: '1rem' }}>
                  <p style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.5rem' }}>
                    Retraining Triggers:
                  </p>
                  {m.trigger_events.map((t: any, i: number) => (
                    <div key={i} className="trigger-item">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem' }}>
                        <strong style={{ fontSize: '0.85rem', color: 'var(--text-primary)' }}>
                          {t.trigger_level}
                        </strong>
                        <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', fontFamily: 'var(--font-mono)' }}>
                          @ {typeof t.severity === 'number' ? `${(t.severity * 100).toFixed(0)}%` : t.severity} drift
                        </span>
                      </div>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{t.reason}</p>
                      {t.recommended_action && (
                        <p style={{ fontSize: '0.76rem', color: 'var(--accent-cyan)', fontStyle: 'italic', marginTop: '0.2rem' }}>
                          Action: {t.recommended_action}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Handle drift from /analyze endpoint (models_detailed)
  if (driftData.models_detailed) {
    return (
      <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
        <div className="section-title">
          <div className="section-icon pink">📈</div>
          <h2>Data Drift Simulation</h2>
        </div>

        <div className="stagger-children">
          {driftData.models_detailed.map((drift: any, idx: number) => (
            <div key={idx} className="drift-card">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                <h3 style={{ color: 'var(--text-primary)' }}>{drift.model}</h3>
                {drift.retraining_urgency && (
                  <span className={`urgency-badge ${getUrgencyClass(drift.retraining_urgency)}`}>
                    {drift.retraining_urgency}
                  </span>
                )}
              </div>

              <div className="drift-stats">
                <div className="drift-stat">
                  <div className="drift-stat-label">Original Performance</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-green)' }}>
                    {drift.original_performance}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Worst Case</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-red)' }}>
                    {drift.worst_case_performance}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Critical Drift</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-amber)' }}>
                    {drift.critical_drift_point ? `${(drift.critical_drift_point * 100).toFixed(0)}%` : 'N/A'}
                  </div>
                </div>
                <div className="drift-stat">
                  <div className="drift-stat-label">Monitoring</div>
                  <div className="drift-stat-value" style={{ color: 'var(--accent-cyan)', fontSize: '0.95rem' }}>
                    {drift.recommended_monitoring_frequency || 'daily'}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return null;
}
