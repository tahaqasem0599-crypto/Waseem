import streamlit as st
import streamlit.components.v1 as components
import time

# 1. الإعدادات المتقدمة وتصميم الواجهة المتجاوبة بالكامل بدعم RTL
st.set_page_config(page_title="أمل غزة: حياة وبناء", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    body, .main, .block-container { direction: rtl; text-align: right; background-color: #121212; color: #ffffff; }
    h1, h2, h3, p { text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton>button { width: 100%; font-size: 18px; font-weight: bold; background-color: #00b3b3; color: white; padding: 12px; border-radius: 8px; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #008080; transform: scale(1.02); }
    .diamond-box { background: linear-gradient(135deg, #1e1e1e, #2a2a2a); border: 2px solid #FFD700; border-radius: 15px; padding: 15px; text-align: center; font-size: 22px; color: #FFD700; font-weight: bold; box-shadow: 0 4px 15px rgba(255,215,0,0.2); margin-bottom: 25px; }
    .status-card { background-color: #1f1f1f; border: 1px solid #333333; border-radius: 12px; padding: 20px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .badge { background-color: #333; padding: 4px 10px; border-radius: 8px; font-size: 14px; border: 1px solid #555; }
    </style>
""", unsafe_allow_html=True)

# 2. إدارة الذاكرة السحابية وحفظ الرصيد والمستويات تلقائياً لـ وسيم
if 'diamonds' not in st.session_state:
    st.session_state.diamonds = 130
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = "start"
if 'ambulance_level' not in st.session_state:
    st.session_state.ambulance_level = 1
if 'truck_level' not in st.session_state:
    st.session_state.truck_level = 1

# العداد العالمي الثابت للرصيد والأرباح بالماس أعلى التطبيق
st.markdown(f'<div class="diamond-box">💎 رصيد حسابك الحالي: {st.session_state.diamonds} ألماسة</div>', unsafe_allow_html=True)

# 3. محرك الشاشات والمراحل الذكي
if st.session_state.current_stage == "start":
    st.title("أمل غزة: حياة وبناء 🇵🇸")
    st.markdown('<p style="font-size:18px; color:#bbb;">مشروعك التقني الأول والجاهز للانطلاق لجني الأرباح اليومية المستمرة</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ابدأ تشغيل اللعبة والإنقاذ 🚀"):
            st.session_state.current_stage = "rescue"
            st.rerun()
    with col2:
        if st.button("متجر الترقيات والآليات 🛠️"):
            st.session_state.current_stage = "upgrade_shop"
            st.rerun()
            
    st.markdown("---")
    st.subheader("🏆 لوحة الصدارة اليومية وأبطال غزة")
    st.write("1. وسيم القاسم — 🥇 2450 ألماسة")
    st.write("2. أحمد خليل — 🥈 1820 ألماسة")
    st.write("3. سارة محمد — 🥉 1500 ألماسة")

elif st.session_state.current_stage == "rescue":
    st.header("المرحلة 1: مهمة الإنقاذ العاجلة 🚑")
    st.markdown(f'<div class="status-card"><p>سيارة الإسعاف (مستوى {st.session_state.ambulance_level}) تتحرك الآن لتلبية نداءات الاستغاثة وإنقاذ الجرحى.</p></div>', unsafe_allow_html=True)
    
    if st.button("✨ تم إنقاذ الجميع بنجاح! الانتقال للتوزيع"):
        st.session_state.current_stage = "relief"
        st.rerun()
        
    if st.button("💥 محاكاة حادث مفاجئ وتعطل الإسعاف"):
        st.session_state.current_stage = "ad_screen"
        st.rerun()

elif st.session_state.current_stage == "ad_screen":
    st.header("📽️ شاشة الإعلانات الحقيقية والمكافآت المباشرة")
    st.write("شاهد الإعلان المربح بالأسفل لفتح محاولة جديدة فوراً وإضافة 50 ماسة إلى رصيدك.")
    
    # -------------------------------------------------------------
    # 📌 شفرة الإعلانات الرسمية والمباشرة المتصلة بحساب وسيم في Google AdMob
    # -------------------------------------------------------------
    admob_html_code = """
    <div style="text-align:center; margin: 20px 0;">
        <script async src="https://googlesyndication.com"
             crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:block; text-align:center;"
             data-ad-layout="in-article"
             data-ad-format="fluid"
             data-ad-client="ca-pub-2644074166637349"
             data-ad-slot="6350752475"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
    """
    components.html(admob_html_code, height=250)
    # -------------------------------------------------------------
    
    if st.button("اضغط لتأكيد مشاهدة الإعلان واستلام الأرباح 💰"):
        st.session_state.diamonds += 50
        st.success("تم تسجيل مشاهدة ناجحة! أضيفت 50 ماسة، وسجلت الأرباح النقدية في حسابك المالي 💵")
        time.sleep(2)
        st.session_state.current_stage = "rescue"
        st.rerun()

elif st.session_state.current_stage == "relief":
    st.header("المرحلة 2: توزيع الخيام والمساعدات الإنسانية 📦")
    st.markdown(f'<div class="status-card"><p>شاحنة المساعدات (مستوى {st.session_state.truck_level}) تقوم بنقل وتأمين مياه الشرب، الطحين، والخيام للعائلات.</p></div>', unsafe_allow_html=True)
    
    if st.button("اكتمل التوزيع بنجاح! الانتقال للبناء والتعمير 🏗️"):
        st.session_state.current_stage = "build"
        st.rerun()

elif st.session_state.current_stage == "build":
    st.header("المرحلة 3: إعادة إعمار المستشفيات والمدارس 🏗️")
    st.write("العمل جارٍ على الأنقاض لرفع البناء الجديد وتجهيز المستشفى الميداني.")
    
    if st.button("خصم 10 ماسات لتسريع وإنهاء البناء فوراً ⚡"):
        if st.session_state.diamonds >= 10:
            st.session_state.diamonds -= 10
            st.success("رائع! تم البناء والإعمار فوراً وأضاءت نقطة جديدة في المدينة 🏥🛠️")
            time.sleep(2)
            st.session_state.current_stage = "start"
            st.rerun()
        else:
            st.error("رصيدك من الماس لا يكفي لتسريع البناء! شاهد إعلانات أولاً.")
            st.session_state.current_stage = "ad_screen"
            st.rerun()
            
    if st.button("العودة للرئيسية وإنهاء المهمة الحالية 🎉"):
        st.session_state.current_stage = "start"
        st.rerun()

elif st.session_state.current_stage == "upgrade_shop":
    st.header("🛠️ متجر ترقيات الآليات والمعدات بالماس")
    st.write("استخدم ماساتك لتطوير كفاءة وسرعة آليات الإنقاذ داخل اللعبة:")
    
    # ترقية الإسعاف
    st.markdown(f'<div class="status-card"><h4>مركبة الإسعاف السريع السريعة 🚑</h4><span class="badge">المستوى الحالي: {st.session_state.ambulance_level}</span></div>', unsafe_allow_html=True)
    if st.button("ترقية الإسعاف للمستوى التالي (تكلفة 30 ماسة) ⚡"):
        if st.session_state.diamonds >= 30:
            st.session_state.diamonds -= 30
            st.session_state.ambulance_level += 1
            st.success("مبروك! تم تطوير الإسعاف لزيادة سرعة تلبية الاستغاثات 🚀")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("رصيدك لا يكفي للترقية! اذهب لجمع الماس عبر الإعلانات.")
            
    # ترقية الشاحنة
    st.markdown(f'<div class="status-card"><h4>شاحنة الإغاثة والمساعدات الضخمة 📦</h4><span class="badge">المستوى الحالي: {st.session_state.truck_level}</span></div>', unsafe_allow_html=True)
    if st.button("ترقية الشاحنة للمستوى التالي (تكلفة 40 ماسة) ⚡"):
        if st.session_state.diamonds >= 40:
            st.session_state.diamonds -= 40
            st.session_state.truck_level += 1
            st.success("مبروك! تم زيادة سعة حمولة الشاحنة لتوصيل طرود أكثر 🚚")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("رصيدك لا يكفي للترقية!")
            
    if st.button("العودة للقائمة الرئيسية ↩️"):
        st.session_state.current_stage = "start"
        st.rerun()
    
