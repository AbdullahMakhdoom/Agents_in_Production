from fastapi.testclient import TestClient
from fastapi_agent.scripts.app import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_agent_endpoint():
    """Test the synchronous agent endpoint"""
    response = client.post(
        "/agent",
        json={"query": "Test query"}
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "Agent" in response.json()["response"]

def test_stream_endpoint():
    """Test the streaming agent endpoint"""
    with client.stream("POST", "/agent/stream", json={"query": "Test query"}) as response:
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream"

        # Check that we receive at least some content
        # content = response.iter_content().read()
        content = ""
        for chunk in response.iter_text():
            content += chunk
        assert len(content) > 0