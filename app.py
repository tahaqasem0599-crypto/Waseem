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
    .article-card { background-color: #1a1a1a; border: 1px solid #D4AF37; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    .profit-text { color: #2ecc71; font-weight: bold; font-size: 28px; display: block; margin-top: 10px; }
    .stButton>button { width: 100%; border-radius: 25px; font-weight: bold; height: 50px; background-color: #D4AF37; color: black; }
    .stButton>button:hover { background-color: #FFF; color: black; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">💰 ماكينة الأتمتة وضخ المحتوى الرقمي المطور العالـمي</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">المطور والمالك المسؤول: وسيم نائل العطار | الحساب المعتمد: tahaqasem0599-crypto</div>', unsafe_allow_html=True)

# ==================== 2. إدارة قاعدة البيانات المحلية المحدثة ====================
def init_db():
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, created_at TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (key TEXT PRIMARY KEY, value TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('is_running', '0')")
    cursor.execute("INSERT OR IGNORE INTO stats (key, value) VALUES ('total_earnings', '0.0')")
    conn.commit()
    conn.close()

init_db()

def db_add_article(title, content):
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO articles (title, content, created_at) VALUES (?, ?, ?)", (title, content, now))
    
    # محاكاة إضافة أرباح تقديرية تراكمية في الحصالة لكل مقال يتم إنشاؤه (مثلاً 50 شيكل لكل حزمة مقالات قوية)
    try:
        cursor.execute("SELECT value FROM stats WHERE key = 'total_earnings'")
        current_earnings = float(cursor.fetchone()[0])
        new_earnings = current_earnings + 50.0
        cursor.execute("INSERT OR REPLACE INTO stats (key, value) VALUES ('total_earnings', ?)", (str(new_earnings),))
    except:
        pass
        
    conn.commit()
    conn.close()

def db_get_all_articles():
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, created_at FROM articles ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def db_delete_article(article_id):
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()

def db_get_stat(key, default="0"):
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM stats WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def db_set_stat(key, value):
    conn = sqlite3.connect('waseem_v2_articles.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO stats (key, value) VALUES (?, ?)", (key, str(value)))
    conn.commit()
    conn.close()

# ==================== 3. جلب المفتاح الآمن ====================
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", os.environ.get("OPENAI_API_KEY", ""))

if not OPENAI_API_KEY:
    st.error("❌ تأكد من إضافة مفتاح OPENAI_API_KEY في الـ Secrets الخاص بـ Streamlit Cloud!")
    client = None
else:
    client = OpenAI(api_key=OPENAI_API_KEY)

# ==================== 4. محرك توليد المقالات التلقائي ====================
def background_generator():
    if not client: return
    topics = [
        "How to build a fully automated online business in 2026",
        "Top AI applications transforming digital marketing and sales",
        "Unlocking passive income through AI automation workflows",
        "Best high-paying remote jobs using artificial intelligence tools",
        "How to safely invest in cryptocurrency using automated trading bots"
    ]
    
    for topic in topics:
        if db_get_stat("is_running") == "0": break
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": f"Write a professional SEO-optimized blog post in English about: '{topic}'. Include beautiful titles, clear paragraphs, and key takeaways. Output clean easy-to-read text."}]
            )
            content = response.choices.message.content
            db_add_article(topic, content)
            time.sleep(3)
        except:
            pass
    db_set_stat("is_running", "0")

# ==================== 5. واجهة المستخدم الرسومية الفاخرة ====================
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.subheader("📊 بنك المقالات التراكمي")
    articles = db_get_all_articles()
    st.metric(label="إجمالي المقالات الجاهزة للنسخ حالياً", value=len(articles))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="status-box">', unsafe_allow_html=True)
    st.subheader("💰 محاكي حصالة الأرباح المتوقعة")
    current_saved_money = float(db_get_stat("total_earnings", "0.0"))
    st.markdown(f"الرصيد التقديري المتراكم: <span class='profit-text'>{current_saved_money:,.2f} ILS (شيكل)</span>", unsafe_allow_html=True)
    st.caption("ملاحظة: هذا محاكي إحصائي داخلي لتتبع ومراقبة نمو المحتوى الخاص بك.")
    if st.button("🔄 تصفير العداد عند السحب من حسابك الإعلاني الحقيقي"):
        db_set_stat("total_earnings", "0.0")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# أزرار التشغيل
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    is_running = db_get_stat("is_running") == "1"
    if st.button("🚀 اضغط هنا لتوليد حزمة مقالات مربحة فوراً", disabled=is_running):
        db_set_stat("is_running", "1")
        threading.Thread(target=background_generator, daemon=True).start()
        time.sleep(1)
        st.rerun()
with c2:
    if st.button("🔄 تحديث الشاشة ورؤية التحديثات"):
        st.rerun()

# عرض بنك المقالات للنسخ
st.markdown("### 📝 بنك المقالات الجاهزة (انسخ وانشر في Site123 مباشرة للربح):")
if not articles:
    st.info("البنك فارغ حالياً. اضغط على الزر الذهبي بالأعلى لتوليد المقالات الأولى وزيادة رصيد الحصالة التقديرية!")
else:
    for art_id, title, content, date in articles:
        with st.container():
            st.markdown(f'<div class="article-card">', unsafe_allow_html=True)
            st.subheader(f"📌 العنوان: {title}")
            st.caption(f"تاريخ التوليد: {date}")
            st.text_area(label="المحتوى الكامل للمقال (قم بنسخه بالكامل):", value=content, height=250, key=f"txt_{art_id}")
            if st.button(f"🗑️ حذف هذا المقال بعد نشره", key=f"del_{art_id}"):
                db_delete_article(art_id)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
