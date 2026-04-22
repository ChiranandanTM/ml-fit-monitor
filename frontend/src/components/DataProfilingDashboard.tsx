import { useState } from 'react';
import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';

interface DataProfile {
  shape: { rows: number; columns: number };
  quality_score: number;
  missing_values: { [key: string]: number };
  outliers: { [key: string]: { outliers: number; percentage: number } };
  class_distribution?: {
    classes: { [key: string]: number };
    percentages: { [key: string]: number };
    imbalance_ratio: number;
  };
  issues: string[];
  columns: {
    [key: string]: {
      dtype: string;
      null_percentage: number;
      unique_values: number;
      unique_percentage: number;
      mean?: number;
      median?: number;
      std?: number;
      min?: number;
      max?: number;
    };
  };
}

interface DataProfilingDashboardProps {
  profile?: DataProfile;
}

export default function DataProfilingDashboard({ profile }: DataProfilingDashboardProps) {
  const [expandedColumn, setExpandedColumn] = useState<string | null>(null);

  if (!profile) {
    return (
      <div style={{ padding: '20px', background: '#0f172a', borderRadius: '8px' }}>
        <h2 style={{ color: 'white' }}>📊 Data Quality Profile</h2>
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
          <p>No data profile available</p>
          <p style={{ fontSize: '12px' }}>Upload a dataset to see data quality analysis</p>
        </div>
      </div>
    );
  }

  const qualityGrade =
    (profile?.quality_score ?? 0) >= 90
      ? 'A'
      : (profile?.quality_score ?? 0) >= 80
        ? 'B'
        : (profile?.quality_score ?? 0) >= 70
          ? 'C'
          : 'D';
  const gradeColor =
    qualityGrade === 'A' ? '#10b981' : qualityGrade === 'B' ? '#3b82f6' : qualityGrade === 'C' ? '#f59e0b' : '#ef4444';

  return (
    <div style={{ padding: '20px', background: '#0f172a', borderRadius: '8px' }}>
      <div style={{ marginBottom: '20px' }}>
        <h2 style={{ margin: '0 0 5px 0', color: 'white', fontSize: '20px' }}>
          🔍 Data Quality Profile
        </h2>
        <p style={{ margin: '0', color: '#94a3b8', fontSize: '14px' }}>
          Comprehensive dataset assessment for training readiness
        </p>
      </div>

      {/* Quality Summary Cards */}
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
            borderLeft: `3px solid ${gradeColor}`
          }}
        >
          <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Quality Grade</div>
          <div style={{ color: gradeColor, fontSize: '32px', fontWeight: 'bold' }}>{qualityGrade}</div>
        </div>

        <div
          style={{
            background: '#1e293b',
            padding: '15px',
            borderRadius: '6px',
            borderLeft: '3px solid #3b82f6'
          }}
        >
          <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Quality Score</div>
          <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>
            {(profile?.quality_score ?? 0).toFixed(1)}/100
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
          <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Dataset Size</div>
          <div style={{ color: '#e2e8f0', fontSize: '18px', fontWeight: 'bold' }}>
            {profile.shape.rows.toLocaleString()} × {profile.shape.columns}
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
          <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Issues Found</div>
          <div style={{ color: '#e2e8f0', fontSize: '24px', fontWeight: 'bold' }}>{(profile?.issues?.length ?? 0)}</div>
        </div>
      </div>

      {/* Issues List */}
      {(profile?.issues ?? []).length > 0 && (
        <div
          style={{
            background: '#1e293b',
            padding: '15px',
            borderRadius: '6px',
            marginBottom: '20px',
            borderLeft: '3px solid #ef4444'
          }}
        >
          <h3 style={{ color: '#e2e8f0', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={18} style={{ color: '#ef4444' }} /> Data Quality Issues
          </h3>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {(profile?.issues ?? []).map((issue, idx) => (
              <div
                key={idx}
                style={{
                  padding: '8px',
                  background: '#0f172a',
                  marginBottom: '8px',
                  borderRadius: '4px',
                  color: '#cbd5e1',
                  fontSize: '13px',
                  borderLeft: '2px solid #ef4444'
                }}
              >
                {issue}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Class Distribution (for classification) */}
      {profile.class_distribution && (
        <div
          style={{
            background: '#1e293b',
            padding: '15px',
            borderRadius: '6px',
            marginBottom: '20px'
          }}
        >
          <h3 style={{ color: '#e2e8f0', marginBottom: '10px' }}>Class Distribution</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '10px' }}>
            {Object.entries(profile.class_distribution.classes).map(([className, count]) => (
              <div
                key={className}
                style={{
                  background: '#0f172a',
                  padding: '12px',
                  borderRadius: '4px',
                  textAlign: 'center'
                }}
              >
                <div style={{ color: '#94a3b8', fontSize: '12px', marginBottom: '5px' }}>Class {className}</div>
                <div style={{ color: '#3b82f6', fontSize: '18px', fontWeight: 'bold' }}>
                  {count.toLocaleString()}
                </div>
                <div style={{ color: '#64748b', fontSize: '11px' }}>
                  ({profile.class_distribution?.percentages[className]?.toFixed(1)}%)
                </div>
              </div>
            ))}
          </div>
          {profile.class_distribution.imbalance_ratio > 3 && (
            <div
              style={{
                marginTop: '10px',
                padding: '10px',
                background: '#7c2d12',
                borderRadius: '4px',
                color: '#fed7aa',
                fontSize: '12px'
              }}
            >
              ⚠️ Class imbalance detected ({profile.class_distribution.imbalance_ratio.toFixed(1)}:1). Consider
              SMOTE or class weights.
            </div>
          )}
        </div>
      )}

      {/* Column Analysis */}
      <div
        style={{
          background: '#1e293b',
          padding: '15px',
          borderRadius: '6px'
        }}
      >
        <h3 style={{ color: '#e2e8f0', marginBottom: '10px' }}>Column Analysis</h3>
        <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
          {Object.entries(profile?.columns ?? {}).map(([colName, colData]) => (
            <div
              key={colName}
              style={{
                background: '#0f172a',
                padding: '12px',
                marginBottom: '8px',
                borderRadius: '4px',
                border: '1px solid #334155',
                cursor: 'pointer'
              }}
              onClick={() => setExpandedColumn(expandedColumn === colName ? null : colName)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ color: '#e2e8f0', fontWeight: '500' }}>{colName}</div>
                  <div style={{ color: '#94a3b8', fontSize: '12px' }}>{colData.dtype}</div>
                </div>
                <div style={{ textAlign: 'right' }}>
                  {colData.null_percentage === 0 ? (
                    <CheckCircle size={18} style={{ color: '#10b981' }} />
                  ) : colData.null_percentage > 20 ? (
                    <AlertCircle size={18} style={{ color: '#ef4444' }} />
                  ) : (
                    <AlertTriangle size={18} style={{ color: '#f59e0b' }} />
                  )}
                </div>
              </div>

              {expandedColumn === colName && (
                <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #334155' }}>
                  <div
                    style={{
                      display: 'grid',
                      gridTemplateColumns: 'repeat(2, 1fr)',
                      gap: '8px',
                      fontSize: '12px'
                    }}
                  >
                    <div>
                      <div style={{ color: '#94a3b8' }}>Missing</div>
                      <div style={{ color: '#e2e8f0' }}>{colData.null_percentage.toFixed(1)}%</div>
                    </div>
                    <div>
                      <div style={{ color: '#94a3b8' }}>Unique</div>
                      <div style={{ color: '#e2e8f0' }}>{colData.unique_values}</div>
                    </div>
                    {colData.mean !== undefined && (
                      <>
                        <div>
                          <div style={{ color: '#94a3b8' }}>Mean</div>
                          <div style={{ color: '#e2e8f0' }}>{colData.mean?.toFixed(2)}</div>
                        </div>
                        <div>
                          <div style={{ color: '#94a3b8' }}>Range</div>
                          <div style={{ color: '#e2e8f0' }}>
                            {colData.min?.toFixed(2)} - {colData.max?.toFixed(2)}
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
