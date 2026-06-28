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
    assert b"multi-model decision system" in response.data
    assert b"Navigation" in response.data
    assert b"Home" in response.data


def test_ask_page():
    client = app.test_client()
    response = client.get("/ask")

    assert response.status_code == 200
    assert b"Ask AI Council" in response.data
    assert b"Question" in response.data
    assert b"<textarea" in response.data
    assert b"Ask" in response.data
    assert b'href="/"' in response.data
    assert b'href="/health"' in response.data


def test_ask_page_accepts_submitted_question(monkeypatch):
    def fake_ask_council(question):
        return {
            "question": question,
            "responses": {
                "gemini": "Gemini test response",
                "deepseek": "DeepSeek test response",
            },
            "status": "ok",
        }

    monkeypatch.setattr("web.ask_council", fake_ask_council)

    client = app.test_client()
    response = client.post("/ask", data={"question": "What is reliability?"})

    assert response.status_code == 200
    assert b"Ask AI Council" in response.data
    assert b"What is reliability?" in response.data

    assert b"<h2>Gemini</h2>" in response.data
    assert b"Gemini test response" in response.data

    assert b"<h2>DeepSeek</h2>" in response.data
    assert b"DeepSeek test response" in response.data

    assert b"<h2>Status</h2>" in response.data
    assert b"ok" in response.data

    assert b'href="/"' in response.data
    assert b'href="/health"' in response.data

def test_ask_page_shows_no_response_for_missing_provider_response(monkeypatch):
    def fake_ask_council(question):
        return {
            "question": question,
            "responses": {
                "gemini": None,
                "deepseek": "DeepSeek test response",
            },
            "status": "degraded",
        }

    monkeypatch.setattr("web.ask_council", fake_ask_council)

    client = app.test_client()
    response = client.post("/ask", data={"question": "What is reliability?"})

    assert response.status_code == 200
    assert b"<h2>Gemini</h2>" in response.data
    assert b"No response" in response.data
    assert b"None" not in response.data
    assert b"<h2>DeepSeek</h2>" in response.data
    assert b"DeepSeek test response" in response.data
    assert b"<h2>Status</h2>" in response.data
    assert b"degraded" in response.data

def test_ask_page_rejects_empty_question():
    client = app.test_client()
    response = client.post("/ask", data={"question": ""})

    assert response.status_code == 200
    assert b"Ask AI Council" in response.data
    assert b"Question is required." in response.data
    assert b'href="/"' in response.data
    assert b'href="/health"' in response.data


def test_ask_page_does_not_show_empty_submitted_question():
    client = app.test_client()
    response = client.post("/ask", data={"question": ""})

    assert response.status_code == 200
    assert b"Submitted question:" not in response.data
    assert b"<p></p>" not in response.data



def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}