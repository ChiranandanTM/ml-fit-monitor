import { uploadDataset, generateDataset, getComprehensiveAnalysis, getSuggestions, getDriftSimulation } from "../api/mlApi";
import { useMLStore } from "../store/useMLStore";
import { useState, useRef } from "react";

type AnalysisMode = "train" | "analyze" | "suggest" | "drift";

const MODES: { key: AnalysisMode; icon: string; label: string; desc: string }[] = [
  { key: "train", icon: "📊", label: "Basic Training", desc: "Train models & detect fit" },
  { key: "analyze", icon: "🔬", label: "Full Analysis", desc: "Comprehensive report" },
  { key: "suggest", icon: "💡", label: "Suggestions", desc: "Actionable improvements" },
  { key: "drift", icon: "📈", label: "Drift Simulation", desc: "Data drift analysis" },
];

export default function UploadPanel() {
  const { setResults, setLastUploadedFile } = useMLStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>("train");
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = async (file: File) => {
    try {
      setLoading(true);
      setError(null);
      setLastUploadedFile(file);
      console.log("Uploading file:", file.name, "mode:", analysisMode);

      let data;
      if (analysisMode === "train") {
        data = await uploadDataset(file);
      } else if (analysisMode === "analyze") {
        data = await getComprehensiveAnalysis(file);
      } else if (analysisMode === "suggest") {
        data = await getSuggestions(file);
      } else if (analysisMode === "drift") {
        data = await getDriftSimulation(file);
      }

      if (data && !data.error) {
        console.log("Results received:", data);
        setResults(data);
      } else if (data?.error) {
        setError(`Server error: ${data.error}`);
      } else {
        setError("Invalid response from server");
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || "Upload failed. Make sure the backend is running.";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    await handleFile(file);
    // Reset the input so the same file can be re-selected
    e.target.value = '';
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    const lower = file?.name.toLowerCase() || "";
    if (file && (lower.endsWith('.csv') || lower.endsWith('.xlsx') || lower.endsWith('.xls'))) {
      await handleFile(file);
    } else {
      setError("Please drop a CSV or Excel file (.csv, .xlsx, .xls)");
    }
  };

  const handleGenerateDataset = async (fitType: "good_fit" | "overfitting" | "underfitting") => {
    try {
      setLoading(true);
      setError(null);

      const data = await generateDataset(fitType);

      if (data?.csv) {
        // Download the file
        const blob = new Blob([data.csv], { type: "text/csv" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = data.filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        // Auto-upload for training
        const file = new File([blob], data.filename, { type: "text/csv" });
        setLastUploadedFile(file);
        const uploadData = await uploadDataset(file);
        if (uploadData?.models) {
          setResults(uploadData);
        }
      }
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail || err.message || "Failed to generate dataset";
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-card animate-fade-in-up" style={{ marginBottom: '1.5rem' }}>
      {/* Analysis Mode Selection */}
      <div className="section-title">
        <div className="section-icon cyan">🎯</div>
        <h2>Analysis Mode</h2>
      </div>

      <div className="mode-tabs" style={{ marginBottom: '1.5rem' }}>
        {MODES.map((mode) => (
          <button
            key={mode.key}
            className={`mode-tab ${analysisMode === mode.key ? 'active' : ''}`}
            onClick={() => setAnalysisMode(mode.key)}
          >
            <span>{mode.icon}</span>
            <div>
              <div style={{ fontWeight: 600 }}>{mode.label}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', marginTop: 1 }}>
                {mode.desc}
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* Upload Zone */}
      <div
        className={`upload-zone ${dragActive ? 'active' : ''}`}
        style={dragActive ? { borderColor: 'var(--accent-cyan)', background: 'var(--accent-cyan-dim)' } : {}}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <span className="upload-zone-icon">{loading ? '⏳' : '📂'}</span>
        <p className="upload-zone-text">
          {loading ? 'Processing your dataset...' : 'Drag & drop your CSV or Excel file here'}
        </p>
        <p className="upload-zone-hint">
          {loading ? 'This may take a moment' : 'or click to browse files'}
        </p>
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          onChange={handleUpload}
          onClick={(e) => e.stopPropagation()}
          disabled={loading}
          id="file-upload-input"
        />
      </div>

      {/* Quick Generate */}
      <div style={{ marginTop: '1.25rem' }}>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-tertiary)', marginBottom: '0.5rem', fontWeight: 500 }}>
          Or generate a sample dataset:
        </p>
        <div className="gen-btn-group">
          <button
            className="gen-btn good"
            onClick={() => handleGenerateDataset("good_fit")}
            disabled={loading}
            id="gen-good-fit"
          >
            <span>✅</span> Good Fit
          </button>
          <button
            className="gen-btn warn"
            onClick={() => handleGenerateDataset("overfitting")}
            disabled={loading}
            id="gen-overfitting"
          >
            <span>⚠️</span> Overfitting
          </button>
          <button
            className="gen-btn danger"
            onClick={() => handleGenerateDataset("underfitting")}
            disabled={loading}
            id="gen-underfitting"
          >
            <span>❌</span> Underfitting
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && (
        <div className="loading-container" style={{ padding: '1.5rem 0 0.5rem' }}>
          <div className="loading-spinner" />
          <span className="loading-text">Analyzing your dataset...</span>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="error-message" style={{ marginTop: '1rem' }}>
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
