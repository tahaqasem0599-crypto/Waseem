import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

st.set_page_config(page_title="Clothing Shop Management", layout="wide", page_icon="📊")

def init_db():
    conn = sqlite3.connect('shop_sales.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT,
            item_name TEXT,
            item_variant TEXT,
            quantity INTEGER,
            cost_price REAL,
            sell_price REAL,
            total_sales REAL,
            net_profit REAL
        )
    ''')
    conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect('shop_sales.db')
    df = pd.read_sql_query("SELECT * FROM sales ORDER BY id DESC", conn)
    conn.close()
    return df

def insert_sale(date, name, variant, qty, cost, sell, total, profit):
    conn = sqlite3.connect('shop_sales.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sales (sale_date, item_name, item_variant, quantity, cost_price, sell_price, total_sales, net_profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (str(date), name, variant, qty, cost, sell, total, profit))
    conn.commit()
    conn.close()

init_db()

st.title("📊 نظام المبيعات والأرباح الذكي لأصحاب المحلات")
st.write("دليلك المتكامل لمتابعة أرباح محل الملابس الخاص بك، تنظيم مخزون المبيعات، وتصدير التقارير بدقة.")
st.markdown("---")

df_sales = load_data()
col1, col2 = st.columns(2)

with col1:
    st.subheader("➕ تسجيل عملية بيع جديدة")
    with st.form("sale_entry_form", clear_on_submit=True):
        date = st.date_input("تاريخ العملية", datetime.now())
        item_name = st.text_input("اسم القطعة (مثال: قميص رجالي، بنطال جينز)")
        item_variant = st.text_input("المقاس واللون (مثال: XL - أزرق)")
        quantity = st.number_input("الكمية المباعة", min_value=1, value=1, step=1)
        cost_price = st.number_input("سعر التكلفة للقطعة الواحدة", min_value=0.0, value=0.0, step=0.5)
        sell_price = st.number_input("سعر البيع للقطعة الواحدة", min_value=0.0, value=0.0, step=0.5)
        
        total_cost = quantity * cost_price
        total_sales = quantity * sell_price
        net_profit = total_sales - total_cost
        
        submit_button = st.form_submit_button("💾 حفظ العملية في النظام")
        if submit_button:
            if item_name.strip() == "":
                st.error("يرجى إدخال اسم القطعة أولاً لتسجيل العملية.")
            elif sell_price <= 0:
                st.warning("تنبيه: سعر البيع يجب أن يكون أكبر من صفر.")
            else:
                insert_sale(date, item_name, item_variant, quantity, cost_price, sell_price, total_sales, net_profit)
                st.success(f"✔️ تم حفظ بيع ({item_name}) بنجاح وتحديث الأرباح!")
                st.rerun()

with col2:
    st.subheader("📈 لوحة الأداء ومراقبة الأرباح")
    if not df_sales.empty:
        total_revenue = df_sales["total_sales"].sum()
        total_profit = df_sales["net_profit"].sum()
        total_items = df_sales["quantity"].sum()
        
        m1, m2, m3 = st.columns(3)
        m1.metric("💰 إجمالي المبيعات", f"{total_revenue:,.2f} د.أ")
        m2.metric("📈 صافي الأرباح", f"{total_profit:,.2f} د.أ")
        m3.metric("📦 قطع مباعة", f"{total_items} قطعة")
        
        st.markdown("---")
        search_query = st.text_input("🔍 ابحث في المبيعات السابقة (باسم القطعة):")
        if search_query:
            df_filtered = df_sales[df_sales["item_name"].str.contains(search_query, case=False, na=False)]
        else:
            df_filtered = df_sales.copy()
            
        df_display = df_filtered.rename(columns={
            "sale_date": "التاريخ",
            "item_name": "اسم القطعة",
            "item_variant": "المقاس/اللون",
            "quantity": "الكمية",
            "cost_price": "سعر التكلفة",
            "sell_price": "سعر البيع",
            "total_sales": "إجمالي البيع",
            "net_profit": "صافي الربح"
        })
        st.dataframe(df_display.drop(columns=["id"], errors="ignore"), use_container_width=True)
        
        st.markdown("### 📄 تصدير التقارير الدورية")
        csv = df_display.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 تحميل سجل المبيعات كملف (CSV)",
            data=csv,
            file_name=f"sales_report_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("ℹ️ النظام جاهز تماماً وبانتظار تسجيل أول عملية بيع.")
