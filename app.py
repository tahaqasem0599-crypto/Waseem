import streamlit as st

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(
    page_title="متجر وسيم نائل للملابس",
    page_icon="👑",
    layout="centered"
)

# 2. تصميم وتنسيق الواجهة ودعم اللغة العربية (RTL) والأزرار الملونة
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
    /* تنسيق زر الواتساب الأخضر الاحترافي */
    .whatsapp-btn {
        display: block;
        width: 100%;
        background-color: #25D366;
        color: white !important;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-family: 'Cairo', sans-serif;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
    }
    /* تنسيق أيقونة البروفايل البديلة لتبدو احترافية */
    .profile-emoji {
        font-size: 80px;
        text-align: center;
        display: block;
        margin: 10px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# رقم واتسابك الخاص بالمقدمة الدولية الصحيحة
whatsapp_number = "972598338642" 
whatsapp_url = f"https://wa.me{whatsapp_number}?text=مرحباً%20متجر%20وسيم%20نائل،%20أود%20الاستفسار%20عن%20الملابس"

# 3. القائمة الجانبية (Sidebar)
with st.sidebar:
    # أيقونة بروفايل بديلة تظهر فوراً دون أي أخطاء أو روابط مكسورة
    st.markdown('<span class="profile-emoji">👤</span>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center !important;'>المؤسس والمطور: وسيم نائل</p>", unsafe_allow_html=True)
    
    # إضافة زر الواتساب في القائمة الجانبية
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">💬 تواصل واتساب مباشر</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.title("📂 الأقسام الرئيسية")
    section = st.radio("انتقل إلى:", ["الرئيسية", "تشكيلة الملابس", "رفع طلب جديد", "تواصل معنا"])

# القسم الأول: الرئيسية
if section == "الرئيسية":
    st.title("مرحباً بكم في متجر وسيم نائل الإلكتروني 🚀")
    st.write("وجهتكم الأولى لأحدث صيحات الموضة والملابس الرياضية والكاجوال في العالم العربي.")
    
    st.markdown('<span class="profile-emoji">👑</span>', unsafe_allow_html=True)
    st.markdown("<p style='text-align:center !important;'>وسيم نائل - نرحب بكم في متجرنا</p>", unsafe_allow_html=True)
            
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
    
    # إضافة زر الواتساب الكبير في صفحة التواصل الأساسية
    st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn" style="font-size: 18px; padding: 15px;">💬 اضغط هنا لمراسلتنا عبر الواتساب واطلب فوراً</a>', unsafe_allow_html=True)
    
    st.write("📧 البريد الإلكتروني: support@waseem-store.com")
    st.write("📍 الموقع: العالم العربي")
