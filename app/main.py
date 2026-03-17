import time

from fastapi import FastAPI, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from app.metrics import REQUEST_COUNT, REQUEST_LATENCY
from app.routers import forecast, wells

app = FastAPI(
    title="Predictiva API",
    description="Hydrocarbon production forecasting platform — Phase 1 mock service",
    version="0.1.0",
)

app.include_router(wells.router, prefix="/api/v1", tags=["Wells"])
app.include_router(forecast.router, prefix="/api/v1", tags=["Forecast"])


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    endpoint = request.url.path
    REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    REQUEST_LATENCY.labels(request.method, endpoint).observe(duration)

    return response


@app.get("/health", tags=["System"])
async def health_check() -> dict:
    return {"status": "ok"}


@app.get("/metrics", include_in_schema=False)
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
