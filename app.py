from flask import Flask, request
import requests

TOKEN = "7864474274:AAGfIlZXU6to65STSxrzo9VNiqlJhmAMHxU"  # ใส่ Token ของบอทคุณ
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is my Flask app!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook:", data)  # ดูข้อมูลที่บอทได้รับ (ตรวจสอบใน Render Logs)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        
        # ส่งข้อความตอบกลับ
        reply_text = f"คุณส่งข้อความว่า: {text}"
        requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": reply_text})

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
