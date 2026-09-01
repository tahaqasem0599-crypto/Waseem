import streamlit as st
import datetime
import json
import os

# إعدادات الصفحة الرسمية للتطبيق بألوان تليجرام
st.set_page_config(page_title="تليجرام المطور", page_icon="💬", layout="centered")

# تغيير التصميم الداخلي ليمثل ألوان تليجرام الشهيرة
st.markdown("""
    <style>
    .stApp { background-color: #E7EBF0; }
    .chat-bubble-me {
        background-color: #EFFDDE; padding: 10px; border-radius: 10px;
        margin: 5px; text-align: right; float: right; clear: both; width: 70%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .chat-bubble-other {
        background-color: #FFFFFF; padding: 10px; border-radius: 10px;
        margin: 5px; text-align: left; float: left; clear: both; width: 70%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .time-text { color: grey; font-size: 10px; display: block; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# ملف قاعدة البيانات المصغر لحفظ الرسائل بشكل دائم داخل السيرفر
DB_FILE = "chat_db.json"

def load_messages():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return [
        {"sender": "أحمد الدلو", "text": "مرحباً يا وسيم، كيف تسير هندسة التطبيق العالمي؟", "time": "04:28 م"},
        {"sender": "وسيم نائل", "text": "أهلاً أحمد، الكود جاهز ومرفوع الآن على جيت هاب ويعمل بكفاءة.", "time": "04:29 م"}
    ]

def save_message(sender, text, time):
    messages = load_messages()
    messages.append({"sender": sender, "text": text, "time": time})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# تحميل الرسائل المحفوظة في قاعدة البيانات الدائمة
all_messages = load_messages()

# الشريط العلوي للتطبيق (تليجرام)
st.markdown("<h2 style='text-align: center; color: #517DA2; font-weight: bold;'>💬 تليجرام المطور</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>مستودع وسيم نائل العالمي</h5>", unsafe_allow_html=True)
st.write("---")

# نظام تسجيل الدخول بالاسم
if "username" not in st.session_state or st.session_state.username == "":
    st.subheader("👋 أهلاً بك في تطبيق تليجرام المطور")
    name_input = st.text_input("الرجاء إدخال اسمك قبل البدء بالدردشة:", placeholder="اكتب اسمك هنا...")
    login_btn = st.button("دخول إلى التطبيق 🚀")
    
    if login_btn and name_input.strip() != "":
        st.session_state.username = name_input.strip()
        st.rerun()
else:
    # عرض الاسم الحالي وزر تحديث الشات لقراءة رسائل الآخرين الجدد
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"👤 متصل الآن باسم: **{st.session_state.username}**")
    with col2:
        if st.button("تحديث 🔄"):
            st.rerun()
        
    st.write("---")

    # عرض المحادثة من قاعدة البيانات الدائمة
    for msg in all_messages:
        if msg["sender"] == st.session_state.username:
            st.markdown(f'<div class="chat-bubble-me">{msg["text"]}<br><span class="time-text">{msg["time"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender"]}:</b><br>{msg["text"]}<br><span class="time-text">{msg["time"]}</span></div>', unsafe_allow_html=True)

    st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
    st.write("---")

    # حقل إدخال الرسائل الجديد
    with st.container():
        user_input = st.text_input("اكتب رسالة...", key="chat_input", placeholder="أرسل رسالة إلى القناة الحية...")
        send_button = st.button("إرسال 🚀")

        if send_button and user_input.strip() != "":
            time_now = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
            
            # حفظ الرسالة في السيرفر الدائم ليراها أي مستخدم آخر فوراً
            save_message(st.session_state.username, user_input.strip(), time_now)
            st.rerun()
    
