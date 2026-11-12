import streamlit as st
import urllib.parse
import requests
import random
from io import BytesIO
from PIL import Image, ImageDraw
from rembg import remove
from deep_translator import GoogleTranslator

# 1. إعدادات الصفحة والهوية الفاخرة
st.set_page_config(
    page_title="الوكالة الذكية المتكاملة | الاستوديو الخاص",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تحسين المظهر العام باللغة العربية والألوان الملكية
st.markdown("""
    <style>
    .main {
        background-color: #0b0d12;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.4em;
        background: linear-gradient(90deg, #d4af37 0%, #aa7c11 100%);
        color: #000000;
        font-weight: bold;
        font-size: 16px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.01);
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔒 نظام الحماية والقفل الخاص بك وحدك
# ==========================================
SECRET_PASSWORD = "Waseem2026@"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_empty1, col_login, col_empty2 = st.columns([1, 1.5, 1])
    with col_login:
        st.title("🔒 استوديو العمل الخاص")
        st.markdown("نظام إدارة وتنفيذ طلبات العملاء الحصري.")
        pwd_input = st.text_input("🔑 أدخل كلمة المرور السرية:", type="password")
        if st.button("دخول إلى الاستوديو"):
            if pwd_input == SECRET_PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة!")
    st.stop()
# ==========================================

# 2. الشريط الجانبي
with st.sidebar:
    st.title("👑 مركز التحكم بالطلبات")
    
    style = st.selectbox(
        "🎨 الأسلوب الفني العام",
        [
            "Minimalist & Luxury (بسيط وفاخر)",
            "3D Modern Render (ثلاثي الأبعاد عصري)",
            "Commercial Advertising (إعلاني تجاري احترافي)",
            "Neon & Vibrant (ألوان نيون مشرقة وجذابة)",
            "Realistic Studio Photo (تصوير استوديو واقعي)",
            "Vintage & Classic (كلاسيكي عتيق)"
        ]
    )
    
    color_palette = st.selectbox(
        "🌈 لوحة الألوان",
        [
            "Gold & Black (ذهبي وأسود ملكي)",
            "Royal Blue & White (أزرق ملكي وأبيض)",
            "Emerald Green & Cream (أخضر زمردي وكريمي)",
            "Vibrant Red & Yellow (أحمر وأصفر للخصومات)",
            "Pastel & Soft (ألوان ناعمة وهادئة)",
            "Silver & Charcoal (فضي وفحمي داكن)"
        ]
    )
    
    aspect_ratio = st.radio(
        "📐 مقاس المنصة المطلوب",
        [
            "مربع - بوست انستغرام/فيسبوك (1080x1080)",
            "عمودي - ستوري/ريلز/تيك توك (720x1280)",
            "أفقي - يوتيوب/غلاف فيسبوك (1280x720)"
        ]
    )
    
    if "1080x1080" in aspect_ratio:
        width, height = 1080, 1080
    elif "720x1280" in aspect_ratio:
        width, height = 720, 1280
    else:
        width, height = 1280, 720

    model_choice = st.selectbox("🧠 دقة المحرك", ["flux", "turbo"])
    
    st.divider()
    watermark_text = st.text_input("🛡️ نص العلامة المائية للمعاينة", value="PREVIEW - غير مدفوع")
    
    st.divider()
    if st.button("🚪 قفل الاستوديو والخروج"):
        st.session_state.authenticated = False
        st.rerun()

# 3. الدوال الذكية المساعدة
def translate_to_english(arabic_text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(arabic_text)
    except Exception:
        return arabic_text

def fetch_image(prompt_text, w, h, model, seed):
    encoded = urllib.parse.quote(prompt_text)
    url = f"https://pollinations.ai{encoded}?width={w}&height={h}&model={model}&seed={seed}&nologo=true"
    try:
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            return response.content
    except Exception:
        return None
    return None

def make_transparent(image_bytes):
    input_image = Image.open(BytesIO(image_bytes)).convert("RGBA")
    output_image = remove(input_image)
    buf = BytesIO()
    output_image.save(buf, format="PNG")
    return buf.getvalue()

def add_watermark(image_bytes, text):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    
    w, h = img.size
    step_x = int(w / 3)
    step_y = int(h / 4)
    
    for x in range(20, w, step_x):
        for y in range(20, h, step_y):
            draw.text((x, y), text, fill=(255, 255, 255, 110))
            
    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")
    buf = BytesIO()
    watermarked.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

def generate_ai_copy_and_script(brand, request_ar):
    prompt = (
        f"أنت خبير تسويق إلكتروني محترف. اكتب لمشروع '{brand}' حول '{request_ar}':\n"
        f"1. بوست إعلاني قصير وجذاب للسوشيال ميديا مع إيموجي وهاشتاغات.\n"
        f"2. نص تعليق صوتي (Voiceover) مدته 15 ثانية يصلح لفيديو ريلز أو تيك توك.\n"
        f"اكتب الرد باللغة العربية الفصحى البسيطة والجاذبة مباشرة بدون مقدمات."
    )
    encoded = urllib.parse.quote(prompt)
    try:
        res = requests.get(f"https://pollinations.ai{encoded}", timeout=30)
        if res.status_code == 200:
            return res.text
    except Exception:
        pass
    return f"🔥 عرض خاص من {brand}!\n✨ {request_ar}\n📩 تواصل معنا الآن عبر الرسائل للطلب والاستفسار!"

def generate_voiceover(text_to_speak):
    clean_text = text_to_speak[:300]
    encoded = urllib.parse.quote(clean_text)
    url = f"https://pollinations.ai{encoded}?model=openai-audio&voice=nova"
    try:
        res = requests.get(url, timeout=45)
        if res.status_code == 200:
            return res.content
    except Exception:
        return None
    return None

# 4. الواجهة الرئيسية
st.title("👑 الاستوديو الشامل لخدمات السوشيال ميديا والتجارة")

tab1, tab2 = st.tabs([
    "🎨 قسم 1: تصميم الشعارات والإعلانات + النصوص والصوت",
    "📸 قسم 2: استوديو دمج وتصوير منتجات العملاء (Mockup)"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        service_type = st.selectbox(
            "🎯 نوع التصميم المطلوب",
            [
                "Logo Design (تصميم شعار وهوية بصرية)",
                "Social Media Ad Post (بوست إعلاني وترويجي)",
                "Instagram/TikTok Story & Reels Cover (ستوري وغلاف ريلز)",
                "YouTube Thumbnail (صورة مصغرة لليوتيوب)",
                "Logo Mockup on Luxury Business Card & Storefront (عرض الشعار على بطاقة ولافتة)"
            ]
        )
        brand_name = st.text_input("🏢 اسم مشروع العميل", placeholder="مثال: متجر الأناقة")
        client_request_ar = st.text_area("📝 تفاصيل طلب العميل بالعربية", placeholder="مثال: شعار تاج ذهبي فاخر لمتجر ملابس، أو إعلان خصم 50% على العطور...")

    with col2:
        num_variations = st.slider("🔢 عدد النماذج للتوليد", min_value=1, max_value=4, value=2)
        do_transparent = st.checkbox("✂️ استخراج نسخة مفرغة بدون خلفية (PNG)", value=True)
        do_copywriting = st.checkbox("✍️ توليد إعلان تسويقي + سيناريو فيديو بالذكاء الاصطناعي", value=True)
        do_voice = st.checkbox("🎙️ توليد تعليق صوتي إعلاني جاهز (MP3)", value=False)

    if st.button("🚀 تنفيذ الباقة الكاملة للعميل"):
        if not client_request_ar and not brand_name:
            st.warning("⚠️ يرجى إدخال اسم المشروع أو وصف الطلب أولاً!")
        else:
            with st.spinner("جاري تجهيز الحملة والتصاميم باحترافية..."):
                desc_en = translate_to_english(client_request_ar)
                clean_service = service_type.split("(").strip()
                clean_style = style.split("(").strip()
                clean_colors = color_palette.split("(").strip()
                
                final_prompt = (
                    f"{clean_service} for '{brand_name}', {desc_en}. "
                    f"Style: {clean_style}, Color palette: {clean_colors}. "
                    f"Isolated clean design, Behance and Dribbble trending, ultra-detailed, "
                    f"high contrast, studio quality, sharp focus, no watermark."
                )

            if do_copywriting:
                st.subheader("✍️ المحتوى التسويقي والسيناريو الجاهز للعميل:")
                ai_text = generate_ai_copy_and_script(brand_name or "المتجر", client_request_ar)
                st.info(ai_text)
                
                if do_voice:
                    with st.spinner("🎙️ جاري تسجيل التعليق الصوتي الإعلاني..."):
                        audio_bytes = generate_voiceover(ai_text)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                            st.download_button(
                                label="⬇️ تحميل التعليق الصوتي (MP3)",
                                data=audio_bytes,
                                file_name=f"{brand_name or 'ad'}_voiceover.mp3",
                                mime="audio/mp3"
                            )

            st.subheader("🎨 التصاميم الجاهزة (مع خيار الحماية قبل الدفع):")
            cols = st.columns(num_variations)
            for i in range(num_variations):
                with cols[i]:
                    with st.spinner(f"جاري تصميم النموذج #{i+1}..."):
                        seed = random.randint(1, 999999)
                        img_bytes = fetch_image(final_prompt, width, height, model_choice, seed)
                        if img_bytes:
                            st.image(img_bytes, use_container_width=True, caption=f"التصميم الأصلي #{i+1}")

    
