import { useState } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertCircle, TrendingDown } from 'lucide-react';

interface ROCAnalysisProps {
  rocData?: {
    model_name: string;
    roc_auc?: number;
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
    confusion_matrix?: {
      confusion_matrix: number[][];
      confusion_matrix_normalized: number[][];
    };
  }[];
}

export default function ROCAnalysis({ rocData = [] }: ROCAnalysisProps) {
  const [selectedModel, setSelectedModel] = useState(0);

  const model = rocData[selectedModel] || {
    model_name: 'No Data',
    roc_auc: 0,
    accuracy: 0,
    precision: 0,
    recall: 0,
    f1_score: 0
  };

  // Prepare metrics comparison data
  const metricsData = [
    { metric: 'Accuracy', value: model.accuracy || 0 },
    { metric: 'Precision', value: model.precision || 0 },
    { metric: 'Recall', value: model.recall || 0 },
    { metric: 'F1-Score', value: model.f1_score || 0 }
  ];

  return (
    <div style={{ padding: '20px', background: '#0f172a', borderRadius: '8px', marginBottom: '20px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ margin: '0 0 5px 0', color: 'white', fontSize: '20px' }}>
          🎯 ROC Curve & Classification Metrics
        </h2>
        <p style={{ margin: '0', color: '#94a3b8', fontSize: '14px' }}>
          Detailed model evaluation with ROC-AUC and confusion matrix analysis
        </p>
      </div>

      {rocData.length > 0 && (
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '15px' }}>
            {rocData.map((model, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedModel(idx)}
                style={{
                  padding: '8px 16px',
                  background: selectedModel === idx ? '#3b82f6' : '#1e293b',
                  color: 'white',
                  border: '1px solid ' + (selectedModel === idx ? '#3b82f6' : '#334155'),
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: selectedModel === idx ? '600' : '400'
                }}
              >
                {model.model_name}
              </button>
            ))}
          </div>
        </div>
      )}

      {rocData.length > 0 ? (
        <>
          {/* Metrics Cards */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
              gap: '12px',
              marginBottom: '20px'
            }}
          >
            <div
              style={{
                background: '#1e293b',
                padding: '15px',
                borderRadius: '6px',
                borderLeft: '3px solid #3b82f6'
              }}
            >
              <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Accuracy</div>
              <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
                {(model.accuracy * 100).toFixed(1)}%
              </div>
            </div>

            <div
              style={{
                background: '#1e293b',
                padding: '15px',
                borderRadius: '6px',
                borderLeft: '3px solid #10b981'
              }}
            >
              <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Precision</div>
              <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
                {(model.precision * 100).toFixed(1)}%
              </div>
            </div>

            <div
              style={{
                background: '#1e293b',
                padding: '15px',
                borderRadius: '6px',
                borderLeft: '3px solid #f59e0b'
              }}
            >
              <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Recall</div>
              <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
                {(model.recall * 100).toFixed(1)}%
              </div>
            </div>

            <div
              style={{
                background: '#1e293b',
                padding: '15px',
                borderRadius: '6px',
                borderLeft: '3px solid #ec4899'
              }}
            >
              <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>F1-Score</div>
              <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
                {(model.f1_score * 100).toFixed(1)}%
              </div>
            </div>

            {model.roc_auc !== undefined && (
              <div
                style={{
                  background: '#1e293b',
                  padding: '15px',
                  borderRadius: '6px',
                  borderLeft: '3px solid #8b5cf6'
                }}
              >
                <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>ROC-AUC</div>
                <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
                  {(model.roc_auc * 100).toFixed(1)}%
                </div>
              </div>
            )}
          </div>

          {/* Metrics Comparison Chart */}
          <div
            style={{
              background: '#1e293b',
              padding: '15px',
              borderRadius: '6px',
              marginBottom: '20px'
            }}
          >
            <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>Classification Metrics Comparison</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="metric" stroke="#64748b" />
                <YAxis stroke="#64748b" domain={[0, 1]} />
                <Tooltip
                  contentStyle={{
                    background: '#0f172a',
                    border: '1px solid #334155',
                    borderRadius: '4px',
                    color: 'white'
                  }}
                  formatter={(value: any) => [(Number(value) * 100).toFixed(1) + '%', 'Score']}
                />
                <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Confusion Matrix */}
          {model.confusion_matrix && (
            <div
              style={{
                background: '#1e293b',
                padding: '15px',
                borderRadius: '6px',
                marginBottom: '20px'
              }}
            >
              <h3 style={{ color: '#e2e8f0', marginBottom: '15px' }}>Confusion Matrix (Normalized)</h3>
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(2, 1fr)',
                  gap: '15px',
                  maxWidth: '300px'
                }}
              >
                {model.confusion_matrix.confusion_matrix_normalized &&
                  model.confusion_matrix.confusion_matrix_normalized.map((row, i) =>
                    row.map((val, j) => (
                      <div
                        key={`${i}-${j}`}
                        style={{
                          background: `rgba(59, 130, 246, ${val})`,
                          padding: '20px',
                          borderRadius: '6px',
                          textAlign: 'center',
                          border: '1px solid #334155'
                        }}
                      >
                        <div style={{ color: '#e2e8f0', fontSize: '12px', marginBottom: '5px' }}>
                          Class {i} → {j}
                        </div>
                        <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>
                          {(val * 100).toFixed(1)}%
                        </div>
                      </div>
                    ))
                  )}
              </div>
            </div>
          )}

          {/* Recommendation */}
          <div
            style={{
              padding: '15px',
              background: '#1e2d4d',
              borderRadius: '6px',
              borderLeft: '3px solid #10b981'
            }}
          >
            <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
              <TrendingDown size={20} style={{ color: '#10b981', marginTop: '2px' }} />
              <div>
                <div style={{ color: '#e2e8f0', fontWeight: '500', marginBottom: '5px' }}>📊 Model Quality Assessment</div>
                <div style={{ color: '#cbd5e1', fontSize: '13px' }}>
                  {model.f1_score > 0.85
                    ? 'Excellent performance - Model is well-calibrated and ready for deployment'
                    : model.f1_score > 0.75
                      ? 'Good performance - Consider fine-tuning for marginal improvements'
                      : 'Moderate performance - Review feature engineering and model complexity'}
                </div>
              </div>
            </div>
          </div>
        </>
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
          <p>No ROC analysis data available</p>
          <p style={{ fontSize: '12px' }}>Train models to generate ROC curves and classification metrics</p>
        </div>
      )}
    </div>
  );
}
