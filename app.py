import streamlit as st
import pandas as pd
import numpy as np

# 1. إعدادات الصفحة وتحسين المظهر لشاشات الهواتف
st.set_page_config(
    page_title="المنصة الذكية المتكاملة",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق واجهة المستخدم لجعلها مريحة وعصرية
st.markdown("""
    <style>
        .main { background-color: #0f172a; color: #f8fafc; }
        .stButton>button { width: 100%; border-radius: 8px; background-color: #38bdf8; color: white; font-weight: bold; }
        .stButton>button:hover { background-color: #0ea5e9; }
        h1, h2, h3 { color: #38bdf8 !important; }
        .stTextInput>div>div>input { background-color: #1e293b; color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية للتنقل بين الأقسام
st.sidebar.title("📌 قائمة الأقسام")
st.sidebar.write("اختر الأداة التي تريد استخدامها:")
section = st.sidebar.radio(
    "الانتقال إلى:",
    ["📊 لوحة البيانات والرسوم", "📝 المساعد الذكي والتلخيص", "🧮 الحاسبة العلمية", "🗒️ مدير المهام اليومية"]
)

st.sidebar.markdown("---")
st.sidebar.write("🚀 تم التطوير بكفاءة عالية للعمل على الهواتف والكمبيوتر.")

# 3. تشغيل الأقسام بناءً على اختيار المستخدم

# --- القسم الأول: لوحة البيانات ---
if section == "📊 لوحة البيانات والرسوم":
    st.title("📊 لوحة تحليل البيانات التفاعلية")
    st.write("عرض إحصائي ذكي ومطور لإنتاجية العمل وجني الأرباح:")
    
    # توليد بيانات وهمية احترافية
    chart_data = pd.DataFrame(
        np.random.randn(20, 3) * [10, 5, 15] +,
        columns=['الأرباح الشهرية', 'الإنتاجية', 'المبيعات الكلية']
    )
    
    # عرض المؤشرات الرقمية السريعة
    col1, col2, col3 = st.columns(3)
    col1.metric("إجمالي الأرباح", "$12,450", "+12.5%")
    col2.metric("كفاءة العمل", "94%", "+4%")
    col3.metric("المبيعات هذا الشهر", "1,180 قطعة", "+8.2%")
    
    st.markdown("---")
    st.subheader("📈 المنحنى البياني للأداء والمبيعات")
    st.line_chart(chart_data)

# --- القسم الثاني: المساعد الذكي وتلخيص النصوص ---
elif section == "📝 المساعد الذكي والتلخيص":
    st.title("📝 المساعد النصي ومحرر التلخيص")
    st.write("اكتب أو الصق أي نص طويل لتلخيصه، أو اطلب صياغة إيميل/رسالة فوراً:")
    
    text_input = st.text_area("ضع النص الخاص بك هنا:", height=150, placeholder="أدخل النص أو المقال الطويل...")
    
    col1, col2 = st.columns(2)
    if col1.button("⚡ تلخيص النص فوراً"):
        if text_input:
            st.success("💡 التلخيص الذكي المقترح:")
            # محاكاة تلخيص ذكي سريع بناءً على النص
            words = text_input.split()
            summary = " ".join(words[:min(len(words), 30)]) + "..."
            st.write(f"**أهم النقاط المستخلصة:** {summary}")
        else:
            st.warning("⚠️ الرجاء كتابة نص أولاً لتلخيصه.")
            
    if col2.button("✍️ تحويل إلى إيميل رسمي"):
        if text_input:
            st.success("✉️ الصيغة الرسمية للإيميل:")
            st.code(f"السلام عليكم ورحمة الله وبركاته،\n\nبناءً على طلبكم، نود إفادتكم بالتالي:\n{text_input}\n\nوتفضلوا بقبول فائق الاحترام والتقدير.", language="text")
        else:
            st.warning("⚠️ الرجاء كتابة الفكرة الأساسية لتحويلها لإيميل.")

# --- القسم الثالث: الحاسبة العلمية ---
elif section == "🧮 الحاسبة العلمية":
    st.title("🧮 الحاسبة العلمية والمطورة")
    st.write("حل المعادلات الحسابية والمسائل الرياضية بدقة متناهية:")
    
    num1 = st.number_input("أدخل الرقم الأول:", value=0.0)
    num2 = st.number_input("أدخل الرقم الثاني:", value=0.0)
    
    operation = st.selectbox("اختر العملية الحسابية:", ["جمع (+)", "طرح (-)", "ضرب (×)", "قسمة (÷)", "أس (💻)"])
    
    if st.button("🧮 احسب النتيجة"):
        if operation == "جمع (+)":
            res = num1 + num2
        elif operation == "طرح (-)":
            res = num1 - num2
        elif operation == "ضرب (×)":
            res = num1 * num2
        elif operation == "قسمة (÷)":
            res = num1 / num2 if num2 != 0 else "خطأ! لا يمكن القسمة على صفر"
        elif operation == "أس (💻)":
            res = num1 ** num2
            
        st.success(f"📊 النتيجة النهائية هي: **{res}**")

# --- القسم الرابع: مدير المهام اليومية ---
elif section == "🗒️ مدير المهام اليومية":
    st.title("🗒️ مدير المهام والملاحظات الحية")
    st.write("نظم وقتك ومهامك البرمجية واليومية لزيادة إنتاجيتك:")
    
    # استخدام session_state لحفظ المهام مؤقتاً أثناء التنقل
    if "todo_list" not in st.session_state:
        st.session_state.todo_list = ["تحديث ملف الكود app.py", "مراجعة إحصائيات الأسبوع", "تجهيز التقارير البرمجية"]
        
    new_task = st.text_input("➕ أضف مهمة جديدة قائمة الأعمال:", placeholder="اكتب المهمة هنا واضغط على الزر...")
    if st.button("إضافة المهمة"):
        if new_task:
            st.session_state.todo_list.append(new_task)
            st.rerun()
            
    st.markdown("---")
    st.subheader("📋 قائمة مهامك الحالية:")
    
    for i, task in enumerate(st.session_state.todo_list):
        col_t, col_b = st.columns([4, 1])
        col_t.write(f"🔹 {task}")
        if col_b.button("🗑️ حذف", key=f"del_{i}"):
            st.session_state.todo_list.pop(i)
            st.rerun()
