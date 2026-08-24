import os; os.system("pip install pycryptodome")
import streamlit as st
import json
import base64
import zlib
from crypto.Cipher import AES

# إعدادات الواجهة الرسومية المميزة للمنظومة
st.set_page_config(page_title="سيرفر منظومة صمود التعليمية", page_icon="🎓", layout="wide")

# مفاتيح التشفير والتعمية المشتركة والمحمية مع تطبيق الهاتف
SECRET_KEY = b"v3ry_s3cr3t_k3y_f0r_g4z4_4pp_2026"
IV = b"g4z4_s3cur3_1v_26"

# دالة فك التشفير والضغط الفائق القادم من الميدان أوفلاين
def decrypt_and_decompress(encrypted_base64):
    try:
        # 1. فك تشفير AES-256-CBC
        encrypted_bytes = base64.b64decode(encrypted_base64)
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        
        # إزالة الحشو (Unpadding)
        padding_len = decrypted_bytes[-1]
        clean_bytes = decrypted_bytes[:-padding_len]
        
        # 2. فك الضغط الفائق (GZip / Zlib)
        decompressed_bytes = zlib.decompress(clean_bytes, 16 + zlib.MAX_WBITS)
        
        return json.loads(decompressed_bytes.decode('utf-8'))
    except Exception as e:
        return None

# إدارة الذاكرة المحلية المؤقتة للسيرفر
if "official_students" not in st.session_state:
    st.session_state.official_students = []
if "guest_students" not in st.session_state:
    st.session_state.guest_students = []

# --- واجهة المستخدم الرئيسية ---
st.title("🎓 لوحة تحكم سيرفر الوزارة المركزي - منظومة صمود")
st.subheader("إدارة وتوثيق الامتحانات الورقية والرقمية لقطاع غزة")

# القسم الأول: استقبال ومزامنة البيانات من المشرفين
st.markdown("### 📥 استقبال كبسولات الطلاب المشفرة")
qr_input = st.text_area("أدخل النص المشفر المنسوخ من كود الـ QR مالي أو من حقيبة المشرف الميدانية:")

if st.button("🚀 فك التشفير ومزامنة الدرجة"):
    if qr_input:
        data = decrypt_and_decompress(qr_input.strip())
        if data:
            # فحص نوع الحساب (رسمي أم ضيف زائر)
            is_guest = data.get('is_guest', False)
            student_id = data.get('student_id', '')
            
            if is_guest:
                # التحقق من عدم التكرار للضيوف
                if not any(s['student_id'] == student_id for s in st.session_state.guest_students):
                    st.session_state.guest_students.append(data)
                    st.success(f"✅ تم بنجاح توثيق حساب الضيف/المستمع: {data.get('student_name')}")
                else:
                    st.warning("⚠️ هذا السجل مضاف مسبقاً في قاعدة بيانات الزوار.")
            else:
                # التحقق من عدم التكرار للطلاب الرسميين
                if not any(s['student_id'] == student_id for s in st.session_state.official_students):
                    st.session_state.official_students.append(data)
                    st.success(f"🔒 تم فك التشفير العسكري بنجاح ورصد درجة الطالب الرسمي: {data.get('student_name')}")
                else:
                    st.warning("⚠️ هذا الطالب مسجل ومحمي مسبقاً في النظام المركزي.")
        else:
            st.error("❌ فشل في قراءة البيانات: الكود تالف أو تم التلاعب بمحتواه التقني!")
    else:
        st.info("الرجاء وضع النص المشفر أولاً.")

st.divider()

# القسم الثاني: لوحة الإحصائيات والتحليلات الرائعة
st.markdown("### 📊 لوحة البيانات والإحصاءات المحدثة")
col1, col2, col3 = st.columns(3)

total_official = len(st.session_state.official_students)
total_guests = len(st.session_state.guest_students)

# حساب متوسط الدرجات الكلي
all_submissions = st.session_state.official_students + st.session_state.guest_students
avg_score = 0.0
if all_submissions:
    avg_score = sum(s.get('score', 0) for s in all_submissions) / len(all_submissions)

col1.metric("عدد الطلاب الرسميين", f"{total_official} طالب")
col2.metric("عدد حسابات الضيوف والزوار", f"{total_guests} حساب")
col3.metric("متوسط أداء المنظومة", f"{avg_score:.1f} درجة")

st.divider()

# القسم الثالث: جداول عرض النتائج المفصلة
tab1, tab2 = st.tabs(["🎓 السجل الرسمي المعتمد", "🔍 سجل الضيوف والمستمعين الجدد"])

with tab1:
    if st.session_state.official_students:
        st.dataframe(st.session_state.official_students)
    else:
        st.caption("لا توجد سجلات رسمية معتمدة مرفوعة حالياً.")

with tab2:
    if st.session_state.guest_students:
        st.dataframe(st.session_state.guest_students)
    else:
        st.caption("لا توجد بيانات ضيوف أو زوار مسجلة حالياً.")
        
