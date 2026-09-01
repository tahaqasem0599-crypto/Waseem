import streamlit as st
import datetime
import json
import os

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="تليجرام", page_icon="🔹", layout="centered")

# هندسة وتصميم واجهة تليجرام الأصلي بالكامل عبر CSS مخصص
st.markdown("""
    <style>
    /* إلغاء الفراغات العلوية الافتراضية لتبدو كشاشة هاتف */
    .block-container { padding-top: 0rem; padding-bottom: 5rem; max-width: 600px; }
    
    /* خلفية تليجرام الرسمية */
    .stApp { 
        background-color: #E7EBF0;
        background-image: url('https://githubusercontent.com');
        background-attachment: fixed;
    }
    
    /* شريط تليجرام العلوي الثابت */
    .telegram-header {
        background-color: #517DA2;
        color: white;
        padding: 13px 20px;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 9999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.15);
        font-family: sans-serif;
    }
    .header-title { font-size: 20px; font-weight: bold; margin: 0; }
    .header-icons { font-size: 22px; cursor: pointer; }
    
    /* حاوية الرسائل لتجنب التداخل مع الأشرطة الثابتة */
    .chat-container { margin-top: 70px; margin-bottom: 20px; }

    /* تصميم فقاعات المحادثة المطابق للأصل */
    .bubble-container-me { display: flex; justify-content: flex-end; width: 100%; clear: both; margin: 6px 0; }
    .bubble-container-other { display: flex; justify-content: flex-start; width: 100%; clear: both; margin: 6px 0; }
    
    .bubble-me {
        background-color: #EFFDDE;
        color: #000000;
        padding: 8px 14px;
        border-radius: 15px 15px 0px 15px;
        max-width: 75%;
        box-shadow: 0px 1px 1px rgba(0,0,0,0.2);
        position: relative;
        font-size: 16px;
        direction: rtl;
    }
    .bubble-other {
        background-color: #FFFFFF;
        color: #000000;
        padding: 8px 14px;
        border-radius: 15px 15px 15px 0px;
        max-width: 75%;
        box-shadow: 0px 1px 1px rgba(0,0,0,0.2);
        position: relative;
        font-size: 16px;
        direction: rtl;
    }
    
    /* تفاصيل اسم المرسل والوقت */
    .sender-name { color: #3a75ad; font-weight: bold; font-size: 14px; margin-bottom: 20px; display: block;}
    .meta-data {
        font-size: 11px;
        color: #70c05a;
        margin-top: 4px;
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 3px;
    }
    .meta-data-other { font-size: 11px; color: #a3a3a3; margin-top: 4px; text-align: left; }
    
    /* شريط الإدخال السفلي الاحترافي */
    .footer-container {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        background-color: transparent;
        padding: 10px;
        display: flex;
        justify-content: center;
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة وتخزين بيانات الشات بشكل دائم في السيرفر
DB_FILE = "telegram_db.json"

def load_messages():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return [
        {"sender": "أحمد الدلو", "text": "مرحباً يا وسيم، كيف تسير هندسة التطبيق العالمي؟", "time": "04:28 م"},
        {"sender": "وسيم نائل", "text": "أهلاً أحمد، الكود جاهز ومرفوع الآن ويعمل بكفاءة مثل تليجرام بالضبط.", "time": "04:29 م"}
    ]

def save_message(sender, text, time):
    messages = load_messages()
    messages.append({"sender": sender, "text": text, "time": time})
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

all_messages = load_messages()

# حقن شريط تليجرام العلوي في الشاشة
st.markdown("""
    <div class="telegram-header">
        <div class="header-icons">☰</div>
        <div class="header-title">تليجرام المطور</div>
        <div class="header-icons">🔍</div>
    </div>
""", unsafe_allow_html=True)

# مساحة لبدء عرض الرسائل تحت الشريط العلوي
st.markdown('<div class="chat-container"></div>', unsafe_allow_html=True)

# 👤 بوابة التحكم وتحديد اسم المستخدم
if "username" not in st.session_state or st.session_state.username == "":
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.subheader("👋 أهلاً بك في تليجرام")
    name_input = st.text_input("ادخل اسمك المستعار لبدء المراسلة الحية:", placeholder="اكتب اسمك هنا...")
    if st.button("دخول 🚀") and name_input.strip() != "":
        st.session_state.username = name_input.strip()
        st.rerun()
else:
    # عرض معلومات المستخدم المسجل وزر تحديث سريع
    col1, col2 = st.columns([4, 1])
    with col1:
        st.caption(f"👤 الحساب النشط: {st.session_state.username}")
    with col2:
        if st.button("تحديث 🔄"):
            st.rerun()

    # 💬 حلقة عرض المحادثات والفقاعات الرائعة
    for msg in all_messages:
        if msg["sender"] == st.session_state.username:
            # تصميم رسائلي الخاصة باللون الأخضر على اليمين مع علامة الصح القراءة ✔✔
            st.markdown(f"""
                <div class="bubble-container-me">
                    <div class="bubble-me">
                        {msg['text']}
                        <div class="meta-data">{msg['time']} ✔✔</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # تصميم رسائل الأصدقاء باللون الأبيض على اليسار مع إظهار أسمائهم بالأزرق
            st.markdown(f"""
                <div class="bubble-container-other">
                    <div class="bubble-other">
                        <span class="sender-name">{msg['sender']}</span>
                        {msg['text']}
                        <div class="meta-data-other">{msg['time']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # نموذج المراسلة والإرسال الذكي أسفل الشاشة
    st.write("---")
    with st.form(key="msg_form", clear_on_submit=True):
        user_input = st.text_input("اكتب رسالة...", placeholder="أرسل رسالة إلى القناة الحية...")
        submit_button = st.form_submit_with_button_type(label="إرسال الرسالة الفورية 🚀")
        
        if submit_button and user_input.strip() != "":
            time_now = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
            save_message(st.session_state.username, user_input.strip(), time_now)
            st.rerun()
