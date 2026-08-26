import streamlit as st
import pandas as pd
import time
from datetime import datetime

# 1. إعدادات الصفحة المتقدمة للتوافق مع الهواتف والكمبيوتر
st.set_page_config(
    page_title="المنصة التعليمية الوطنية الموحدة - فلسطين",
    page_icon="🇵🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إنشاء قاعدة بيانات داخلية مؤقتة
if 'students_db' not in st.session_state:
    st.session_state['students_db'] = {
        "123456789": {"name": "أحمد محمد", "grade": "المرحلة الثانوية (10-12)", "scores": {"اللغة العربية": 95, "الرياضيات": 88}},
        "987654321": {"name": "سارة أحمد", "grade": "المرحلة المتوسطة (5-9)", "scores": {"العلوم": 92}}
    }

if 'uploaded_files_log' not in st.session_state:
    st.session_state['uploaded_files_log'] = []

if 'announcements' not in st.session_state:
    st.session_state['announcements'] = [
        {"date": "2026-08-26", "title": "بدء التسجيل للامتحانات الاستدراكية الموحدة."},
        {"date": "2026-08-20", "title": "إطلاق وحدة المناهج التفاعلية الموفرة للباقة."}
    ]

# 3. تحسين اتجاه النصوص والمظهر الأساسي (تم تصحيحه بالكامل)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .main, .block-container {
    direction: rtl !important;
    text-align: right !important;
}
[data-testid="stSidebar"] {
    direction: rtl !important;
}
.main-title {
    color: #1e3a8a;
    text-align: center;
    font-family: sans-serif;
}
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #f1f5f9;
    margin-bottom: 10px;
    border-right: 5px solid #059669;
}
</style>
""", unsafe_allow_code=True)

# 4. القائمة الجانبية الموحدة
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🇵🇸 المنصة الموحدة</h2>", unsafe_allow_code=True)
    st.write("---")
    
    user_role = st.selectbox("👤 نوع المستخدم:", ["طالب / زائر", "معلم / مدير النظام"])
    st.write("---")
    
    if user_role == "طالب / زائر":
        menu = st.radio("📋 القائمة الرئيسية:", [
            "🏠 الرئـيسية والتعميمات", 
            "📚 المناهج والكتب الرقمية", 
            "✍️ نظام الامتحانات الذكي",
            "📊 كشف علاماتي"
        ])
    else:
        menu = st.radio("🛠️ لوحة تحكم الإدارة:", [
            "🏠 الرئـيسية والتعميمات",
            "🧑‍🎓 إدارة بيانات الطلاب", 
            "📤 رفع وتحديث المناهج", 
            "⚙️ إعدادات وتصفير السيرفر"
        ])
        
    st.write("---")
    st.caption("📱 إصدار المنصة المطور v2.2 - متوافق وآمن.")

# 5. معالجة محتوى الصفحات
if menu == "🏠 الرئـيسية والتعميمات":
    st.markdown("<h1 class='main-title'>المنصة التعليمية الوطنية الموحدة</h1>", unsafe_allow_code=True)
    st.markdown("<h3 style='text-align: center; color: #475569;'>دولة فلسطين</h3>", unsafe_allow_code=True)
    st.write("---")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("الطلاب المسجلين بالسيرفر", f"{len(st.session_state['students_db'])} طلاب نشطين")
    c2.metric("الملفات المرفوعة للشبكة", f"{len(st.session_state['uploaded_files_log'])} ملف")
    c3.metric("حالة النظام", "متصل ونشط 🟢")
    
    st.write("### 📢 آخر التعميمات والإعلانات الرسمية:")
    for ann in st.session_state['announcements']:
        st.markdown(f"<div class='card'><strong>📅 {ann['date']}</strong> - {ann['title']}</div>", unsafe_allow_code=True)

elif menu == "📚 المناهج والكتب الرقمية":
    st.title("📚 بوابة المناهج والمواد الدراسية (تحميل موفر)")
    grade = st.selectbox("اختر المرحلة الدراسية:", ["المرحلة الأساسية (1-4)", "المرحلة المتوسطة (5-9)", "المرحلة الثانوية (10-12)"])
    subject = st.selectbox("اختر المادة:", ["اللغة العربية", "الرياضيات", "العلوم والحياة", "اللغة الإنجليزية"])
    
    st.write("---")
    st.success(f"📦 تم تجهيز روابط العرض السريع لمادة ({subject}) - {grade}.")
    
    st.download_button(
        label=f"⬇️ تحميل كتاب {subject} (نسخة مضغوطة خفيفة PDF)",
        data="محتوى الكتاب التجريبي خفيف الحجم",
        file_name=f"{subject}_{grade}.pdf",
        mime="text/plain"
    )

elif menu == "✍️ نظام الامتحانات الذكي":
    st.title("✍️ تقديم الاختبارات المؤتمتة خفيفة الوزن")
    st.write("### 📝 اختبار تجريبي قصير: مادة الثقافة العلمية والذكاء الاصطناعي")
    
    q1 = st.radio("1. ما هي البيئة البرمجية المستخدمة لبناء هذه المنصة الموحدة؟", ["Django", "Streamlit", "Flask"])
    q2 = st.radio("2. لتقليل استهلاك الإنترنت والبطارية على الهواتف، يفضل إخفاء:", ["النصوص والعلامات", "الصور الكبيرة والفيديوهات الثقيلة", "الأزرار الرئيسية"])
    
    if st.button("إرسال الإجابات ورصد العلامة"):
        score = 0
        if q1 == "Streamlit": score += 50
        if q2 == "الصور الكبيرة والفيديوهات الثقيلة": score += 50
        st.balloons()
        st.success(f"🎉 تم رصد إجابتك بنجاح! نتيجتك هي: {score}/100")

elif menu == "📊 كشف علاماتي":
    st.title("📊 نظام الاستعلام عن العلامات الموحد")
    sid = st.text_input("أدخل رقم هويتك الشخصي (مثال للتجربة: 123456789):")
    
    if st.button("بحث واستخراج الشهادة"):
        if sid in st.session_state['students_db']:
            student = st.session_state['students_db'][sid]
            st.markdown(f"### 🧑‍🎓 اسم الطالب: **{student['name']}**")
            st.write(f"🏫 المرحلة: {student['grade']}")
            df_scores = pd.DataFrame(list(student['scores'].items']), columns=['المادة', 'العلامة'])
            st.table(df_scores)
        else:
            st.error("❌ رقم الهوية غير مسجل في قاعدة البيانات الحالية.")

elif menu == "🧑‍🎓 إدارة بيانات الطلاب":
    st.title("🛠️ لوحة تحكم المعلم: إضافة وإدارة الطلاب")
    with st.form("add_student_form"):
        new_id = st.text_input("رقم هوية الطالب الجديد:")
        new_name = st.text_input("اسم الطالب بالكامل:")
        new_grade = st.selectbox("المرحلة:", ["المرحلة الأساسية (1-4)", "المرحلة المتوسطة (5-9)", "المرحلة الثانوية (10-12)"])
        submitted = st.form_submit_button("➕ تسجيل الطالب في النظام")
        
        if submitted:
            if new_id and new_name:
                st.session_state['students_db'][new_id] = {"name": new_name, "grade": new_grade, "scores": {}}
                st.success(f"✅ تم إضافة الطالب {new_name} بنجاح!")
            else:
                st.error("⚠️ يرجى ملء جميع الحقول المطلوبة.")
    st.write("### 📋 قائمة الطلاب المسجلين حالياً:")
    st.json(st.session_state['students_db'])

elif menu == "📤 رفع وتحديث المناهج":
    st.title("📤 مركز رفع الملفات والمناهج والمرفقات")
    uploaded_file = st.file_uploader("اختر الملف من جهازك:", type=['pdf', 'docx', 'png', 'jpg'])
    file_description = st.text_input("وصف مختصر للملف المرفوع:")
    
    if st.button("🚀 رفع واعتماد الملف بالمنصة"):
        if uploaded_file is not None and file_description:
            file_info = {
                "name": uploaded_file.name,
                "desc": file_description,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state['uploaded_files_log'].append(file_info)
            st.success(f"✅ تم رفع وتعميم ملف '{uploaded_file.name}' بنجاح!")
            
    if st.session_state['uploaded_files_log']:
        st.write("### 🗂️ السجل الحالي للملفات المرفوعة:")
        st.dataframe(pd.DataFrame(st.session_state['uploaded_files_log']))

elif menu == "⚙️ إعدادات وتصفير السيرفر":
    st.title("⚙️ نظام صيانة وإيقاظ التطبيق الاحترافي")
    if st.button("🧹 مسح ذاكرة التخزين المؤقت (Cache Clear)"):
        st.cache_data.clear()
        st.success("تم تصفير وتنظيف كاش السيرفر!")
    if st.button("🔄 إعادة ضبط المصنع لقاعدة البيانات المؤقتة"):
        st.session_state.clear()
        st.warning("تم تصفير وإعادة تهيئة كافة البيانات المضافة حديثاً بنجاح.")
        st.rerun()
    
