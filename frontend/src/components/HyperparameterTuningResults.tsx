import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Settings, Check } from 'lucide-react';

interface TuningResult {
  model_name: string;
  fit_status: string;
  tuned: boolean;
  baseline_train_score: number;
  baseline_val_score: number;
  baseline_gap: number;
  tuned_train_score: number;
  tuned_val_score: number;
  tuned_gap: number;
  train_improvement: number;
  val_improvement: number;
  gap_improvement: number;
  best_params?: Record<string, any>;
}

interface HyperparameterTuningResultsProps {
  results: TuningResult[];
}

export default function HyperparameterTuningResults({
  results
}: HyperparameterTuningResultsProps) {
  const tuned = results.filter(r => r.tuned);
  const notTuned = results.filter(r => !r.tuned);

  // Prepare data for chart
  const chartData = tuned.map(r => ({
    name: r.model_name,
    'Baseline Train': r.baseline_train_score,
    'Tuned Train': r.tuned_train_score,
    'Baseline Val': r.baseline_val_score,
    'Tuned Val': r.tuned_val_score
  }));

  const gapData = tuned.map(r => ({
    name: r.model_name,
    'Before': r.baseline_gap,
    'After': r.tuned_gap
  }));

  const getImprovementColor = (value: number) => {
    if (value > 0.05) return '#10b981';
    if (value > 0) return '#3b82f6';
    return '#ef4444';
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem',
      animation: 'fadeInUp 0.6s ease-out'
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem'
      }}>
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '0.5rem',
          background: 'var(--gradient-accent)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white'
        }}>
          <Settings size={22} />
        </div>
        <div>
          <h2 style={{
            margin: 0,
            fontSize: '1.25rem',
            color: 'var(--text-primary)',
            fontWeight: 600
          }}>
            Hyperparameter Tuning Results
          </h2>
          <p style={{
            margin: '0.25rem 0 0 0',
            fontSize: '0.85rem',
            color: 'var(--text-tertiary)'
          }}>
            {tuned.length} model{tuned.length !== 1 ? 's' : ''} tuned · {notTuned.length} model{notTuned.length !== 1 ? 's' : ''} not applicable
          </p>
        </div>
      </div>

      {/* Summary Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
        gap: '1rem'
      }}>
        <div style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-default)',
          padding: '1.25rem'
        }}>
          <div style={{
            fontSize: '0.8rem',
            color: 'var(--text-tertiary)',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Models Tuned
          </div>
          <div style={{
            fontSize: '1.75rem',
            fontWeight: 700,
            color: 'var(--text-primary)'
          }}>
            {tuned.length}
          </div>
        </div>

        <div style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-default)',
          padding: '1.25rem'
        }}>
          <div style={{
            fontSize: '0.8rem',
            color: 'var(--text-tertiary)',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Avg Val Improvement
          </div>
          <div style={{
            fontSize: '1.75rem',
            fontWeight: 700,
            color: tuned.length > 0 && tuned.reduce((a, b) => a + b.val_improvement, 0) / tuned.length > 0
              ? '#10b981'
              : '#ef4444'
          }}>
            {tuned.length > 0
              ? `+${((tuned.reduce((a, b) => a + b.val_improvement, 0) / tuned.length) * 100).toFixed(1)}%`
              : 'N/A'}
          </div>
        </div>

        <div style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-default)',
          padding: '1.25rem'
        }}>
          <div style={{
            fontSize: '0.8rem',
            color: 'var(--text-tertiary)',
            marginBottom: '0.5rem',
            textTransform: 'uppercase',
            letterSpacing: '0.5px'
          }}>
            Avg Gap Reduction
          </div>
          <div style={{
            fontSize: '1.75rem',
            fontWeight: 700,
            color: tuned.length > 0 && tuned.reduce((a, b) => a + b.gap_improvement, 0) / tuned.length > 0
              ? '#10b981'
              : '#ef4444'
          }}>
            {tuned.length > 0
              ? `-${((tuned.reduce((a, b) => a + b.gap_improvement, 0) / tuned.length) * 100).toFixed(1)}%`
              : 'N/A'}
          </div>
        </div>
      </div>

      {/* Charts */}
      {tuned.length > 0 && (
        <>
          {/* Score Comparison */}
          <div style={{
            background: 'var(--bg-card)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-default)',
            padding: '1.5rem'
          }}>
            <h3 style={{
              margin: '0 0 1rem 0',
              fontSize: '1rem',
              color: 'var(--text-primary)',
              fontWeight: 600
            }}>
              Score Improvements
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <XAxis
                  dataKey="name"
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border-subtle)' }}
                />
                <YAxis
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border-subtle)' }}
                />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-default)',
                    borderRadius: '0.4rem',
                    color: 'var(--text-primary)'
                  }}
                  formatter={(value: any) => `${(value * 100).toFixed(1)}%`}
                />
                <Legend />
                <Bar dataKey="Baseline Train" fill="#fee2e2" />
                <Bar dataKey="Tuned Train" fill="#10b981" />
                <Bar dataKey="Baseline Val" fill="#fecaca" />
                <Bar dataKey="Tuned Val" fill="#34d399" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Gap Reduction */}
          <div style={{
            background: 'var(--bg-card)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-default)',
            padding: '1.5rem'
          }}>
            <h3 style={{
              margin: '0 0 1rem 0',
              fontSize: '1rem',
              color: 'var(--text-primary)',
              fontWeight: 600
            }}>
              Generalization Gap Reduction
            </h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={gapData}>
                <XAxis
                  dataKey="name"
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border-subtle)' }}
                />
                <YAxis
                  tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
                  axisLine={{ stroke: 'var(--border-subtle)' }}
                />
                <Tooltip
                  contentStyle={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-default)',
                    borderRadius: '0.4rem',
                    color: 'var(--text-primary)'
                  }}
                  formatter={(value: any) => `${(value * 100).toFixed(1)}%`}
                />
                <Legend />
                <Bar dataKey="Before" fill="#fecaca" />
                <Bar dataKey="After" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}

      {/* Detailed Results */}
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-default)',
        overflow: 'hidden'
      }}>
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          background: 'linear-gradient(135deg, rgba(99,102,241,0.05), rgba(139,92,246,0.05))'
        }}>
          <h3 style={{
            margin: 0,
            fontSize: '1rem',
            color: 'var(--text-primary)',
            fontWeight: 600
          }}>
            Detailed Tuning Results
          </h3>
        </div>

        <div style={{
          borderTop: '1px solid var(--border-subtle)'
        }}>
          {tuned.map((result, idx) => (
            <div
              key={idx}
              style={{
                padding: '1.5rem',
                borderTop: idx > 0 ? '1px solid var(--border-subtle)' : 'none'
              }}
            >
              {/* Model Header */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '1rem'
              }}>
                <div>
                  <h4 style={{
                    margin: '0 0 0.25rem 0',
                    fontSize: '1rem',
                    color: 'var(--text-primary)',
                    fontWeight: 600,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <Check size={18} style={{ color: '#10b981' }} />
                    {result.model_name}
                  </h4>
                  <div style={{
                    fontSize: '0.8rem',
                    color: 'var(--text-tertiary)'
                  }}>
                    Status: <strong>{result.fit_status}</strong>
                  </div>
                </div>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem'
                }}>
                  <div style={{
                    textAlign: 'right'
                  }}>
                    <div style={{
                      fontSize: '0.8rem',
                      color: 'var(--text-tertiary)',
                      marginBottom: '0.25rem'
                    }}>
                      Val Score Improvement
                    </div>
                    <div style={{
                      fontSize: '1.25rem',
                      fontWeight: 700,
                      color: getImprovementColor(result.val_improvement)
                    }}>
                      {result.val_improvement > 0 ? '+' : ''}{(result.val_improvement * 100).toFixed(2)}%
                    </div>
                  </div>
                  <div style={{
                    textAlign: 'right'
                  }}>
                    <div style={{
                      fontSize: '0.8rem',
                      color: 'var(--text-tertiary)',
                      marginBottom: '0.25rem'
                    }}>
                      Gap Improvement
                    </div>
                    <div style={{
                      fontSize: '1.25rem',
                      fontWeight: 700,
                      color: getImprovementColor(result.gap_improvement)
                    }}>
                      {result.gap_improvement > 0 ? '+' : ''}{(result.gap_improvement * 100).toFixed(2)}%
                    </div>
                  </div>
                </div>
              </div>

              {/* Metrics Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '1rem',
                marginBottom: '1rem'
              }}>
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginBottom: '0.25rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    Train Score
                  </div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', marginBottom: '0.25rem' }}>
                    <span style={{ textDecoration: 'line-through', opacity: 0.5 }}>
                      {(result.baseline_train_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, color: '#10b981', fontFamily: 'var(--font-mono)' }}>
                    {(result.tuned_train_score * 100).toFixed(1)}%
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginBottom: '0.25rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    Val Score
                  </div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', marginBottom: '0.25rem' }}>
                    <span style={{ textDecoration: 'line-through', opacity: 0.5 }}>
                      {(result.baseline_val_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, color: '#10b981', fontFamily: 'var(--font-mono)' }}>
                    {(result.tuned_val_score * 100).toFixed(1)}%
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', marginBottom: '0.25rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    Gen. Gap
                  </div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', fontFamily: 'var(--font-mono)', marginBottom: '0.25rem' }}>
                    <span style={{ textDecoration: 'line-through', opacity: 0.5 }}>
                      {(result.baseline_gap * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, color: '#10b981', fontFamily: 'var(--font-mono)' }}>
                    {(result.tuned_gap * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* Best Params */}
              {result.best_params && Object.keys(result.best_params).length > 0 && (
                <div style={{
                  padding: '1rem',
                  background: 'rgba(99, 102, 241, 0.05)',
                  borderRadius: '0.4rem',
                  border: '1px solid rgba(99, 102, 241, 0.1)'
                }}>
                  <div style={{
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    color: 'var(--text-secondary)',
                    marginBottom: '0.5rem'
                  }}>
                    Optimized Parameters:
                  </div>
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                    gap: '0.5rem'
                  }}>
                    {Object.entries(result.best_params).map(([key, value], pidx) => (
                      <div key={pidx} style={{
                        fontSize: '0.8rem',
                        fontFamily: 'var(--font-mono)',
                        color: 'var(--text-secondary)'
                      }}>
                        <strong>{key}:</strong> {String(value).substring(0, 30)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}

          {/* Not Tuned Models */}
          {notTuned.length > 0 && (
            <div style={{
              padding: '1.5rem',
              borderTop: tuned.length > 0 ? '2px solid var(--border-subtle)' : 'none',
              background: 'rgba(156, 163, 175, 0.03)'
            }}>
              <h4 style={{
                margin: '0 0 0.75rem 0',
                fontSize: '0.95rem',
                color: 'var(--text-secondary)',
                fontWeight: 600
              }}>
                Models Not Tuned
              </h4>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
                gap: '0.5rem'
              }}>
                {notTuned.map((model, idx) => (
                  <div key={idx} style={{
                    padding: '0.5rem 0.75rem',
                    background: 'var(--border-subtle)',
                    borderRadius: '0.3rem',
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)'
                  }}>
                    {model.model_name}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
