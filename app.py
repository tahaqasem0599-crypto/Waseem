import streamlit as st
import datetime
import requests
import time
from PIL import Image

# 1. إعدادات الشاشة الكاملة للتطبيق وإخفاء قوائم Streamlit الافتراضية
st.set_page_config(
    page_title="تليجرام - Telegram Web",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. هندسة الواجهة الرسومية بالكامل (CSS Injection) لتطابق التليجرام الأصلي 100%
st.markdown("""
<style>
/* تهيئة الخلفية الرسمية للتليجرام الداكن */
.stApp {
    background-color: #0e1621 !important;
    color: #f5f5f5 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* تخصيص القائمة الجانبية بالكامل */
[data-testid="stSidebar"] {
    background-color: #17212b !important;
    border-right: 1px solid #101921 !important;
}

/* تصفير هوامش البناء لملء الشاشة */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 7rem !important;
    max-width: 100% !important;
}

/* تصميم هيدر المحادثة العلوي الثابت */
.tg-main-header {
    background-color: #17212b;
    padding: 14px 24px;
    border-bottom: 1px solid #101921;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 999;
}
.tg-chat-title {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    margin: 0;
}
.tg-chat-status {
    font-size: 13px;
    color: #5288c1;
}

/* قائمة الدردشات الجانبية الأنيقة */
.sidebar-chat-item {
    padding: 12px;
    margin: 4px 8px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: transparent;
    cursor: pointer;
    transition: background 0.2s;
}
.sidebar-chat-item:hover {
    background-color: #202b36;
}
.chat-item-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.chat-avatar {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background-color: #5288c1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    font-size: 18px;
}
.chat-meta-info h4 {
    margin: 0;
    font-size: 15px;
    color: white;
}
.chat-meta-info p {
    margin: 2px 0 0 0;
    font-size: 13px;
    color: #7f8c8d;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 150px;
}
.badge-unread {
    background-color: #45ae55;
    color: white;
    border-radius: 50%;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: bold;
}

/* ساحة المحادثة الرئيسية وبناء الفقاعات المتطورة */
.chat-flow {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 20px;
    background-color: #0e1621;
}

.bubble {
    padding: 10px 14px;
    border-radius: 16px;
    max-width: 60%;
    font-size: 15px;
    line-height: 1.4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
    position: relative;
    display: flex;
    flex-direction: column;
}

/* رسائلك أنت (تظهر على اليمين باللون الأزرق الرسمي للتليجرام) */
.bubble-me {
    background-color: #2b5278 !important;
    color: white !important;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}

/* رسائل المستلمين الآخرين (تظهر على اليسار باللون الرمادي الداكن المريح) */
.bubble-other {
    background-color: #182533 !important;
    color: #f5f5f5 !important;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}

.bubble-sender {
    font-size: 12px;
    font-weight: bold;
    color: #5288c1;
    margin-bottom: 3px;
}

.bubble-footer {
    font-size: 10px;
    color: #7f8c8d;
    align-self: flex-end;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.bubble-me .bubble-footer {
    color: #abc6e0;
}

/* تثبيت صندوق الإدخال الفاخر أسفل الشاشة تماماً */
.premium-input-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #17212b;
    padding: 16px 30px;
    border-top: 1px solid #101921;
    z-index: 9999;
}

/* تعديل شكل حقل الكتابة الافتراضي ليدمج بشكل دائري */
div.stTextInput > div > div > input {
    background-color: #0e1621 !important;
    color: white !important;
    border: 1px solid #101921 !important;
    border-radius: 24px !important;
    padding: 12px 20px !important;
}

/* تحويل زر الإرسال الافتراضي إلى دائرة تحمل شعار تليجرام بالكامل مع إلغاء حواف الإطار الافتراضي لـ Streamlit */
div.stButton > button {
    background-color: #2481cc !important;
    background-image: url('https://wikimedia.org') !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 60% !important;
    color: transparent !important; /* إخفاء النص النصي المكتوب داخل الزر */
    border-radius: 50% !important;
    width: 48px !important;
    height: 48px !important;
    border: none !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background-color: #288fde !important;
}
</style>
""", unsafe_allow_html=True)

# 3. تهيئة قواعد البيانات المؤقتة لتشغيل المحادثات حياً وبدون انقطاع
if "messages" not in st.session_state:
    st.session_state.messages = {
        "🍉 تلجرام غزة": [
            {"sender": "Waseem", "type": "text", "content": "أهلاً يا شباب، هذا هو التحديث البرمجي الأقوى للتطبيق لتطابق النسخة الأصلية بالملّي! 🔥", "time": "03:15 ص"},
            {"sender": "أبو أحمد", "type": "text", "content": "ما شاء الله واجهة خرافية وسريعة جداً كأننا داخل التليجرام الفعلي.", "time": "03:16 ص"}
        ],
        "📢 الأخبار العاجلة": [
            {"sender": "المشرف", "type": "text", "content": "تغطية مستمرة وحية للأوضاع الميدانية على مدار الساعة.", "time": "02:00 ص"}
        ],
        "⚙️ الدعم الفني المطور": [
            {"sender": "الدعم", "type": "text", "content": "مرحباً بك وسيم، السيرفر يعمل الآن بكفاءة 100%.", "time": "أمس"}
        ]
    }

if "username" not in st.session_state:
    st.session_state.username = "Waseem"

# 🔑 إعدادات الربط ببوت التليجرام للبث المباشر (استبدلها ببياناتك لتفعيل الإرسال الحقيقي لقناتك)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def relay_message_to_telegram_server(text):
    if BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN":
        url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
        try: requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=3)
        except: pass

# 4. بناء الشريط الجانبي الفاخر (قائمة تليجرام الجانبية للدردشات)
st.sidebar.markdown("<h2 style='text-align:center; color:#5288c1; font-weight:bold; margin-bottom:20px;'>Telegram</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color:#7f8c8d; padding-left:12px; font-size:13px;'>الدردشات الأخيرة</p>", unsafe_allow_html=True)

chat_keys = list(st.session_state.messages.keys())

# محاكاة القائمة الحقيقية بالتطبيق
for key in chat_keys:
    last_msg = st.session_state.messages[key][-1]["content"] if st.session_state.messages[key] else "لا توجد رسائل"
    avatar_letter = key if len(key) > 2 else "T"
    
    st.sidebar.markdown(f"""
    <div class="sidebar-chat-item">
        <div class="chat-item-left">
            <div class="chat-avatar">{avatar_letter}</div>
            <div class="chat-meta-info">
                <h4>{key}</h4>
                <p>{last_msg}</p>
            </div>
        </div>
        <div>
            <span class="badge-unread">1</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
selected_chat = st.sidebar.selectbox("تبديل غرف المحادثة النشطة:", chat_keys)
st.session_state.username = st.sidebar.text_input("⚙️ اسمك داخل المحادثات:", value=st.session_state.username)

# 5. عرض هيدر تليجرام الأصلي في أعلى نافذة الشات النشطة
st.markdown(f"""
<div class="tg-main-header">
    <div class="header-info">
        <h3 class="tg-chat-title">{selected_chat}</h3>
        <span class="tg-chat-status">{'3 أعضاء نشطين • متصل الآن' if 'غزة' in selected_chat else 'قناة رسمية موثقة'}</span>
    </div>
    <div style="color: #7f8c8d; font-size: 24px; cursor: pointer; font-weight:bold;">⋮</div>
</div>
""", unsafe_allow_html=True)

# 6. ساحة التدفق الحي وعرض الفقاعات الرسمية الدائرية (Chat View Screen)
st.markdown('<div class="chat-flow">', unsafe_allow_html=True)

for msg in st.session_state.messages[selected_chat]:
    is_me = msg["sender"] == st.session_state.username
    bubble_side_class = "bubble-me" if is_me else "bubble-other"
    sender_title = "أنت" if is_me else msg["sender"]
    
    # فلترة آمنة لمنع اختلال الأقواس وحماية السينتكس
    if msg["type"] == "text":
        body_layout = f"<div>{msg['content']}</div>"
    elif msg["type"] == "image":
        body_layout = f"<div style='color:#5288c1; font-weight:bold;'>🖼️ صورة مرفقة في الدردشة</div>"
    else:
        body_layout = f"<div>📁 ملف مستند: {msg['content']}</div>"

    # حقن الفقاعة المقفلة تماماً بإحكام هائل
    st.markdown(f"""
    <div class="bubble {bubble_side_class}">
        {f'<div class="bubble-sender">{sender_title}</div>' if not is_me else ''}
        {body_layout}
        <div class="bubble-footer">
            {msg['time']} { '✓✓' if is_me else '' }
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # عرض ملفات الميديا الحقيقية المرفوعة أسفل الفقاعة مباشرة بداخل Streamlit
    if msg["type"] == "image" and not isinstance(msg["content"], str):
        st.image(msg["content"], width=320)

st.markdown('</div>', unsafe_allow_html=True)

# 7. صندوق إرسال الرسائل الفاخر والمثبت بالأسفل (Sticky Floating Actions Bar)
st.markdown('<div class="premium-input-bar">', unsafe_allow_html=True)

with st.form(key="tg_perfect_form", clear_on_submit=True):
    txt_col, file_col, button_col = st.columns()
    
    with txt_col:
        text_payload = st.text_input("الكتابة", placeholder="اكتب رسالتك المنسقة هنا...", label_visibility="collapsed")
    
    with file_col:
        file_payload = st.file_uploader("الملفات", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
        
    with button_col:
