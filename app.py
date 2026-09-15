import streamlit as st
import requests
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
    
    /* تحسين اتجاه النصوص داخل حقول الإدخال والزر ليتناسب مع الواجهة العربية */
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

# عنوان التطبيق
st.markdown('<h1 class="title-text">✨ مساعد التوليد الذكي للملابس ✨</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">توليد أفكار وأوصاف تسويقية فخمة باستخدام الذكاء الاصطناعي</p>', unsafe_allow_html=True)
st.write("---")

# الحقول الأساسية بناءً على واجهة تطبيقك
price_input = st.text_input("💰 سعر القطعة (بالشيكل أو الدولار):", value="10")
details_input = st.text_area("📝 تفاصيل إضافية (المقاسات المتوفرة، الألوان، خيارات الشحن):", value="متوفر كل المقاسات وزبط الكلام من عندك")

st.write("---")

# زر تشغيل المحرك
if st.button("🔥 تشغيل محرك الذكاء الاصطناعي وتوليد الرد"):
    # جلب المفتاح تلقائياً من Secrets بشكل مخفي وآمن
    # سيبحث التطبيق أولاً في Secrets عن متغير باسم gemini_api_key
    if "gemini_api_key" in st.secrets:
        api_key = st.secrets["gemini_api_key"]
    else:
        api_key = None

    if not api_key:
        st.error("⚠️ لم يتم العثور على مفتاح Gemini API في إعدادات التطبيق (Secrets)!")
        st.info("يا وسيم، تأكد من إضافة `gemini_api_key = 'مفتاحك_هنا'` في لوحة تحكم Streamlit Cloud.")
    else:
        with st.spinner("🔄 جاري الاتصال بالذكاء الاصطناعي وتوليد الوصف التسويقي..."):
            try:
                # 1. تهيئة إعدادات المفتاح وتطهيره من أي مسافات زائدة
                genai.configure(api_key=api_key.strip())
                
                # 2. استدعاء النموذج المستقر والسريع
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # 3. صياغة البرومبت التسويقي باحترافية بناءً على مدخلاتك
                prompt = f"""
                أنت خبير تسويق رقمي وكتابة إعلانات محترف.
                قم بكتابة وصف تسويقي فخم، جذاب ومقنع جداً لقطعة ملابس بالمواصفات التالية:
                - السعر: {price_input}
                - تفاصيل إضافية: {details_input}
                
                اجعل الأسلوب مشوقاً ومناسباً لوسائل التواصل الاجتماعي (استخدم إيموجي مناسبة وعناوين فرعية).
                """
                
                # 4. طلب توليد المحتوى
                response = model.generate_content(prompt)
                
                # 5. عرض النتيجة بنجاح في الواجهة
                st.success("✨ تم توليد الوصف التسويقي بنجاح!")
                st.markdown(f"<div style='background-color: #f8fafc; padding: 20px; border-radius: 8px; border-right: 5px solid #2563eb;'>{response.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                # معالجة الخطأ بذكاء وعرض تفاصيله للمطور دون توقف التطبيق
                st.error("⚠️ عذراً، حدث خطأ أثناء الاتصال بالذكاء الاصطناعي.")
                st.warning("تأكد من أن مفتاح الـ API المضاف في الـ Secrets صحيح وصالح للعمل.")
                with st.expander("🛠️ تفاصيل الخطأ البرمجي (للمطور وسيم):"):
                    st.code(str(e))

# تذييل الصفحة الخاص بك بشكل منسق واحترافي
st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار 🌍</p>', unsafe_allow_html=True)
