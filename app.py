import streamlit as st
import requests
import json

# 1. إعدادات الصفحة وهوية التطبيق العالمية #
st.set_page_config(page_title="Waseem AI", page_icon="✨", layout="centered")

# 2. تحسينات المظهر الفاخر وتنسيق الـ RTL #
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    body, .main, p, div, span, h1, h2, h3, h4, h5, h6, label, input, textarea, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .title-text { color: #2563eb; text-align: center !important; font-weight: 700; }
    .subtitle-text { color: #64748b; text-align: center !important; }
    .footer-text { text-align: center !important; color: #94a3b8; font-size: 14px; margin-top: 50px; }
    
    /* ضبط اتجاه حقول الإدخال */
    .stTextInput input, .stTextArea textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    /* تصميم الزر الفاخر */
    div.stButton > button:first-child {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# واجهة التطبيق العربية
st.markdown('<h1 class="title-text">✨ مساعد التوليد الذكي للملابس ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">توليد أفكار وأوصاف تسويقية فخمة باستخدام الذكاء الاصطناعي</p>', unsafe_allow_html=True)
st.write("---")

# الحقول الأساسية لمتجرك
price_input = st.text_input("💰 سعر القطعة (بالشيكل أو الدولار):", value="10")
details_input = st.text_area("📝 تفاصيل إضافية عن الملابس:", value="متوفر كل المقاسات وزبط الكلام من عندك")

st.write("---")

# 3. زر التفعيل واستدعاء المحرك المباشر #
if st.button("🔥 تشغيل محرك الذكاء الاصطناعي وتوليد الرد"):
    # جلب المفتاح الموثق الذي قدمناه في الخطوة السابقة تلقائياً من الإعدادات
    api_key = st.secrets.get("gemini_api_key", "").strip()

    if not api_key:
        st.error("⚠️ لم يتم العثور على مفتاح Gemini API في إعدادات الـ Secrets!")
    else:
        with st.spinner("🔄 جاري الاتصال المباشر بالسيرفر وتوليد الوصف..."):
            try:
                # الرابط العالمي المباشر لطلب الخدمة من السيرفر دون مكتبات وسيطة
                url = f"https://googleapis.com{api_key}"
                headers = {'Content-Type': 'application/json'}
                
                # صياغة البرومبت التسويقي بذكاء ليعطيك نصوص فخمة
                prompt = f"""
                أنت خبير تسويق رقمي محترف ومختص في التجارة الإلكترونية للملابس. 
                اكتب وصف تسويقي فخم، وجذاب ومقنع جداً لقطعة ملابس بالمواصفات التالية:
                - السعر المطلوب: {price_input}
                - تفاصيل القطعة: {details_input}
                اجعل الأسلوب مشوقاً ومناسباً للنشر الفوري على منصات التواصل الاجتماعي، مع استخدام عناوين منسقة وإيموجي فخمة.
                """
                
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                
                # إرسال الطلب واستقبال النتيجة
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response_data = response.json()
                
                # فك تشفير النص وعرضه داخل التطبيق
                generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
                
                st.success("✨ تم توليد الوصف التسويقي بنجاح!")
                st.markdown(f"<div style='background-color: #f8fafc; padding: 20px; border-radius: 8px; border-right: 5px solid #2563eb; color: #1e293b; line-height: 1.6;'>{generated_text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error("⚠️ عذراً، حدثت مشكلة أثناء استخراج الرد السريع.")
                with st.expander("🛠️ تفاصيل الخطأ البرمجي للمطور وسيم:"):
                    st.code(str(e))

st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار 🌍</p>', unsafe_allow_html=True)
            
