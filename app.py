import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# تشغيل الذكاء الاصطناعي بالمفتاح السري
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return "البوت يعمل بنجاح ومستعد للربط والتلقائي!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or {}
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({"status": "error", "message": "No message"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد مبيعات محترف لمتجر وسيم العطار. هدفك الرد بلطف واحتصار وإقناع الزبون بالشراء."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({"status": "success", "reply": response.choices[0].message.content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
