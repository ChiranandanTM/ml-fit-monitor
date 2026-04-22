interface FitStatusCardProps {
  model: any;
  index: number;
}

function getStatusClass(status: string): string {
  if (status === "Good Fit") return "good";
  if (status === "Overfitting") return "overfit";
  return "underfit";
}

function getStatusEmoji(status: string): string {
  if (status === "Good Fit") return "✅";
  if (status === "Overfitting") return "⚠️";
  return "❌";
}

function getScoreColor(score: number): string {
  if (score >= 0.8) return "green";
  if (score >= 0.65) return "amber";
  return "red";
}

export default function FitStatusCard({ model, index }: FitStatusCardProps) {
  const statusClass = getStatusClass(model.fit_status);
  const gap = Math.abs(model.train_score - model.val_score);

  return (
    <div
      className={`model-card ${statusClass}`}
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      {/* Header */}
      <div className="model-card-header">
        <div>
          <div className="model-card-name">{model.model}</div>
        </div>
        <span className={`status-badge ${statusClass}`}>
          {getStatusEmoji(model.fit_status)} {model.fit_status}
        </span>
      </div>

      {/* Scores Grid */}
      <div className="model-card-scores">
        <div className="score-item">
          <div className="score-label">Train Score</div>
          <div className={`score-value metric-value ${getScoreColor(model.train_score)}`}>
            {(model.train_score * 100).toFixed(1)}%
          </div>
          <div className="progress-bar-container">
            <div
              className="progress-bar-fill"
              style={{
                width: `${model.train_score * 100}%`,
                background: 'var(--gradient-accent)',
              }}
            />
          </div>
        </div>
        <div className="score-item">
          <div className="score-label">Val Score</div>
          <div className={`score-value metric-value ${getScoreColor(model.val_score)}`}>
            {(model.val_score * 100).toFixed(1)}%
          </div>
          <div className="progress-bar-container">
            <div
              className="progress-bar-fill"
              style={{
                width: `${model.val_score * 100}%`,
                background: model.fit_status === "Good Fit"
                  ? 'var(--gradient-good)'
                  : model.fit_status === "Overfitting"
                    ? 'var(--gradient-warn)'
                    : 'var(--gradient-danger)',
              }}
            />
          </div>
        </div>
      </div>

      {/* Additional Stats */}
      <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
        <div className="score-item" style={{ flex: 1, minWidth: '120px' }}>
          <div className="score-label">Gap</div>
          <div className={`score-value metric-value ${gap > 0.15 ? 'red' : gap > 0.08 ? 'amber' : 'green'}`}
            style={{ fontSize: '1rem' }}>
            {(gap * 100).toFixed(1)}%
          </div>
        </div>
        {model.confidence_interval && (
          <div className="score-item" style={{ flex: 2, minWidth: '180px' }}>
            <div className="score-label">95% Confidence Interval</div>
            <div className="score-value" style={{ fontSize: '0.9rem', color: 'var(--accent-cyan)' }}>
              [{(model.confidence_interval[0] * 100).toFixed(1)}% — {(model.confidence_interval[1] * 100).toFixed(1)}%]
            </div>
          </div>
        )}
      </div>

      {/* Detailed Classification Metrics (NEW) */}
      {model.detailed_metrics && Object.keys(model.detailed_metrics).length > 0 && (
        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)' }}>
          <div className="score-label" style={{ marginBottom: '0.75rem', color: 'var(--accent-cyan)' }}>
            📊 Classification Metrics
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '0.5rem' }}>
            {model.detailed_metrics.accuracy !== undefined && (
              <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '0.5rem', borderRadius: '4px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Accuracy</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--accent-cyan)' }}>
                  {((model.detailed_metrics.accuracy || 0) * 100).toFixed(1)}%
                </div>
              </div>
            )}
            {model.detailed_metrics.precision !== undefined && (
              <div style={{ background: 'rgba(34, 197, 94, 0.1)', padding: '0.5rem', borderRadius: '4px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Precision</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--accent-green)' }}>
                  {((model.detailed_metrics.precision || 0) * 100).toFixed(1)}%
                </div>
              </div>
            )}
            {model.detailed_metrics.recall !== undefined && (
              <div style={{ background: 'rgba(168, 85, 247, 0.1)', padding: '0.5rem', borderRadius: '4px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Recall</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--accent-purple)' }}>
                  {((model.detailed_metrics.recall || 0) * 100).toFixed(1)}%
                </div>
              </div>
            )}
            {model.detailed_metrics.f1_score !== undefined && (
              <div style={{ background: 'rgba(249, 115, 22, 0.1)', padding: '0.5rem', borderRadius: '4px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>F1 Score</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--accent-amber)' }}>
                  {((model.detailed_metrics.f1_score || 0) * 100).toFixed(1)}%
                </div>
              </div>
            )}
            {model.detailed_metrics.roc_auc !== undefined && model.detailed_metrics.roc_auc !== null && (
              <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: '0.5rem', borderRadius: '4px' }}>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>ROC-AUC</div>
                <div style={{ fontSize: '1rem', fontWeight: 'bold', color: 'var(--accent-yellow)' }}>
                  {((model.detailed_metrics.roc_auc || 0) * 100).toFixed(1)}%
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
