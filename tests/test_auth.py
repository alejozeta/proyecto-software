async def test_missing_api_key_returns_403(client):
    resp = await client.get("/api/v1/wells", params={"date_query": "2023-10-01"})
    assert resp.status_code == 403


async def test_invalid_api_key_returns_403(client):
    resp = await client.get(
        "/api/v1/wells",
        params={"date_query": "2023-10-01"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert resp.status_code == 403


async def test_valid_api_key_returns_200(client):
    resp = await client.get(
        "/api/v1/wells",
        params={"date_query": "2023-10-01"},
        headers={"X-API-Key": "abcdef12345"},
    )
    assert resp.status_code == 200
