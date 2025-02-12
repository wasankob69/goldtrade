from flask import Flask, request
import requests
import config  # ดึงค่าจาก config.py

app = Flask(__name__)

# 📌 Endpoint หลัก สำหรับเช็คสถานะ
@app.route('/')
def home():
    return "Hello, this is my Flask bot!"

# 📌 Endpoint Webhook รับข้อมูลจาก Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Received webhook:", data)  # Debugging

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        # ถ้าเป็นคำสั่ง /get_signal ให้ดึงสัญญาณเทรด
        if text == "/get_signal":
            signal = get_trading_signal()
            send_message(chat_id, signal)

        else:
            send_message(chat_id, f"คุณส่งข้อความว่า: {text}")

    return "OK", 200

# 📌 ฟังก์ชันดึงสัญญาณเทรดจาก API
def get_trading_signal():
    try:
        response = requests.get(config.API_URL)
        print(f"🔍 ดึงข้อมูลจาก API: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            return f"📈 สัญญาณเทรด: {data['signal']} ที่ราคา {data['price']}"
        else:
            return "❌ ไม่สามารถดึงข้อมูลได้"
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"

# 📌 ฟังก์ชันส่งข้อความไป Telegram
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{config.TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)