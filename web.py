from flask import Flask, jsonify, request
from agent.council import ask_council

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


@app.route("/ask", methods=["GET", "POST"])
def ask():
    submitted_question = ""
    error_message = ""

    if request.method == "POST":
        submitted_question = request.form.get("question", "").strip()

        if not submitted_question:
            error_message = "Question is required."

    submitted_question_html = ""
    error_message_html = ""
    council_response_html = ""
    council_status_html = ""
    degraded_reason_html = ""

    if submitted_question:
        submitted_question_html = f"<p>Submitted question: {submitted_question}</p>"
        council_result = ask_council(submitted_question)
        gemini_response = council_result["responses"]["gemini"] or "No response"
        deepseek_response = council_result["responses"]["deepseek"] or "No response"
        council_status = council_result["status"]
        degraded_reason = council_result.get("degraded_reason")
        council_response_html = (
            f"<h2>Gemini</h2><pre>{gemini_response}</pre>"
            f"<h2>DeepSeek</h2><pre>{deepseek_response}</pre>"
        )
        council_status_html = f"<h2>Status</h2><p>{council_status}</p>"

        if degraded_reason:
            degraded_reason_html = f"<h2>Reason</h2><p>{degraded_reason}</p>"

    if error_message:
        error_message_html = f"<p>{error_message}</p>"

    return f"""
<!doctype html>
<html>
  <head>
    <title>Ask AI Council</title>
  </head>
  <body>
    <h1>Ask AI Council</h1>

    <p>Ask page form foundation. Submissions are handled locally only.</p>

    <form method="post">
      <label for="question">Question</label><br>
      <textarea id="question" name="question" rows="6" cols="60">{submitted_question}</textarea><br>
      <button type="submit">Ask</button>
    </form>

    {submitted_question_html}
    {council_response_html}
    {council_status_html}
    {degraded_reason_html}
    {error_message_html}

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