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
from flask import Flask, request
import requests

# 🔹 ใส่ Token ของ Telegram Bot
TOKEN = "7864474274:AAGfIlZXU6to65STSxrzo9VNiqlJhmAMHxU"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# 🔹 ใส่ API URL สำหรับดึงสัญญาณเทรด
API_URL = "https://<API_URL>/get_signal"  # แก้ไข <API_URL> เป็น URL จริงของ API เทรด

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is my Flask app!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook:", data)  # ตรวจสอบข้อมูลที่ได้รับ (เช็คจาก Logs ใน Render)

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # 🔹 ถ้าใช้คำว่า "/signal" ให้ดึงข้อมูลสัญญาณจาก API
        if text == "/signal":
            response = requests.get(API_URL)
            if response.status_code == 200:
                signal_data = response.json()
                signal_text = f"📊 สัญญาณเทรด:\n{signal_data}"  # ปรับรูปแบบข้อความตามต้องการ
            else:
                signal_text = "❌ ไม่สามารถดึงสัญญาณได้"

            requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": signal_text})

        else:
            reply_text = f"คุณส่งข้อความว่า: {text}"
            requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": reply_text})

    return "OK", 200

# 🔹 เพิ่ม API สำหรับดึงสัญญาณเทรดอัตโนมัติ
@app.route('/get_signal', methods=['GET'])
def get_signal():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json(), 200
        else:
            return {"error": "ไม่สามารถดึงข้อมูลได้"}, 500
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)