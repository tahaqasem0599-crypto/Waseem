import streamlit as st
import urllib.parse
import requests

# إعدادات الصفحة وهوية التطبيق العالمية
st.set_page_config(page_title="Waseem AI Auto-Sales Pro", page_icon="🚀", layout="centered")

# تحسينات المظهر وتنسيق الـ RTL الاحترافي
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    body, .main, p, div, span, h1, h2, h3, input, textarea, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .title-text { color: #2563eb; text-align: center !important; font-size: 32px; font-weight: bold; width: 100%; display: block; margin-bottom: 5px; }
    .subtitle-text { color: #64748b; text-align: center !important; font-size: 16px; width: 100%; display: block; margin-bottom: 20px; }
    .footer-text { text-align: center !important; color: #94a3b8; font-size: 14px; margin-top: 60px; width: 100%; display: block; }
    .response-box { text-align: right !important; }
    </style>
""", unsafe_allow_html=True)

# واجهة التطبيق الاحترافية
st.markdown('<p class="title-text">🚀 Waseem AI Auto-Sales Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">النظام السحابي الذكي لأتمتة مبيعات المتاجر الرقمية المربوط بالذكاء الاصطناعي التفاعلي</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("📊 لوحة تحكم التاجر الذكية")
product_name = st.text_input("📦 اسم المنتج أو قطعة الملابس:")
product_price = st.number_input("💰 سعر القطعة (بالشيكل أو الدولار):", min_value=0)
product_details = st.text_area("📝 تفاصيل إضافية (المقاسات المتوفرة، الألوان، خيارات الشحن):")

# خانة لإدخال مفتاح الـ API الخاص بـ Gemini لضمان استمرارية عمل الخدمة بشكل مستقل وعالمي
gemini_api_key = st.text_input("🔑 أدخل مفتاح Gemini API الخاص بك (اختياري للاستخدام الخاص):", type="password")

if st.button("🔥 تشغيل محرك الذكاء الاصطناعي وتوليد الرد"):
    if product_name and product_price:
        with st.spinner("🤖 يقوم الذكاء الاصطناعي الآن بتحليل المنتج وصياغة الرد التسويقي الخارق..."):
            
            # صياغة الأوامر الذكية الموجهة للنموذج (Prompt Engineering)
            prompt = f"""
            أنت خبير تسويق رقمي ومسؤول مبيعات محترف. قم بكتابة رد تسويقي مقنع جداً لعميل يستفسر عن المنتج التالي:
            اسم المنتج: {product_name}
            السعر: {product_price}
            تفاصيل إضافية: {product_details if product_details else 'متوفر بأعلى جودة وأفضل خامات'}
            
            شروط الرد:
            1. ابدأ بترحيب حار بالعميل وبأسلوب فخم.
            2. اعرض مميزات المنتج بذكاء واشرح تفاصيله بشكل جذاب باستخدام الإيموجي المناسبة.
            3. اذكر السعر بطريقة تشجع على الشراء (مثلاً: السعر المفاجأة، أو استثمار مميز).
            4. أضف عبارة تحفيزية لخلق شعور بالعجلة (مثال: الكمية محدودة جداً، الطلب مرتفع اليوم).
            5. اسأله في النهاية إذا كان يود تأكيد الحجز فوراً وتجهيز الشحن له.
            """
            
            # استخدام مفتاح افتراضي إذا لم يقم المستخدم بإدخال مفتاحه الخاص
            api_key = gemini_api_key if gemini_api_key else "AIzaSyD-YOUR_DEFAULT_API_KEY_HERE"
            
            # إرسال الطلب الفعلي لخوادم Google Gemini
            url = f"https://googleapis.com{api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                response = requests.post(url, json=payload, headers=headers)
                result = response.json()
                
                # استخراج النص المولد من استجابة الذكاء الاصطناعي
                ai_response = result['candidates'][0]['content']['parts'][0]['text']
                st.success(f"✅ نجح نظام Waseem AI في التوليد الديناميكي!")
                
                st.write("### 🤖 الرد التسويقي الذكي المولد تفاعلياً:")
                st.text_area("", value=ai_response, height=250, key="generated_text")
                
                # تجهيز رابط الإرسال المباشر للواتساب
                encoded_text = urllib.parse.quote(ai_response)
                whatsapp_url = f"https://wa.me{encoded_text}"
                
                # أزرار التفاعل السريع
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none;"><button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer;">📲 إرسال مباشر عبر WhatsApp</button></a>', unsafe_allow_html=True)
                with col2:
                    st.info("💡 يمكنك نسخ النص مباشرة من الصندوق أعلاه واستخدامه في أي منصة!")
                    
            except Exception as e:
                st.error("⚠️ عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي. تأكد من إدخال مفتاح API صحيح أو حاول مجدداً لاحقاً.")
                
    else:
        st.warning("⚠️ الرجاء إدخال اسم المنتج وسعره لتفعيل محرك الذكاء الاصطناعي.")

# بصمة الشهرة العالمية للمطور
st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار</p>', unsafe_allow_html=True)
            
