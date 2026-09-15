import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة وهوية التطبيق العالمية #
st.set_page_config(page_title="Waseem AI", page_icon="✨", layout="centered")

# الاحترافي RTL تحسينات المظهر وتنسيق الـ #
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
    
    .stTextInput input, .stTextArea textarea {
        direction: rtl !important;
        text-align: right !important;
    }
    div.stButton > button:first-child {
        width: 100%;
        background-color: #2563eb;
        color: white;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title-text">✨ مساعد التوليد الذكي للملابس ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">توليد أفكار وأوصاف تسويقية فخمة باستخدام الذكاء الاصطناعي</p>', unsafe_allow_html=True)
st.write("---")

price_input = st.text_input("💰 سعر القطعة (بالشيكل أو الدولار):", value="10")
details_input = st.text_area("📝 تفاصيل إضافية (المقاسات المتوفرة، الألوان، خيارات الشحن):", value="متوفر كل المقاسات وزبط الكلام من عندك")

st.write("---")

if st.button("🔥 تشغيل محرك الذكاء الاصطناعي وتوليد الرد"):
    # جلب المفتاح تلقائياً من الإعدادات السريّة
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"].strip()
    else:
        api_key = None

    if not api_key:
        st.error("⚠️ لم يتم العثور على مفتاح Gemini API في إعدادات التطبيق (Secrets)!")
    else:
        with st.spinner("🔄 جاري الاتصال بالذكاء الاصطناعي وتوليد الوصف التسويقي..."):
            try:
                # تحديث طريقة التهيئة لدعم جميع أنواع المفاتيح (الداخلية والخارجية)
                genai.configure(api_key=api_key)
                
                # استخدام النموذج الافتراضي المستقر والمحدث لعام 2026
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                أنت خبير تسويق رقمي وكتابة إعلانات محترف.
                قم بكتابة وصف تسويقي فخم، جذاب ومقنع جداً لقطعة ملابس بالمواصفات التالية:
                - السعر: {price_input}
                - تفاصيل إضافية: {details_input}
                
                اجعل الأسلوب مشوقاً ومناسباً لوسائل التواصل الاجتماعي مع إيموجي وعناوين فرعية فخمة.
                """
                
                response = model.generate_content(prompt)
                
                st.success("✨ تم توليد الوصف التسويقي بنجاح!")
                st.markdown(f"<div style='background-color: #f8fafc; padding: 20px; border-radius: 8px; border-right: 5px solid #2563eb; color: #1e293b; font-weight: 500;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error("⚠️ عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.")
                st.warning("تأكد من أن المفتاح المضاف في الـ Secrets صحيح.")
                with st.expander("🛠️ تفاصيل الخطأ البرمجي (للمطور وسيم):"):
                    st.code(str(e))

st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار 🌍</p>', unsafe_allow_html=True)
        
