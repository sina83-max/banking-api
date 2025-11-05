from fastapi import APIRouter

from backend.app.core.logging import get_logger

logger = get_logger()

router = APIRouter(
    prefix="/home",
)

@router.get("/")
async def home():
    logger.info("home route called")
    logger.debug("home route called")
    logger.error("home route called")
    # logger.warning("home route called")
    logger.critical("home route called")
    return {"message": "Hello world!"}