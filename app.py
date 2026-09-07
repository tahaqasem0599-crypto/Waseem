import streamlit as st
import datetime
from PIL import Image

# 1. إعدادات الشاشة الكاملة لتطبيق تليجرام
st.set_page_config(
    page_title="تليجرام - Telegram Web",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. هندسة واجهة المستخدم (CSS) لمحاكاة تطبيق تليجرام الداكن والشعار الرسمي
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
    padding-bottom: 9rem !important;
    max-width: 100% !important;
}

/* هيدر تليجرام العلوي مع الشعار الدائري */
.tg-header-container {
    background-color: #17212b;
    padding: 12px 20px;
    border-bottom: 1px solid #101921;
    border-radius: 8px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 15px;
}
.tg-logo-img {
    width: 40px;
    height: 40px;
    background-image: url('https://wikimedia.org');
    background-size: cover;
    background-position: center;
    border-radius: 50%;
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

/* تخصيص وتثبيت شريط الإدخال في الأسفل تماماً على شاشات الهاتف */
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

/* تعديل حقل الكتابة الافتراضي ليدمج بشكل دائري سلس */
div.stTextInput > div > div > input {
    background-color: #0e1621 !important;
    color: white !important;
    border: 1px solid #101921 !important;
    border-radius: 24px !important;
    padding: 10px 18px !important;
}

/* إخفاء حواف مربع رفع الملفات واحتوائه بشكل نظيف */
[data-testid="stFileUploader"] {
    padding: 0 !important;
    margin: 0 !important;
}

/* تحويل زر الإرسال الافتراضي إلى دائرة تحمل شعار تليجرام الفعلي المطور */
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

# 3. تهيئة البيانات بشكل سليم ومستقر
if "messages" not in st.session_state:
    st.session_state.messages = {
        "🍉 تلجرام غزة": [
            {"sender": "Waseem", "type": "text", "content": "أهلاً يا شباب، تم إضافة شعار تليجرام الرسمي للواجهة وتحديث الأزرار! ✈️🔥", "time": "03:15 ص"},
            {"sender": "أبو أحمد", "type": "text", "content": "ما شاء الله الواجهة ممتازة ومثالية الآن بشعار تليجرام الأصلي.", "time": "03:16 ص"}
        ],
        "📢 الأخبار العاجلة": [
            {"sender": "المشرف", "type": "text", "content": "تغطية مستمرة وحية للأوضاع الميدانية على مدار الساعة.", "time": "02:00 ص"}
        ]
    }

if "username" not in st.session_state:
    st.session_state.username = "Waseem"

# 4. بناء القائمة الجانبية (شريط المحادثات) مع شعار التليجرام الرئيسي
st.sidebar.markdown("""
<div style="display:flex; align-items:center; gap:10px; padding:10px;">
    <div style="width:35px; height:35px; background-image: url('https://wikimedia.org'); background-size:cover; border-radius:50%;"></div>
    <h2 style="margin:0; color:#5288c1; font-weight:bold; font-size:22px;">Telegram</h2>
</div>
""", unsafe_allow_html=True)

chat_keys = list(st.session_state.messages.keys())
selected_chat = st.sidebar.selectbox("اختر المحادثة النشطة:", chat_keys)
st.session_state.username = st.sidebar.text_input("⚙️ اسمك في المحادثة:", value=st.session_state.username)

# زر بسيط لتنظيف الشاشة إذا أردت البدء من جديد
if st.sidebar.button("🗑️ تنظيف وإعادة تهيئة المحادثة"):
    st.session_state.messages[selected_chat] = st.session_state.messages[selected_chat][:2]
    st.rerun()

# 5. عرض هيدر تليجرام مع الشعار الرسمي في الشاشة الرئيسية
st.markdown(f"""
<div class="tg-header-container">
    <div class="tg-logo-img"></div>
    <div>
        <h3 style="margin:0; color:white; font-size:16px;">{selected_chat}</h3>
        <span style="color:#5288c1; font-size:12px;">متصل الآن • تطبيق مخصص</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. ساحة عرض الرسائل والفقاعات بشكل آمن ونظيف
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages[selected_chat]:
    is_me = msg["sender"] == st.session_state.username
    bubble_class = "my-msg" if is_me else "other-msg"
    sender_title = "أنت" if is_me else msg["sender"]
    
    st.markdown(f"""
    <div class="message-bubble {bubble_class}">
        <div style="font-size:12px; font-weight:bold; color:#5288c1; margin-bottom:3px;">{sender_title}</div>
        <div>{msg['content']}</div>
        <div class="msg-info">{msg['time']} {'✓✓' if is_me else ''}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if msg["type"] == "image" and not isinstance(msg["content"], str):
        st.image(msg["content"], width=280)
st.markdown('</div>', unsafe_allow_html=True)

# 7. صندوق إرسال ومرفقات محكم الإغلاق وثابت بأسفل المتصفح لسهولة الاستخدام
st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
with st.form(key="telegram_secure_form", clear_on_submit=True):
    txt_col, file_col, btn_col = st.columns()
    
    with txt_col:
        user_text = st.text_input("الرسالة النصية", placeholder="اكتب رسالة...", label_visibility="collapsed")
    with file_col:
        uploaded_media = st.file_uploader("إرفاق ملف", type=["png", "jpg", "jpeg", "pdf"], label_visibility="collapsed")
    with btn_col:
        btn_trigger = st.form_submit_button("إرسال")

    if btn_trigger:
        time_stamp = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
        
        if user_text:
            st.session_state.messages[selected_chat].append({
                "sender": st.session_state.username,
                "type": "text",
                "content": user_text,
                "time": time_stamp
            })
            
        if uploaded_media is not None:
            media_kind = "image" if uploaded_media.type.startswith("image/") else "file"
            try:
                media_object = Image.open(uploaded_media) if media_kind == "image" else uploaded_media.name
                st.session_state.messages[selected_chat].append({
                    "sender": st.session_state.username,
                    "type": media_kind,
                    "content": media_object,
                    "time": time_stamp
                })
            except Exception as e:
                st.error(f"خطأ في المرفق: {e}")
                
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
