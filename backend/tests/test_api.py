import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

@pytest.mark.asyncio
async def test_easter_egg():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/antigravity")
    assert response.status_code == 200
    assert "easter egg" in response.json()["message"]

@pytest.mark.asyncio
async def test_generate_rate_limit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "age": 25, 
            "weight": 70, 
            "height": 175, 
            "goal": "Weight Loss", 
            "fitness_level": "Intermediate"
        }
        
        # We simulate multiple requests to trigger slowapi limit
        responses = []
        for _ in range(6):
            res = await ac.post("/api/generate", json=payload)
            responses.append(res)
        
        # First 5 should be 200 OK
        for res in responses[:5]:
            assert res.status_code == 200
            
        # 6th should be 429 Too Many Requests
        assert responses[5].status_code == 429
