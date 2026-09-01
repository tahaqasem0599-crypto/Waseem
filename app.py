import streamlit as st
import datetime

# إعدادات الصفحة الرسمية للتطبيق بألوان تليجرام
st.set_page_config(page_title="تليجرام المطور", page_icon="💬", layout="centered")

# تغيير التصميم الداخلي ليمثل ألوان تليجرام الشهيرة (الأزرق والخلفية الفاتحة)
st.markdown("""
    <style>
    .stApp { background-color: #E7EBF0; }
    .chat-bubble-me {
        background-color: #EFFDDE; padding: 10px; border-radius: 10px;
        margin: 5px; text-align: right; float: right; clear: both; width: 70%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .chat-bubble-other {
        background-color: #FFFFFF; padding: 10px; border-radius: 10px;
        margin: 5px; text-align: left; float: left; clear: both; width: 70%;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .time-text { color: grey; font-size: 10px; block: right; }
    </style>
""", unsafe_allow_html=True)

# تهيئة الذاكرة المؤقتة لتخزين الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "أحمد الدلو", "text": "مرحباً يا وسيم، كيف تسير هندسة التطبيق العالمي؟", "is_me": False, "time": "4:28 م"},
        {"sender": "وسيم نائل", "text": "أهلاً أحمد، الكود جاهز ومرفوع الآن على جيت هاب ويعمل بكفاءة.", "is_me": True, "time": "4:29 م"}
    ]

# الشريط العلوي للتطبيق (تليجرام)
st.markdown("<h2 style='text-align: center; color: #517DA2; font-weight: bold;'>💬 تليجرام المطور</h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>مستودع وسيم نائل العالمي</h5>", unsafe_allow_html=True)
st.write("---")

# عرض المحادثة داخل فقاعات تليجرام المنسقة
for msg in st.session_state.messages:
    if msg["is_me"]:
        st.markdown(f'<div class="chat-bubble-me">{msg["text"]}<br><span class="time-text">{msg["time"]}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-other"><b>{msg["sender"]}:</b><br>{msg["text"]}<br><span class="time-text">{msg["time"]}</span></div>', unsafe_allow_html=True)

st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
st.write("---")

# حقل إدخال الرسائل الجديد أسفل الشاشة
with st.container():
    user_input = st.text_input("اكتب رسالة...", key="chat_input", placeholder="أرسل رسالة إلى القناة الحية...")
    send_button = st.button("إرسال 🚀")

    if send_button and user_input.strip() != "":
        time_now = datetime.datetime.now().strftime("%I:%M %p").replace("AM", "ص").replace("PM", "م")
        
        # إضافة الرسالة الجديدة إلى السيرفر المشترك
        st.session_state.messages.append({
            "sender": "وسيم نائل (المالك)",
            "text": user_input,
            "is_me": True,
            "time": time_now
        })
        # إعادة تنشيط الصفحة لرؤية الرسالة فوراً
        st.rerun()
