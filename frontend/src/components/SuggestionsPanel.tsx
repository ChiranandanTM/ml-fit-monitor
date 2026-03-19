interface SuggestionsPanelProps {
  suggestions: any[];
}

function getPriorityClass(priority: string): string {
  const p = priority?.toUpperCase();
  if (p === "HIGH") return "high";
  if (p === "MEDIUM") return "medium";
  if (p === "LOW") return "low";
  return "info-priority";
}

export default function SuggestionsPanel({ suggestions }: SuggestionsPanelProps) {
  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  return (
    <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
      <div className="section-title">
        <div className="section-icon amber">💡</div>
        <h2>Improvement Suggestions</h2>
      </div>

      <div className="stagger-children">
        {suggestions.map((sugg: any, idx: number) => (
          <div key={idx} style={{ marginBottom: '1.5rem' }}>
            {/* Model Header */}
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              marginBottom: '0.75rem',
            }}>
              <h3 style={{ color: 'var(--text-primary)' }}>{sugg.model}</h3>
              <span className={`status-badge ${sugg.status === "Good Fit" ? "good" :
                  sugg.status === "Overfitting" ? "overfit" : "underfit"
                }`}>
                {sugg.status}
              </span>
            </div>

            {/* Suggestion Items */}
            {sugg.recommendations?.map((rec: any, i: number) => (
              <div
                key={i}
                className={`suggestion-item ${getPriorityClass(rec.priority)}`}
              >
                <div className="suggestion-header">
                  <span className="suggestion-action">{rec.action}</span>
                  <span className={`suggestion-priority ${getPriorityClass(rec.priority)}`}>
                    {rec.priority}
                  </span>
                </div>
                <div className="suggestion-details">{rec.details}</div>
                {(rec.impl_effort || rec.expected_impact) && (
                  <div className="suggestion-meta">
                    {rec.impl_effort && <>Effort: {rec.impl_effort}</>}
                    {rec.impl_effort && rec.expected_impact && <> · </>}
                    {rec.expected_impact && <>Impact: {rec.expected_impact}</>}
                  </div>
                )}

                {/* For Good Fit - show recommendations list */}
                {rec.recommendations && (
                  <ul className="next-steps-list" style={{ marginTop: '0.5rem' }}>
                    {rec.recommendations.map((r: string, j: number) => (
                      <li key={j}>{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
