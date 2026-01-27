import os
import hashlib
from datetime import datetime, timezone
from flask import Flask, request

app = Flask(__name__)

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@app.get("/")
def home():
    return """
    <html>
      <head><title>IP Envoy</title></head>
      <body style="font-family: Arial; max-width: 720px; margin: 40px auto;">
        <h1>IP Envoy</h1>
        <p>Save an idea and generate a timestamped proof.</p>
        <form method="POST" action="/record">
          <label>Email (optional)</label><br/>
          <input name="email" style="width:100%; padding:10px;"/><br/><br/>
          <label>Your idea</label><br/>
          <textarea name="idea" rows="10" style="width:100%; padding:10px;"></textarea><br/><br/>
          <button type="submit">Record Idea</button>
        </form>
      </body>
    </html>
    """

@app.post("/record")
def record():
    email = (request.form.get("email") or "").strip()
    idea = (request.form.get("idea") or "").strip()

    now = datetime.now(timezone.utc).isoformat()
    digest = sha256(f"{email}|{now}|{idea}")

    return f"""
    <html>
      <body style="font-family: Arial; max-width: 720px; margin: 40px auto;">
        <h2>Proof of Creation</h2>
        <p><b>Timestamp:</b> {now}</p>
        <p><b>Creator:</b> {email or "Not provided"}</p>
        <p><b>Fingerprint (SHA-256):</b></p>
        <pre>{digest}</pre>
        <a href="/">Record another</a>
      </body>
    </html>
    """
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
