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
    </div>
  );
}
