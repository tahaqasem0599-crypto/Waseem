import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image

# 1. إعدادات الصفحة العامة
st.set_page_config(page_title="منصة بنك المقاسات المطور", page_icon="🇵🇸", layout="centered")

# 2. تحسين المظهر ودعم كامل للغة العربية (RTL)
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl; text-align: right; font-family: 'Cairo', sans-serif !important;
    }
    h1, h2, h3, h4, p, label, span, button { font-family: 'Cairo', sans-serif !important; }
    div.stButton > button {
        width: 100%; background-color: #2e7d32; color: white !important;
        border-radius: 8px; font-size: 18px; font-weight: bold; border: none; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #1b5e20; box-shadow: 0px 4px 10px rgba(0,0,0,0.15); }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة قواعد البيانات المحلية (ملفات CSV لحفظ البيانات بشكل دائم)
CLOTHING_DB = "clothing_db_v5.csv"
WISHLIST_DB = "wishlist_db_v5.csv"
USERS_DB = "users_db_v5.csv"

def init_databases():
    if not os.path.exists(CLOTHING_DB):
        pd.DataFrame(columns=["معرف", "النوع", "المنطقة", "الجنس", "المقاس", "الوصف", "الحالة", "الهاتف", "الصورة", "الالتقاط"]).to_csv(CLOTHING_DB, index=False)
    if not os.path.exists(WISHLIST_DB):
        pd.DataFrame(columns=["الهاتف", "المنطقة", "المقاس_المطلوب", "التاريخ"]).to_csv(WISHLIST_DB, index=False)
    if not os.path.exists(USERS_DB):
        pd.DataFrame(columns=["الهاتف", "النقاط"]).to_csv(USERS_DB, index=False)

init_databases()

def get_or_create_user(phone):
    df = pd.read_csv(USERS_DB)
    df["الهاتف"] = df["الهاتف"].astype(str)
    phone_str = str(phone).strip()
    if phone_str in df["الهاتف"].values:
        return int(df[df["الهاتف"] == phone_str]["النقاط"].values)
    else:
        new_user = pd.DataFrame([{"الهاتف": phone_str, "النقاط": 3}])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv(USERS_DB, index=False)
        return 3

def update_user_points(phone, change):
    df = pd.read_csv(USERS_DB)
    df["الهاتف"] = df["الهاتف"].astype(str)
    phone_str = str(phone).strip()
    if phone_str in df["الهاتف"].values:
        df.loc[df["الهاتف"] == phone_str, "النقاط"] += change
        df.to_csv(USERS_DB, index=False)

def encode_image(uploaded_file):
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.thumbnail((350, 350))
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=80)
        return base64.b64encode(buffered.getvalue()).decode()
    return "None"

# 4. واجهة التطبيق الرئيسية
st.title("🇵🇸 بنك المقاسات ومستلزمات الأطفال الذكي")
st.subheader("المنصة التكافلية الأولى في قطاع غزة لمقايضة الملابس والمستلزمات مجاناً في مركزنا")

st.divider()

# نظام التبويبات المتطور
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 تصفح المعروض بالمحل", 
    "👕 عرض قطعة جديدة (+1 نقطة)", 
    "📢 طلب مقاس غير متوفر", 
    "🏪 عنوان المحل وموعد الاستلام", 
    "📊 لوحة التحكم والإحصائيات"
])

# --- التبويب الأول: تصفح الملابس والمستلزمات والطلب الذكي ---
with tab1:
    st.header("🔎 ابحث عما يحتاجه طفلك في المحل")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        f_type = st.selectbox("قسم البحث", ["الكل", "ملابس", "مستلزمات (عربات/أسرة)", "ألعاب وكتب"])
    with c2:
        f_region = st.selectbox("منطقة صاحب القطعة الأصلية", ["الكل", "غزة", "الوسطى", "دير البلح", "خان يونس", "رفح"])
    with c3:
        f_gender = st.selectbox("الجنس", ["الكل", "أولادي", "بناتي", "مواليد جديد"])
    with c4:
        f_size = st.selectbox("المقاس/العمر", ["الكل", "0-3 أشهر", "3-6 أشهر", "سنة واحدة", "سنتين", "3-5 سنوات", "أكبر"])

    df_items = pd.read_csv(CLOTHING_DB)
    
    if f_type != "الكل": df_items = df_items[df_items["النوع"] == f_type]
    if f_region != "الكل": df_items = df_items[df_items["المنطقة"] == f_region]
    if f_gender != "الكل": df_items = df_items[df_items["الجنس"] == f_gender]
    if f_size != "الكل": df_items = df_items[df_items["المقاس"] == f_size]

    if df_items.empty:
        st.info("⚠️ لا توجد قطعة متوفرة حالياً تطابق بحثك. يمكنك الانتقال لتبويب 'طلب مقاس غير متوفر' لتسجيل طلبك!")
    else:
        for idx, row in df_items.iterrows():
            with st.container(border=True):
                col_txt, col_img = st.columns()
                with col_txt:
                    st.markdown(f"### 📦 {row['الوصف']}")
                    st.write(f"📏 **المقاس:** {row['المقاس']} | 👥 **الفئة:** {row['الجنس']}")
                    st.write(f"✨ **حالة ونظافة القطعة:** {row['الالتقاط']}")
                    
                    with st.expander("📞 اضغط لحجز هذه القطعة من المحل (يخصم 1 نقطة)"):
                        user_phone = st.text_input("أدخل رقم جوالك أولاً للتحقق من رصيد نقاطك:", key=f"phone_{idx}")
                        if user_phone:
                            points = get_or_create_user(user_phone)
                            st.info(f"رصيدك الحالي: {points} نقاط.")
                            if points > 0:
                                st.success("✅ رصيدك يسمح! تفضل بزيارة المحل في خانيونس لإتمام التبادل، واذكر لنا رقم القطعة.")
                                st.caption(f"معرف القطعة المرجعي بالمحل: #{row['معرف']}")
                            else:
                                st.error("❌ رصيد نقاطك 0. يرجى إحضار قطعة صغرت على أطفالك للمحل لرفعها وتكسب نقاطاً جديدة!")

                with col_img:
                    if str(row['الصورة']) != "None" and str(row['الصورة']) != "":
                        try:
                            st.image(BytesIO(base64.b64decode(row['الصورة'])), use_container_width=True)
                        except:
                            st.caption("📷 صورة غير متاحة")
                    else:
                        st.caption("📷 لا توجد صورة")

# --- التبويب الثاني: إضافة قطعة جديدة وكسب نقاط للمستخدم ---
with tab2:
    st.header("➕ اعرض قطعة جديدة واكسب (+1) نقطة رصيد")
    st.write("أدخل بيانات الملابس التي تود إحضارها للمحل لتبديلها بمقاسات أخرى.")
    
    with st.form("add_item_form", clear_on_submit=True):
        u_phone = st.text_input("رقم جوالك (أساسي لحفظ نقاطك وحسابك لدينا)", placeholder="059xxxxxxx")
        u_type = st.selectbox("تصنيف القطعة", ["ملابس", "مستلزمات (عربات/أسرة)", "ألعاب وكتب"])
        u_region = st.selectbox("منطقتك الحالية", ["غزة", "الوسطى", "دير البلح", "خان يونس", "رفح"])
        u_gender = st.selectbox("الفئة", ["أولادي", "بناتي", "مواليد جديد", "غير محدد"])
        u_size = st.selectbox("المقاس المناسب للعمر", ["0-3 أشهر", "3-6 أشهر", "سنة واحدة", "سنتين", "3-5 سنوات", "أكبر"])
        u_desc = st.text_input("وصف دقيق (مثال: جاكيت شتوي أحمر دافئ، أو سرير مواليد خشبي)")
        u_eval = st.select_slider("حالة ونظافة القطعة بكل أمانة", options=["مقبولة ومتوسطة", "جيدة ونظيفة", "جيدة جداً", "ممتازة كالمستجدة"])
        u_img = st.file_uploader("📸 صوّر القطعة وارفعها هنا ليراها الباحثون قبل حضورهم للمحل", type=["jpg", "png", "jpeg"])
        
        btn_submit = st.form_submit_button("🚀 انشر القطعة واكسب نقطة الآن")
        
        if btn_submit:
            if not u_phone or not u_desc:
                st.error("❌ يرجى كتابة رقم الجوال ووصف القطعة لإتمام النشر.")
            else:
                img_encoded = encode_image(u_img)
                df_clothing = pd.read_csv(CLOTHING_DB)
                new_id = int(df_clothing["معرف"].max()) + 1 if not df_clothing.empty else 1
                
                new_row = pd.DataFrame([{
                    "معرف": new_id, "النوع": u_type, "المنطقة": u_region, "الجنس": u_gender,
                    "المقاس": u_size, "الوصف": u_desc, "الحالة": "متاح", "الهاتف": u_phone,
                    "الصورة": img_encoded, "الالتقاط": u_eval
                }])
                
                pd.concat([df_clothing, new_row], ignore_index=True).to_csv(CLOTHING_DB, index=False)
                
                get_or_create_user(u_phone)
                update_user_points(u_phone, 1)
                
                st.success("🎉 تم نشر قطعتك بنجاح! أحضرها معك للمحل في زيارتك القادمة لتسليمها.")
                st.rerun()

# --- التبويب الثالث: طلب مقاس غير متوفر (قائمة الانتظار الذكية) ---
with tab3:
    st.header("📢 مش لاقي مقاس ابنك بالمحل؟ سجل طلبك")
    st.write("سجل المقاس أو المستلزم الذي تبحث عنه، لنتواصل معك فور توفره أو تسليمه بالمحل.")
    
    with st.form("wishlist_form", clear_on_submit=True):
        w_phone = st.text_input("رقم جوالك")
        w_region = st.selectbox("منطقتك السكنية", ["غزة", "الوسطى", "دير البلح", "خان يونس", "رفح"])
        w_req = st.text_input("ماذا تحتاج بالتحديد؟ (مثال: حذاء مقاس 24 أولادي، سرير مواليد خشبي)")
        btn_wish = st.form_submit_button("📌 تسجيل الطلب في قائمة الانتظار")
        
        if btn_wish and w_phone and w_req:
            df_wish = pd.read_csv(WISHLIST_DB)
            new_wish = pd.DataFrame([{"الهاتف": w_phone, "المنطقة": w_region, "المقاس_المطلوب": w_req, "التاريخ": datetime.today().strftime('%Y-%m-%d')}])
            pd.concat([df_wish, new_wish], ignore_index=True).to_csv(WISHLIST_DB, index=False)
            st.success("🎯 تم إدراج طلبك بنجاح. سنقوم بالاتصال بك فور توفر القطعة داخل المحل.")
            st.rerun()
            
    st.subheader("📋 طلبات الأهالي المعلقة المنتظر توفرها بالمحل:")
    df_w_show = pd.read_csv(WISHLIST_DB)
    if df_w_show.empty:
        st.caption("لا توجد طلبات معلقة حالياً.")
    else:
        for i, r in df_w_show.iterrows():
            st.warning(f"👤 طلب معلق لعائلة في **{r['المنطقة']}** بحاجة إلى: **{r['المقاس_المطلوب']}**")

# --- التبويب الرابع: عنوان المحل الحصري والدائم والمحدث ---
with tab4:
    st.header("🏪 عنوان المحل ومواعيد استقبال الأهالي")
    st.write("لتسليم قطع الملابس أو استلام القطع المحجوزة، يسعدنا استقبالكم في موقعنا الرئيسي والوحيد:")
    
    st.success("""
