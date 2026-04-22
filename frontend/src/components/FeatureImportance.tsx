import { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertCircle } from 'lucide-react';

interface FeatureImportanceProps {
  features?: Array<{
    name: string;
    importance: number;
    rank: number;
  }>;
}

export default function FeatureImportance({ features = [] }: FeatureImportanceProps) {
  const [topN, setTopN] = useState(10);

  const displayFeatures = features.slice(0, topN);

  return (
    <div style={{ padding: '20px', background: '#0f172a', borderRadius: '8px', marginBottom: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <h2 style={{ margin: '0 0 5px 0', color: 'white', fontSize: '20px' }}>
            📊 Feature Importance Analysis
          </h2>
          <p style={{ margin: '0', color: '#94a3b8', fontSize: '14px' }}>
            Identify most influential features for model predictions
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="number"
            min="1"
            max={features.length}
            value={topN}
            onChange={(e) => setTopN(parseInt(e.target.value))}
            style={{
              padding: '8px 12px',
              background: '#1e293b',
              border: '1px solid #334155',
              color: 'white',
              borderRadius: '4px',
              width: '60px'
            }}
          />
          <label style={{ color: '#cbd5e1', fontSize: '14px', display: 'flex', alignItems: 'center' }}>
            Top N Features
          </label>
        </div>
      </div>

      {displayFeatures.length > 0 ? (
        <div style={{ background: '#1e293b', padding: '15px', borderRadius: '6px', marginBottom: '20px' }}>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={displayFeatures}>
              <XAxis dataKey="name" stroke="#64748b" />
              <YAxis stroke="#64748b" />
              <Tooltip
                contentStyle={{
                  background: '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '4px',
                  color: 'white'
                }}
              />
              <Bar dataKey="importance" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <div
          style={{
            background: '#1e293b',
            padding: '40px',
            borderRadius: '6px',
            textAlign: 'center',
            color: '#94a3b8'
          }}
        >
          <AlertCircle style={{ margin: '0 auto', marginBottom: '10px' }} size={32} />
          <p>No feature importance data available</p>
          <p style={{ fontSize: '12px' }}>Upload a dataset and train models to see feature importance</p>
        </div>
      )}

      {displayFeatures.length > 0 && (
        <div style={{ marginTop: '20px' }}>
          <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>Top {topN} Features</h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {displayFeatures.map((feature, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px',
                  background: '#0f172a',
                  marginBottom: '8px',
                  borderRadius: '4px',
                  borderLeft: '3px solid #3b82f6'
                }}
              >
                <div>
                  <div style={{ color: '#e2e8f0', fontWeight: '500' }}>#{feature.rank} {feature.name}</div>
                  <div style={{ color: '#94a3b8', fontSize: '12px' }}>Importance Score</div>
                </div>
                <div style={{ color: '#3b82f6', fontWeight: 'bold', fontSize: '18px' }}>
                  {(feature.importance * 100).toFixed(1)}%
                </div>
              </div>
            ))}
          </div>

          <div
            style={{
              marginTop: '15px',
              padding: '15px',
              background: '#1e2d4d',
              borderRadius: '6px',
              borderLeft: '3px solid #10b981'
            }}
          >
            <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
              <TrendingUp size={20} style={{ color: '#10b981', marginTop: '2px' }} />
              <div>
                <div style={{ color: '#e2e8f0', fontWeight: '500', marginBottom: '5px' }}>💡 Recommendation</div>
                <div style={{ color: '#cbd5e1', fontSize: '13px' }}>
                  Focus on the top features for feature engineering. Consider removing low-importance features to reduce
                  model complexity and improve training time.
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
