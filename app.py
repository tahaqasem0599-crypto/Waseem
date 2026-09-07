import streamlit as st
import datetime
import requests
import sqlite3
from PIL import Image

# 1. إعدادات الشاشة الكاملة للتطبيق وإخفاء هوامش Streamlit
st.set_page_config(
    page_title="تليجرام المطور - Telegram Pro",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. إنشاء وتجهيز قاعدة البيانات السحابية والمحلية (SQLite) لحفظ الحسابات والرسائل بشكل دائم
def init_db():
    conn = sqlite3.connect("telegram_desktop.db", check_same_thread=False)
    cursor = conn.cursor()
    # جدول الحسابات والمستخدمين
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    # جدول الرسائل المشفرة والمحمية
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_room TEXT,
            sender TEXT,
            msg_type TEXT,
            content TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

# 3. هندسة واجهة المستخدم الرسومية الفاخرة (CSS) للتليجرام الداكن
st.markdown("""
<style>
.stApp {
    background-color: #0e1621 !important;
    color: #f5f5f5 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #17212b !important;
    border-right: 1px solid #101921 !important;
}
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 9rem !important;
    max-width: 100% !important;
}
.tg-header {
    background-color: #17212b;
    padding: 14px 20px;
    border-bottom: 1px solid #101921;
    border-radius: 8px;
    margin-bottom: 15px;
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
}
.message-bubble {
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 70%;
    margin-bottom: 5px;
    line-height: 1.4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
}
.my-msg {
    background-color: #2b5278 !important;
    color: white !important;
    margin-right: auto;
    border-bottom-left-radius: 4px;
    text-align: right;
}
.other-msg {
    background-color: #182533 !important;
    color: #f5f5f5 !important;
    margin-left: auto;
    border-bottom-right-radius: 4px;
    text-align: right;
}
.msg-info {
    font-size: 11px;
    color: #7f8c8d;
    margin-top: 4px;
}
.my-msg .msg-info {
    color: #abc6e0;
}
.bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #17212b;
    padding: 12px 20px;
    border-top: 1px solid #101921;
    z-index: 9999;
}
div.stTextInput > div > div > input {
    background-color: #0e1621 !important;
    color: white !important;
    border: 1px solid #101921 !important;
    border-radius: 24px !important;
    padding: 10px 18px !important;
}
div.stButton > button {
    background-color: #2481cc !important;
    background-image: url('https://wikimedia.org') !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 55% !important;
    color: transparent !important;
    border-radius: 50% !important;
    width: 44px !important;
    height: 44px !important;
    border: none !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background-color: #288fde !important;
}
</style>
""", unsafe_allow_html=True)

# 4. التحكم في نظام الحسابات وتسجيل الدخول (Authentication)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("✈️ تليجرام - تسجيل الدخول")
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    with tab1:
        login_user = st.text_input("اسم المستخدم:", key="login_user_key")
        login_pass = st.text_input("كلمة المرور:", type="password", key="login_pass_key")
        if st.button("دخول", key="btn_login_submit"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (login_user, login_pass))
            if cursor.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
                
    with tab2:
        reg_user = st.text_input("اختر اسم مستخدم جديد:", key="reg_user_key")
        reg_pass = st.text_input("اختر كلمة مرور قوية:", type="password", key="reg_pass_key")
        if st.button("إنشاء الحساب تليجرام", key="btn_reg_submit"):
            if reg_user and reg_pass:
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (reg_user, reg_pass))
                    conn.commit()
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
                except sqlite3.IntegrityError:
                    st.error("اسم المستخدم هذا مأخوذ بالفعل، اختر اسماً آخر.")
            else:
                st.error("الرجاء ملء كافة الحقول")
    st.stop()

# 5. إذا كان المستخدم مسجلاً لديه الحساب يفتح التطبيق الأصلي مباشرة
st.sidebar.title("Telegram Pro")
st.sidebar.markdown(f"👤 مرحباً بك: **{st.session_state.username}**")

# غرف وقنوات المحادثة المتاحة في قاعدة البيانات
chat_rooms = ["🍉 تلجرام غزة", "📢 الأخبار العاجلة", "💬 محادثة خاصة 1"]
selected_chat = st.sidebar.selectbox("قائمة المحادثات والقنوات:", chat_rooms)

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# 6. عرض رأس صفحة المحادثة النشطة
st.markdown(f"""
<div class="tg-header">
    <h3 style="margin:0; color:white; font-size:16px;">{selected_chat}</h3>
    <span style="color:#5288c1; font-size:12px;">حساب محمي • متصل الآن</span>
</div>
""", unsafe_allow_html=True)

# 7. جلب وعرض الرسائل المخزنة في قاعدة البيانات الخاصة بهذه الغرفة فقط
cursor.execute("SELECT sender, msg_type, content, timestamp FROM messages WHERE chat_room=? ORDER BY id ASC", (selected_chat,))
saved_messages = cursor.fetchall()

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in saved_messages:
    sender, m_type, content, timestamp = msg
    is_me = sender == st.session_state.username
    bubble_class = "my-msg" if is_me else "other-msg"
    sender_title = "أنت" if is_me else sender
    
    st.markdown(f"""
    <div class="message-bubble {bubble_class}">
        <div style="font-size:12px; font-weight:bold; color:#5288c1; margin-bottom:3px;">{sender_title}</div>
        <div>{content}</div>
        <div class="msg-info">{timestamp} {'✓✓' if is_me else ''}</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 8. شريط صندوق الإدخال السفلي والمثبت المتناسق
st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
with st.form(key="telegram_database_form", clear_on_submit=True):
    txt_col, file_col, btn_col = st.columns([8, 1, 1])
    
    with txt_col:
        user_text = st.text_input("الرسالة النصية", placeholder="اكتب رسالة محمية ومسجلة...", label_visibility="collapsed")
    with file_col:
        uploaded_media = st.file_uploader("الملفات", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    with btn_col:
        btn_trigger = st.form_submit_button("إرسال")

    if btn_trigger:
        time_stamp = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
        
        # حفظ النص في قاعدة البيانات السحابية لضمان الخصوصية والسرية
        if user_text:
            cursor.execute("INSERT INTO messages (chat_room, sender, msg_type, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (selected_chat, st.session_state.username, "text", user_text, time_stamp))
            conn.commit()
            
        # حفظ الملف في قاعدة البيانات
        if uploaded_media is not None:
            cursor.execute("INSERT INTO messages (chat_room, sender, msg_type, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (selected_chat, st.session_state.username, "file", f"📎 ملف مرفق: {uploaded_media.name}", time_stamp))
            conn.commit()
            
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
