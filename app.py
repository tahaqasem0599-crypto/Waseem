import streamlit as st

# إعدادات المنصة الاحترافية الشاملة لوسيم نائل
st.set_page_config(page_title="منصة وسيم نائل الشاملة والتجارة الرقمية", page_icon="💎", layout="wide")

# تقسيم الصفحة لعرض الصورة الشخصية بجانب العنوان لبناء الثقة فوراً
col_header1, col_header2 = st.columns([1, 4])

with col_header1:
    # دمج صورتك الشخصية الاحترافية مباشرة في الواجهة
    st.image("https://githubusercontent.com", width=160)

with col_header2:
    st.markdown("<h1 style='color: #1E3A8A; margin-top: 10px;'>💎 منصة وسيم نائل الرقمية والتجارية الشاملة</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #4B5563;'>بوابتك الذكية للتجارة الإلكترونية، الأدوات البرمجية، والخدمات الإعلانية</p>", unsafe_allow_html=True)

st.divider()

# رابط الواتساب المباشر لوسيم نائل
whatsapp_base_url = "https://wa.me"

# تقسيم الشاشة إلى تبويبات احترافية
tab_store, tab_services, tab_payment, tab_ai, tab_finance = st.tabs([
    "🛍️ متجر الملابس الفاخرة", 
    "💼 الخدمات الرقمية والإعلانات",
    "💳 الدفع عبر بنك فلسطين",
    "🤖 أدوات الذكاء الاصطناعي", 
    "📊 الحاسبة التجارية والأرباح"
])

# 1️⃣ التبويب الأول: متجر الملابس والتجارة
with tab_store:
    st.header("👕 أحدث تشكيلات الملابس والأزياء الفاخرة")
    st.write("تصفح واطلب قطعتك المفضلة الآن، الدفع متوفر عبر تطبيق بنك فلسطين أو كاش عند الاستلام.")
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.subheader("🧥 جاكيتات وهوديز شتوية سبورت")
        st.write("السعر: **150 شيكل**")
        msg1 = "مرحباً أستاذ وسيم، أريد طلب الجاكيت الشتوي السبورت (150 شيكل)"
        st.markdown(f'<a href="{whatsapp_base_url}{msg1}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">🛍️ اطلب عبر الواتساب</button></a>', unsafe_allow_html=True)
        
    with col_img2:
        st.subheader("👕 أطقم كاجوال صيفية ورياضية")
        st.write("السعر: **120 شيكل**")
        msg2 = "مرحباً أستاذ وسيم، أريد طلب الطقم الكاجوال الرياضي (120 شيكل)"
        st.markdown(f'<a href="{whatsapp_base_url}{msg2}" target="_blank"><button style="background-color:#25D366; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">🛍️ اطلب عبر الواتساب</button></a>', unsafe_allow_html=True)

# 2️⃣ التبويب الثاني: الخدمات الرقمية والتسويق
with tab_services:
    st.header("💼 خدمات وسيم نائل للأعمال والتسويق")
    st.write("نساعدك في تنمية أعمالك ومبيعاتك عبر الإنترنت من خلال خدماتنا المدفوعة الاحترافية.")
    
    srv1, srv2, srv3 = st.columns(3)
    with srv1:
        st.subheader("🎯 إدارة الحملات الإعلانية")
        st.write("نطلق لك إعلانات ممولة احترافية على فيسبوك وإنستغرام لتجلب لك آلاف الزبائن.")
        msg_srv1 = "مرحباً أستاذ وسيم، أريد استشارة حول إدارة الحملات الإعلانية المموّلة"
        st.markdown(f'<a href="{whatsapp_base_url}{msg_srv1}" target="_blank"><button style="width:100%; background-color:#1E3A8A; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">💬 احجز الخدمة الآن</button></a>', unsafe_allow_html=True)
        
    with srv2:
        st.subheader("🎨 تصميم الجرافيك والهويات")
        st.write("تصميم شعارات، بنرات إعلانية، وصور احترافية لمنتجاتك تجذب المشترين.")
        msg_srv2 = "مرحباً أستاذ وسيم، أريد طلب خدمة تصميم جرافيك وشعارات"
        st.markdown(f'<a href="{whatsapp_base_url}{msg_srv2}" target="_blank"><button style="width:100%; background-color:#1E3A8A; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">💬 احجز الخدمة الآن</button></a>', unsafe_allow_html=True)
        
    with srv3:
        st.subheader("🌐 إنشاء المواقع والتطبيقات")
        st.write("برمجة صفحات هبوط وتطبيقات ذكية مخصصة لعملك مثل هذا التطبيق تماماً.")
        msg_srv3 = "مرحباً أستاذ وسيم، أريد طلب خدمة برمجة وإنشاء موقع إلكتروني"
        st.markdown(f'<a href="{whatsapp_base_url}{msg_srv3}" target="_blank"><button style="width:100%; background-color:#1E3A8A; color:white; border:none; padding:8px; border-radius:5px; cursor:pointer;">💬 احجز الخدمة الآن</button></a>', unsafe_allow_html=True)

# 3️⃣ التبويب الثالث: طرق الدفع البنكية
with tab_payment:
    st.header("💳 طرق الدفع المتاحة وتحويل الأموال")
    st.write("لتسهيل معاملاتكم، يمكنك تحويل قيمة البضاعة أو الخدمات عبر تطبيق بنك فلسطين مباشرة:")
    
    st.success("🏦 **التحويل البنكي أو عبر تطبيق بنك فلسطين (Bank of Palestine)**")
    st.info("💡 يمكنك إرسال الحوالة إلى حسابنا مباشرة، أو الدفع السريع باستخدام ميزة **(بالمحفظة / PalPay)** من داخل تطبيقك البنكي.")
    
    st.markdown("""
    * **اسم صاحب الحساب:** وسيم نائل
    * **رقم الحساب أو المحفظة:** (اكتب رقم حسابك هنا عند تعديل الكود)
    * **ملاحظة:** يرجى تصوير شاشة إشعار التحويل الناجح من التطبيق وإرسالها عبر الواتساب لتأكيد طلبك فوراً.
    """)
    
    msg_pay = "مرحباً أستاذ وسيم، لقد قمت بتحويل المبلغ عبر تطبيق بنك فلسطين وأريد تأكيد الطلب"
    st.markdown(f'<a href="{whatsapp_base_url}{msg_pay}" target="_blank"><button style="background-color:#A16207; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">📸 أرسل إشعار الدفع عبر الواتساب</button></a>', unsafe_allow_html=True)

# 4️⃣ التبويب الرابع: أدوات الذكاء الاصطناعي
with tab_ai:
    st.header("🤖 أدوات الذكاء الاصطناعي الذكية لرواد الأعمال")
    st.write("أدوات برمجية ذكية وحصرية لمساعدتك في كتابة المحتوى الإعلاني والتسويقي فوراً.")
    
    ai_choice = st.selectbox("اختر أداة الذكاء الاصطناعي التي تريد استخدامها:", ["كاتب الإعلانات السريعة", "صانع الأفكار التسويقية"])
    
    if ai_choice == "كاتب الإعلانات السريعة":
        prod = st.text_input("اكتب اسم المنتج أو الخدمة التي تبيعها:")
        if st.button("🚀 توليد نص إعلاني ذكي"):
            if prod:
                st.success(f"🔥 **الإعلان المقترح:** هل تبحث عن أفضل ({prod})؟ لا تبحث بعيداً! منصة وسيم نائل تقدم لك الجودة الأعلى والأسعار الأفضل في السوق مع خدمة توصيل سريعة. اضغط للطلب الآن ولا تفوت الفرصة! 🔥")
            else:
                st.warning("يرجى كتابة اسم المنتج أولاً لتوليد الإعلان.")
                
    elif ai_choice == "صانع الأفكار التسويقية":
        niche = st.text_input("اكتب مجالك التجاري (مثال: ملابس، عطور، مطاعم):")
        if st.button("💡 توليد أفكار تسويقية"):
            if niche:
                st.info(f"💡 **أفكار لزيادة مبيعات {niche}:**\n1. اعمل عرض 'اشتري قطعة واصل على الثانية بنصف السعر'.\n2. أطلق إعلان ممول مستهدفاً لقطتك الشخصية الفخمة لبناء الثقة.\n3. قدم كود خصم خاص لأول 50 مشتري يتواصلون معك عبر الواتساب.")

# 5️⃣ التبويب الخامس: الحاسبة المالية والتجارية
with tab_finance:
    st.header("📊 الحاسبة المالية الذكية لحساب صافي الأرباح والـ ROI")
    st.write("ادخل الأرقام الخاصة بتجارتك أو حملتك الإعلانية لحساب صافي ربحك بدقة بالشيكل.")
    
    currency = st.radio("اختر عملة الحساب والتعامل:", ["ILS (شيكل جديد)", "USD (دولار أمريكي)"])
    
    rev = st.number_input("إجمالي المبيعات أو الإيرادات:", min_value=0.0, value=1000.0)
    cost_prod = st.number_input("تكلفة البضاعة أو المنتجات الأساسية:", min_value=0.0, value=400.0)
    cost_ads = st.number_input("تكلفة الإعلانات المموّلة والمصاريف الأخرى:", min_value=0.0, value=200.0)
    
    if st.button("🧮 احسب صافي الأرباح فوراً"):
        total_costs = cost_prod + cost_ads
        net_profit = rev - total_costs
        
        st.metric(label=f"صافي أرباح وسيم نائل المباشرة ({currency})", value=f"{net_profit} {currency}")
        if net_profit > 0:
            st.balloons()
            st.success("🎉 عمل ممتاز! تجارتك تحقق أرباحاً صافية وصحية.")
        elif net_profit == 0:
            st.warning("⚠️ أنت في نقطة التعادل (لا يوجد أرباح ولا خسائر). حاول تقليل التكاليف.")
        else:
            st.error("❌ تنبيه: هناك خسارة مالية. يرجى مراجعة ميزانية الإعلانات وأسعار البضائع فوراً.")

st.divider()
st.markdown("<p style='text-align: center; color: #9CA3AF;'>© 2026 جميع الحقوق محفوظة ومطورة بالكامل بواسطة المستشار وسيم نائل</p>", unsafe_allow_html=True)
