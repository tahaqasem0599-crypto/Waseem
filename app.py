import streamlit as st
import pandas as pd

# إعدادات الميتا والإعلان التلقائي عند مشاركة الرابط
st.set_page_config(
    page_title="نظام مبيعات وسيم نائل", 
    page_icon="📊",
    menu_items={
        'Get Help': 'https://streamlit.app',
        'Report a bug': 'https://streamlit.app',
        'About': "تطبيق وسيم نائل لإدارة المبيعات الاحترافية"
    }
)

# كود لمنع الترجمة التلقائية داخل التطبيق
st.markdown('<div translate="no">', unsafe_allow_html=True)

st.title("📊 نظام إدارة المبيعات المطور")
st.write("صُنع بواسطة: وسيم نائل ✨")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["المنتج", "الكمية", "السعر", "الإجمالي"])

name = st.text_input("اسم المنتج:")
qty = st.number_input("الكمية:", min_value=1, value=1)
price = st.number_input("السعر للملف الواحد:", min_value=1)

if st.button("إضافة"):
    if name:
        total = qty * price
        new_row = pd.DataFrame([{"المنتج": name, "الكمية": qty, "السعر": price, "الإجمالي": total}])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success("تم الحفظ بنجاح!")

if not st.session_state.df.empty:
    st.markdown("---")
    total_revenue = st.session_state.df["الإجمالي"].sum()
    st.metric(label="💰 إجمالي الإيرادات والأرباح", value=f"{total_revenue} $")
    st.dataframe(st.session_state.df, use_container_width=True)
    st.markdown("### 📈 رسم بياني للمبيعات حسب المنتج")
    st.bar_chart(data=st.session_state.df, x="المنتج", y="الإجمالي")
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تحميل جدول المبيعات (متوافق مع Excel)",
        data=csv_data,
        file_name="sales_report.csv",
        mime="text/csv"
    )
else:
    st.info("لا توجد مبيعات مسجلة حتى الآن. أضف منتجاً لتشاهد لوحة التحكم الحية.")

st.markdown('</div>', unsafe_allow_html=True)
