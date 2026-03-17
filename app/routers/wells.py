import datetime

from fastapi import APIRouter, Depends, Query

from app.auth import verify_api_key
from app.mock_data import get_wells

router = APIRouter()


@router.get("/wells")
async def list_wells(
    date_query: datetime.date = Query(..., description="Date for the well query (YYYY-MM-DD)"),
    _api_key: str = Depends(verify_api_key),
) -> list[dict]:
    return get_wells()
