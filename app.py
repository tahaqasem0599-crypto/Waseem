import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import stripe

app = Flask(__name__)

# 1. تهيئة المفاتيح السرية للذكاء الاصطناعي وبوابات الدفع
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# معلومات المورد (AliExpress API كمثال)
ALIEXPRESS_API_URL = "https://aliexpress.com" 
ALI_API_KEY = os.environ.get("ALIEXPRESS_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "🚀 محرك الأرباح التلقائي لمتجر وسيم العطار يعمل أونلاين 24 ساعة!", 200

# 2. رابط استقبال الأموال (Stripe Webhook)
# هذا الرابط يتلقى إشعاراً فورياً كلما قام زبون بالدفع لك في المتجر
@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # عندما تنجح عملية الدفع وتستلم المال كليوم
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # جلب بيانات الزبون وعنوانه والمنتج الذي اشتراه
        customer_email = session['customer_details']['email']
        customer_name = session['shipping_details']['name']
        address = session['shipping_details']['address']
        
        # خطوة جلب المال الآلي: البوت يرسل طلباً للتاجر الأصلي ليشحن للزبون فوراً
        order_status = order_from_supplier(customer_name, address, session['metadata']['product_id'])
        
        if order_status:
            print(f"💰 نجاح! تم استلام المال من {customer_name} وشحن المنتج له تلقائياً.")
            return jsonify({"status": "success", "message": "Money received, product ordered!"}), 200

    return jsonify({"status": "ignored"}), 200

# 3. وظيفة الشراء التلقائي من التاجر والمورد الأصلي
def order_from_supplier(name, address, product_id):
    try:
        # البوت يتصل بالمورد ويشتري المنتج ببيانات الزبون مستخدماً أموال الأرباح
        headers = {"Authorization": f"Bearer {ALI_API_KEY}", "Content-Type": "application/json"}
        order_data = {
            "product_id": product_id,
            "quantity": 1,
            "shipping_address": {
                "name": name,
                "country": address['country'],
                "city": address['city'],
                "line1": address['line1']
            }
        }
        # إرسال أمر الشراء الفوري للمورد
        response = requests.post(f"{ALIEXPRESS_API_URL}/order", json=order_data, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في الشحن التلقائي: {str(e)}")
        return False

# 4. وظيفة توليد واختيار المنتجات الأكثر مبيعاً وترويجها
@app.route('/find-and-promote', methods=['GET'])
def find_and_promote():
    try:
        # البوت يبحث عن منتج "تريند" عالي المبيعات من منصة التوريد
        best_selling_product = "ساعة رولكس ذكية فائقة الفخامة" 
        
        # صياغة النص الإعلاني بذكاء خارق لإقناع الناس بالشراء
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت خبير تسويق إلكتروني عالمي. صغ إعلاناً بيعياً ساحراً باللغة العربية يجبر العميل على الشراء فوراً."},
                {"role": "user", "content": best_selling_product}
            ]
        )
        ad_text = ai_response.choices.message.content
        return jsonify({"status": "success", "product": best_selling_product, "ad": ad_text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
