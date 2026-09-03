import streamlit as st
import sqlite3
import os
import hashlib
from datetime import datetime

# --- إعدادات الواجهة الاحترافية الرسمية ---
st.set_page_config(page_title="تليجرام بريميوم الأصلي", page_icon="✈️", layout="centered")

# --- إدارة قاعدة البيانات الكلية ---
def init_db():
    conn = sqlite3.connect('telegram_premium_ultimate.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    phone TEXT PRIMARY KEY, username TEXT, password TEXT, 
                    bio TEXT, avatar TEXT, status TEXT, role TEXT, is_banned INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, phone TEXT, 
                    username TEXT, msg_type TEXT, content TEXT, timestamp TEXT, 
                    is_edited INTEGER DEFAULT 0, reply_to_text TEXT DEFAULT NULL,
                    is_pinned INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rooms (
                    name TEXT PRIMARY KEY, type TEXT, creator TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS reactions (
                    msg_id INTEGER, phone TEXT, emoji TEXT, PRIMARY KEY(msg_id, phone))''')
    c.execute('''CREATE TABLE IF NOT EXISTS polls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, question TEXT, option1 TEXT, option2 TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS poll_votes (
                    poll_id INTEGER, phone TEXT, option_num INTEGER, PRIMARY KEY(poll_id, phone))''')
    
    c.execute("SELECT * FROM users WHERE phone = 'admin'")
    if not c.fetchone():
        hashed_pass = hashlib.sha256(str.encode("admin123")).hexdigest()
        c.execute("INSERT INTO users VALUES ('admin', 'المشرف العام 👑', ?, 'إدارة منصة تليجرام بريميوم', '👑', 'offline', 'admin', 0)", (hashed_pass,))
        c.execute("INSERT INTO rooms VALUES ('📢 أخبار عاجلة دولية', 'قناة', 'admin')")
        c.execute("INSERT INTO rooms VALUES ('👥 ملتقى المطورين المحترفين', 'مجموعة', 'admin')")
    conn.commit()
    return conn

conn = init_db()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def trigger_bot_response(room, user_msg):
    msg_lower = user_msg.lower()
    bot_reply = ""
    if "مرحبا" in msg_lower or "سلام" in msg_lower:
        bot_reply = "🏆 أهلاً بك في تليجرام بريميوم الفاخر! أنا البوت الرسمي لخدمتك."
    elif "وقت" in msg_lower or "ساعة" in msg_lower:
        bot_reply = f"⏰ الوقت الحالي: {datetime.now().strftime('%I:%M %p')}"
    elif "تصويت" in msg_lower or "استطلاع" in msg_lower:
        bot_reply = "📊 يمكنك إنشاء استطلاع رأي من التبويب بالأسفل!"
    else:
        bot_reply = "🤖 رسالتك مستلمة ومحفوظة بأمان في السيرفر."

    c = conn.cursor()
    if bot_reply:
        t_now = datetime.now().strftime("%I:%M %p")
        c.execute("INSERT INTO messages (room, phone, username, msg_type, content, timestamp) VALUES (?, 'bot', 'Telegram_Bot 🤖', 'text', ?, ?)",
                  (room, bot_reply, t_now))
        conn.commit()

# --- واجهات التسجيل والدخول الآمن ---
if 'user_phone' not in st.session_state:
    st.title("✈️ تليجرام ويب - النسخة المستقرة الرسمية")
    
    tab1, tab2 = st.tabs(["🔑 تسجيل الدخول الرسمي", "📝 فتح حساب بريميوم"])
    
    with tab1:
        login_phone = st.text_input("رقم الهاتف الذكي", placeholder="مثال: 0598338642 أو admin")
        login_pass = st.text_input("كلمة السر الخاصة بالحساب", type="password")
        if st.button("تسجيل الدخول والربط", use_container_width=True):
            c = conn.cursor()
            c.execute("SELECT password, username, role, is_banned FROM users WHERE phone = ?", (login_phone,))
            res = c.fetchone()
            if res:
                if res[3] == 1:
                    st.error("❌ تم حظر هذا الحساب!")
                elif check_hashes(login_pass, res[0]):
                    st.session_state.user_phone = login_phone
                    st.session_state.user_role = res[2]
                    st.session_state.username = res[1]
                    c.execute("UPDATE users SET status = 'online' WHERE phone = ?", (login_phone,))
                    conn.commit()
                    st.rerun()
                else:
                    st.error("⚠️ كلمة المرور المدخلة غير صحيحة.")
            else:
                st.error("⚠️ رقم الهاتف غير مسجل.")
                
    with tab2:
        reg_phone = st.text_input("تعيين رقم الهاتف الجديد")
        reg_user = st.text_input("اسم العرض في المحادثات")
        reg_pass = st.text_input("أدخل كلمة مرور قوية الحساب", type="password")
        if st.button("تفعيل الحساب فوراً", use_container_width=True):
            if reg_phone.strip() and reg_user.strip() and reg_pass.strip():
                try:
                    c = conn.cursor()
                    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, 0)", 
                              (reg_phone, reg_user, make_hashes(reg_pass), "أستخدم تليجرام بريميوم!", "👤", "offline", "user"))
                    conn.commit()
                    st.success("🎉 تم إنشاء الحساب بنجاح! توجه إلى تبويب تسجيل الدخول الآن.")
                except sqlite3.IntegrityError:
                    st.error("رقم الهاتف مسجل بالفعل.")

else:
    user_phone = st.session_state.user_phone
    user_role = st.session_state.user_role
    
    if 'reply_msg' not in st.session_state:
        st.session_state.reply_msg = None

    c = conn.cursor()

    with st.sidebar:
        st.write(f"<h3>👤 {st.session_state.username}</h3>", unsafe_allow_html=True)
        st.caption(f"📱 {user_phone} | رتبة: {user_role.upper()}")
        
        st.markdown("---")
        global_search = st.text_input("🔍 بحث عن غرف وقنوات:", placeholder="اكتب اسم الغرفة...")
        
        with st.expander("➕ إنشاء مجموعة أو قناة"):
            r_name = st.text_input("اسم الوجهة الجديدة:")
            r_type = st.radio("نوع الوجهة الحصري:", ["مجموعة عامة", "قناة بث"])
            if st.button("تأكيد الإنشاء"):
                if r_name.strip():
                    try:
                        final_type = "قناة" if "قناة" in r_type else "مجموعة"
                        c.execute("INSERT INTO rooms VALUES (?, ?, ?)", (r_name.strip(), final_type, user_phone))
                        conn.commit()
                        st.success("تم الإنشاء!")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("الاسم مستخدم مسبقاً.")

        st.markdown("---")
        st.subheader("💬 قائمة المحادثات")
        c.execute("SELECT name, type FROM rooms")
        all_rooms_db = c.fetchall()
        if global_search:
            all_rooms_db = [r for r in all_rooms_db if global_search.lower() in r[0].lower()]
            
        if all_rooms_db:
            room_names = [r[0] for r in all_rooms_db]
            current_room = st.radio("اختر المحادثة:", room_names, label_visibility="collapsed")
            is_news_channel = next((r[1] == "قناة" for r in all_rooms_db if r[0] == current_room), False)
        else:
            current_room = "📢 أخبار عاجلة دولية"
            is_news_channel = True

        st.markdown("---")
        if st.button("🔄 تحديث الشات الفوري", use_container_width=True):
            st.rerun()

        if st.button("🚪 تسجيل الخروج الفوري", use_container_width=True):
            c.execute("UPDATE users SET status = 'offline' WHERE phone = ?", (user_phone,))
            conn.commit()
            del st.session_state.user_phone
            del st.session_state.user_role
            st.rerun()

    st.title(f"📍 {current_room}")
    
    # عرض الرسائل المثبتة 
    c.execute("SELECT username, content FROM messages WHERE room = ? AND is_pinned = 1 ORDER BY id DESC LIMIT 1", (current_room,))
    pinned = c.fetchone()
    if pinned:
        st.markdown(f"<div style='background-color: #E0F7FA; padding: 10px; border-radius: 8px; border-right: 5px solid #00acc1; margin-bottom: 10px;'>📌 <b>مثبتة بقلم {pinned[0]}:</b> {pinned[1]}</div>", unsafe_allow_html=True)

    # نافذة عرض أرشيف الشات
    chat_container = st.container(height=400, border=True)
    with chat_container:
        c.execute("""SELECT m.id, m.username, m.msg_type, m.content, m.timestamp, m.phone, m.is_edited, m.reply_to_text 
                     FROM messages m WHERE m.room = ? ORDER BY m.id ASC""", (current_room,))
        messages = c.fetchall()
        
        for msg_id, msg_user, msg_type, content, time_str, msg_owner_phone, is_edited, reply_text in messages:
            is_me = (msg_owner_phone == user_phone)
            align = "right" if is_me else "left"
            bg_color = "#E8F5E9" if is_me else "#F5F5F5"
            
            st.markdown(f"""
            <div style='text-align: {align}; margin-bottom: 12px;'>
                <div style='background-color: {bg_color}; display: inline-block; padding: 12px; border-radius: 14px; max-width: 85%; text-align: right; box-shadow: 1px 1px 3px rgba(0,0,0,0.04);'>
                    <b style='color: #0088cc;'>👤 {msg_user}</b> <small style='color: gray; float: left; margin-right: 15px;'>{time_str}</small>
            """, unsafe_allow_html=True)
            
            if reply_text:
                st.markdown(f"<div style='background: rgba(0,0,0,0.04); padding: 5px; margin: 4px 0; border-right: 3px solid #999; font-size: 13px;'>↪️ {reply_text}</div>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: 5px; color: black;'>", unsafe_allow_html=True)
            if msg_type == "text":
                st.write(content)
            elif msg_type == "sticker":
                st.markdown(f"<p style='font-size:50px; margin:0;'>{content}</p>", unsafe_allow_html=True)
            elif msg_type == "image":
    
