from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # <-- VERY IMPORTANT (for Hoppscotch / browser)


# -------------------------------
# TEXT GENERATION
# -------------------------------
def get_text_response(message):
    payload = {
        "messages": [
            {"role": "assistant", "content": "Hello!"},
            {"role": "user", "content": message}
        ]
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Text generation failed: {str(e)}"


# -------------------------------
# IMAGE GENERATION (DUMMY)
# -------------------------------
def generate_image(prompt):
    return f"https://dummyimage.com/512x512/000/fff&text={prompt.replace(' ', '+')}"


# -------------------------------
# MAIN API
# -------------------------------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)

    message = data.get("message")
    image_prompt = data.get("image_prompt")

    if not message and not image_prompt:
        return jsonify({"error": "message or image_prompt required"}), 400

    result = {}

    if message:
        result["text"] = get_text_response(message)

    if image_prompt:
        result["image_url"] = generate_image(image_prompt)

    return jsonify({
        "status": "success",
        "result": result
    })


# -------------------------------
# HOME ROUTE
# -------------------------------
@app.route("/")
def home():
    return {"status": "API running successfully 🚀"}


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
