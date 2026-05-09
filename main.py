from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CHAT_ID = -74435268265279
API_URL = f"https://platform-api.max.ru/messages?chat_id={CHAT_ID}"

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    token = data.get("token")
    text = data.get("text")
    btn_text = data.get("btn_text", "Написать нам")

    if not token or not text:
        return jsonify({"error": "token and text required"}), 400

    payload = {
        "text": text,
        "attachments": [{
            "type": "inline_keyboard",
            "payload": {
                "buttons": [[{
                    "text": "👉 " + btn_text,
                    "url": "https://t.me/MetryPiteraBot"
                }]]
            }
        }]
    }

    res = requests.post(API_URL, json=payload, headers={
        "Authorization": token,
        "Content-Type": "application/json"
    })

    return jsonify(res.json()), res.status_code

@app.route("/")
def index():
    return "OK"

if __name__ == "__main__":
    app.run()
