import streamlit as st
import datetime
import requests
import streamlit.components.v1 as components
from PIL import Image

# 1. إعدادات الصفحة العامة بالاسم الجديد للتطبيق
st.set_page_config(
    page_title="تلجرام غزة - Telegram Gaza",
    page_icon="📢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تخصيص واجهة المستخدم (CSS) لدعم المظهر الجديد، الألوان، والاتجاه العربي
st.markdown("""
    <style>
    /* دعم الكتابة من اليمين إلى اليسار بالتطبيق كامل */
    .stApp {
        background-color: #0e1621;
        color: #ffffff;
        direction: rtl;
        text-align: right;
    }
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #17212b;
        border-left: 1px solid #101921;
        border-right: none;
        direction: rtl;
    }
    /* تصميم شعار التطبيق الاحترافي */
    .app-logo {
        background: linear-gradient(135deg, #2488cb 0%, #00b4d8 100%);
        width: 70px;
        height: 70px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px auto;
        box-shadow: 0px 4px 15px rgba(0, 180, 216, 0.4);
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 32px;
        color: white;
        position: relative;
    }
    .app-logo::after {
        content: '✈';
        font-size: 16px;
        position: absolute;
        bottom: 8px;
        right: 8px;
        transform: rotate(-45deg);
        color: #e0f2fe;
    }
    /* فقاعات رسائل المستخدم */
    .user-msg {
        background-color: #2b5278;
        padding: 12px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
        color: white;
        direction: rtl;
        text-align: right;
    }
    /* فقاعات رسائل الأعضاء الآخرين */
    .other-msg {
        background-color: #182533;
        padding: 12px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
        border: 1px solid #202b36;
        color: white;
        direction: rtl;
        text-align: right;
    }
    /* وقت إرسال الرسائل */
    .msg-time {
        font-size: 0.75rem;
        color: #7f91a4;
        margin-top: 5px;
        text-align: left;
    }
    /* تصميم رأس المحادثة */
    .chat-header {
        background-color: #17212b;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 2px solid #24303f;
        margin-bottom: 20px;
        direction: rtl;
    }
    </style>
""", unsafe_allow_html=True)

# 3. سكريبت منع خمول وانطفاء الشاشة في الخلفية تلقائياً
js_wake_lock = """
<script>
let wakeLock = null;
async function requestWakeLock() {
    try {
        if ('wakeLock' in navigator) {
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('Screen Wake Lock is active!');
        }
    } catch (err) {
        console.error(`${err.name}, ${err.message}`);
    }
}
requestWakeLock();
document.addEventListener('visibilitychange', async () => {
    if (wakeLock !== null && document.visibilityState === 'visible') {
        requestWakeLock();
    }
});
</script>
"""
components.html(js_wake_lock, height=0, width=0)

# 4. دالة مخصصة لإرسال الرسائل إلى خوادم التلجرام الحقيقي عبر الـ API
def send_to_telegram_bot(token, chat_id, text):
    if token and chat_id:
        url = f"https://telegram.org{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            pass

# 5. إدارة جلسة البيانات وحفظ الرسائل داخلياً
if "messages" not in st.session_state:
    st.session_state.messages = {
        "القناة الإخبارية العاجلة 📢": [
            {"sender": "المشرف", "type": "text", "content": "أهلاً بكم في قناة الأخبار العاجلة لقطاع غزة.", "time": "09:00 ص"},
            {"sender": "المشرف", "type": "text", "content": "تحديث: تفعيل الرابط التعليمي الجديد لطلابنا بنجاح.", "time": "10:15 ص"}
        ],
        "مجموعة المطورين العرب 💻": [
            {"sender": "أحمد", "type": "text", "content": "السلام عليكم يا شباب، كيف برمجت واجهة التلجرام هذه؟", "time": "11:00 ص"},
            {"sender": "المطور وسيم", "type": "text", "content": "وعليكم السلام، برمجتها باستخدام Streamlit و Python بكل سهولة!", "time": "11:02 ص"}
        ]
    }

# 6. شاشة تسجيل الدخول وإنشاء الحساب
if "username" not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #4ba3e3;'>🌐 بوابة دخول تلجرام غزة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7f91a4;'>مرحباً بك في النسخة المطورة والمخصصة لقطاع غزة</p>", unsafe_allow_html=True)
    st.write("يرجى إدخال بياناتك لإنشاء حسابك والدخول:")
    
    username_input = st.text_input("👤 اسم المستخدم:", value="المطور وسيم")
    avatar_option = st.selectbox("🖼️ اختر نوع الحساب والرمز الشخصي:", ["💻 مطور برمجيات", "🚀 رائد أعمال", "🛡️ مشرف أمان", "👤 مستخدم عام"])
    
    if st.button("تسجيل الدخول والبدء فورا 🚀"):
        if username_input.strip() != "":
            st.session_state.username = username_input.strip()
            st.session_state.avatar = avatar_option
            st.rerun()
        else:
            st.error("الرجاء إدخال اسم مستخدم صالح!")
    st.stop()

# ----------------- الشريط الجانبي (Sidebar) -----------------
# عرض الشعار الجديد واسم التطبيق بالتصميم الأنيق
st.sidebar.markdown("""
    <div class="app-logo">G</div>
    <h2 style='color: #4ba3e3; text-align: center; margin-top:0; font-size:22px;'>تلجرام غزة</h2>
    <p style='color: #7f91a4; text-align: center; font-size:12px; margin-top:-10px;'>Telegram Gaza Edition</p>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **المستكشف الحالي:** {st.session_state.username} ({st.session_state.avatar})")
st.sidebar.success("⚡ وضع عدم السكون نشط: الشاشة ستبقى مضيئة.")
st.sidebar.markdown("---")

# ربط تطبيقك ببوت تلجرام حقيقي
st.sidebar.markdown("### 🤖 ربط API للبوت الحقيقي")
with st.sidebar.expander("⚙️ إعدادات ربط البوت"):
    bot_token = st.sidebar.text_input("Bot Token:", type="password", help="ضع توكن البوت الذي حصلت عليه من BotFather")
    telegram_chat_id = st.sidebar.text_input("Chat ID / القناة:", help="مثال: @my_channel أو الآي دي الرقمي")
    st.sidebar.caption("عند تفعيل هذا القسم، أي رسالة ترسلها هنا ستنتقل مباشرة إلى قناتك أو مجموعتك على التلجرام الحقيقي!")

st.sidebar.markdown("---")

# قائمة القنوات والمجموعات
st.sidebar.markdown("### 💬 القنوات والمجموعات")
chat_options = list(st.session_state.messages.keys())
selected_chat = st.sidebar.radio("اختر المحادثة أو القناة:", chat_options)

# إنشاء أقسام جديدة
st.sidebar.markdown("---")
st.sidebar.markdown("### ➕ إنشاء قسم جديد")
new_chat_name = st.sidebar.text_input("اسم القناة/المجموعة الجديدة:")
chat_type = st.sidebar.selectbox("النوع:", ["قناة عامة 📢", "مجموعة دردشة 👥"])

if st.sidebar.button("إنشاء الآن"):
    if new_chat_name:
        full_name = f"{new_chat_name} {chat_type}"
        if full_name not in st.session_state.messages:
            st.session_state.messages[full_name] = []
            st.sidebar.success(f"تم إنشاء {full_name} بنجاح!")
            st.rerun()
    else:
        st.sidebar.error("الرجاء إدخال اسم!")

# ----------------- نافذة الدردشة الرئيسية -----------------
st.markdown(f"""
    <div class="chat-header">
        <h3 style="margin:0; color:#4ba3e3;">{selected_chat}</h3>
        <p style="margin:5px 0 0 0; color:#7f91a4; font-size:14px;">نسخة تواصل متكاملة ومحسنة تدعم المراسلة الفورية والوسائط المتعددة</p>
    </div>
""", unsafe_allow_html=True)

chat_placeholder = st.container()
with chat_placeholder:
    for msg in st.session_state.messages[selected_chat]:
        alignment_class = "user-msg" if msg["sender"] == st.session_state.username else "other-msg"
        
        st.markdown(f"""
            <div class="{alignment_class}">
                <strong>{msg["sender"]}</strong><br>
        """, unsafe_allow_html=True)
        
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"], width=250)
        elif msg["type"] == "file":
            st.info(f"📁 ملف مرفق: {msg['content']}")
            
        st.markdown(f"""
                <div class="msg-time">{msg["time"]}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='clear:both; margin-bottom:40px;'></div>", unsafe_allow_html=True)

# ----------------- صندوق إرسال الرسائل والمرفقات -----------------
st.markdown("---")

with st.form(key="send_message_form", clear_on_submit=True):
    col1, col2 = st.columns()
    with col1:
        user_input = st.text_input("اكتب رسالتك هنا...", placeholder="اكتب رسالة...", label_visibility="collapsed")
    with col2:
        submit_button = st.form_submit_button(label="إرسال 🚀")

uploaded_file = st.file_uploader("📎 إرفاق ملف أو صورة إلى الدردشة الحالية:", type=["png", "jpg", "jpeg", "pdf", "txt", "zip"])

if submit_button and user_input:
    now = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    
    st.session_state.messages[selected_chat].append({
        "sender": st.session_state.username,
        "type": "text",
        "content": user_input,
        "time": now
    })
    
    if bot_token and telegram_chat_id:
        full_tele_text = f"👤 {st.session_state.username} ({selected_chat}):\n{user_input}"
        send_to_telegram_bot(bot_token, telegram_chat_id, full_tele_text)
        
    st.rerun()

if uploaded_file is not None:
    now = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
    file_type = "image" if uploaded_file.type.startswith("image") else "file"
    content_data = Image.open(uploaded_file) if file_type == "image" else uploaded_file.name
    
    st.session_state.messages[selected_chat].append({
