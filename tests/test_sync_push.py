import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from datetime import datetime, timedelta

pytestmark = pytest.mark.asyncio


async def test_push_newer_update():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        payload = {
            "device_id": "device123",
            "entity": "order",
            "payload": {
                "id": 1,
                "updated_at": datetime.utcnow().isoformat(),
                "total": 100
            }
        }

        res = await client.post("/api/sync/push", json=payload)
        assert res.status_code == 200
        assert res.json()["status"] == "queued"


async def test_push_older_update():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:

        new_time = datetime.utcnow()

        await client.post("/api/sync/push", json={
            "device_id": "device123",
            "entity": "order",
            "payload": {
                "id": 1,
                "updated_at": new_time.isoformat(),
                "total": 200
            }
        })

        old_time = new_time - timedelta(hours=1)

        res = await client.post("/api/sync/push", json={
            "device_id": "device123",
            "entity": "order",
            "payload": {
                "id": 1,
                "updated_at": old_time.isoformat(),
                "total": 150
            }
        })

        assert res.status_code == 200
        assert res.json()["status"] == "ignored"
