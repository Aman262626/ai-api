from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)

# ---------------------------
# CONFIG
# ---------------------------
AI_API = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
AUDIO_FOLDER = "static/audio"

os.makedirs(AUDIO_FOLDER, exist_ok=True)

# ---------------------------
# EMOJI MAGIC ✨
# ---------------------------
def add_emojis(text):
    emojis = ["💖", "🥰", "😘", "💫", "🌸", "💗"]
    return f"{text} {emojis[hash(text) % len(emojis)]}"

# ---------------------------
# TEXT GENERATION
# ---------------------------
def get_text_response(message):
    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "Reply romantically in Hinglish. "
                    "Be sweet, caring, girlfriend-style. "
                    "No adult content."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(AI_API, json=payload, headers=headers, timeout=20)
        text = r.json()["choices"][0]["message"]["content"]
        return add_emojis(text)

    except Exception as e:
        return "Oops jaan 😔 thoda sa network issue ho gaya."


# ---------------------------
# TEXT → VOICE
# ---------------------------
def text_to_voice(text):
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    tts = gTTS(text=text, lang="hi")
    tts.save(filepath)

    return f"/static/audio/{filename}"


# ---------------------------
# MAIN CHAT API
# ---------------------------
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True)
    message = data.get("message")

    if not message:
        return jsonify({"error": "message required"}), 400

    reply_text = get_text_response(message)
    voice_url = text_to_voice(reply_text)

    return jsonify({
        "response": reply_text,
        "audio_url": voice_url
    })


# ---------------------------
# HOME
# ---------------------------
@app.route("/")
def home():
    return {"status": "Romantic AI is running 💖"}


# ---------------------------
# RUN SERVER
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
