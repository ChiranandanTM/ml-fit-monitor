import { useState } from 'react';
import { ArrowUp, ArrowDown, TrendingUp } from 'lucide-react';

interface MetricDelta {
  metric: string;
  before: number;
  after: number;
  absolute_delta: number;
  percent_delta: number;
  improved: boolean;
}

interface ExperimentMetrics {
  id: string;
  timestamp: string;
  best_model: string;
  status: string;
}

interface MetricsDeltaTableProps {
  experiment1: ExperimentMetrics;
  experiment2: ExperimentMetrics;
  deltas: MetricDelta[];
  tuningImprovements?: {
    exp1_models_tuned: number;
    exp2_models_tuned: number;
  };
}

function getStatusColor(status: string): string {
  if (status === "Good Fit") return "#10b981";
  if (status === "Overfitting") return "#f59e0b";
  return "#ef4444";
}

export default function MetricsDeltaTable({ 
  experiment1, 
  experiment2, 
  deltas,
  tuningImprovements 
}: MetricsDeltaTableProps) {
  const [expandedMetric, setExpandedMetric] = useState<string | null>(null);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const getImprovementBadge = (improved: boolean, metric: string) => {
    // For gap metric, the logic is inverted (smaller gap is better)
    const isPositive = metric === 'Generalization Gap' ? !improved : improved;
    
    if (isPositive) {
      return (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          color: '#10b981',
          fontSize: '0.85rem',
          fontWeight: 600,
          padding: '0.4rem 0.8rem',
          background: 'rgba(16, 185, 129, 0.1)',
          borderRadius: '0.4rem',
          border: '1px solid rgba(16, 185, 129, 0.2)'
        }}>
          <ArrowUp size={16} />
          Improved
        </div>
      );
    } else {
      return (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          color: '#ef4444',
          fontSize: '0.85rem',
          fontWeight: 600,
          padding: '0.4rem 0.8rem',
          background: 'rgba(239, 68, 68, 0.1)',
          borderRadius: '0.4rem',
          border: '1px solid rgba(239, 68, 68, 0.2)'
        }}>
          <ArrowDown size={16} />
          Declined
        </div>
      );
    }
  };

  return (
    <div style={{
      background: 'var(--bg-card)',
      borderRadius: 'var(--radius-lg)',
      border: '1px solid var(--border-default)',
      overflow: 'hidden',
      animation: 'fadeIn 0.6s ease-out'
    }}>
      {/* Header */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '1rem',
        padding: '1.5rem',
        borderBottom: '1px solid var(--border-subtle)',
        background: 'linear-gradient(135deg, rgba(99,102,241,0.05), rgba(139,92,246,0.05))'
      }}>
        {/* Exp 1 */}
        <div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem' }}>
            EXPERIMENT 1 (Before)
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <div style={{
              fontSize: '0.9rem',
              color: 'var(--text-secondary)',
              marginBottom: '0.25rem'
            }}>
              {experiment1.best_model}
            </div>
            <div style={{
              display: 'inline-block',
              padding: '0.3rem 0.8rem',
              background: getStatusColor(experiment1.status),
              color: 'white',
              borderRadius: '0.3rem',
              fontSize: '0.75rem',
              fontWeight: 600
            }}>
              {experiment1.status}
            </div>
          </div>
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-tertiary)',
            marginTop: '0.5rem'
          }}>
            {formatDate(experiment1.timestamp)}
          </div>
        </div>

        {/* Exp 2 */}
        <div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem' }}>
            EXPERIMENT 2 (After)
          </div>
          <div style={{ marginBottom: '0.5rem' }}>
            <div style={{
              fontSize: '0.9rem',
              color: 'var(--text-secondary)',
              marginBottom: '0.25rem'
            }}>
              {experiment2.best_model}
            </div>
            <div style={{
              display: 'inline-block',
              padding: '0.3rem 0.8rem',
              background: getStatusColor(experiment2.status),
              color: 'white',
              borderRadius: '0.3rem',
              fontSize: '0.75rem',
              fontWeight: 600
            }}>
              {experiment2.status}
            </div>
          </div>
          <div style={{
            fontSize: '0.75rem',
            color: 'var(--text-tertiary)',
            marginTop: '0.5rem'
          }}>
            {formatDate(experiment2.timestamp)}
          </div>
        </div>
      </div>

      {/* Metrics Table */}
      <div style={{
        overflowX: 'auto'
      }}>
        <table style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontSize: '0.9rem'
        }}>
          <thead>
            <tr style={{
              background: 'rgba(99, 102, 241, 0.03)',
              borderBottom: '1px solid var(--border-subtle)'
            }}>
              <th style={{
                padding: '1rem',
                textAlign: 'left',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>Metric</th>
              <th style={{
                padding: '1rem',
                textAlign: 'right',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>Before</th>
              <th style={{
                padding: '1rem',
                textAlign: 'right',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>After</th>
              <th style={{
                padding: '1rem',
                textAlign: 'right',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>Delta</th>
              <th style={{
                padding: '1rem',
                textAlign: 'left',
                color: 'var(--text-secondary)',
                fontWeight: 600,
                fontSize: '0.85rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {deltas.map((delta, idx) => (
              <tr
                key={idx}
                onClick={() => setExpandedMetric(expandedMetric === delta.metric ? null : delta.metric)}
                style={{
                  borderBottom: '1px solid var(--border-subtle)',
                  background: expandedMetric === delta.metric ? 'rgba(99, 102, 241, 0.05)' : 'transparent',
                  cursor: 'pointer',
                  transition: 'background 0.2s ease'
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLTableRowElement).style.background = 'rgba(99, 102, 241, 0.08)';
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLTableRowElement).style.background = 
                    expandedMetric === delta.metric ? 'rgba(99, 102, 241, 0.05)' : 'transparent';
                }}
              >
                {/* Metric Name */}
                <td style={{
                  padding: '1rem',
                  color: 'var(--text-primary)',
                  fontWeight: 500
                }}>
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <TrendingUp size={16} style={{ color: 'var(--accent-purple)' }} />
                    {delta.metric}
                  </div>
                </td>

                {/* Before */}
                <td style={{
                  padding: '1rem',
                  textAlign: 'right',
                  color: 'var(--text-secondary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.9rem'
                }}>
                  {(delta.before * 100).toFixed(2)}%
                </td>

                {/* After */}
                <td style={{
                  padding: '1rem',
                  textAlign: 'right',
                  color: 'var(--text-secondary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.9rem',
                  fontWeight: 600
                }}>
                  {(delta.after * 100).toFixed(2)}%
                </td>

                {/* Delta */}
                <td style={{
                  padding: '1rem',
                  textAlign: 'right',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.9rem',
                  fontWeight: 600,
                  color: delta.improved ? '#10b981' : '#ef4444'
                }}>
                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.25rem'
                  }}>
                    {delta.improved ? '+' : ''}{(delta.absolute_delta * 100).toFixed(2)}%
                    ({delta.improved ? '+' : ''}{delta.percent_delta.toFixed(1)}%)
                  </span>
                </td>

                {/* Status */}
                <td style={{
                  padding: '1rem',
                  textAlign: 'left'
                }}>
                  {getImprovementBadge(delta.improved, delta.metric)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Tuning Summary */}
      {tuningImprovements && (
        <div style={{
          padding: '1rem',
          background: 'rgba(99, 102, 241, 0.05)',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <h4 style={{
              margin: '0 0 0.5rem 0',
              fontSize: '0.9rem',
              color: 'var(--text-primary)',
              fontWeight: 600
            }}>
              Hyperparameter Tuning Summary
            </h4>
            <p style={{
              margin: 0,
              fontSize: '0.85rem',
              color: 'var(--text-secondary)'
            }}>
              Experiment 1: {tuningImprovements.exp1_models_tuned} models optimized
              {' | '}
              Experiment 2: {tuningImprovements.exp2_models_tuned} models optimized
            </p>
          </div>
          <div style={{
            padding: '0.5rem 1rem',
            background: 'var(--gradient-accent)',
            color: 'white',
            borderRadius: '0.4rem',
            fontSize: '0.85rem',
            fontWeight: 600
          }}>
            {tuningImprovements.exp2_models_tuned > tuningImprovements.exp1_models_tuned 
              ? `+${tuningImprovements.exp2_models_tuned - tuningImprovements.exp1_models_tuned} more tuned`
              : 'Tuning maintained'
            }
          </div>
        </div>
      )}
    </div>
  );
}
