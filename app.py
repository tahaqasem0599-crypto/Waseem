import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="بنك كسوة أطفال غزة - وسيم نائل",
    page_icon="👶",
    layout="centered"
)

# 2. التنسيق العربي والجميل للواجهة
st.markdown("""
    <style>
    .reportview-container .main .block-container {
        direction: RTL;
        text-align: right;
    }
    h1, h2, h3, p, span {
        text-align: right !important;
        direction: RTL !important;
        font-family: 'Cairo', sans-serif;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .box {
        border: 2px dashed #0056b3;
        padding: 20px;
        border-radius: 12px;
        background-color: #f0f7ff;
        margin-bottom: 20px;
    }
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

whatsapp_number = "972598338642"

# 3. القائمة الجانبية للتنقل
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>👶 بنك الكسوة</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>فكرة المطور: وسيم نائل</p>", unsafe_allow_html=True)
    section = st.radio("اختار القسم:", ["💡 عن الفكرة", "🔍 تصفح المقاسات المتوفرة", "🔄 اعرض ملابس للتبادل"])

# القسم الأول: شرح الفكرة
if section == "💡 عن الفكرة":
    st.title("مرحباً بكم في بنك مقاسات أطفال غزة 🇵🇸")
    st.write("أول تطبيق في غزة لمقايضة وتبديل ملابس الأطفال مجاناً! ملابس أولادك صغرت عليهم؟ لا ترميها ولا تشتري بغالي، بدّلها بمقاس أكبر من محلي فوراً.")
    
    st.markdown("""
    <div class="box">
    <h3>🔄 كيف بتستفيد هلقيت؟</h3>
    <p>1. بتصور الملابس النظيفة اللي صغرت على ابنك وترفعها ع التطبيق.</p>
    <p>2. بتدور ع المقاس الجديد اللي بدك إياه لأولادك في قسم المتوفر.</p>
    <p>3. بتشرفنا على المحل (مركز التبادل)، بتسلمنا القديم وبتستلم الجديد ونقداً رسوم الفحص 5 شيكل فقط!</p>
    </div>
    """, unsafe_allow_html=True)

# القسم الثاني: تصفح المقاسات
elif section == "🔍 تصفح المقاسات المتوفرة":
    st.title("👕 القطع المتوفرة للتبادل هلقيت")
    age_filter = st.selectbox("اختار عمر طفلك لرؤية المتوفر له:", ["حديث ولادة - 6 أشهر", "سنة إلى سنتين", "3 إلى 5 سنوات", "6 إلى 10 سنوات"])
    
    st.info(f"يتم الآن عرض القطع المتوفرة لعمر: {age_filter}")
    
    # مثال لقطعة متوفرة
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("<font size='6'>🧥</font>", unsafe_allow_html=True) # أيقونة تعبيرية كبديل مستقر للصورة
    with col2:
        st.subheader("جاكيت شتوي ناعم مبطن")
        st.write("• **الحالة:** ممتازة جداً (شبه جديد)")
        st.write("• **المقاس الحالي للقطعة:** يناسب عمر 4 سنوات")
        
        chat_url = f"https://wa.me{whatsapp_number}?text=مرحباً%20وسيم،%20أريد%20حجز%20الجاكيت%20المبطن%20عمر%204%20سنوات%20للمقايضة"
        st.markdown(f'<a href="{chat_url}" target="_blank" class="whatsapp-btn">🛍️ احجز القطعة هلقيت وتواصل واتساب</a>', unsafe_allow_html=True)

# القسم الثالث: رفع الملابس للتبادل
elif section == "🔄 اعرض ملابس للتبادل":
    st.title("📸 ارفع الملابس التي تريد تبديلها")
    st.write("ساعد غيرك واستفد! ارفع تفاصيل الملابس النظيفة هلقيت:")
    
    parent_name = st.text_input("اسمك الكريم:")
    item_age = st.selectbox("المقاس الحالي للملابس (تناسب عمر كام؟):", ["0-6 أشهر", "1-2 سنة", "3-5 سنوات", "6-10 سنوات"])
    photo = st.file_uploader("صور القطعة بشكل واضح وارفعها هنا:", type=["jpg", "png", "jpeg"])
    
    if st.button("تأكيد ونشر في البنك"):
        if parent_name and photo:
            st.balloons()
            st.success(f"كفو يا {parent_name}! تم رفع القطعة بنجاح، وجاري فحصها لتظهر في قسم المتوفر. تفضل بزيارة المحل لإتمام التبادل.")
        else:
            st.error("الرجاء كتابة الاسم ورفع صورة القطعة أولاً.")
    
