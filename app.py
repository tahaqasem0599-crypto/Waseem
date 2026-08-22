import streamlit as st
# تأكد من وجود ملف صورتك بنفس المجلد واسمه "waseem.jpg"
# أو استبدله بالاسم الصحيح لملفك

# 1. إعدادات الصفحة والأيقونة (تظهر في تبويب المتصفح)
st.set_page_config(
    page_title="تطبيق وسيم نائل",
    page_icon="waseem.jpg", # صورتك كأيقونة للموقع
    layout="centered"
)

# 2. دعم محاذاة اللغة العربية (RTL) باستخدام CSS
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        direction: RTL;
        text-align: right;
    }
    div.stButton > button:first-child {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. الشريط الجانبي (Sidebar) - وضع صورتك والتعريف
with st.sidebar:
    st.image("waseem.jpg", caption="المطور: وسيم نائل", width=150)
    st.title("القائمة الرئيسية")
    st.write("أهلاً بك في تطبيقنا المخصص للعالم العربي")

# 4. الواجهة الرئيسية
st.title("مرحباً بك في تطبيق وسيم نائل 🚀")
st.image("waseem.jpg", caption="وسيم نائل - مؤسس المشروع", use_container_width=True)

st.header("مشروعنا الجديد")
st.write("نحن نعمل على تطوير هذا التطبيق لخدمة قطاع الملابس والتجارة في العالم العربي.")

# 5. خطوة تفاعلية: السماح للمستخدم برفع صورته
st.subheader("شاركنا صورتك أو شعار محلك")
uploaded_file = st.file_uploader("اختر صورة من جهازك", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="الصورة التي قمت برفعها", width=300)
    st.success("تم رفع الصورة بنجاح!")

# 6. زر للتواصل أو النشر
if st.button("انشر التطبيق الآن"):
    st.balloons()
    st.write("جاهزون للانطلاق نحو المتجر!")
