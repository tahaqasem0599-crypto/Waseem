import streamlit as st
import requests
import json
import base64

# 1. إعدادات الصفحة وهوية التطبيق العالمية #
st.set_page_config(page_title="Waseem AI - Clothing Store", page_icon="👕", layout="wide")

# 2. تحسينات المظهر وتنسيق الـ RTL الفخم #
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
    
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        direction: rtl !important;
        text-align: right !important;
    }
    div.stButton > button:first-child {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px;
    }
    .cache-box {
        background-color: #f1f5f9;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-right: 4px solid #2563eb;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# تهيئة نظام الكاش في جلسة المستخدم لمنع اختفاء البيانات
if "descriptions_cache" not in st.session_state:
    st.session_state.descriptions_cache = []

# --- القائمة الجانبية (نظام الكاش وحفظ الأوصاف) ---
with st.sidebar:
    st.markdown("### 🗄️ الأوصاف المحفوظة سابقاً (Cache)")
    if not st.session_state.descriptions_cache:
        st.info("لا توجد أوصاف محفوظة حالياً.")
    else:
        for idx, item in enumerate(reversed(st.session_state.descriptions_cache)):
            st.markdown(f"""
            <div class="cache-box">
                <strong>📦 السعر: {item['price']} | 📱 {item['platform']}</strong><br>
                <small>{item['desc'][:60]}...</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"📋 نسخ الوصف {len(st.session_state.descriptions_cache) - idx}", key=f"btn_{idx}"):
                st.info("اضغط مرتين لنسخ النص المكتوب بالأسفل:")
                st.text_area("النص الجاهز للنسخ:", value=item['desc'], key=f"copy_area_{idx}")

# --- الواجهة الرئيسية للتطبيق ---
st.markdown('<h1 class="title-text">✨ مساعد التوليد الذكي للملابس ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">توليد أفكار وأوصاف تسويقية فخمة مخصصة لمنصات التواصل الاجتماعي بالصور والنصوص</p>', unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

with col1:
    price_input = st.text_input("💰 سعر القطعة (بالشيكل أو الدولار):", value="10")
    platform_choice = st.selectbox("📱 اختر منصة النشر المستهدفة:", ["فيسبوك (Facebook)", "إنستغرام (Instagram)", "تيك توك (TikTok)"])
    details_input = st.text_area("📝 تفاصيل إضافية (ألوان، مقاسات وخامات):", value="متوفر كل المقاسات وزبط الكلام من عندك")

with col2:
    uploaded_file = st.file_uploader("📸 ارفع صورة قطعة الملابس (اختياري):", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="الصورة المرفوعة بنجاح", use_column_width=True)

st.write("---")

if st.button("🔥 تشغيل محرك الذكاء الاصطناعي وتوليد الرد"):
    api_key = st.secrets.get("gemini_api_key", "").strip()

    if not api_key:
        st.error("⚠️ لم يتم العثور على مفتاح Gemini API في إعدادات الـ Secrets!")
    else:
        with st.spinner("🔄 جاري تحليل البيانات وتوليد الوصف الاحترافي للمنصة..."):
            try:
                headers = {'Content-Type': 'application/json'}
                
                prompt_text = f"""
                أنت خبير تسويق رقمي وكتابة إعلانات محترف متخصص في مبيعات الملابس على السوشيال ميديا.
                قم بكتابة منشور تسويقي فخم ومقنع جداً لقطعة ملابس بالمواصفات التالية:
                - السعر: {price_input}
                - التفاصيل: {details_input}
                
                شروط الصياغة الإلزامية للمنصة المختارة [{platform_choice}]:
                """
                
                if "فيسبوك" in platform_choice:
                    prompt_text += "اجعل الأسلوب تفاعلياً، يركز على العائلة أو التوصيل، ويتضمن دعوة واضحة لاتخاذ إجراء لشراء المنتج مع إيموجيات جذابة للفيسبوك."
                elif "إنستغرام" in platform_choice:
                    prompt_text += "اجعل الأسلوب عصرياً، فاخراً، وموجهاً لعشاق الموضة على إنستغرام. في نهاية المنشور، أضف مجموعة مكونة من 10 إلى 15 هاشتاج نشطة في الملابس."
                elif "تيك توك" in platform_choice:
                    prompt_text += "ابدأ المنشور بـ 'خُطاف لجذب الانتباه' مثير جداً يناسب تيك توك في أول 3 ثوانٍ. واقترح في سطر منفصل فكرة حركة فيديو سريعة تناسب استعراض هذه القطعة."

                url = f"https://googleapis.com{api_key}"

                if uploaded_file is not None:
                    image_bytes = uploaded_file.read()
                    base64_image = base64.b64encode(image_bytes).decode('utf-8')
                    
                    payload = {
                        "contents": [{
                            "parts": [
                                {"text": prompt_text},
                                {
                                    "inline_data": {
                                        "mime_type": uploaded_file.type,
                                        "data": base64_image
                                    }
                                }
                            ]
                        }]
                    }
                else:
                    payload = {
                        "contents": [{"parts": [{"text": prompt_text}]}]
                    }

                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response_data = response.json()
                
                if 'candidates' in response_data and response_data['candidates']:
                    generated_text = response_data['candidates']['content']['parts']['text']
                    
                    st.success(f"✨ تم توليد وصف مخصص بنجاح!")
                    st.markdown(f"<div style='background-color: #f8fafc; padding: 20px; border-radius: 8px; border-right: 5px solid #2563eb; color: #1e293b; line-height: 1.6;'>{generated_text}</div>", unsafe_allow_html=True)
                    
                    # تم إصلاح الحفظ الآمن هنا لمنع خطأ الـ KeyError تماماً
                    st.session_state.descriptions_cache.append({
                        "price": price_input,
                        "platform": platform_choice,
                        "desc": generated_text
                    })
                    st.rerun()
                    
                elif 'error' in response_data:
                    st.error(f"❌ خطأ من سيرفر قوقل: {response_data['error']['message']}")
                else:
                    st.error("⚠️ استجابة غير متوقعة من السيرفر.")
                    st.json(response_data)
                    
            except Exception as e:
                st.error("⚠️ عذراً، حدثت مشكلة أثناء استخراج الرد السريع.")
                with st.expander("🛠️ تفاصيل الخطأ البرمجي للمطور وسيم:"):
                    st.code(str(e))

st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار 🌍</p>', unsafe_allow_html=True)
    
