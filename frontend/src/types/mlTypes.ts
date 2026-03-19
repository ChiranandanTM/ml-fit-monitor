export type FitStatus = "Good Fit" | "Overfitting" | "Underfitting";

export interface ModelResult {
  model: string;
  train_score: number;
  val_score: number;
  cv_mean: number;
  confidence_interval: [number, number];
  fit_status: FitStatus;
  drift_detected?: boolean;
}

export interface MLResponse {
  task_type: "classification" | "regression";
  models: ModelResult[];
}
