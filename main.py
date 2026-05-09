from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

CHAT_ID = -74435268265279
API_URL = f"https://platform-api.max.ru/messages?chat_id={CHAT_ID}"
UPLOAD_URL = "https://platform-api.max.ru/uploads"

@app.route("/publish", methods=["POST"])
def publish():
    data = request.json
    token = data.get("token")
    text = data.get("text")
    btn_text = data.get("btn_text", "Написать нам")
    image_b64 = data.get("image")
    image_type = data.get("image_type", "image/jpeg")

    if not token or not text:
        return jsonify({"error": "token and text required"}), 400

    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    attachments = []

    if image_b64:
        try:
            image_bytes = base64.b64decode(image_b64)
            upload_res = requests.post(
                UPLOAD_URL + "?type=photo",
                headers={"Authorization": token, "Content-Type": image_type},
                data=image_bytes
            )
            if upload_res.status_code == 200:
                upload_data = upload_res.json()
                photos = upload_data.get("photos", {})
                for key, val in photos.items():
                    attachments.append({
                        "type": "image",
                        "payload": {"token": val.get("token")}
                    })
                    break
        except Exception as e:
            print(f"Image upload error: {e}")

    attachments.append({
        "type": "inline_keyboard",
        "payload": {
            "buttons": [[{
                "text": "👉 " + btn_text,
                "url": "https://t.me/MetryPiteraBot"
            }]]
        }
    })

    payload = {"text": text, "attachments": attachments}
    res = requests.post(API_URL, json=payload, headers=headers)
    return jsonify(res.json()), res.status_code

@app.route("/")
def index():
    return "OK"

if __name__ == "__main__":
    app.run()
