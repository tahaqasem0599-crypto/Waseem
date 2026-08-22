import streamlit as st

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(
    page_title="متجر وسيم نائل للملابس",
    page_icon="👑",
    layout="centered"
)

# 2. تصميم وتنسيق الواجهة ودعم اللغة العربية (RTL)
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
        background-color: #0056b3;
        color: white;
        border-radius: 8px;
    }
    .product-box {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    # الكود يحاول قراءة أي صورة ترفعها بدون أن يسبب خطأ أحمر
    try:
        st.image("image_fyI0Hp.png", caption="المؤسس والمطور: وسيم نائل", use_container_width=True)
    except:
        try:
            st.image("waseem.jpg", caption="المؤسس والمطور: وسيم نائل", use_container_width=True)
        except:
            st.info("💡 نصيحة: يرجى رفع صورتك الشخصية وتسميتها image_fyI0Hp.png لتظهر هنا.")
            
    st.markdown("---")
    st.title("📂 الأقسام الرئيسية")
    section = st.radio("انتقل إلى:", ["الرئيسية", "تشكيلة الملابس", "رفع طلب جديد", "تواصل معنا"])

# القسم الأول: الرئيسية
if section == "الرئيسية":
    st.title("مرحباً بكم في متجر وسيم نائل الإلكتروني 🚀")
    st.write("وجهتكم الأولى لأحدث صيحات الموضة والملابس الرياضية والكاجوال في العالم العربي.")
    
    try:
        st.image("image_fyI0Hp.png", caption="وسيم نائل - نرحب بكم في متجرنا", use_container_width=True)
    except:
        pass
            
    st.subheader("🌟 لماذا تختار متجرنا؟")
    st.write("• جودة عالية وخامات أصلية ممتازة.")
    st.write("• أسعار تنافسية تناسب الجميع.")
    st.write("• توصيل سريع وآمن لكافة المناطق.")

# القسم الثاني: تشكيلة الملابس
elif section == "تشكيلة الملابس":
    st.title("👕 أحدث الموديلات المتوفرة")
    st.write("تصفح تشكيلتنا المميزة المستوحاة من أفضل البراندات العالمية:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        st.subheader("تيشرت رياضي مميز")
        st.write("السعر: 25 دولار")
        if st.button("إضافة للسلة", key="p1"):
            st.success("تم إضافة التيشرت الرياضي إلى السلة!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="product-box">', unsafe_allow_html=True)
        st.subheader("جاكيت كاجوال شتوي")
        st.write("السعر: 45 دولار")
        if st.button("إضافة للسلة", key="p2"):
            st.success("تم إضافة الجاكيت الكاجوال إلى السلة!")
        st.markdown('</div>', unsafe_allow_html=True)

# القسم الثالث: رفع طلب جديد
elif section == "رفع طلب جديد":
    st.title("📦 اطلب منتجك المخصص")
    st.write("هل لديك تصميم معين أو صورة لملابس تريد تفصيلها أو طلبها؟ ارفعها لنا هنا:")
    
    customer_name = st.text_input("اسمك الكريم:")
    customer_phone = st.text_input("رقم الهاتف للتواصل:")
    uploaded_file = st.file_uploader("اختر صورة الملابس أو التصميم:", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="الصورة التي قمت برفعها", width=300)
        
    if st.button("إرسال الطلب الآن"):
        if customer_name and customer_phone:
            st.balloons()
            st.success(f"شكراً لك يا {customer_name}! تم استلام طلبك بنجاح، وسنتواصل معك قريباً.")
        else:
            st.error("الرجاء إدخال الاسم ورقم الهاتف أولاً.")

# القسم الرابع: تواصل معنا
elif section == "تواصل معنا":
    st.title("📞 معلومات التواصل")
    st.write("يسعدنا دائماً تواصلكم معنا للاستفسارات والشكاوي:")
    st.write("📧 البريد الإلكتروني: support@waseem-store.com")
    st.write("📍 الموقع: العالم العربي")
    
