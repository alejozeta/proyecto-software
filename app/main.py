from fastapi import FastAPI

from app.routers import forecast, wells

app = FastAPI(
    title="Predictiva API",
    description="Hydrocarbon production forecasting platform — Phase 1 mock service",
    version="0.1.0",
)

app.include_router(wells.router, prefix="/api/v1", tags=["Wells"])
app.include_router(forecast.router, prefix="/api/v1", tags=["Forecast"])


@app.get("/health", tags=["System"])
async def health_check() -> dict:
    return {"status": "ok"}
