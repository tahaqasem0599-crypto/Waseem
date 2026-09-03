import streamlit as st
import sqlite3
from datetime import datetime

# إعداد الصفحة لتكون مريحة للعين وتماثل التطبيقات
st.set_page_config(page_title="تليجرام ويب الأصلي", page_icon="✈️", layout="centered")

# --- تحسين التصميم بالكامل عبر CSS لمحاكاة تليجرام ---
st.markdown("""
<style>
    /* تغيير خلفية التطبيق بالكامل إلى لون رمادي تليجرام الخفيف */
    .stApp {
        background-color: #e7ebf0;
    }
    /* تصميم حاوية الدردشة بخلفية تليجرام الشهيرة */
    .chat-container {
        background-color: #f4f4f5;
        background-image: url('https://transparenttextures.com');
        padding: 15px;
        border-radius: 12px;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    /* فقاعة رسائل المستخدم الحالي (أنت) - باللون الأخضر/الأزرق التليجرامي محاذاة لليمين */
    .message-me {
        background-color: #effdde;
        color: #000000;
        padding: 10px 14px;
        border-radius: 15px 15px 0px 15px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        width: fit-content;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.15);
        text-align: right;
    }
    /* فقاعة رسائل الآخرين - باللون الأبيض محاذاة لليسار */
    .message-other {
        background-color: #ffffff;
        color: #000000;
        padding: 10px 14px;
        border-radius: 15px 15px 15px 0px;
        margin: 8px auto 8px 0;
        max-width: 75%;
        width: fit-content;
        box-shadow: 0px 1px 2px rgba(0,0,0,0.15);
        text-align: right;
    }
    .user-name {
        color: #388e3c;
        font-weight: bold;
        font-size: 13px;
        margin-bottom: 2px;
    }
    .time-stamp {
        color: #707579;
        font-size: 10px;
        display: block;
        text-align: left;
        margin-top: 4px;
    }
    /* تخصيص الأزرار لتصبح دائرية وأنيقة */
    .stButton>button {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('tg_premium_v2.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS msgs (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, content TEXT, ts TEXT)')
    conn.commit()
    return conn

conn = init_db()

# --- إدارة جلسة المستخدم ---
if 'user' not in st.session_state:
    st.markdown("<h1 style='text-align: center; color: #2481cc;'>✈️ Telegram</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>مرحباً بك في تليجرام ويب المطور. سجل اسمك لبدء المحادثة الفورية.</p>", unsafe_allow_html=True)
    
    with st.container(border=True):
        name = st.text_input("اسم العرض (اللقب):", placeholder="مثال: أبو مالك العطار")
        if st.button("📌 دخول آمن للمنصة", use_container_width=True):
            if name.strip():
                st.session_state.user = name.strip()
                st.rerun()
else:
    # شريط علوي أنيق يحمل هوية تليجرام الزرقاء
    st.markdown(f"""
    <div style='background-color: #2481cc; padding: 12px; border-radius: 10px; color: white; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;'>
        <b style='font-size: 18px;'>✈️ تليجرام بلس المشترك</b>
        <span>👤 {st.session_state.user}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # القائمة الجانبية للتحكم
    with st.sidebar:
        st.subheader("⚙️ خيارات الحساب")
        if st.button("🚪 تسجيل الخروج من التطبيق", use_container_width=True):
            del st.session_state.user
            st.rerun()
        st.markdown("---")
        st.caption("مطور باحترافية لمحاكاة واجهة تليجرام الأصلية.")

    # صندوق الشات المخصص بالتصميم الجديد
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    chat_box = st.container(height=350, border=False)
    
    with chat_box:
        c = conn.cursor()
        c.execute('SELECT user, content, ts FROM msgs ORDER BY id ASC')
        records = c.fetchall()
        
        if not records:
            st.markdown("<p style='text-align:center; color:gray; font-style:italic;'>لا توجد رسائل بعد... ابدأ ببث رسالتك الأولى الآن! 🚀</p>", unsafe_allow_html=True)
            
        for usr, txt, t in records:
            if usr == st.session_state.user:
                # رسالتي أنا
                st.markdown(f"""
                <div class='message-me'>
                    <div>{txt}</div>
                    <span class='time-stamp'>{t} ✔️</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                # رسائل الأعضاء الآخرين
                st.markdown(f"""
                <div class='message-other'>
                    <div class='user-name'>@{usr}</div>
                    <div>{txt}</div>
                    <span class='time-stamp'>{t}</span>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # نموذج إرسال الرسائل الفوري
    with st.form("send_msg_form", clear_on_submit=True):
        col_input, col_btn = st.columns([4, 1])
        with col_input:
            msg = st.text_input("اكتب رسالة...", placeholder="اكتب رسالتك هنا...", label_visibility="collapsed")
        with col_btn:
            submit = st.form_submit_button("🚀 إرسال", use_container_width=True)
            
        if submit and msg.strip():
            t_now = datetime.now().strftime("%I:%M %p")
            c = conn.cursor()
            c.execute('INSERT INTO msgs (user, content, ts) VALUES (?, ?, ?)', (st.session_state.user, msg.strip(), t_now))
            conn.commit()
            st.rerun()
            
    # زر تحديث يدوي سريع وسلس بجانب الشات
    if st.button("🔄 تحديث غرف الدردشة", use_container_width=True):
        st.rerun()
