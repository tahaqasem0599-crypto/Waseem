import streamlit as st
import time

# 1. إعدادات الصفحة العامة ودعم اللغة العربية (RTL)
st.set_page_config(page_title="أمل غزة: حياة وبناء", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    body, .main, .block-container { direction: rtl; text-align: right; }
    h1, h2, h3, p { text-align: center; }
    .stButton>button { width: 100%; font-size: 18px; font-weight: bold; background-color: #00b3b3; color: white; padding: 10px; border-radius: 8px; }
    .stButton>button:hover { background-color: #008080; }
    .diamond-box { background-color: #2a2a2a; border: 1px solid #FFD700; border-radius: 20px; padding: 10px; text-align: center; font-size: 20px; color: #FFD700; font-weight: bold; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة رصيد الماس وحالة التطبيق في الذاكرة
if 'diamonds' not in st.session_state:
    st.session_state.diamonds = 0
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "start"

# عرض العداد العالمي للماس في الأعلى دائماً
st.markdown(f'<div class="diamond-box">💎 رصيدك الحالي: {st.session_state.diamonds} ماسة</div>', unsafe_allow_html=True)

# 3. شاشات ومراحل التطبيق
if st.session_state.current_stage == "start":
    st.title("أمل غزة: حياة وبناء 🇵🇸")
    st.write("مرحباً بك يا وسيم في مشروعك الأول. اجمع الماس من خلال إنقاذ الأرواح وإعادة الإعمار، وحوّل الإعلانات إلى أرباح!")
    
    if st.button("ابدأ تشغيل التطبيق واللعب 🚀"):
        st.session_state.current_stage = "rescue"
        st.rerun()

elif st.session_state.current_stage == "rescue":
    st.header("المرحلة 1: مهمة الإنقاذ العاجلة 🚑")
    st.write("سيارة الإسعاف تتحرك الآن لإنقاذ المصابين في شوارع غزة.")
    
    if st.button("تم إنقاذ الجميع بنجاح! الانتقال للتوزيع ✨"):
        st.session_state.current_stage = "relief"
        st.rerun()
        
    if st.button("💥 محاكاة حادث مفاجئ (خسارة)"):
        st.session_state.current_stage = "ad_screen"
        st.rerun()

elif st.session_state.current_stage == "ad_screen":
    st.header("📽️ تحميل إعلان المكافأة التلقائي")
    st.write("شاهد هذا الفيديو القصير لفتح محاولة ثانية مجانية وكسب 50 ماسة فوراً لحسابك.")
    
    if st.button("شاهد الإعلان الآن واكسب المال والماس 💰"):
        with st.spinner("جاري تشغيل الإعلان المربح... (يتم تسجيل الأرباح تلقائياً في حساب وسيم) 💵"):
            time.sleep(2) # محاكاة وقت الإعلان
        st.session_state.diamonds += 50
        st.success("رائع! شاهدت الإعلان كاملاً وحصلت على 50 ماسة في رصيدك 💎")
        time.sleep(1)
        st.session_state.current_stage = "rescue"
        st.rerun()

elif st.session_state.current_stage == "relief":
    st.header("المرحلة 2: توزيع الخيام والمساعدات 📦")
    st.write("قم بتأمين الطعام، المياه، والملابس للعائلات النازحة لرفع معدل البقاء.")
    
    if st.button("اكتمل التوزيع! اذهب لإعادة الإعمار 🏗️"):
        st.session_state.current_stage = "build"
        st.rerun()

elif st.session_state.current_stage == "build":
    st.header("المرحلة 3: بناء المستشفيات والمدارس 🏗️")
    st.write("المبنى قيد الإنشاء ويحتاج إلى وقت ليكتمل تماماً.")
    
    if st.button("إنهاء البناء فوراً (يخصم 10 ماسات) ⚡"):
        if st.session_state.diamonds >= 10:
            st.session_state.diamonds -= 10
            st.success("تم استخدام 10 ماسات لتسريع البناء بنجاح! 🏥🛠️")
            time.sleep(1.5)
            st.session_state.current_stage = "start"
            st.rerun()
        else:
            st.error("رصيد الماس غير كافٍ! شاهد إعلانات للحصول على المزيد.")
            st.session_state.current_stage = "ad_screen"
            st.rerun()
            
    if st.button("العودة للرئيسية وإنهاء المهمة 🎉"):
        st.session_state.current_stage = "start"
        st.rerun()
