from fastapi import APIRouter
from utils.response import DEFAULT_RESPONSES
from settings import settings

router = APIRouter(
    tags=["core"]
)

@router.get("/")
async def root():
    return {
        "app_name": settings.app_name,
        "environement": settings.environment,
        "status": 'RUNNING'
    }

