import streamlit as st

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="منصة وسيم نائل للخدمات الرقمية", page_icon="💰", layout="wide")

# الهيدر العلوي والترحيب
st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🔥 منصة وسيم نائل الرقمية الشاملة</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 20px;'>بوابتك للخدمات الذكية، الأدوات الاحترافية، وفرص الربح</p>", unsafe_allow_html=True)
st.divider()

# تقسيم الصفحة إلى قسمين (يسار ويمين) لزيادة التنظيم
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 👤 صاحب المنصة")
    st.info("**الاسم:** وسيم نائل\n\n**التخصص:** مستشار أعمال ومطور حلول رقمية.")
    
    # 💰 القسم الأول: طلب الخدمات المدفوعة مباشر
    st.markdown("### 💼 اطلب خدمتك المدفوعة")
    st.write("احصل على استشارة مخصصة أو حلول برمجية وتسويقية لعملك الآن.")
    
    # زر تواصل مباشر للاتفاق المالي عبر الواتساب
    whatsapp_url = "https://wa.meً%20أستاذ%20وسيم%20أريد%20طلب%20خدمة%20مدفوعة"
    st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; font-size:16px; cursor:pointer;">💬 اطلب الخدمة واستلم أرباحك عبر الواتساب</button></a>', unsafe_allow_html=True)

with col2:
    # 🔒 القسم الثاني: الأدوات الذكية والاشتراكات (SaaS)
    st.markdown("### ⚡ الأدوات الذكية (متاح للمشتركين)")
    
    tab1, tab2 = st.tabs(["🤖 أداة كتابة الإعلانات", "📈 حاسبة الأرباح الذكية"])
    
    with tab1:
        st.write("استخدم الذكاء الاصطناعي لتوليد نصوص إعلانية تبيع فوراً.")
        prod_name = st.text_input("اكتب اسم منتجك:")
        if st.button("توليد النص الإعلاني"):
            if prod_name:
                st.success(f"🔥 إعلان احترافي لـ ({prod_name}): اشتري الآن واحصل على خصم 50% لفترة محدودة مع المستشار وسيم نائل!")
            else:
                st.warning("الرجاء كتابة اسم المنتج أولاً.")
                
    with tab2:
        st.write("احسب صافي أرباح حملتك الإعلانية بدقة.")
        revenue = st.number_input("إجمالي الإيرادات ($):", min_value=0.0, value=100.0)
        costs = st.number_input("تكلفة الإعلانات والمصاريف ($):", min_value=0.0, value=40.0)
        if st.button("احسب صافي الربح"):
            profit = revenue - costs
            st.metric(label="صافي أرباحك المباشرة", value=f"${profit}")

    st.divider()

    # 🔗 القسم الثالث: التسويق بالعمولة (Affiliate Links)
    st.markdown("### 🌟 توصيات وسيم نائل (روابط مخصصة)")
    st.write("أدوات ومواقع ننصح بها لبناء عملك على الإنترنت (نحصل على عمولة عند الشراء):")
    
    # استبدل هذه الروابط بروابط الأفلييت الخاصة بك لاحقاً
    st.markdown("- 🛠️ [أفضل استضافة مواقع عالمية بخصم خاص](https://hostinger.com)")
    st.markdown("- 🎨 [اشترك في Canva الاحترافية للتصميم](https://canva.com)")

st.divider()
st.markdown("<p style='text-align: center; color: gray;'>© 2026 جميع الحقوق محفوظة للمطور وسيم نائل</p>", unsafe_allow_html=True)
  
