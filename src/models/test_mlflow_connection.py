import mlflow

EXPERIMENT_NAME = "umkm_success_prediction_rating_regression"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name="test_connection_umkm"):
    mlflow.log_param("project_name", "umkm_success_prediction")
    mlflow.log_param("concept", "prediksi_potensi_keberhasilan_umkm")
    mlflow.log_param("target", "google_rating")
    mlflow.log_param("problem_type", "regression")

    mlflow.log_metric("mae", 0.0)
    mlflow.log_metric("rmse", 0.0)
    mlflow.log_metric("r2_score", 1.0)

print("Test MLflow berhasil.")
print(f"Experiment: {EXPERIMENT_NAME}")
print("Cek dashboard di http://127.0.0.1:5000")