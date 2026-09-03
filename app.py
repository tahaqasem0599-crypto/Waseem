import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="تليجرام بلس", page_icon="✈️")

def init_db():
    conn = sqlite3.connect('tg_simple.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, content TEXT, ts TEXT)')
    conn.commit()
    return conn

conn = init_db()

if 'user' not in st.session_state:
    st.title("✈️ تليجرام المطور")
    name = st.text_input("اكتب اسمك هنا للبدء:")
    if st.button("📌 دخول"):
        if name.strip():
            st.session_state.user = name.strip()
            st.rerun()
else:
    st.title(f"💬 غرفة الدردشة الحية")
    st.write(f"المستخدم الحالي: **{st.session_state.user}**")
    
    if st.button("🚪 تسجيل الخروج"):
        del st.session_state.user
        st.rerun()

    st.markdown("---")
    chat_box = st.container(height=300)
    with chat_box:
        c = conn.cursor()
        c.execute('SELECT user, content, ts FROM msgs ORDER BY id ASC')
        for usr, txt, t in c.fetchall():
            st.markdown(f"**{usr}** <small style='color:gray;'>({t})</small>: {txt}")

    with st.form("send", clear_on_submit=True):
        msg = st.text_input("اكتب رسالتك هنا...")
        if st.form_submit_button("🚀 إرسال"):
            if msg.strip():
                t_now = datetime.now().strftime("%I:%M %p")
                c = conn.cursor()
                c.execute('INSERT INTO msgs (user, content, ts) VALUES (?, ?, ?)', (st.session_state.user, msg.strip(), t_now))
                conn.commit()
                st.rerun()
    
    if st.button("🔄 تحديث الرسائل"):
        st.rerun()
    
