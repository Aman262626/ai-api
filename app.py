from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# -------------------------------
# TEXT GENERATION (EN + HI + HINGLISH)
# -------------------------------
def get_text_response(message):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "Reply in THREE formats:\n"
                    "1. English\n"
                    "2. Hindi\n"
                    "3. Hinglish (mix of Hindi and English).\n\n"
                    "Format exactly like this:\n"
                    "ENGLISH:\n...\n\nHINDI:\n...\n\nHINGLISH:\n..."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=20)
        text = r.json()["choices"][0]["message"]["content"]

        parts = text.split("\n\n")

        result = {
            "english": "",
            "hindi": "",
            "hinglish": ""
        }

        for part in parts:
            p = part.lower()
            if p.startswith("english"):
                result["english"] = part.replace("ENGLISH:", "").strip()
            elif p.startswith("hindi"):
                result["hindi"] = part.replace("HINDI:", "").strip()
            elif p.startswith("hinglish"):
                result["hinglish"] = part.replace("HINGLISH:", "").strip()

        return result

    except Exception as e:
        return {
            "english": "Error occurred",
            "hindi": "Kuch galat ho gaya",
            "hinglish": str(e)
        }


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
        text_data = get_text_response(message)
        result["text_en"] = text_data["english"]
        result["text_hi"] = text_data["hindi"]
        result["text_hinglish"] = text_data["hinglish"]

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
