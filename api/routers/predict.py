from fastapi import APIRouter
from api.services.prediction_service import get_dummy_prediction

router = APIRouter(prefix="/predict", tags=["predict"])

@router.get("/")
def predict_dummy():
    return get_dummy_prediction()