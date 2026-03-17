API_KEY_HEADER = {"X-API-Key": "abcdef12345"}


async def test_wells_returns_list(client):
    resp = await client.get(
        "/api/v1/wells",
        params={"date_query": "2023-10-01"},
        headers=API_KEY_HEADER,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id_well" in data[0]


async def test_wells_missing_date_query_returns_422(client):
    resp = await client.get("/api/v1/wells", headers=API_KEY_HEADER)
    assert resp.status_code == 422
