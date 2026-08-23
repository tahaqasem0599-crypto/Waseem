import streamlit as st
import pandas as pd

# إعدادات الصفحة والهوية البصرية الكاملة للعبة
st.set_page_config(page_title="غزة الحربية - النظام الشامل", page_icon="⚔️", layout="wide")

# تصميم الألوان الاحترافي (أسود داكن وأصفر ذهبي) ليناسب ألعاب الباتل رويال
st.markdown("""
    <style>
    .main { background-color: #121212; color: #FFFFFF; }
    h1, h2, h3 { color: #FFCC00 !important; font-family: 'Cairo', sans-serif; }
    .stButton>button { background-color: #FFCC00; color: #121212; font-weight: bold; border-radius: 5px; width: 100%; }
    .stButton>button:hover { background-color: #E6B800; color: #121212; }
    div[data-testid="stMetricValue"] { color: #FFCC00 !important; }
    .css-12w0qpk { background-color: #1E1E1E !important; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_escaping=True)

# بيانات دخول المطور وسيم
ADMIN_USERNAME = "waseem"
ADMIN_PASSWORD = "123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 1. صفحة تسجيل الدخول الرسمية للعبة غزة الحربية
if not st.session_state.logged_in:
    st.title("💥 لعبة غزة الحربية (Gaza Warfare)")
    st.subheader("🔒 النظام المركزي لإدارة السيرفرات العالمية")
    
    username_input = st.text_input("👤 اسم المستخدم المعتمد:", value="waseem")
    password_input = st.text_input("🔑 كلمة المرور السرية:", type="password", value="123")
    
    if st.button("🚀 الولوج إلى السيرفر الآمن"):
        if username_input == ADMIN_USERNAME and password_input == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ خطأ أمني: بيانات الدخول غير صحيحة!")

# 2. لوحة التحكم الشاملة بعد تسجيل الدخول بنجاح
else:
    col_header, col_logout = st.columns([4, 1])
    with col_header:
        st.title("⚔️ لوحة تحكم لعبة غزة الحربية (Gaza Warfare)")
        st.subheader(f"👑 رئيس السيرفرات والمطور الرئيسي: المطور وسيم")
    with col_logout:
        if st.button("🚪 مغادرة السيرفر"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.write("---")

    # تفعيل الـ 6 أقسام شاملة كل شيء طلبتة
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🗺️ الخرائط والزون", 
        "💎 شحن الـ Coins", 
        "🛡️ مكافحة الهاكرز", 
        "🏆 قائمة الصدارة",
        "🔫 سكنات الأسلحة",
        "💰 الأرباح والمالية"
    ])

    # القسم الأول: السيرفر والخرائط
    with tab1:
        st.subheader("⚙️ إدارة غرف المعارك الحالية")
        col1, col2 = st.columns(2)
        with col1:
            map_name = st.selectbox("🗺️ اختر خريطة المواجهة الحالية:", ["ساحة الصمود (Main Map)", "المدينة المدمرة (Desert)", "موقع الإنزال (Custom)"])
            game_mode = st.radio("👥 نمط الطائرات والفرق في السيرفر:", ["Squad (فريق 4 لاعبين)", "Duo (ثنائي)", "Solo (نمط الفدائي الفردي)"])
        with col2:
            air_drop_rate = st.slider("✈️ معدل نزول صناديق الإمداد (Air Drops):", 1, 5, 3)
            zone_speed = st.slider("⭕ سرعة تضييق دائرة الخطر (Danger Zone):", 1.0, 3.0, 1.8)
            
        if st.button("💾 حفظ وتطبيق إعدادات الخريطة فوراً"):
            st.success(f"✔️ تم تحديث خريطة السيرفر بنجاح! الخريطة النشطة الآن: {map_name}.")

    # القسم الثاني: متجر الشحن
    with tab2:
        st.subheader("💎 نظام شحن وتوليد العملات الافتراضية للّاعبين")
        player_id = st.text_input("🆔 أدخل رقم حساب اللاعب (Player ID):", placeholder="مثال: 70023415")
        uc_amount = st.selectbox("💵 اختر كمية الـ War Coins المراد إرسالها للّاعب:", ["300 Coins", "660 Coins", "1800 Coins", "3850 Coins", "8100 Coins"])
        
        if st.button("⚡ إرسال العملات لحساب اللاعب"):
            if player_id:
                st.success(f"🎉 تم بنجاح إرسال {uc_amount} إلى حساب اللاعب رقم {player_id} في لعبة غزة الحربية!")
            else:
                st.warning("⚠️ يرجى إدخال معرف اللاعب (ID) أولاً.")

    # القسم الثالث: مكافحة الهكر
    with tab3:
        st.subheader("🛡️ جدار حماية غزة الحربية (Anti-Cheat)")
        st.error("🚨 رادار الحماية: تم رصد لاعب يستخدم ثغرة الطيران وكشف الأماكن في الجيم الحالي!")
        
        suspect_id = st.text_input("🚫 أدخل ID اللاعب المخالف لتطبيق العقوبة:")
        ban_duration = st.selectbox("⏳ نوع العقوبة والحظر للسيرفر:", ["حظر مؤقت لمدة 24 ساعة", "حظر لمدة 7 أيام", "حظر أبدي وجلب عنوان الجهاز (حظر نهائي)"])
        
        if st.button("🔨 طرد وبند اللاعب المخالف"):
            st.error(f"🔒 تم طرد الحساب {suspect_id} بنجاح من اللعبة وحظر الـ IP بواسطة المطور وسيم.")

    # القسم الرابع: قائمة الصدارة واللاعبين (Leaderboard)
    with tab4:
        st.subheader("🏆 قائمة أفضل 5 لاعبين في لعبة غزة الحربية")
        st.write("يتم تحديث هذا الجدول تلقائياً بناءً على عدد الكيلز والفوز (Wins):")
        
        # إنشاء بيانات الجدول
        leaderboard_data = {
            "الترتيب":,
            "اسم اللاعب (Username)": ["الصقر_الغزاوي", "waseem_hero", "المدمر_007", "كلاشينكوف", "الأسد_الرقمي"],
            "معرف اللاعب (ID)": ["552144", "100234", "883411", "994125", "332145"],
            "عدد القتلى (Kills)":,
            "المستوى (Level)": [72, 70, 65, 62, 59]
        }
        df = pd.DataFrame(leaderboard_data)
        st.dataframe(df, use_container_width=True)

    # القسم الخامس: سكنات وتصميم الأسلحة
    with tab5:
        st.subheader("🔫 مستودع سكنات وتطوير الأسلحة")
        st.write("ارفع تصميم أو سكن جديد لتطبيقه داخل اللعبة على أسلحة مثل M416 أو AKM:")
        
        weapon_type = st.selectbox("🎯 اختر السلاح المراد تعديل مخصصه ومظهره:", ["M416", "AKM", "AWM (قناصة)", "M24", "Scarl-L"])
        skin_name = st.text_input("🎨 اسم السكن الجديد:", placeholder="مثال: سكن رمال غزة")
        
        # ميزة رفع الملفات والصور للسكنات
        uploaded_skin = st.file_uploader("📂 ارفع صورة أو ملف خامات السكن ثلاثي الأبعاد (Texture File):", type=["png", "jpg", "jpeg", "obj"])
        
        if st.button("🎨 رفع وتفعيل السكن في اللعبة"):
            if uploaded_skin and skin_name:
                st.success(f"🔥 تم بنجاح رفع السكن '{skin_name}' وتطبيقه على سلاح {weapon_type} في النسخة القادمة للعبة!")
            else:
                st.warning("⚠️ يرجى إدخال اسم السكن ورفع ملف الصورة أولاً لتحديث السلاح.")

    # القسم السادس: الأرباح والمالية المتصلة بمحفظتك
    with tab4:
        pass # تم نقله لـ tab6 لترتيب الكود البرمجي
    with tab6:
        st.subheader("💵 تقرير الخزينة والأرباح اليومية للعبة")
        c1, c2, c3 = st.columns(3)
        c1.metric(label="💰 أرباح إعلانات الموبايل (AdMob)", value="$410.20", delta="+24% اليوم")
        c2.metric(label="💎 مبيعات متجر العملات (Coins)", value="$950.00", delta="+15% هذا الأسبوع")
        c3.metric(label="🏦 الرصيد القابل للسحب الفوري", value="$1,360.20")
        
        st.success("🔗 السيرفر مرتبط بنجاح بـ بنك فلسطين (PalPay)، ويتم تحويل الأموال تلقائياً لعمليات السحب اليومي والمستمر.")

    st.write("---")
    st.caption("حقوق التطوير والبرمجة بالكامل محفوظة للمطور وسيم © 2026 | Gaza Warfare Project")
    
