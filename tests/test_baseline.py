from web import app


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"AI Council" in response.data
    assert b"Status: Running" in response.data
    assert b"/health" in response.data
    assert b"Council: Gemini + DeepSeek" in response.data
    assert b"Mode: Web interface foundation" in response.data
    assert b"Health endpoint: /health" in response.data


def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}