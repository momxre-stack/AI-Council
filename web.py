from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return """
<!doctype html>
<html>
  <head>
    <title>AI Council</title>
  </head>
  <body>
    <h1>AI Council</h1>

    <p>Status: Running</p>

    <h2>Navigation</h2>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/health">Health</a></li>
    </ul>

    <h2>System details</h2>
    <ul>
      <li>Council: Gemini + DeepSeek</li>
      <li>Mode: Web interface foundation</li>
      <li>Health endpoint: /health</li>
    </ul>

    <h2>Project overview</h2>
    <p>
      AI Council is a multi-model decision system focused on reliable answers
      through provider agreement and debate.
    </p>

    <h2>Available endpoints</h2>
    <ul>
      <li><a href="/health">/health</a></li>
    </ul>

    <p>Web interface foundation</p>
  </body>
</html>
"""


@app.get("/ask")
def ask():
    return """
<!doctype html>
<html>
  <head>
    <title>Ask AI Council</title>
  </head>
  <body>
    <h1>Ask AI Council</h1>

    <p>Ask page form foundation. Submissions are not enabled yet.</p>

    <form>
      <label for="question">Question</label><br>
      <textarea id="question" name="question" rows="6" cols="60"></textarea><br>
      <button type="button">Ask</button>
    </form>

    <p>
      <a href="/">Home</a>
      |
      <a href="/health">Health</a>
    </p>
  </body>
</html>
"""


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)