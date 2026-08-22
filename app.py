import streamlit as st

# إعدادات الصفحة وظهور اسمك في علامة تبويب المتصفح العلوي
st.set_page_config(page_title="تطبيق وسيم نائل", page_icon="✨", layout="centered")

# تصميم واجهة التطبيق الشخصية
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>مرحباً بكم في تطبيقي الشخصي</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #31333F;'>إعداد وتطوير: وسيم نائل</h3>", unsafe_allow_html=True)

st.divider()

# محتوى تعريفي بسيط وجاهز
st.info("💡 هذا التطبيق تم إنشاؤه ونشره بنجاح باسمي وصورتي عبر منصة Streamlit Cloud.")

st.write("يمكنك الآن استخدام هذا الرابط المخصص ونشره كإعلان ممول أو مشاركته مع أصدقائك وعملائك.")

# إضافة تذييل الصفحة باسمك
st.caption("© 2026 جميع الحقوق محفوظة | وسيم نائل")
