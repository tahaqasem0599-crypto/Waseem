import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام المبيعات المحترف", page_icon="📊")
st.title("📊 نظام إدارة المبيعات المطور")

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
    
    # حساب وعرض المجموع الإجمالي
    total_revenue = st.session_state.df["الإجمالي"].sum()
    st.metric(label="💰 إجمالي الإيرادات والأرباح", value=f"{total_revenue} $")
    
    # عرض الجدول
    st.dataframe(st.session_state.df, use_container_width=True)
    
    # رسم بياني تفاعلي للمبيعات
    st.markdown("### 📈 رسم بياني للمبيعات حسب المنتج")
    st.bar_chart(data=st.session_state.df, x="المنتج", y="الإجمالي")
    
    # تحويل الجدول إلى صيغة CSV متوافقة مع الإكسل
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
    
    # زر تحميل البيانات السليم
    st.download_button(
        label="📥 تحميل جدول المبيعات (متوافق مع Excel)",
        data=csv_data,
        file_name="sales_report.csv",
        mime="text/csv"
    )
else:
    st.info("لا توجد مبيعات مسجلة حتى الآن. أضف منتجاً لتشاهد لوحة التحكم الحية.")
        
