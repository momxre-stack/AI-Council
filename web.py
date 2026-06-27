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

    <h2>System details</h2>
    <ul>
      <li>Council: Gemini + DeepSeek</li>
      <li>Mode: Web interface foundation</li>
      <li>Health endpoint: /health</li>
    </ul>

    <h2>Available endpoints</h2>
    <ul>
      <li><a href="/health">/health</a></li>
    </ul>

    <p>Web interface foundation</p>
  </body>
</html>
"""


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
