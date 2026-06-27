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


def test_ask_page_accepts_submitted_question():
    client = app.test_client()
    response = client.post("/ask", data={"question": "What is reliability?"})

    assert response.status_code == 200
    assert b"Ask AI Council" in response.data
    assert b"What is reliability?" in response.data
    assert b'href="/"' in response.data
    assert b'href="/health"' in response.data

def test_ask_page_rejects_empty_question():
    client = app.test_client()
    response = client.post("/ask", data={"question": ""})

    assert response.status_code == 200
    assert b"Ask AI Council" in response.data
    assert b"Question is required." in response.data
    assert b'href="/"' in response.data
    assert b'href="/health"' in response.data



def test_health():
    client = app.test_client()
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}