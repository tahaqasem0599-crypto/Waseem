import streamlit as st

# إعدادات الصفحة وهوية التطبيق الفخمة
st.set_page_config(page_title="Waseem AI Auto-Sales", page_icon="🤖", layout="centered")

# تحسينات المظهر وجعل التطبيق يدعم اللغة العربية بشكل احترافي بالكامل
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    body, .main, p, div, span, h1, h2, h3, input, textarea, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .title-text { color: #1e3a8a; text-align: center !important; font-size: 28px; font-weight: bold; width: 100%; display: block; }
    .footer-text { text-align: center !important; color: #64748b; font-size: 14px; margin-top: 50px; width: 100%; display: block; }
    .response-box { background-color: #f8fafc; padding: 20px; border-radius: 12px; border-right: 6px solid #2563eb; color: #1e293b; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); line-height: 1.8; }
    </style>
""", unsafe_allow_html=True)

# واجهة التطبيق الرئيسية
st.markdown('<p class="title-text">🤖 Waseem AI - نظام أتمتة المبيعات الذكي</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("📊 لوحة تحكم المحل الذكية")
product_name = st.text_input("اسم المنتج أو قطعة الملابس:")
product_price = st.number_input("سعر القطعة (بالشيكل أو الدولار):", min_value=0)
product_details = st.text_area("تفاصيل إضافية (المقاسات المتوفرة، الألوان):")

if st.button("🚀 تفعيل وتوليد الرد الذكي للزبائن"):
    if product_name and product_price:
        st.success(f"✅ تم بنجاح ربط الذكاء الاصطناعي بمنتج: {product_name}")
        
        # هندسة النص الذكي (Prompt Engineering) بتنسيق عربي مرتب ومحاذٍ لليمين
        ai_response = f"""
        ✨ <b>مرحباً بك يا فندم!</b> يسعدنا جداً اهتمامك بمنتجنا الفخم والمميز.<br><br>
        🛍️ <b>{product_name}</b> متوفر الآن لدينا بأعلى جودة تفاصيلها كالتالي:<br>
        📝 {product_details if product_details else 'متوفر بألوان ومقاسات تناسب الجميع'}<br><br>
        💰 <b>السعر المفاجأة:</b> {product_price} فقط! <br><br>
        🔥 الكمية محدودة جداً والطلب عليه مرتفع اليوم، هل ترغب في حجز قطعتك وتأكيد الطلب الآن قبل نفاد الكمية؟
        """
        
        st.write("### 🤖 الرد التسويقي الذكي المولد للزبائن:")
        st.markdown(f'<div class="response-box">{ai_response}</div>', unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ الرجاء إدخال اسم المنتج وسعره لتفعيل النظام وتوليد الرد.")

# التوقيع العالمي الخاص بك
st.write("---")
st.markdown('<p class="footer-text">تم التطوير والبرمجة بواسطة المطور العالمي: وسيم نائل العطار</p>', unsafe_allow_html=True)
        
