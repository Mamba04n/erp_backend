import pytest
from httpx import AsyncClient, ASGITransport
from main import app

pytestmark = pytest.mark.asyncio


async def test_pull_updates():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        await client.post("/api/sync/push", json={
            "device_id": "deviceXYZ",
            "entity": "order",
            "payload": {"id": 99, "updated_at": "2025-01-12T10:30:00", "total": 500}
        })

        res = await client.post("/api/sync/pull", json={"device_id": "deviceXYZ"})

        assert res.status_code == 200
        assert "updates" in res.json()
        assert len(res.json()["updates"]) >= 1
