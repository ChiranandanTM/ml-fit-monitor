import React from 'react';
import FitStatusCard from './FitStatusCard';
import FeatureImportance from './FeatureImportance';
import DataProfilingDashboard from './DataProfilingDashboard';

export default function AgentPanel({ agentResult }: { agentResult: any }) {
  if (!agentResult) return null;

  const { trace, final_result, models, feature_importance } = agentResult;

  return (
    <div className="agent-panel" style={{ marginTop: '2rem' }}>
      <div className="section-title">
        <div className="section-icon purple">🤖</div>
        <h2>Agentic Analysis Trace</h2>
      </div>
      
      <div className="timeline" style={{ position: 'relative', paddingLeft: '1.5rem', borderLeft: '2px solid rgba(255, 255, 255, 0.1)', marginBottom: '2rem' }}>
        {trace.map((step: any, idx: number) => (
          <div key={idx} className="glass-card animate-fade-in-up" style={{ marginBottom: '1.5rem', position: 'relative' }}>
            <div style={{
              position: 'absolute',
              left: '-2.15rem',
              top: '1.5rem',
              width: '1.25rem',
              height: '1.25rem',
              borderRadius: '50%',
              background: step.improved ? 'var(--accent-green)' : 'var(--accent-amber)',
              border: '3px solid var(--bg-primary)'
            }} />
            
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
              <h3 style={{ color: 'var(--text-primary)', margin: 0 }}>Step {step.step_number}</h3>
              {step.improved !== undefined && (
                <span className={`status-badge ${step.improved ? 'good' : 'overfit'}`}>
                  {step.improved ? '✅ Improved' : 'No Improvement'}
                </span>
              )}
            </div>
            
            <div style={{ display: 'grid', gap: '0.75rem' }}>
              <div>
                <strong style={{ color: 'var(--accent-cyan)' }}>Observation:</strong>
                <div style={{ color: 'var(--text-secondary)' }}>{step.observation}</div>
              </div>
              <div>
                <strong style={{ color: 'var(--accent-purple)' }}>Reasoning:</strong>
                <div style={{ color: 'var(--text-secondary)' }}>{step.decision_reasoning}</div>
              </div>
              <div>
                <strong style={{ color: 'var(--accent-amber)' }}>Action:</strong>
                <div style={{ color: 'var(--text-secondary)' }}>{step.action_taken}</div>
              </div>
              {step.result && typeof step.result === 'string' && (
                <div>
                  <strong style={{ color: 'var(--text-primary)' }}>Result:</strong>
                  <div style={{ color: 'var(--text-secondary)' }}>{step.result}</div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {final_result && (
        <div style={{ marginTop: '2rem' }}>
          <div className="section-title">
            <div className="section-icon green">✅</div>
            <h2>Final Result</h2>
          </div>
          
          {final_result.data_profile && (
            <div style={{ marginBottom: '1.5rem' }}>
              <DataProfilingDashboard profile={final_result.data_profile} />
            </div>
          )}
          
          <div className="model-cards-grid stagger-children" style={{ marginBottom: '1.5rem' }}>
            {models.map((m: any, idx: number) => (
              <FitStatusCard key={idx} model={m} index={idx} />
            ))}
          </div>
          
          {feature_importance && Object.keys(feature_importance).length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              <FeatureImportance features={
                Object.values(feature_importance)[0]?.plot_data || []
              } />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
