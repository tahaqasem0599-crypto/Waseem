import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="المنصة التعليمية",
    page_icon="🇵🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. قاعدة البيانات الداخلية الآمنة
if 'students_db' not in st.session_state:
    st.session_state['students_db'] = {
        "123456789": {"name": "Ahmed", "grade": "High School", "arabic": 95, "math": 88},
        "987654321": {"name": "Sara", "grade": "Middle School", "science": 92}
    }

if 'uploaded_files_log' not in st.session_state:
    st.session_state['uploaded_files_log'] = []

# 3. تعديل الاتجاه للغة العربية بدون نصوص طويلة معقدة
st.markdown("<style>body, .main, .block-container, [data-testid='stSidebar'] { direction: rtl; text-align: right; }</style>", unsafe_allow_code=True)

# 4. القائمة الجانبية
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🇵🇸 المنصة الموحدة</h2>", unsafe_allow_code=True)
    st.write("---")
    user_role = st.selectbox("👤 نوع المستخدم:", ["طالب / زائر", "معلم / مدير النظام"])
    st.write("---")
    
    if user_role == "طالب / زائر":
        menu = st.radio("📋 القائمة الرئيسية:", ["الصفحة الرئيسية", "المناهج والكتب", "نظام الامتحانات", "كشف العلامات"])
    else:
        menu = st.radio("🛠️ لوحة التحكم:", ["الصفحة الرئيسية", "إدارة الطلاب", "رفع المناهج", "صيانة السيرفر"])

# 5. تشغيل الصفحات بناءً على الاختيار
if menu == "الصفحة الرئيسية":
    st.markdown("<h1 style='text-align: center; color: #059669;'>المنصة التعليمية الوطنية الموحدة</h1>", unsafe_allow_code=True)
    st.markdown("<h3 style='text-align: center;'>دولة فلسطين</h3>", unsafe_allow_code=True)
    st.write("---")
    st.info("📢 أهلاً بك في المنصة الموحدة الموفرة لبيانات الإنترنت والبطارية.")

elif menu == "المناهج والكتب":
    st.title("📚 بوابة المناهج والمواد الدراسية")
    grade = st.selectbox("اختر المرحلة:", ["الأساسية", "المتوسطة", "الثانوية"])
    subject = st.selectbox("اختر المادة:", ["اللغة العربية", "الرياضيات", "العلوم", "اللغة الإنجليزية"])
    st.success(f"تم تجهيز روابط العرض لمادة {subject} - مرحلة {grade}.")

elif menu == "نظام الامتحانات":
    st.title("✍️ نظام الامتحانات المؤتمتة")
    q1 = st.radio("1. ما هي البيئة البرمجية المستخدمة هنا؟", ["Django", "Streamlit", "Flask"])
    if st.button("إرسال الإجابة"):
        if q1 == "Streamlit":
            st.success("إجابة صحيحة! 🎉 نتيجتك: 100/100")
        else:
            st.error("إجابة خاطئة، حاول مجدداً.")

elif menu == "كشف العلامات":
    st.title("📊 نظام الاستعلام عن العلامات")
    sid = st.text_input("أدخل رقم الهوية للتجربة (123456789):")
    if st.button("عرض الشهادة"):
        if sid in st.session_state['students_db']:
            student = st.session_state['students_db'][sid]
            st.write(f"🧑‍🎓 الطالب: {student['name']} | المرحلة: {student['grade']}")
            st.success("تم جلب البيانات بنجاح من قاعدة البيانات.")
        else:
            st.error("رقم الهوية غير مسجل.")

elif menu == "إدارة الطلاب":
    st.title("🛠️ إضافة طلاب جدد")
    with st.form("add_form"):
        new_id = st.text_input("رقم الهوية:")
        new_name = st.text_input("الاسم بالكامل:")
        if st.form_submit_button("تسجيل الطالب"):
            if new_id and new_name:
                st.session_state['students_db'][new_id] = {"name": new_name, "grade": "مُسجل حديثاً"}
                st.success("تم التسجيل بنجاح!")
            else:
                st.error("يرجى تعبئة الحقول.")

elif menu == "رفع المناهج":
    st.title("📤 مركز رفع المناهج والملفات")
    uploaded_file = st.file_uploader("اختر ملف:")
    if st.button("اعتماد ورفع الملف"):
        if uploaded_file:
            st.session_state['uploaded_files_log'].append(uploaded_file.name)
            st.success("تم الرفع بنجاح!")

elif menu == "صيانة السيرفر":
    st.title("⚙️ صيانة النظام")
    if st.button("تصفير الذاكرة المؤقتة"):
        st.cache_data.clear()
        st.success("تم تنظيف السيرفر كلياً!")
