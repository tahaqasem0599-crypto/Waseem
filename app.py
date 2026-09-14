import streamlit as st

# إعدادات الصفحة وهوية التطبيق الفخمة
st.set_page_config(page_title="Waseem AI Auto-Sales", page_icon="🤖", layout="centered")

# تحسينات المظهر والخطوط
st.markdown("""
    <style>
    .title-text { color: #1e3a8a; text-align: center; font-size: 28px; font-weight: bold; font-family: 'Arial'; }
    .footer-text { text-align: center; color: #64748b; font-size: 14px; margin-top: 50px; }
    .response-box { background-color: #f1f5f9; padding: 15px; border-radius: 8px; border-right: 5px solid #38bdf8; color: #1e293b; }
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
        
        # هندسة النص الذكي (Prompt Engineering) لتوليد رد تسويقي مقنع
        ai_response = f"""
        ✨ مرحباً بك يا فندم! يسعدنا اهتمامك بمنتجنا الفخم والمميز.
        
        🛍️ **{product_name}** متوفر الآن لدينا بأعلى جودة تفاصيلها كالتالي:
        📝 {product_details if product_details else 'متوفر بألوان ومقاسات تناسب الجميع'}
        
        💰 **السعر المفاجأة:** {product_price} فقط! 
        
        🔥 الكمية محدودة جداً والطلب عليه مرتفع اليوم، هل ترغب في حجز قطعتك وتأكيد الطلب الآن قبل نفاد الكمية؟
        """
        
        st.write("### 🤖 الرد التسويقي الذكي المولد للزبائن:")
        st.markdown(f'<div class="response-box">{ai_response}</div>', unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ الرجاء إدخال اسم المنتج وسعره لتفعيل النظام وتوليد الرد.")

# التوقيع العالمي الخاص بك
st.write("---")
st.markdown('<p class="footer-text">تم التطوير والبرمجة بواسطة المطور العالمي: وسيم نائل العطار</p>', unsafe_allow_html=True)
        
