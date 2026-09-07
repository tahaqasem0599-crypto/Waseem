import streamlit as st
import datetime
import requests
from PIL import Image

# 1. إعدادات الشاشة الكاملة وإخفاء هوامش Streamlit لتوسيع التصميم
st.set_page_config(
    page_title="تليجرام - Telegram Web",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. حقن تصميم الـ CSS الخارق لتحويل الواجهة بالكامل إلى تليجرام أصلي 100%
st.markdown("""
<style>
/* تصفير هوامش التطبيق بالكامل ليصبح كالموقع الرسمي */
.stApp {
    background-color: #0e1621 !important;
    color: #f5f5f5 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* تخصيص شريط الدردشات الجانبي لتليجرام */
[data-testid="stSidebar"] {
    background-color: #17212b !important;
    border-right: 1px solid #101921 !important;
}

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 7rem !important; /* مساحة حرة بالأسفل لصندوق الإدخال العائم */
    max-width: 100% !important;
}

/* هيدر تليجرام العلوي الثابت مع اسم المجموعة وحالتها */
.tg-actual-header {
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
.tg-title-text {
    font-size: 16px;
    font-weight: bold;
    color: #ffffff;
    margin: 0;
}
.tg-status-text {
    font-size: 13px;
    color: #5288c1;
}

/* قائمة المحادثات الجانبية الأنيقة */
.tg-sidebar-item {
    padding: 12px;
    margin: 4px 8px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: transparent;
}
.tg-avatar-circle {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background-color: #2b5278;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
}

/* ساحة تدفق فقاعات الرسائل الدائرية الشبيهة بالتطبيق الفعلي */
.chat-flow-zone {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px;
}

.tg-bubble {
    padding: 10px 15px;
    border-radius: 16px;
    max-width: 60%;
    font-size: 15px;
    line-height: 1.4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
    position: relative;
    display: flex;
    flex-direction: column;
}

/* رسائلك الزرقاء */
.bubble-outgoing {
    background-color: #2b5278 !important;
    color: white !important;
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}

/* رسائل أصدقائك الملونة بالرمادي الداكن الأصلي */
.bubble-incoming {
    background-color: #182533 !important;
    color: #f5f5f5 !important;
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}

.tg-bubble-sender {
    font-size: 12px;
    font-weight: bold;
    color: #5288c1;
    margin-bottom: 4px;
}

.tg-bubble-footer {
    font-size: 10px;
    color: #7f8c8d;
    align-self: flex-end;
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 4px;
}
.bubble-outgoing .tg-bubble-footer {
    color: #abc6e0;
}

/* تثبيت شريط إدخال الرسائل بشكل عائم وسلس بالأسفل تماماً لمنع الانزلاق */
.fixed-bottom-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #17212b;
    padding: 12px 24px;
    border-top: 1px solid #101921;
    z-index: 9999;
}

/* إخفاء حواف وتفاصيل حقول الرفع الافتراضية المزعجة */
[data-testid="stFileUploader"] {
    padding: 0 !important;
    margin: 0 !important;
}

/* زر إرسال دائري يحمل شعار التليجرام الرسمي وبأبعاد دقيقة */
div.stButton > button {
    background-color: #2481cc !important;
    background-image: url('https://wikimedia.org') !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 60% !important;
    color: transparent !important;
    border-radius: 50% !important;
    width: 46px !important;
    height: 46px !important;
    border: none !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
div.stButton > button:hover {
    background-color: #288fde !important;
}
</style>
""", unsafe_allow_html=True)

# 3. قاعدة البيانات المحلية وجلسة تخزين المحادثات والرسائل حياً
if "messages" not in st.session_state:
    st.session_state.messages = {
        "🍉 تلجرام غزة": [
            {"sender": "Waseem", "type": "text", "content": "أهلاً يا شباب، هذا هو التحديث البرمجي الأقوى للتطبيق لتطابق النسخة الأصلية بالملّي! 🔥", "time": "03:15 ص"},
            {"sender": "أبو أحمد", "type": "text", "content": "ما شاء الله واجهة خرافية وسريعة جداً كأننا داخل التليجرام الفعلي.", "time": "03:16 ص"}
        ],
        "📢 الأخبار العاجلة": [
            {"sender": "المشرف", "type": "text", "content": "تغطية مستمرة وحية للأوضاع الميدانية على مدار الساعة.", "time": "02:00 ص"}
        ]
    }

if "username" not in st.session_state:
    st.session_state.username = "Waseem"

# 🔑 إعدادات الربط ببوت التليجرام للبث المباشر (اكتب رموزك الحقيقية هنا للتفعيل)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def relay_message_to_telegram_server(text):
    if BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN":
        url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
        try: requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=3)
        except: pass

# 4. بناء القائمة الجانبية (شريط المحادثات المألوف)
st.sidebar.markdown("<h2 style='text-align:center; color:#5288c1; font-weight:bold; margin-bottom:20px;'>Telegram</h2>", unsafe_allow_html=True)

chat_keys = list(st.session_state.messages.keys())
for key in chat_keys:
    last_msg = st.session_state.messages[key][-1]["content"] if st.session_state.messages[key] else "لا توجد رسائل"
    st.sidebar.markdown(f"""
    <div class="tg-sidebar-item">
        <div class="chat-item-left">
            <div class="tg-avatar-circle">💬</div>
            <div class="chat-meta-info">
                <h4 style="margin:0; font-size:14px; color:white;">{key}</h4>
                <p style="font-size:12px; color:#7f8c8d; margin:2px 0 0 0;">{last_msg[:18]}...</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
selected_chat = st.sidebar.selectbox("اختر غرف المحادثة النشطة:", chat_keys)
st.session_state.username = st.sidebar.text_input("⚙️ اسمك داخل المحادثات:", value=st.session_state.username)

# 5. عرض رأس الصفحة المحدث للتليجرام
st.markdown(f"""
<div class="tg-main-header">
    <div class="header-info">
        <h3 class="tg-title-text">{selected_chat}</h3>
        <span class="tg-status-text">متصل الآن • تطبيق مخصص عالي الدقة</span>
    </div>
    <div style="color: #7f8c8d; font-size: 24px; cursor: pointer;">⋮</div>
</div>
""", unsafe_allow_html=True)

# 6. ساحة عرض الرسائل والفقاعات المصلحة والآمنة من تسريبات الـ HTML
st.markdown('<div class="chat-flow-zone">', unsafe_allow_html=True)

for msg in st.session_state.messages[selected_chat]:
    is_me = msg["sender"] == st.session_state.username
    bubble_side_class = "bubble-outgoing" if is_me else "bubble-incoming"
    sender_title = "أنت" if is_me else msg["sender"]
    
    st.markdown(f"""
    <div class="tg-bubble {bubble_side_class}">
        {f'<div class="tg-bubble-sender">{sender_title}</div>' if not is_me else ''}
        <div style="direction: rtl; text-align: right; word-wrap: break-word;">{msg['content']}</div>
        <div class="tg-bubble-footer">
            {msg['time']} { '✓✓' if is_me else '' }
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if msg["type"] == "image" and not isinstance(msg["content"], str):
        st.image(msg["content"], width=320)

st.markdown('</div>', unsafe_allow_html=True)

# 7. صندوق إرسال الرسائل العائم الفاخر المثبت بالأسفل تماماً
st.markdown('<div class="fixed-bottom-container">', unsafe_allow_html=True)

with st.form(key="tg_perfect_form", clear_on_submit=True):
    txt_col, file_col, button_col = st.columns([75, 15, 10]) # نسب دقيقة جداً للأعمدة تمنع التداخل والانزلاق
    
    with txt_col:
        text_payload = st.text_input("الكتابة", placeholder="اكتب رسالة...", label_visibility="collapsed")
    
    with file_col:
        file_payload = st.file_uploader("الملفات", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
        
    with button_col:
        trigger_send = st.form_submit_button("إرسال")

# معالجة عمليات الضغط البرمجية وتحديث الشاشة فوراً
if trigger_send and text_payload:
    stamp_time = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    st.session_state.messages[selected_chat].append({
        "sender": st.session_state.username,
        "type": "text",
        "content": text_payload,
        "time": stamp_time
    })
    relay_message_to_telegram_server(f"👤 {st.session_state.username} [{selected_chat}]:\n{text_payload}")
    st.rerun()

if file_payload is not None:
    stamp_time = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    resolved_kind = "image" if file_payload.type.startswith("image/") else "file"
    try:
        stored_object = Image.open(file_payload) if resolved_kind == "image" else file_payload.name
        st.session_state.messages[selected_chat].append({
            "sender": st.session_state.username,
            "type": resolved_kind,
            "content": stored_object,
            "time": stamp_time
        })
        st.rerun()
    except Exception as error_log:
        st.error(f"مشكلة في المستند: {error_log}")

st.markdown('</div>', unsafe_allow_html=True)
