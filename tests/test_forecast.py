API_KEY_HEADER = {"X-API-Key": "abcdef12345"}


async def test_forecast_returns_data(client):
    resp = await client.get(
        "/api/v1/forecast",
        params={
            "id_well": "POZO-001",
            "date_start": "2023-10-01",
            "date_end": "2023-10-03",
        },
        headers=API_KEY_HEADER,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["id_well"] == "POZO-001"
    assert len(body["data"]) == 3
    assert body["data"][0]["date"] == "2023-10-01"
    assert "prod" in body["data"][0]


async def test_forecast_linear_decline(client):
    resp = await client.get(
        "/api/v1/forecast",
        params={
            "id_well": "POZO-001",
            "date_start": "2023-10-01",
            "date_end": "2023-10-03",
        },
        headers=API_KEY_HEADER,
    )
    data = resp.json()["data"]
    assert data[0]["prod"] > data[1]["prod"] > data[2]["prod"]


async def test_forecast_invalid_date_range_returns_400(client):
    resp = await client.get(
        "/api/v1/forecast",
        params={
            "id_well": "POZO-001",
            "date_start": "2023-10-05",
            "date_end": "2023-10-01",
        },
        headers=API_KEY_HEADER,
    )
    assert resp.status_code == 400


async def test_forecast_unknown_well_returns_404(client):
    resp = await client.get(
        "/api/v1/forecast",
        params={
            "id_well": "POZO-999",
            "date_start": "2023-10-01",
            "date_end": "2023-10-03",
        },
        headers=API_KEY_HEADER,
    )
    assert resp.status_code == 404


async def test_forecast_missing_params_returns_422(client):
    resp = await client.get(
        "/api/v1/forecast",
        params={"id_well": "POZO-001"},
        headers=API_KEY_HEADER,
    )
    assert resp.status_code == 422
