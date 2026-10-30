import os
import time
import sqlite3
import threading
import streamlit as st
from openai import OpenAI
from datetime import datetime

# ==================== 1. إعدادات واجهة المنصة الفاخرة ====================
st.set_page_config(page_title="نظام الأتمتة الشامل - وسيم العطار", page_icon="💰", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 38px; color: #D4AF37; text-align: center; font-weight: bold; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .sub-title { font-size: 16px; color: #A0A0A0; text-align: center; margin-bottom: 30px; }
    .status-box { background-color: #111111; border-right: 6px solid #D4AF37; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .article-box { background-color: #1a1a1a; border: 1px solid #D4AF37; padding: 25px; border-radius: 10px; margin-top: 20px; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 25px; font-weight: bold; height: 50px; background-color: #D4AF37; color: black; }
    .stButton>button:hover { background-color: #FFF; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💰 ماكينة الأتمتة وضخ المحتوى الرقمي المطور العالـمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">المطور والمالك المسؤول: وسيم نائل العطار | الحساب المعتمد: tahaqasem0599-crypto</div>', unsafe_allow_html=True)

# ==================== 2. إدارة قاعدة البيانات الدائمة ====================
def init_db():
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS topics (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (key TEXT PRIMARY KEY, value TEXT)''')
    high_cpc_topics = [
        "How to build a fully automated online business in 2026",
        "Top AI applications transforming digital marketing and sales",
        "Unlocking passive income through AI automation workflows"
    ]
    for t in high_cpc_topics:
        try: cursor.execute("INSERT INTO topics (topic) VALUES (?)", (t,))
        except: pass
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_published', '0')")
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('last_topic', 'لم يتم البدء بعد')")
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('last_content', 'المحتوى الجاهز للنسخ سيظهر هنا عند توليده...')")
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('is_running', '0')")
    conn.commit()
    conn.close()

init_db()

def db_get_topics():
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    cursor.execute("SELECT topic FROM topics")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def db_add_topic(topic):
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO topics (topic) VALUES (?)", (topic,))
        conn.commit()
        success = True
    except:
        success = False
    conn.close()
    return success

def db_delete_topic(topic):
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM topics WHERE topic = ?", (topic,))
    conn.commit()
    conn.close()

def db_get_stat(key, default=""):
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM stats WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def db_set_stat(key, value):
    conn = sqlite3.connect('global_profit_engine.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO stats (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

# ==================== 3. إعداد عميل OpenAI بأمان ====================
if "OPENAI_API_KEY" in st.secrets:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
else:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    st.error("❌ يرجى التأكد من إضافة مفتاح OPENAI_API_KEY في الـ Secrets!")
else:
    client = OpenAI(api_key=OPENAI_API_KEY)

# ==================== 4. محرك التوليد الفوري للمقالات ====================
def auto_generate_new_topics():
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Generate 5 high-CPC blog titles in English about AI and finance. Return only titles separated by newlines."}]
        )
        for title in response.choices.message.content.strip().split('\n'):
            if title.strip(): db_add_topic(title.strip())
    except: pass

def generate_seo_article(topic):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Write a professional SEO-optimized blog post in English about: '{topic}'. Include headings, clear paragraphs, and key takeaways. Output clean readable text."}]
        )
        return response.choices.message.content
    except: return None

def background_worker():
    current_index = 0
    while db_get_stat("is_running") == "1":
        topics = db_get_topics()
        if len(topics) <= 2:
            auto_generate_new_topics()
            topics = db_get_topics()
        if not topics:
            time.sleep(5)
            continue
        
        topic = topics[current_index % len(topics)]
        db_set_stat("last_topic", topic)
        
        content = generate_seo_article(topic)
        if content:
            db_set_stat("last_content", content)
            current_total = int(db_get_stat("total_published", "0"))
            db_set_stat("total_published", current_total + 1)
            db_delete_topic(topic)  # حذف الموضوع بعد توليده لكي لا يتكرر
            
        db_set_stat("is_running", "0")  # التوقف بعد توليد المقال لينسخه وسيم يدوياً
        break

# ==================== 5. لوحة التحكم والإحصائيات الفورية ====================
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.subheader("📊 العدادات الذكية والمقالات الجاهزة")
    published_count = int(db_get_stat("total_published", "0"))
    st.metric(label="إجمالي المقالات الجاهزة للنسخ"، value=published_count)
    st.write(f"**الموضوع المستهدف الحالي:** {db_get_stat('last_topic')}")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.subheader("📡 حالة الماكينة")
    is_running_state = db_get_stat("is_running") == "1"
    if is_running_state: st.success("● جاري توليد المقال القادم بذكاء فائق... انتظر ثواني ثم حدث الشاشة")
    else: st.warning("○ الماكينة جاهزة. اضغط تشغيل لتوليد مقال جديد فوراً")
    st.write(f"**التوقيت الحالي:** {datetime.now().strftime('%H:%M:%S')}")
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== 6. عرض المقال المتولد للنسخ الفوري ====================
st.markdown('### 📝 المقال الاحترافي الجاهز للنسخ الآن:')
last_generated_content = db_get_stat("last_content")
st.text_area(label="انسخ النص أدناه بالكامل وانشره في موقعك لتبدأ بجني الأرباح:", value=last_generated_content, height=400)

# ==================== 7. أزرار التحكم ====================
st.markdown("---")
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("🚀 توليد مقال احترافي جديد فوراً", disabled=is_running_state):
        db_set_stat("is_running", "1")
        threading.Thread(target=background_worker, daemon=True).start()
        time.sleep(2)
        st.rerun()

with col_btn2:
    if st.button("🔄 تحديث الشاشة لرؤية المقال الجديد"):
        st.rerun()
    
