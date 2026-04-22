import { useState, useEffect } from 'react';
import { Clock, Tag, TrendingUp, Download } from 'lucide-react';

interface ExperimentHistoryItem {
  id: string;
  timestamp: string;
  fit_status: string;
  best_model: string;
  tags: string[];
}

export default function ExperimentHistory() {
  const [experiments, setExperiments] = useState<ExperimentHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("");
  const [trends, setTrends] = useState<any>(null);

  useEffect(() => {
    loadExperiments();
    loadTrends();
  }, []);

  const loadExperiments = async () => {
    try {
      setLoading(true);
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(
        `${apiUrl}/experiments/list?limit=20`
      );
      if (response.ok) {
        const data = await response.json();
        setExperiments(data.experiments || []);
      }
    } catch (err) {
      console.error("Failed to load experiments:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadTrends = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(
        `${apiUrl}/experiments/trends?window_size=10`
      );
      if (response.ok) {
        const data = await response.json();
        setTrends(data.trends || {});
      }
    } catch (err) {
      console.error("Failed to load trends:", err);
    }
  };

  const getStatusColor = (status: string): string => {
    if (status === "Good Fit") return "#10b981";
    if (status === "Overfitting") return "#f59e0b";
    return "#ef4444";
  };

  const getStatusEmoji = (status: string): string => {
    if (status === "Good Fit") return "✅";
    if (status === "Overfitting") return "⚠️";
    return "❌";
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const filteredExperiments = experiments.filter(exp => {
    if (!filter) return true;
    return (
      exp.fit_status.toLowerCase().includes(filter.toLowerCase()) ||
      exp.best_model.toLowerCase().includes(filter.toLowerCase()) ||
      exp.tags.some(tag => tag.toLowerCase().includes(filter.toLowerCase()))
    );
  });

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem',
      animation: 'fadeInUp 0.6s ease-out'
    }}>
      {/* Header with Trends */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem'
      }}>
        {/* Total Experiments Card */}
        <div style={{
          background: 'var(--bg-card)',
          borderRadius: 'var(--radius-lg)',
          border: '1px solid var(--border-default)',
          padding: '1.5rem'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <div>
              <div style={{
                fontSize: '0.85rem',
                color: 'var(--text-tertiary)',
                marginBottom: '0.25rem',
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                Total Experiments
              </div>
              <div style={{
                fontSize: '2rem',
                fontWeight: 700,
                color: 'var(--text-primary)'
              }}>
                {experiments.length}
              </div>
            </div>
            <Clock size={32} style={{ color: 'var(--accent-purple)', opacity: 0.5 }} />
          </div>
        </div>

        {/* Trend Card */}
        {trends && (
          <div style={{
            background: 'var(--bg-card)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-default)',
            padding: '1.5rem'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div>
                <div style={{
                  fontSize: '0.85rem',
                  color: 'var(--text-tertiary)',
                  marginBottom: '0.25rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px'
                }}>
                  Recent Trend
                </div>
                <div style={{
                  fontSize: '1.25rem',
                  fontWeight: 700,
                  color: trends.trend === 'improving' ? '#10b981' : trends.trend === 'degrading' ? '#ef4444' : '#f59e0b',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  {trends.trend === 'improving' ? '📈' : trends.trend === 'degrading' ? '📉' : '→'}
                  {trends.trend?.charAt(0).toUpperCase() + trends.trend?.slice(1)}
                </div>
              </div>
              <TrendingUp size={32} style={{ color: 'var(--accent-blue)', opacity: 0.5 }} />
            </div>
          </div>
        )}

        {/* Most Common Status Card */}
        {trends && (
          <div style={{
            background: 'var(--bg-card)',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-default)',
            padding: '1.5rem'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div>
                <div style={{
                  fontSize: '0.85rem',
                  color: 'var(--text-tertiary)',
                  marginBottom: '0.25rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px'
                }}>
                  Most Common
                </div>
                <div style={{
                  fontSize: '1.25rem',
                  fontWeight: 700,
                  color: getStatusColor(trends.most_common_status)
                }}>
                  {getStatusEmoji(trends.most_common_status)} {trends.most_common_status}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Experiments List */}
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-default)',
        overflow: 'hidden'
      }}>
        {/* Header */}
        <div style={{
          padding: '1.5rem',
          borderBottom: '1px solid var(--border-subtle)',
          background: 'linear-gradient(135deg, rgba(99,102,241,0.05), rgba(139,92,246,0.05))'
        }}>
          <h3 style={{
            margin: '0 0 1rem 0',
            fontSize: '1.1rem',
            color: 'var(--text-primary)',
            fontWeight: 600
          }}>
            Experiment History
          </h3>
          <input
            type="text"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Search by status, model, or tags..."
            style={{
              width: '100%',
              padding: '0.75rem',
              borderRadius: '0.4rem',
              border: '1px solid var(--border-default)',
              background: 'var(--bg-input)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem'
            }}
          />
        </div>

        {/* Experiments List */}
        {loading ? (
          <div style={{
            padding: '2rem',
            textAlign: 'center',
            color: 'var(--text-tertiary)'
          }}>
            Loading experiments...
          </div>
        ) : filteredExperiments.length === 0 ? (
          <div style={{
            padding: '2rem',
            textAlign: 'center',
            color: 'var(--text-tertiary)'
          }}>
            No experiments found
          </div>
        ) : (
          <div style={{
            maxHeight: '600px',
            overflowY: 'auto',
            borderTop: '1px solid var(--border-subtle)'
          }}>
            {filteredExperiments.map((exp, idx) => (
              <div
                key={exp.id}
                style={{
                  padding: '1rem',
                  borderTop: idx > 0 ? '1px solid var(--border-subtle)' : 'none',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  transition: 'background 0.2s ease',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLDivElement).style.background = 'rgba(99, 102, 241, 0.05)';
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLDivElement).style.background = 'transparent';
                }}
              >
                <div style={{
                  flex: 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem'
                }}>
                  {/* Status Badge */}
                  <div style={{
                    padding: '0.5rem 0.75rem',
                    background: getStatusColor(exp.fit_status),
                    color: 'white',
                    borderRadius: '0.3rem',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    minWidth: '80px',
                    textAlign: 'center'
                  }}>
                    {getStatusEmoji(exp.fit_status)} {exp.fit_status}
                  </div>

                  {/* Info */}
                  <div style={{
                    flex: 1
                  }}>
                    <div style={{
                      fontSize: '0.9rem',
                      color: 'var(--text-primary)',
                      marginBottom: '0.25rem',
                      fontWeight: 500
                    }}>
                      {exp.best_model}
                    </div>
                    <div style={{
                      fontSize: '0.8rem',
                      color: 'var(--text-tertiary)',
                      display: 'flex',
                      gap: '1rem'
                    }}>
                      <span>{formatDate(exp.timestamp)}</span>
                      <span style={{ fontFamily: 'var(--font-mono)' }}>
                        ID: {exp.id.slice(0, 12)}...
                      </span>
                    </div>
                  </div>

                  {/* Tags */}
                  {exp.tags && exp.tags.length > 0 && (
                    <div style={{
                      display: 'flex',
                      gap: '0.5rem',
                      flexWrap: 'wrap'
                    }}>
                      {exp.tags.map((tag, idx) => (
                        <span
                          key={idx}
                          style={{
                            padding: '0.3rem 0.6rem',
                            background: 'rgba(99, 102, 241, 0.15)',
                            color: 'var(--accent-blue)',
                            borderRadius: '0.25rem',
                            fontSize: '0.75rem',
                            fontWeight: 600,
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.25rem'
                          }}
                        >
                          <Tag size={12} />
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Download Button */}
                <button
                  onClick={() => {
                    // TODO: Implement download functionality
                  }}
                  style={{
                    padding: '0.5rem',
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--accent-blue)',
                    cursor: 'pointer',
                    borderRadius: '0.3rem',
                    transition: 'background 0.2s ease'
                  }}
                  onMouseEnter={(e) => {
                    (e.target as HTMLButtonElement).style.background = 'rgba(99, 102, 241, 0.1)';
                  }}
                  onMouseLeave={(e) => {
                    (e.target as HTMLButtonElement).style.background = 'transparent';
                  }}
                >
                  <Download size={18} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
