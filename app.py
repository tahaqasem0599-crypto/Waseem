import streamlit as st
import datetime
import requests
from PIL import Image

# 1. إعدادات الشاشة الكاملة للتطبيق
st.set_page_config(
    page_title="تليجرام - Telegram Web",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. هندسة واجهة المستخدم (CSS) لمحاكاة تطبيق التليجرام الداكن
st.markdown("""
<style>
/* تهيئة الخلفية الرسمية للتليجرام الداكن */
.stApp {
    background-color: #0e1621 !important;
    color: #f5f5f5 !important;
}

/* تخصيص القائمة الجانبية وقائمة المحادثات */
[data-testid="stSidebar"] {
    background-color: #17212b !important;
    border-right: 1px solid #101921 !important;
}

/* تصفير مسافات التدفق لمنع انزلاق العناصر */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 8rem !important;
    max-width: 100% !important;
}

/* هيدر تليجرام العلوي */
.tg-header {
    background-color: #17212b;
    padding: 12px 20px;
    border-bottom: 1px solid #101921;
    border-radius: 8px;
    margin-bottom: 15px;
}

/* ساحة المحادثة وعرض فقاعات الرسائل */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
}

/* تصميم الفقاعة الأساسي */
.message-bubble {
    padding: 10px 14px;
    border-radius: 14px;
    max-width: 75%;
    margin-bottom: 5px;
    line-height: 1.4;
    box-shadow: 0 1px 2px rgba(0,0,0,0.2);
}

/* رسائلك أنت (باللون الأزرق على اليمين) */
.my-msg {
    background-color: #2b5278 !important;
    color: white !important;
    margin-right: auto;
    border-bottom-left-radius: 4px;
    text-align: right;
}

/* رسائل الآخرين (باللون الرمادي على اليسار) */
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
    text-align: left;
}
.my-msg .msg-info {
    color: #abc6e0;
}

/* زر إرسال دائري يحمل شعار تليجرام بالكامل وبمقاسات ثابتة */
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
    margin-top: 10px;
}
div.stButton > button:hover {
    background-color: #288fde !important;
}
</style>
""", unsafe_allow_html=True)

# 3. تهيئة البيانات بشكل سليم ونصوص نظيفة خالية من تاغات الـ HTML القديمة
if "messages" not in st.session_state:
    st.session_state.messages = {
        "🍉 تلجرام غزة": [
            {"sender": "Waseem", "type": "text", "content": "أهلاً يا شباب، تم إصلاح نصوص الواجهة وتحديثها بالكامل لتصبح نظيفة ومتناسقة! 🔥", "time": "03:15 ص"},
            {"sender": "أبو أحمد", "type": "text", "content": "ما شاء الله الواجهة ممتازة الآن وسريعة كأننا داخل التطبيق الفعلي.", "time": "03:16 ص"}
        ],
        "📢 الأخبار العاجلة": [
            {"sender": "المشرف", "type": "text", "content": "تغطية مستمرة وحية للأوضاع الميدانية على مدار الساعة.", "time": "02:00 ص"}
        ]
    }

if "username" not in st.session_state:
    st.session_state.username = "Waseem"

# 🔑 إعدادات الربط ببوت التليجرام الخارجي (ضع رموزك هنا للتفعيل)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

def relay_message_to_telegram(text):
    if BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN":
        url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
        try: requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=3)
        except: pass

# 4. بناء الشريط الجانبي لقائمة القنوات والمحادثات
st.sidebar.title("Telegram")
chat_keys = list(st.session_state.messages.keys())
selected_chat = st.sidebar.selectbox("اختر المحادثة النشطة:", chat_keys)
st.session_state.username = st.sidebar.text_input("⚙️ اسمك في المحادثة:", value=st.session_state.username)

# زر لمسح ذاكرة التخزين المؤقتة إذا علقت النصوص القديمة في متصفحك
if st.sidebar.button("🗑️ إعادة تهيئة ومسح النصوص القديمة"):
    del st.session_state.messages
    st.rerun()

# 5. عرض هيدر تليجرام في الشاشة الرئيسية
st.markdown(f"""
<div class="tg-header">
    <h3 style="margin:0; color:white; font-size:16px;">{selected_chat}</h3>
    <span style="color:#5288c1; font-size:12px;">متصل الآن • تطبيق مخصص</span>
</div>
""", unsafe_allow_html=True)

# 6. ساحة عرض الرسائل والفقاعات بشكل آمن ونظيف تماماً
for msg in st.session_state.messages[selected_chat]:
    is_me = msg["sender"] == st.session_state.username
    bubble_class = "my-msg" if is_me else "other-msg"
    sender_title = "أنت" if is_me else msg["sender"]
    
    # عرض الفقاعة بطريقة برمجية نظيفة ومعزولة
    st.markdown(f"""
    <div class="message-bubble {bubble_class}">
        <div style="font-size:12px; font-weight:bold; color:#5288c1; margin-bottom:3px;">{sender_title}</div>
        <div>{msg['content']}</div>
        <div class="msg-info">{msg['time']} {'✓✓' if is_me else ''}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if msg["type"] == "image" and not isinstance(msg["content"], str):
        st.image(msg["content"], width=280)

# 7. صندوق إرسال الرسائل والملفات المبسط والتلقائي لمنع الانزلاق والتشوه على الهاتف
st.write("---")
with st.container():
    # حقل النص الأساسي منفصل ليعطيه المساحة الكاملة على شاشات الهاتف ويمنع انزلاقه
    user_text = st.text_input("الرسالة النصية:", placeholder="اكتب رسالتك هنا...", label_visibility="collapsed")
    
    # كولوم مخصص فقط للمرفقات وزر الإرسال لترتيب مريح وثابت
    col_file, col_btn = st.columns([5, 1])
    
    with col_file:
        uploaded_media = st.file_uploader("إرفاق ملف", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    
    with col_btn:
        btn_trigger = st.form_submit_button("إرسال") if 'form' in locals() else st.button("إرسال")

# معالجة الضغط على زر الإرسال لتسجيل النصوص حياً
if (btn_trigger and user_text) or (user_text and not btn_trigger and st.session_state.get('last_text') != user_text):
    time_stamp = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    st.session_state.messages[selected_chat].append({
        "sender": st.session_state.username,
        "type": "text",
        "content": user_text,
        "time": time_stamp
    })
    relay_message_to_telegram(f"👤 {st.session_state.username} [{selected_chat}]:\n{user_text}")
    st.rerun()

# معالجة رفع الملفات والصور بطريقة مغلقة وآمنة
if uploaded_media is not None:
    time_stamp = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    media_kind = "image" if uploaded_media.type.startswith("image/") else "file"
    try:
        media_object = Image.open(uploaded_media) if media_kind == "image" else uploaded_media.name
        st.session_state.messages[selected_chat].append({
            "sender": st.session_state.username,
            "type": media_kind,
            "content": media_object,
            "time": time_stamp
        })
        st.rerun()
    except Exception as e:
        st.error(f"خطأ في المرفق: {e}")
    
