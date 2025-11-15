import pytest
from httpx import AsyncClient, ASGITransport
from main import app

pytestmark = pytest.mark.asyncio


async def test_device_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        await client.post("/api/sync/pull", json={"device_id": "device_status_test"})

        res = await client.get("/api/sync/status/device_status_test")

        assert res.status_code == 200
        data = res.json()

        assert data["device_id"] == "device_status_test"
        assert "last_sync" in data
        assert "registered_at" in data
