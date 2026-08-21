import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import io

st.set_page_config(page_title="Shop Sales")

def init_db():
    conn = sqlite3.connect('shop_sales.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT,
            item_name TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

st.title("📊 نظام إدارة مبيعات المتجر")
st.write("تم تهيئة قاعدة البيانات بنجاح وجاهزة للاستخدام.")
