import streamlit as st
import urllib.parse

# إعدادات الصفحة وهوية التطبيق العالمية
st.set_page_config(page_title="Waseem AI Auto-Sales Pro", page_icon="🚀", layout="centered")

# تحسينات المظهر وتنسيق الـ RTL الاحترافي
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    body, .main, p, div, span, h1, h2, h3, input, textarea, button {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    .title-text { color: #2563eb; text-align: center !important; font-size: 32px; font-weight: bold; width: 100%; display: block; margin-bottom: 5px; }
    .subtitle-text { color: #64748b; text-align: center !important; font-size: 16px; width: 100%; display: block; margin-bottom: 20px; }
    .footer-text { text-align: center !important; color: #94a3b8; font-size: 14px; margin-top: 60px; width: 100%; display: block; }
    .response-box { background-color: #ffffff; padding: 25px; border-radius: 16px; border-right: 8px solid #2563eb; color: #1e293b; box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.05); line-height: 2; margin-bottom: 20px; text-align: right !important; }
    </style>
""", unsafe_allow_html=True)

# واجهة التطبيق الاحترافية الجديدة
st.markdown('<p class="title-text">🚀 Waseem AI Auto-Sales Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">النظام السحابي الذكي لأتمتة مبيعات المتاجر الرقمية وعمليات الرد التلقائي</p>', unsafe_allow_html=True)
st.write("---")

st.subheader("📊 لوحة تحكم التاجر الذكية")
product_name = st.text_input("📦 اسم المنتج أو قطعة الملابس:")
product_price = st.number_input("💰 سعر القطعة (بالشيكل أو الدولار):", min_value=0)
product_details = st.text_area("📝 تفاصيل إضافية (المقاسات المتوفرة، الألوان، خيارات الشحن):")

if st.button("🔥 تفعيل وتوليد الرد بالذكاء الاصطناعي"):
    if product_name and product_price:
        st.success(f"✅ تم ربط نموذج الذكاء الاصطناعي بنجاح بمنتج: {product_name}")
        
        # هندسة النص التسويقي بنمط فخم ومقنع جداً
        ai_response = f"""✨ مرحباً بك يا فندم! يسعدنا جداً اهتمامك بمنتجنا الفخم والمميز.

🛍️ منتج ( {product_name} ) متوفر الآن لدينا بأعلى جودة وتفاصيله كالتالي:
📝 {product_details if product_details else 'متوفر بجميع المقاسات والألوان وتصميم عصري يناسب الجميع.'}

💰 السعر المفاجأة: {product_price} فقط!

🔥 الكمية محدودة جداً والطلب عليه مرتفع للغاية اليوم.. هل ترغب في حجز قطعتك وتأكيد الطلب الآن قبل نفاد الكمية وتجهيز الشحن لك؟"""
        
        st.write("### 🤖 الرد التسويقي الذكي الجاهز للإرسال:")
        
        # عرض النص داخل صندوق فخم
        st.text_area("", value=ai_response, height=250, key="generated_text")
        
        # ميزة العالمية: تجهيز رابط الإرسال المباشر للواتساب
        encoded_text = urllib.parse.quote(ai_response)
        whatsapp_url = f"https://wa.me{encoded_text}"
        
        # أزرار التفاعل السريع
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" style="text-decoration: none;"><button style="width: 100%; background-color: #25d366; color: white; border: none; padding: 10px; border-radius: 8px; font-weight: bold; cursor: pointer;">📲 إرسال مباشر عبر WhatsApp</button></a>', unsafe_allow_html=True)
        with col2:
            st.info("💡 يمكنك نسخ النص مباشرة من الصندوق أعلاه واستخدامه في أي منصة!")
            
    else:
        st.warning("⚠️ الرجاء إدخال اسم المنتج وسعره لتفعيل محرك الذكاء الاصطناعي.")

# بصمة الشهرة العالمية للمطور
st.write("---")
st.markdown('<p class="footer-text">🌍 تم تصميم وتطوير النظام بواسطة المطور العالمي: وسيم نائل العطار</p>', unsafe_allow_html=True)
        
