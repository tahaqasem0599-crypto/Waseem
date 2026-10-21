import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# تهيئة الذكاء الاصطناعي (مفتاح الربط سيتم وضعه في السيرفر لاحقاً للأمان)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return "البوت يعمل بنجاح ومستعد للاتصال بالمتجر ومواقع التواصل!", 200

# هذه الوظيفة تستقبل رسائل العملاء (من الواتساب أو الفيسبوك) وترد عليها ذكياً
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # افتراض أن الرسالة القادمة تحتوي على نص العميل تحت اسم 'message'
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"status": "error", "message": "No message received"}), 400

    try:
        # إرسال الرسالة للذكاء الاصطناعي ليصيغ رداً بيعياً احترافياً
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد مبيعات محترف لمتجر وسيم العطار للأزياء. هدفك إقناع العميل بالشراء والرد بلطف واختصار."},
                {"role": "user", "content": user_message}
            ]
        )
        
        bot_reply = response.choices[0].message.content
        return jsonify({"status": "success", "reply": bot_reply}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
