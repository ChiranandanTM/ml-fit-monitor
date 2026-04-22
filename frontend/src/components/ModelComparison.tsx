import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
  Cell,
} from "recharts";

interface ModelComparisonProps {
  models: any[];
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: 'var(--bg-card)',
        border: '1px solid var(--border-default)',
        borderRadius: 'var(--radius-md)',
        padding: '0.85rem 1rem',
        boxShadow: 'var(--shadow-lg)',
        backdropFilter: 'blur(20px)',
      }}>
        <p style={{
          fontWeight: 700,
          color: 'var(--text-primary)',
          marginBottom: '0.4rem',
          fontSize: '0.88rem'
        }}>
          {label}
        </p>
        {payload.map((p: any, idx: number) => (
          <p key={idx} style={{
            color: p.color,
            fontSize: '0.82rem',
            fontFamily: 'var(--font-mono)',
            marginBottom: '0.15rem',
          }}>
            {p.name}: {(p.value * 100).toFixed(1)}%
          </p>
        ))}
      </div>
    );
  }
  return null;
};

export default function ModelComparison({ models }: ModelComparisonProps) {
  if (!models || models.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-tertiary)' }}>
        No model data available
      </div>
    );
  }

  return (
    <div className="chart-container animate-fade-in-up">
      <div className="section-title" style={{ marginBottom: '1.5rem' }}>
        <div className="section-icon purple">📊</div>
        <h3>Model Performance Comparison</h3>
      </div>
      <ResponsiveContainer width="100%" height={340}>
        <BarChart data={models} barGap={4} barCategoryGap="20%">
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,255,255,0.04)"
            vertical={false}
          />
          <XAxis
            dataKey="model"
            tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
            axisLine={{ stroke: 'var(--border-subtle)' }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: 'var(--text-tertiary)', fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            domain={[0, 1]}
            tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{
              color: 'var(--text-secondary)',
              fontSize: '0.82rem',
              paddingTop: '0.5rem',
            }}
          />
          <Bar
            dataKey="train_score"
            name="Training Score"
            radius={[6, 6, 0, 0]}
            maxBarSize={50}
          >
            {models.map((_: any, idx: number) => (
              <Cell key={idx} fill="#a855f7" />
            ))}
          </Bar>
          <Bar
            dataKey="val_score"
            name="Validation Score"
            radius={[6, 6, 0, 0]}
            maxBarSize={50}
          >
            {models.map((_: any, idx: number) => (
              <Cell key={idx} fill="#00d4ff" />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      {/* Detailed Metrics Comparison Table (NEW) */}
      {models.some(m => m.detailed_metrics && Object.keys(m.detailed_metrics).length > 0) && (
        <div style={{ marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)' }}>
          <div className="section-title" style={{ marginBottom: '1rem' }}>
            <div className="section-icon cyan">📈</div>
            <h3>Detailed Metrics Comparison</h3>
          </div>
          <div style={{ overflowX: 'auto', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '8px', padding: '1rem' }}>
            <table style={{
              width: '100%',
              borderCollapse: 'collapse',
              color: 'var(--text-secondary)',
              fontSize: '0.85rem',
            }}>
              <thead>
                <tr style={{ borderBottom: '1px solid rgba(226, 232, 240, 0.2)' }}>
                  <th style={{ textAlign: 'left', padding: '0.75rem', fontWeight: '600', color: 'var(--text-primary)' }}>Model</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem', fontWeight: '600', color: 'var(--accent-cyan)' }}>Accuracy</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem', fontWeight: '600', color: 'var(--accent-green)' }}>Precision</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem', fontWeight: '600', color: 'var(--accent-purple)' }}>Recall</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem', fontWeight: '600', color: 'var(--accent-amber)' }}>F1 Score</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem', fontWeight: '600', color: 'var(--accent-yellow)' }}>ROC-AUC</th>
                </tr>
              </thead>
              <tbody>
                {models.map((model, idx) => {
                  const metrics = model.detailed_metrics || {};
                  const hasMetrics = Object.keys(metrics).length > 0;
                  
                  return (
                    <tr key={idx} style={{
                      borderBottom: '1px solid rgba(226, 232, 240, 0.1)',
                      background: idx % 2 === 0 ? 'transparent' : 'rgba(226, 232, 240, 0.03)',
                    }}>
                      <td style={{ padding: '0.75rem', fontWeight: '500', color: 'var(--text-primary)' }}>
                        {model.model}
                      </td>
                      <td style={{ textAlign: 'center', padding: '0.75rem', color: hasMetrics && metrics.accuracy ? 'var(--accent-cyan)' : 'var(--text-tertiary)' }}>
                        {hasMetrics && metrics.accuracy !== undefined ? `${(metrics.accuracy * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td style={{ textAlign: 'center', padding: '0.75rem', color: hasMetrics && metrics.precision ? 'var(--accent-green)' : 'var(--text-tertiary)' }}>
                        {hasMetrics && metrics.precision !== undefined ? `${(metrics.precision * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td style={{ textAlign: 'center', padding: '0.75rem', color: hasMetrics && metrics.recall ? 'var(--accent-purple)' : 'var(--text-tertiary)' }}>
                        {hasMetrics && metrics.recall !== undefined ? `${(metrics.recall * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td style={{ textAlign: 'center', padding: '0.75rem', color: hasMetrics && metrics.f1_score ? 'var(--accent-amber)' : 'var(--text-tertiary)' }}>
                        {hasMetrics && metrics.f1_score !== undefined ? `${(metrics.f1_score * 100).toFixed(1)}%` : '—'}
                      </td>
                      <td style={{ textAlign: 'center', padding: '0.75rem', color: hasMetrics && metrics.roc_auc ? 'var(--accent-yellow)' : 'var(--text-tertiary)' }}>
                        {hasMetrics && metrics.roc_auc !== undefined && metrics.roc_auc !== null ? `${(metrics.roc_auc * 100).toFixed(1)}%` : '—'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
