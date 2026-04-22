import { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Activity } from 'lucide-react';
import MetricsDeltaTable from './MetricsDeltaTable';

interface ExperimentComparisonProps {
  experimentId1?: string;
  experimentId2?: string;
  onClose?: () => void;
}

export default function ExperimentComparison({ 
  experimentId1, 
  experimentId2,
  onClose 
}: ExperimentComparisonProps) {
  const [loading, setLoading] = useState(false);
  const [comparison, setComparison] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [selectedExp1, setSelectedExp1] = useState(experimentId1 || "");
  const [selectedExp2, setSelectedExp2] = useState(experimentId2 || "");
  const [experiments, setExperiments] = useState<any[]>([]);

  useEffect(() => {
    loadExperiments();
  }, []);

  const loadExperiments = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/experiments/list?limit=20`);
      if (response.ok) {
        const data = await response.json();
        setExperiments(data.experiments || []);
      }
    } catch (err) {
      console.error("Failed to load experiments:", err);
    }
  };

  const handleCompare = async () => {
    if (!selectedExp1 || !selectedExp2) {
      setError("Please select both experiments");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(
        `${apiUrl}/experiments/compare/${selectedExp1}/${selectedExp2}`
      );
      
      const data = await response.json();
      
      if (response.ok) {
        setComparison(data.comparison);
      } else {
        setError(data.error || "Failed to compare experiments");
      }
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '1.5rem',
      animation: 'fadeInUp 0.6s ease-out'
    }}>
      {/* Experiment Selection */}
      <div style={{
        background: 'var(--bg-card)',
        borderRadius: 'var(--radius-lg)',
        border: '1px solid var(--border-default)',
        padding: '1.5rem'
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          marginBottom: '1rem'
        }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '0.5rem',
            background: 'var(--gradient-accent)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white'
          }}>
            <BarChart3 size={18} />
          </div>
          <h3 style={{
            margin: 0,
            fontSize: '1.1rem',
            color: 'var(--text-primary)',
            fontWeight: 600
          }}>
            Compare Experiments
          </h3>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1rem',
          marginBottom: '1rem'
        }}>
          {/* Experiment 1 Selection */}
          <div>
            <label style={{
              display: 'block',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              marginBottom: '0.5rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Experiment 1 (Before)
            </label>
            <select
              value={selectedExp1}
              onChange={(e) => setSelectedExp1(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '0.4rem',
                border: '1px solid var(--border-default)',
                background: 'var(--bg-input)',
                color: 'var(--text-primary)',
                fontSize: '0.9rem',
                fontFamily: 'var(--font-mono)',
                cursor: 'pointer'
              }}
            >
              <option value="">Select experiment...</option>
              {experiments.map((exp) => (
                <option key={exp.id} value={exp.id}>
                  {exp.id.slice(0, 20)}... - {exp.fit_status} ({new Date(exp.timestamp).toLocaleDateString()})
                </option>
              ))}
            </select>
          </div>

          {/* Experiment 2 Selection */}
          <div>
            <label style={{
              display: 'block',
              fontSize: '0.85rem',
              color: 'var(--text-secondary)',
              marginBottom: '0.5rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              Experiment 2 (After)
            </label>
            <select
              value={selectedExp2}
              onChange={(e) => setSelectedExp2(e.target.value)}
              style={{
                width: '100%',
                padding: '0.75rem',
                borderRadius: '0.4rem',
                border: '1px solid var(--border-default)',
                background: 'var(--bg-input)',
                color: 'var(--text-primary)',
                fontSize: '0.9rem',
                fontFamily: 'var(--font-mono)',
                cursor: 'pointer'
              }}
            >
              <option value="">Select experiment...</option>
              {experiments.map((exp) => (
                <option key={exp.id} value={exp.id}>
                  {exp.id.slice(0, 20)}... - {exp.fit_status} ({new Date(exp.timestamp).toLocaleDateString()})
                </option>
              ))}
            </select>
          </div>
        </div>

        {error && (
          <div style={{
            padding: '0.75rem',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.3)',
            borderRadius: '0.4rem',
            color: '#ef4444',
            fontSize: '0.85rem',
            marginBottom: '1rem'
          }}>
            {error}
          </div>
        )}

        <button
          onClick={handleCompare}
          disabled={loading || !selectedExp1 || !selectedExp2}
          style={{
            width: '100%',
            padding: '0.875rem',
            background: (!selectedExp1 || !selectedExp2) ? 'var(--border-default)' : 'var(--gradient-accent)',
            color: 'white',
            border: 'none',
            borderRadius: '0.4rem',
            fontSize: '0.95rem',
            fontWeight: 600,
            cursor: (!selectedExp1 || !selectedExp2) ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1,
            transition: 'opacity 0.2s ease',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem'
          }}
        >
          {loading ? (
            <>
              <Activity size={18} style={{ animation: 'spin 1s linear infinite' }} />
              Comparing...
            </>
          ) : (
            <>
              <TrendingUp size={18} />
              Compare Experiments
            </>
          )}
        </button>
      </div>

      {/* Comparison Results */}
      {comparison && (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1.5rem',
          animation: 'fadeInUp 0.6s ease-out'
        }}>
          {/* Summary Card */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1))',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-default)',
            padding: '1.5rem'
          }}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              marginBottom: '1rem'
            }}>
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '0.4rem',
                background: comparison.status_improved ? '#10b981' : '#ef4444',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                {comparison.status_improved ? '✓' : '!'}
              </div>
              <h4 style={{
                margin: 0,
                fontSize: '1rem',
                color: 'var(--text-primary)',
                fontWeight: 600
              }}>
                {comparison.overall_improvement_summary}
              </h4>
            </div>

            <p style={{
              margin: 0,
              fontSize: '0.9rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.5
            }}>
              Status progression: <strong>{comparison.exp1_status}</strong> → <strong>{comparison.exp2_status}</strong>
            </p>
          </div>

          {/* Metrics Delta Table */}
          {comparison.model_changes && comparison.model_changes.length > 0 && (
            <MetricsDeltaTable
              experiment1={{
                id: comparison.exp1_id,
                timestamp: comparison.exp1_timestamp,
                best_model: comparison.best_model_1,
                status: comparison.exp1_status
              }}
              experiment2={{
                id: comparison.exp2_id,
                timestamp: comparison.exp2_timestamp,
                best_model: comparison.best_model_2,
                status: comparison.exp2_status
              }}
              deltas={comparison.model_changes.map((change: any) => ({
                metric: change.model,
                before: change.exp1_val_score,
                after: change.exp2_val_score,
                absolute_delta: change.val_improvement,
                percent_delta: (change.val_improvement / change.exp1_val_score) * 100,
                improved: change.val_improvement > 0
              }))}
            />
          )}

          {/* Close Button */}
          {onClose && (
            <button
              onClick={onClose}
              style={{
                padding: '0.75rem 1.5rem',
                background: 'var(--border-default)',
                color: 'var(--text-primary)',
                border: 'none',
                borderRadius: '0.4rem',
                fontSize: '0.9rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'background 0.2s ease'
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLButtonElement).style.background = 'var(--border-subtle)';
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLButtonElement).style.background = 'var(--border-default)';
              }}
            >
              Close
            </button>
          )}
        </div>
      )}
    </div>
  );
}
