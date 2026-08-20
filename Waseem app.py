import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة مبيعات الملابس العربي", layout="wide")
st.title("📊 نظام إدارة المبيعات والأرباح الذكي لأصحاب المحلات")
st.write("هذا البرنامج مصمم لمساعدتك في مراقبة أموالك ومعرفة أرباحك ومبيعاتك بكل سهولة وبدون تعقيد.")

if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=[
        "التاريخ", "اسم القطعة", "المقاس/اللون", "الكمية", "سعر Tكلفة", "سعر البيع", "إجمالي المبيعات", "صافي الربح"
    ])

col1, col2 = st.columns(2)

with col1:
    st.header("➕ تسجيل عملية بيع جديدة")
    date = st.date_input("تاريخ العملية")
    item_name = st.text_input("اسم قطعة الملابس (مثال: قميص رجالي)")
    item_variant = st.text_input("المقاس واللون (مثال: XL / أزرق)")
    quantity = st.number_input("الكمية المباعة", min_value=1, value=1)
    cost_price = st.number_input("سعر التكلفة للقطعة الواحدة ($)", min_value=0.0, value=10.0)
    sell_price = st.number_input("سعر البيع للقطعة الواحدة ($)", min_value=0.0, value=25.0)
    
    total_sales = quantity * sell_price
    total_cost = quantity * cost_price
    net_profit = total_sales - total_cost
    
    if st.button("حفظ العملية وتحديث الكشف"):
        new_row = {
            "التاريخ": str(date), "اسم القطعة": item_name, "المقاس/اللون": item_variant, 
            "الكمية": quantity, "سعر Tكلفة": cost_price, "سعر البيع": sell_price, 
            "إجمالي المبيعات": total_sales, "صافي الربح": net_profit
        }
        st.session_state.sales_data = pd.concat([st.session_state.sales_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("تم تسجيل العملية بنجاح وحماية الأرباح!")

with col2:
    st.header("📈 كشف المبيعات والأرباح الفوري")
    
    if not st.session_state.sales_data.empty:
        total_revenue = st.session_state.sales_data["إجمالي المبيعات"].sum()
        total_profit = st.session_state.sales_data["صافي الربح"].sum()
        
        stat1, stat2 = st.columns(2)
        stat1.metric(label="💰 إجمالي المبيعات المستلمة", value=f"${total_revenue:,.2f}")
        stat2.metric(label="🟩 صافي الربح الحقيقي", value=f"${total_profit:,.2f}")
        
        st.dataframe(st.session_state.sales_data, use_container_width=True)
        
        csv = st.session_state.sales_data.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل كشف المبيعات كملف Excel (CSV)",
            data=csv,
            file_name='sales_report.csv',
            mime='text/csv',
        )
    else:
        st.info("لا توجد مبيعات مسجلة اليوم. قم بإدخال أول عملية بيع من القائمة الجانبية.")
  
