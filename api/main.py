from fastapi import FastAPI
from api.routers import health, predict

app = FastAPI(title="UMKM Success Prediction API")

app.include_router(health.router)
app.include_router(predict.router)