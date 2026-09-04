import streamlit as st
import datetime
import streamlit.components.v1 as components

# إعدادات الصفحة العامة لمنح التطبيق مظهراً احترافياً
st.set_page_config(
    page_title="Telegram Clone - وسيم المطور",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم (CSS) لتطابق ألوان ومظهر التلجرام الحقيقي
st.markdown("""
    <style>
    /* خلفية التطبيق العامة */
    .stApp {
        background-color: #0e1621;
        color: #ffffff;
    }
    /* تخصيص الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #17212b;
        border-right: 1px solid #101921;
    }
    /* فقاعات رسائل المستخدم (أزرق تلجرام) */
    .user-msg {
        background-color: #2b5278;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
        color: white;
    }
    /* فقاعات رسائل الطرف الآخر أو البوت */
    .other-msg {
        background-color: #182533;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        border: 1px solid #202b36;
        color: white;
    }
    /* نصوص الوقت والمسميات داخل غرف الدردشة */
    .msg-time {
        font-size: 0.8rem;
        color: #7f91a4;
        margin-top: 5px;
        text-align: right;
    }
    /* تصميم العناوين */
    .chat-header {
        background-color: #17212b;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 2px solid #24303f;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- كود منع خمول الهاتف وانطفاء الشاشة (Anti-Sleep JavaScript) -----------------
js_wake_lock = """
<script>
let wakeLock = null;

async function requestWakeLock() {
    try {
        if ('wakeLock' in navigator) {
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('Screen Wake Lock is active!');
        } else {
            console.log('Wake Lock API not supported in this browser.');
        }
    } catch (err) {
        console.error(`${err.name}, ${err.message}`);
    }
}

// تفعيل قفل السكون فور تحميل الصفحة
requestWakeLock();

// إعادة تفعيل القفل إذا قام المستخدم بتبديل التبويبات ثم عاد للتطبيق
document.addEventListener('visibilitychange', async () => {
    if (wakeLock !== null && document.visibilityState === 'visible') {
        requestWakeLock();
    }
});
</script>
"""
# دمج السكريبت في التطبيق ليعمل في الخلفية صامتاً
components.html(js_wake_lock, height=0, width=0)

# إدارة حالة التطبيق لحفظ الرسائل (Session State) لكي لا تختفي عند التحديث
if "messages" not in st.session_state:
    st.session_state.messages = {
        "القناة الإخبارية العاجلة 📢": [
            {"sender": "المشرف", "text": "أهلاً بكم في قناة الأخبار العاجلة لقطاع غزة.", "time": "09:00 ص"},
            {"sender": "المشرف", "text": "تحديث: تفعيل الرابط التعليمي الجديد لطلابنا بنجاح.", "time": "10:15 ص"}
        ],
        "مجموعة المطورين العرب 💻": [
            {"sender": "أحمد", "text": "السلام عليكم يا شباب، كيف برمجت واجهة التلجرام هذه؟", "time": "11:00 ص"},
            {"sender": "المطور وسيم", "text": "وعليكم السلام، برمجتها باستخدام Streamlit و Python بكل سهولة!", "time": "11:02 ص"}
        ],
        "دردشة الدعم الفني الخاص 🛠️": [
            {"sender": "الدعم", "text": "مرحباً وسيم، كيف يمكننا مساعدتك في مشروعك اليوم؟", "time": "07:30 ص"}
        ]
    }

# ----------------- الشريط الجانبي (Sidebar) -----------------
st.sidebar.markdown("<h2 style='color: #4ba3e3; text-align: center;'>Telegram</h2>", unsafe_allow_html=True)
st.sidebar.write(f"👤 **المطور:** وسيم نائل")
st.sidebar.markdown("---")

# لافتة تأكيد في الشريط الجانبي لتعرف أن النظام شغال
st.sidebar.success("⚡ وضع عدم السكون نشط: الشاشة ستبقى مضيئة دائماً.")
st.sidebar.markdown("---")

# أقسام التلجرام (القنوات والمجموعات)
st.sidebar.markdown("### 💬 القنوات والمجموعات")
chat_options = list(st.session_state.messages.keys())
selected_chat = st.sidebar.radio("اختر المحادثة أو القناة:", chat_options)

# ميزة إضافية بالشريط الجانبي: إنشاء قناة جديدة
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
# رأس المحادثة المستهدفة
st.markdown(f"""
    <div class="chat-header">
        <h3 style="margin:0; color:#4ba3e3;">{selected_chat}</h3>
        <p style="margin:5px 0 0 0; color:#7f91a4; font-size:14px;">تطبيق ويب متكامل ومطور يحاكي خصائص التلجرام الأصلي</p>
    </div>
""", unsafe_allow_html=True)

# عرض الرسائل المخزنة داخل القناة أو المجموعة المختارة
chat_placeholder = st.container()

with chat_placeholder:
    for msg in st.session_state.messages[selected_chat]:
        if msg["sender"] == "المطور وسيم" or msg["sender"] == "المشرف":
            st.markdown(f"""
                <div class="user-msg">
                    <strong>{msg["sender"]}</strong><br>
                    {msg["text"]}
                    <div class="msg-time">{msg["time"]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="other-msg">
                    <strong>{msg["sender"]}</strong><br>
                    {msg["text"]}
                    <div class="msg-time">{msg["time"]}</div>
                </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='clear:both; margin-bottom:40px;'></div>", unsafe_allow_html=True)

# صندوق إرسال الرسائل
st.markdown("---")
with st.form(key="send_message_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("اكتب رسالتك هنا...", placeholder="اكتب رسالة...")
    with col2:
        submit_button = st.form_submit_button(label="إرسال 🚀")

# معالجة إرسال الرسالة وإضافتها فوراً للقائمة
if submit_button and user_input:
    now = datetime.datetime.now().strftime("%I:%M %p")
    now_ar = now.replace("AM", "ص").replace("PM", "م")
    
    st.session_state.messages[selected_chat].append({
        "sender": "المطور وسيم",
        "text": user_input,
        "time": now_ar
    })
    st.rerun()
    
