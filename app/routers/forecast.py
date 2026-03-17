import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import verify_api_key
from app.mock_data import WELL_IDS, generate_forecast

router = APIRouter()


@router.get("/forecast")
async def get_forecast(
    id_well: str = Query(..., description="Well identifier (e.g. POZO-001)"),
    date_start: datetime.date = Query(..., description="Start date (YYYY-MM-DD)"),
    date_end: datetime.date = Query(..., description="End date (YYYY-MM-DD)"),
    _api_key: str = Depends(verify_api_key),
) -> dict:
    if date_start > date_end:
        raise HTTPException(
            status_code=400,
            detail="date_start must be less than or equal to date_end",
        )

    if id_well not in WELL_IDS:
        raise HTTPException(status_code=404, detail=f"Well '{id_well}' not found")

    data = generate_forecast(id_well, date_start, date_end)
    return {"id_well": id_well, "data": data}
