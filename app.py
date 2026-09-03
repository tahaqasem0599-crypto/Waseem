import streamlit as st
import sqlite3
import os
import hashlib
import time
import datetime
from datetime import datetime

# --- إعدادات الواجهة الاحترافية الرسمية وتصميم الهواتف ---
st.set_page_config(page_title="تليجرام بريميوم الأصلي", page_icon="✈️", layout="centered")

# هندسة وتصميم واجهة تليجرام الأصلي بالكامل عبر CSS
st.markdown("""
<style>
    /* إلغاء الفراغات العلوية الافتراضية لتبدو كشاشة هاتف */
    .block-container { padding-top: 0rem; padding-bottom: 1rem; }
    
    /* خلفية تليجرام الرسمية */
    .stApp {
        background-color: #E7EBF0;
        background-image: url('https://githubusercontent.com');
        background-attachment: fixed;
        background-size: cover;
    }
    
    /* تنسيق أزرار التنقل والقوائم */
    .stButton>button {
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- إدارة قاعدة البيانات الكلية ---
def init_db():
    conn = sqlite3.connect('telegram_premium_ultimate.db', check_same_thread=False)
    c = conn.cursor()
    # 1. جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    phone TEXT PRIMARY KEY, username TEXT, password TEXT, 
                    bio TEXT, avatar TEXT, status TEXT, role TEXT, is_banned INTEGER DEFAULT 0)''')
    # 2. جدول الرسائل (مع دعم الرد، التثبيت والتدمير الذاتي)
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, phone TEXT, 
                    username TEXT, msg_type TEXT, content TEXT, timestamp TEXT, 
                    is_edited INTEGER DEFAULT 0, reply_to_text TEXT DEFAULT NULL,
                    is_pinned INTEGER DEFAULT 0, burn_after INTEGER DEFAULT 0, created_at REAL)''')
    # 3. جدول الغرف والقنوات
    c.execute('''CREATE TABLE IF NOT EXISTS rooms (
                    name TEXT PRIMARY KEY, type TEXT, creator TEXT, pinned_msg_text TEXT DEFAULT NULL)''')
    # 4. جدول التفاعلات
    c.execute('''CREATE TABLE IF NOT EXISTS reactions (
                    msg_id INTEGER, phone TEXT, emoji TEXT, PRIMARY KEY(msg_id, phone))''')
    # 5. جدول الاستطلاعات (Polls)
    c.execute('''CREATE TABLE IF NOT EXISTS polls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, question TEXT, option1 TEXT, option2 TEXT)''')
    # 6. جدول أصوات الاستطلاعات
    c.execute('''CREATE TABLE IF NOT EXISTS poll_votes (
                    poll_id INTEGER, phone TEXT, option_num INTEGER, PRIMARY KEY(poll_id, phone))''')
    
    # حساب المشرف والغرف الافتراضية
    c.execute("SELECT * FROM users WHERE phone = 'admin'")
    if not c.fetchone():
        hashed_pass = hashlib.sha256(str.encode("admin123")).hexdigest()
        c.execute("INSERT INTO users VALUES ('admin', 'المشرف العام 👑', ?, 'إدارة منصة تليجرام بريميوم', '👑', 'offline', 'admin', 0)", (hashed_pass,))
        c.execute("INSERT INTO rooms VALUES ('📢 أخبار عاجلة دولية', 'قناة', 'admin', NULL)")
        c.execute("INSERT INTO rooms VALUES ('👥 ملتقى المطورين المحترفين', 'مجموعة', 'admin', NULL)")
    conn.commit()
    return conn

conn = init_db()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# --- معالجة وتنظيف الرسائل ذاتية التدمير ---
def clean_burned_messages(room):
    c = conn.cursor()
    now_ts = time.time()
    c.execute("SELECT id FROM messages WHERE room = ? AND burn_after > 0 AND (? - created_at) > burn_after", (room, now_ts))
    expired = c.fetchall()
    for (m_id,) in expired:
        c.execute("DELETE FROM messages WHERE id = ?", (m_id,))
        c.execute("DELETE FROM reactions WHERE msg_id = ?", (m_id,))
    conn.commit()

# --- بوت الرد التلقائي للمحاكاة ---
def trigger_bot_response(room, user_msg):
    msg_lower = user_msg.lower()
    bot_reply = ""
    if "مرحبا" in msg_lower or "سلام" in msg_lower:
        bot_reply = "🏆 أهلاً بك في تليجرام بريميوم الفاخر! أنا البوت الرسمي لخدمتك."
    elif "وقت" in msg_lower or "ساعة" in msg_lower:
        bot_reply = f"⏰ الوقت والنبض الحالي: {datetime.now().strftime('%I:%M %p')}"
    elif "تصويت" in msg_lower or "استطلاع" in msg_lower:
        bot_reply = "📊 يمكنك الآن إنشاء استطلاعات رأي حقيقية باستخدام اللوحة المخصصة بالأسفل!"
    else:
        bot_reply = "🤖 رسالتك مشفرة ومستلمة بأمان في خوادم السيرفر الفوري للبرنامج."

    if bot_reply:
        t_now = datetime.now().strftime("%I:%M %p")
        c = conn.cursor()
        c.execute("INSERT INTO messages (room, phone, username, msg_type, content, timestamp, created_at) VALUES (?, 'bot', 'Telegram_Bot 🤖', 'text', ?, ?, ?)",
                  (room, bot_reply, t_now, time.time()))
        conn.commit()

# --- واجهات التسجيل والدخول الآمن ---
if 'user_phone' not in st.session_state:
    st.title("✈️ تليجرام ويب - النسخة الاحترافية الرسمية")
    st.markdown("<p style='color:gray;'>مرحباً بك في نظام محاكاة تليجرام بريميوم المتكامل</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول الرسمي", "📝 فتح حساب بريميوم"])
    
    with tab1:
        login_phone = st.text_input("رقم الهاتف الذكي", placeholder="مثال: admin أو 0590000")
        login_pass = st.text_input("كلمة السر الخاصة بالحساب", type="password")
        if st.button("تسجيل الدخول والربط", use_container_width=True):
            c = conn.cursor()
            c.execute("SELECT password, username, role, is_banned FROM users WHERE phone = ?", (login_phone,))
            res = c.fetchone()
            if res:
                if res[3] == 1:
                    st.error("❌ تم حظر هذا الحساب من قبل الإدارة لمخالفة شروط الاستخدام!")
                elif check_hashes(login_pass, res[0]):
                    st.session_state.user_phone = login_phone
                    st.session_state.user_role = res[2]
                    st.session_state.muted_rooms = set()
                    c.execute("UPDATE users SET status = 'online' WHERE phone = ?", (login_phone,))
                    conn.commit()
                    st.rerun()
                else:
                    st.error("⚠️ كلمة المرور المدخلة غير صحيحة.")
            else:
                st.error("⚠️ رقم الهاتف غير مسجل في قاعدة البيانات.")
                
    with tab2:
        reg_phone = st.text_input("تعيين رقم الهاتف")
        reg_user = st.text_input("اسم العرض في المحادثات")
        reg_pass = st.text_input("أدخل كلمة مرور قوية", type="password")
        if st.button("تفعيل الحساب فوراً", use_container_width=True):
            if reg_phone.strip() and reg_user.strip() and reg_pass.strip():
                try:
                    c = conn.cursor()
                    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, 0)", 
                              (reg_phone, reg_user, make_hashes(reg_pass), "أستخدم تليجرام بريميوم الرسمي مبرمج باحتراف!", "👤", "offline", "user"))
                    conn.commit()
                    st.success("🎉 رائع جداً! تم إنشاء الحساب بنجاح، توجه إلى تبويب تسجيل الدخول الآن.")
                except sqlite3.IntegrityError:
                    st.error("رقم الهاتف مسجل ومستخدم بالفعل.")

else:
    # --- إعدادات الحساب النشط ---
    user_phone = st.session_state.user_phone
    user_role = st.session_state.user_role
    
    c = conn.cursor()
    c.execute("SELECT username, bio, avatar FROM users WHERE phone = ?", (user_phone,))
    u_info = c.fetchone()
    st.session_state.username = u_info[0]
    
    if 'reply_msg' not in st.session_state:
        st.session_state.reply_msg = None

    # الشريحة الجانبية للتحكم الكلي (Sidebar)
    with st.sidebar:
        st.write(f"<h3>{u_info[2]} {u_info[0]}</h3>", unsafe_allow_html=True)
        st.caption(f"📱 {user_phone} | رتبة الحساب: {user_role.upper()}")
        
        # 1. محرك البحث الشامل (Global Search)
        st.markdown("---")
        global_search = st.text_input("🔍 بحث شامل عن غرف وقنوات:", placeholder="اكتب اسم الغرفة...")
        
        # 2. إنشاء المجموعات والقنوات ديناميكياً
        with st.expander("➕ إنشاء مجموعة أو قناة"):
            r_name = st.text_input("اسم الوجهة الجديدة:")
            r_type = st.radio("نوع الوجهة الحصري:", ["مجموعة عامة", "قناة بث"])
            if st.button("تأكيد الإنشاء"):
                if r_name.strip():
                    try:
                        final_type = "قناة" if "قناة" in r_type else "مجموعة"
                        c.execute("INSERT INTO rooms VALUES (?, ?, ?, NULL)", (r_name.strip(), final_type, user_phone))
                        conn.commit()
                        st.success("تم الإنشاء بنجاح!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("الاسم مستخدم مسبقاً.")

        # جلب وتصفية الغرف حسب البحث الشامل
        st.markdown("---")
        st.subheader("💬 قائمة المحادثات")
        c.execute("SELECT name, type FROM rooms")
        all_rooms_db = c.fetchall()
        if global_search:
            all_rooms_db = [r for r in all_rooms_db if global_search.lower() in r[0].lower()]
            
        if all_rooms_db:
            room_names = [r[0] for r in all_rooms_db]
            current_room = st.radio("اختر المحادثة المستهدفة:", room_names, label_visibility="collapsed")
            is_news_channel = [r[1] for r in all_rooms_db if r[0] == current_room][0] == "قناة"
        else:
            st.write("_لا توجد غرف مطابقة لبحثك_")
            current_room = "📢 أخبار عاجلة دولية"
            is_news_channel = True

        # 3. لوحة إدارة الآدمن للحظر والفك
        if user_role == "admin":
            st.markdown("---")
            with st.expander("🛡️ إدارة الأعضاء والحظر"):
                ban_target = st.text_input("رقم الهاتف المراد حظره:")
                if st.button("🚫 حظر فوري للمستخدم", use_container_width=True):
