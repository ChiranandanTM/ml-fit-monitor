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
    </div>
  );
}
