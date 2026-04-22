import UploadPanel from "./UploadPanel";
import ModelComparison from "./ModelComparison";
import FitStatusCard from "./FitStatusCard";
import SuggestionsPanel from "./SuggestionsPanel";
import DriftSimulation from "./DriftSimulation";
import ModelAnalysisDetail from "./LearningCurves";
import FeatureImportance from "./FeatureImportance";
import DataProfilingDashboard from "./DataProfilingDashboard";
import ReportExporter from "./ReportExporter";
import { useMLStore } from "../store/useMLStore";
import { improveFitDataset } from "../api/mlApi";
import { useState } from "react";

function AppHeader() {
  return (
    <header className="app-header">
      <div className="app-header-left">
        <div className="app-logo">🧠</div>
        <div>
          <div className="app-title">ML Fit Monitor</div>
          <div className="app-subtitle">Model Quality Intelligence Platform</div>
        </div>
      </div>
      <span className="app-header-badge">v1.0</span>
    </header>
  );
}

function HowToGuide() {
  const cards = [
    { icon: '📊', title: 'Basic Training', desc: 'Train multiple ML models and instantly detect overfitting or underfitting patterns', color: 'var(--accent-cyan)' },
    { icon: '🔬', title: 'Full Analysis', desc: 'Comprehensive report with learning curves, bias-variance decomposition, and expert insights', color: 'var(--accent-purple)' },
    { icon: '💡', title: 'Suggestions', desc: 'Get actionable, prioritized recommendations to improve your model performance', color: 'var(--accent-amber)' },
    { icon: '📈', title: 'Drift Simulation', desc: 'Simulate data distribution shifts and understand when to retrain your models', color: 'var(--accent-pink)' },
  ];

  return (
    <div className="glass-card animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
      <div className="section-title">
        <div className="section-icon green">📋</div>
        <h2>How to Use This System</h2>
      </div>
      <div className="howto-grid stagger-children">
        {cards.map((card, i) => (
          <div key={i} className="howto-card">
            <span className="howto-icon">{card.icon}</span>
            <div className="howto-title" style={{ color: card.color }}>{card.title}</div>
            <div className="howto-desc">{card.desc}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ExecutiveSummary({ data }: { data: any }) {
  return (
    <div className="glass-card animate-fade-in-up">
      <div className="section-title">
        <div className="section-icon purple">📊</div>
        <h2>Executive Summary</h2>
      </div>

      <div className="metric-grid" style={{ marginBottom: '1.25rem' }}>
        <div className="metric-card">
          <div className="metric-label">Dataset</div>
          <div className="metric-value cyan" style={{ fontSize: '1.1rem' }}>
            {data.dataset}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Problem Type</div>
          <div className="metric-value purple" style={{ fontSize: '1.1rem' }}>
            {data.problem_type}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Models Trained</div>
          <div className="metric-value green" style={{ fontSize: '1.1rem' }}>
            {data.models_trained}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Best Model</div>
          <div className="metric-value amber" style={{ fontSize: '1.1rem' }}>
            🏆 {data.best_performing || "N/A"}
          </div>
        </div>
      </div>

      <div className="exec-summary-recommendation">
        {data.overall_recommendation}
      </div>
    </div>
  );
}

function SuggestionsModeView({
  results,
  onImprove,
  improving,
  improveError,
}: {
  results: any;
  onImprove: () => Promise<void>;
  improving: boolean;
  improveError: string | null;
}) {
  return (
    <>
      {results.best_model && (
        <div className="glass-card animate-fade-in-up" style={{ marginBottom: '1.5rem' }}>
          <div className="section-title">
            <div className="section-icon amber">🏆</div>
            <h2>Best Model Recommendation</h2>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
            <div>
              <div style={{ color: 'var(--text-primary)', fontWeight: 700, marginBottom: '0.4rem' }}>
                {results.best_model.model || "N/A"}
              </div>
              <span className={`status-badge ${results.best_model.fit_status === "Good Fit" ? "good" : results.best_model.fit_status === "Overfitting" ? "overfit" : "underfit"}`}>
                {results.best_model.fit_status}
              </span>
              <div style={{ color: 'var(--text-tertiary)', fontSize: '0.82rem', marginTop: '0.5rem' }}>
                Validation: {((results.best_model.val_score || 0) * 100).toFixed(1)}% | Gap: {((results.best_model.gap || 0) * 100).toFixed(1)}%
              </div>
            </div>

            {results.best_model.fit_status !== "Good Fit" && (
              <button className="gen-btn good" onClick={onImprove} disabled={improving}>
                {improving ? "Improving..." : "Improve File Using Best Model Suggestions"}
              </button>
            )}
          </div>

          {improveError && (
            <div className="error-message" style={{ marginTop: '1rem' }}>
              <span>⚠️</span>
              <span>{improveError}</span>
            </div>
          )}
        </div>
      )}

      {/* Dataset Info */}
      <div className="glass-card animate-fade-in-up" style={{ marginBottom: '1.5rem' }}>
        <div className="section-title">
          <div className="section-icon blue">📈</div>
          <h2>Dataset Info</h2>
        </div>
        <div className="metric-grid">
          <div className="metric-card">
            <div className="metric-label">Rows</div>
            <div className="metric-value cyan">{results.dataset_info?.rows}</div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Features</div>
            <div className="metric-value purple">{results.dataset_info?.columns}</div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Problem Type</div>
            <div className="metric-value green" style={{ fontSize: '1.1rem' }}>
              {results.dataset_info?.problem_type}
            </div>
          </div>
        </div>
      </div>

      {/* Suggestions */}
      {results.model_suggestions?.map((ms: any, idx: number) => (
        <div key={idx} className="glass-card animate-fade-in-up" style={{ marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
            <h3 style={{ color: 'var(--text-primary)' }}>{ms.model}</h3>
            <span className={`status-badge ${ms.fit_status === "Good Fit" ? "good" :
                ms.fit_status === "Overfitting" ? "overfit" : "underfit"
              }`}>
              {ms.fit_status}
            </span>
          </div>
          <div className="stagger-children">
            {ms.suggestions?.map((s: any, i: number) => (
              <div
                key={i}
                className={`suggestion-item ${s.priority === "HIGH" ? "high" :
                    s.priority === "MEDIUM" ? "medium" :
                      s.priority === "LOW" ? "low" : "info-priority"
                  }`}
              >
                <div className="suggestion-header">
                  <span className="suggestion-action">{s.action}</span>
                  <span className={`suggestion-priority ${s.priority === "HIGH" ? "high" :
                      s.priority === "MEDIUM" ? "medium" :
                        s.priority === "LOW" ? "low" : "info-priority"
                    }`}>
                    {s.priority}
                  </span>
                </div>
                <div className="suggestion-details">{s.details}</div>
                {(s.impl_effort || s.expected_impact) && (
                  <div className="suggestion-meta">
                    {s.impl_effort && <>Effort: {s.impl_effort}</>}
                    {s.impl_effort && s.expected_impact && <> · </>}
                    {s.expected_impact && <>Impact: {s.expected_impact}</>}
                  </div>
                )}
                {s.recommendations && (
                  <ul className="next-steps-list" style={{ marginTop: '0.5rem' }}>
                    {s.recommendations.map((r: string, j: number) => (
                      <li key={j}>{r}</li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      {/* General Recommendations */}
      {results.general_recommendations && (
        <div className="glass-card animate-fade-in-up">
          <div className="section-title">
            <div className="section-icon green">✅</div>
            <h2>General Recommendations</h2>
          </div>
          <ul className="next-steps-list">
            {results.general_recommendations.map((r: string, i: number) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}

function AutoImprovePanel({
  overallStatus,
  onImprove,
  loading,
  error,
}: {
  overallStatus: string;
  onImprove: () => Promise<void>;
  loading: boolean;
  error: string | null;
}) {
  const isGood = overallStatus === "Good Fit";
  const badgeClass = isGood ? "good" : overallStatus === "Overfitting" ? "overfit" : "underfit";

  return (
    <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.25rem' }}>
      <div className="section-title">
        <div className="section-icon amber">🛠️</div>
        <h2>Overall Fit Status</h2>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', flexWrap: 'wrap' }}>
        <div>
          <div style={{ color: 'var(--text-tertiary)', fontSize: '0.85rem', marginBottom: '0.35rem' }}>Detected Status</div>
          <span className={`status-badge ${badgeClass}`}>{overallStatus}</span>
        </div>

        {!isGood && (
          <button className="gen-btn good" onClick={onImprove} disabled={loading}>
            {loading ? "Improving..." : "Auto Improve To Good Fit"}
          </button>
        )}
      </div>

      {error && (
        <div className="error-message" style={{ marginTop: '1rem' }}>
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}

function ImprovedFitView({ results }: { results: any }) {
  const downloadImproved = () => {
    const csv = results?.improved_file?.csv;
    if (!csv) return;
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = results?.improved_file?.filename || "improved_fit_dataset.csv";
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  return (
    <>
      <div className="glass-card animate-fade-in-up" style={{ marginBottom: '1.25rem' }}>
        <div className="section-title">
          <div className="section-icon green">✅</div>
          <h2>Fit Improvement Result</h2>
        </div>

        <p style={{ color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>{results.message}</p>

        <div className="metric-grid" style={{ marginBottom: '1rem' }}>
          <div className="metric-card">
            <div className="metric-label">Original Status</div>
            <div className="metric-value amber" style={{ fontSize: '1rem' }}>{results.original_overall_status}</div>
          </div>
          <div className="metric-card">
            <div className="metric-label">Improved Status</div>
            <div className="metric-value green" style={{ fontSize: '1rem' }}>{results.improved_overall_status}</div>
          </div>
        </div>

        <button className="gen-btn good" onClick={downloadImproved}>
          Download Improved Dataset
        </button>
      </div>

      {results.improved_results?.models && (
        <>
          <ModelComparison models={results.improved_results.models} />
          <div style={{ marginTop: '1.25rem' }} className="model-cards-grid stagger-children">
            {results.improved_results.models.map((m: any, idx: number) => (
              <FitStatusCard key={`${m.model}-${idx}`} model={m} index={idx} />
            ))}
          </div>
        </>
      )}
    </>
  );
}

export default function DashboardLayout() {
  const { results, setResults, lastUploadedFile } = useMLStore();
  const [improving, setImproving] = useState(false);
  const [improveError, setImproveError] = useState<string | null>(null);

  const handleReset = () => setResults(null);

  const handleImproveFit = async () => {
    if (!lastUploadedFile) {
      setImproveError("Please upload a dataset first.");
      return;
    }

    try {
      setImproveError(null);
      setImproving(true);
      const data = await improveFitDataset(lastUploadedFile, "best_model");
      if (data?.error) {
        setImproveError(data.error);
        return;
      }
      setResults(data);
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || "Failed to improve fit.";
      setImproveError(msg);
    } finally {
      setImproving(false);
    }
  };

  // ====== NO RESULTS - Landing Page ======
  if (!results) {
    return (
      <div className="app-container">
        <AppHeader />
        <UploadPanel />
        <HowToGuide />
      </div>
    );
  }

  // ====== FULL ANALYSIS (executive_summary) ======
  if (results.executive_summary) {
    return (
      <div className="app-container">
        <AppHeader />

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem' }}>
            <span style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Full Analysis Report
            </span>
          </h1>
          <button className="reset-btn" onClick={handleReset}>
            ← New Analysis
          </button>
        </div>

        <ExecutiveSummary data={results.executive_summary} />

        {results.model_analysis && results.model_analysis.length > 0 && (
          <ModelAnalysisDetail modelAnalysis={results.model_analysis} />
        )}

        {results.suggestions && results.suggestions.length > 0 && (
          <SuggestionsPanel suggestions={results.suggestions} />
        )}

        {results.drift_analysis && (
          <DriftSimulation driftData={results.drift_analysis} />
        )}

        {/* Advanced Analysis Features */}
        <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)', paddingTop: '2rem' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🔬 Advanced Analysis & Model Diagnostics
          </h2>

          {/* Data Quality Profiling */}
          <div style={{ marginBottom: '1.5rem' }}>
            <DataProfilingDashboard profile={results.data_profile} />
          </div>

          {/* Feature Importance */}
          <div style={{ marginBottom: '1.5rem' }}>
            <FeatureImportance features={results.feature_importance} />
          </div>

          {/* Report Exporter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <ReportExporter hasAnalysisData={true} />
          </div>
        </div>

        {results.next_steps && (
          <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
            <div className="section-title">
              <div className="section-icon green">✅</div>
              <h2>Recommended Next Steps</h2>
            </div>
            <ul className="next-steps-list">
              {results.next_steps.map((step: string, i: number) => (
                <li key={i}>{step}</li>
              ))}
            </ul>
          </div>
        )}

        <div style={{ marginTop: '2rem' }}>
          <UploadPanel />
        </div>
      </div>
    );
  }

  // ====== IMPROVED FIT RESULTS ======
  if (results.improved_results) {
    return (
      <div className="app-container">
        <AppHeader />

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem' }}>
            <span style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Auto Fit Improvement
            </span>
          </h1>
          <button className="reset-btn" onClick={handleReset}>
            ← New Analysis
          </button>
        </div>

        <UploadPanel />
        <ImprovedFitView results={results} />

        {/* Advanced Analysis Features after improvement */}
        <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)', paddingTop: '2rem' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🔬 Advanced Analysis & Model Diagnostics
          </h2>

          {/* Data Quality Profiling */}
          <div style={{ marginBottom: '1.5rem' }}>
            <DataProfilingDashboard profile={results.data_profile} />
          </div>

          {/* Feature Importance */}
          <div style={{ marginBottom: '1.5rem' }}>
            <FeatureImportance features={results.feature_importance} />
          </div>

          {/* Report Exporter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <ReportExporter hasAnalysisData={true} />
          </div>
        </div>
      </div>
    );
  }

  // ====== BASIC TRAINING (models) ======
  if (results.models && !results.simulation_summary && !results.model_suggestions) {
    return (
      <div className="app-container">
        <AppHeader />

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem' }}>
            <span style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Model Training Results
            </span>
          </h1>
          <button className="reset-btn" onClick={handleReset}>
            ← New Analysis
          </button>
        </div>

        <UploadPanel />

        <ModelComparison models={results.models} />

        <div style={{ marginTop: '1.5rem' }}>
          <div className="section-title">
            <div className="section-icon cyan">🎯</div>
            <h2>Model Performance Cards</h2>
          </div>
          <div className="model-cards-grid stagger-children">
            {results.models.map((m: any, idx: number) => (
              <FitStatusCard key={m.model} model={m} index={idx} />
            ))}
          </div>
        </div>

        {/* Summary Stats */}
        {results.summary && (
          <div className="glass-card animate-fade-in-up" style={{ marginTop: '1.5rem' }}>
            <div className="section-title">
              <div className="section-icon purple">📊</div>
              <h2>Summary</h2>
            </div>
            <div className="metric-grid">
              <div className="metric-card">
                <div className="metric-label">Task Type</div>
                <div className="metric-value cyan" style={{ fontSize: '1.1rem', textTransform: 'capitalize' }}>
                  {results.task_type}
                </div>
              </div>
              <div className="metric-card">
                <div className="metric-label">Models Trained</div>
                <div className="metric-value purple">{results.summary.successful_models}</div>
              </div>
              {results.summary.best_model && (
                <div className="metric-card">
                  <div className="metric-label">Best Model</div>
                  <div className="metric-value green" style={{ fontSize: '1rem' }}>
                    🏆 {results.summary.best_model}
                  </div>
                </div>
              )}
              {results.summary.recommendation && (
                <div className="metric-card" style={{ gridColumn: 'span 1' }}>
                  <div className="metric-label">Recommendation</div>
                  <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginTop: '0.3rem' }}>
                    {results.summary.recommendation}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        <AutoImprovePanel
          overallStatus={results.summary?.overall_fit_status || "Unknown"}
          onImprove={handleImproveFit}
          loading={improving}
          error={improveError}
        />

        {/* Advanced Analysis Features */}
        <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)', paddingTop: '2rem' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🔬 Advanced Analysis & Model Diagnostics
          </h2>

          {/* Data Quality Profiling */}
          <div style={{ marginBottom: '1.5rem' }}>
            <DataProfilingDashboard profile={results.data_profile} />
          </div>

          {/* Feature Importance */}
          <div style={{ marginBottom: '1.5rem' }}>
            <FeatureImportance features={results.feature_importance} />
          </div>

          {/* Report Exporter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <ReportExporter hasAnalysisData={true} />
          </div>
        </div>
      </div>
    );
  }

  // ====== SUGGESTIONS MODE ======
  if (results.model_suggestions) {
    return (
      <div className="app-container">
        <AppHeader />

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem' }}>
            <span style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Model Improvement Suggestions
            </span>
          </h1>
          <button className="reset-btn" onClick={handleReset}>
            ← New Analysis
          </button>
        </div>

        <UploadPanel />
        <SuggestionsModeView
          results={results}
          onImprove={handleImproveFit}
          improving={improving}
          improveError={improveError}
        />

        {/* Advanced Analysis Features for Suggestions Mode */}
        <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)', paddingTop: '2rem' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🔬 Advanced Analysis & Model Diagnostics
          </h2>

          {/* Data Quality Profiling */}
          <div style={{ marginBottom: '1.5rem' }}>
            <DataProfilingDashboard profile={results.data_profile} />
          </div>

          {/* Feature Importance */}
          <div style={{ marginBottom: '1.5rem' }}>
            <FeatureImportance features={results.feature_importance} />
          </div>

          {/* Report Exporter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <ReportExporter hasAnalysisData={true} />
          </div>
        </div>
      </div>
    );
  }

  // ====== DRIFT SIMULATION ======
  if (results.simulation_summary) {
    return (
      <div className="app-container">
        <AppHeader />

        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
          <h1 style={{ fontSize: '1.5rem' }}>
            <span style={{ background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              Drift Simulation Report
            </span>
          </h1>
          <button className="reset-btn" onClick={handleReset}>
            ← New Analysis
          </button>
        </div>

        <UploadPanel />
        <DriftSimulation driftData={results} />

        {/* Advanced Analysis Features for Drift Simulation */}
        <div style={{ marginTop: '2rem', borderTop: '1px solid rgba(226, 232, 240, 0.1)', paddingTop: '2rem' }}>
          <h2 style={{ fontSize: '1.3rem', marginBottom: '1.5rem', background: 'var(--gradient-accent)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            🔬 Advanced Analysis & Model Diagnostics
          </h2>

          {/* Data Quality Profiling */}
          <div style={{ marginBottom: '1.5rem' }}>
            <DataProfilingDashboard profile={results.data_profile} />
          </div>

          {/* Feature Importance */}
          <div style={{ marginBottom: '1.5rem' }}>
            <FeatureImportance features={results.feature_importance} />
          </div>

          {/* Report Exporter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <ReportExporter hasAnalysisData={true} />
          </div>
        </div>
      </div>
    );
  }

  // ====== FALLBACK ======
  return (
    <div className="app-container">
      <AppHeader />
      <UploadPanel />
      <div className="glass-card" style={{ textAlign: 'center', padding: '3rem' }}>
        <p style={{ color: 'var(--text-tertiary)', fontSize: '1rem' }}>
          Upload a dataset to get started with your ML model analysis.
        </p>
      </div>
    </div>
  );
}
