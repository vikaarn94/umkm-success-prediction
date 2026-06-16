from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {
        "status": "ok",
        "message": "API berjalan dengan baik"
    }