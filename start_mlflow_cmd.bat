@echo off
title MLflow UI - UMKM Success Prediction

cd /d "C:\PBL 4\umkm-success-prediction"

echo ==========================================
echo Menjalankan MLflow UI Project UMKM
echo ==========================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] File activate.bat tidak ditemukan.
    echo Pastikan virtual environment berada di folder .venv
    pause
    exit /b
)

echo [INFO] Mengaktifkan virtual environment...
call ".venv\Scripts\activate.bat"

echo.
echo [INFO] Mengecek versi MLflow...
python -m mlflow --version

echo.
echo [INFO] Menjalankan MLflow UI...
echo [INFO] Buka browser ke: http://127.0.0.1:5000
echo [INFO] Jangan tutup terminal ini selama MLflow digunakan.
echo.

python -m mlflow ui --host 127.0.0.1 --port 5000

pause