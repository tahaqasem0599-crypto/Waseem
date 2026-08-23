import streamlit as st
import streamlit.components.v1 as components
import random
import time

# إعدادات شاشة اللعبة والهوية البصرية الرسمية
st.set_page_config(page_title="غزة الحربية - النظام الشامل", page_icon="⚔️", layout="wide")

# بيانات دخول المطور وسيم
ADMIN_USERNAME = "waseem"
ADMIN_PASSWORD = "123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"user": "المطور وسيم", "msg": "تم تشغيل سيرفرات لعبة غزة الحربية بنجاح! 🔥"},
        {"user": "النظام الآلي", "msg": "جدار الحماية Anti-Cheat يعمل بكفاءة 100% 🛡️"}
    ]

# 1. صفحة تسجيل الدخول الرسمية للعبة غزة الحربية
if not st.session_state.logged_in:
    st.title("💥 لعبة غزة الحربية (Gaza Warfare)")
    st.subheader("🔒 النظام المركزي لإدارة السيرفرات العالمية")
    st.image("https://unsplash.com", 
             caption="⚔️ استعد لدخول ساحة المعركة الشرسة", use_container_width=True)
    
    username_input = st.text_input("👤 اسم المستخدم المعتمد:", value="waseem")
    password_input = st.text_input("🔑 كلمة المرور السرية:", type="password", value="123")
    
    if st.button("🚀 الولوج إلى السيرفر الآمن"):
        if username_input == ADMIN_USERNAME and password_input == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ خطأ أمني: بيانات الدخول غير صحيحة!")

# 2. لوحة التحكم واللعب الشاملة بعد تسجيل الدخول بنجاح
else:
    col_header, col_logout = st.columns()
    with col_header:
        st.title("⚔️ لوحة تحكم لعبة غزة الحربية (Gaza Warfare)")
        st.subheader("👑 رئيس السيرفرات والمطور الرئيسي: المطور وسيم")
    with col_logout:
        if st.button("🚪 مغادرة السيرفر"):
            st.session_state.logged_in = False
            st.rerun()
            
    st.write("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎮 العب الآن (Play Game)",
        "🕹️ محاكي السيرفر",
        "🗺️ الخرائط والزون", 
        "💎 شحن الـ Coins", 
        "🏆 رويال باس (Premium)",
        "💬 شات المطورين",
        "🛡️ مكافحة الهاكرز"
    ])

    # قسم اللعب المباشر - كود اللعبة المدمج يعمل باللمس على الموبايل
    with tab1:
        st.subheader("🎯 ساحة القتال المباشرة - لعبة غزة الحربية")
        st.write("استخدم أزرار التحكم باللمس أسفل الشاشة لتحريك اللاعب وإطلاق النار وتدمير الأهداف القادمة:")
        
        game_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
            <style>
                body { margin: 0; background: #111; color: white; font-family: sans-serif; text-align: center; touch-action: none; }
                canvas { background: #222; display: block; margin: 10px auto; border: 2px solid #FFCC00; max-width: 100%; border-radius: 8px; }
                .controls { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 320px; margin: 15px auto; }
                button { background: #FFCC00; color: #111; font-weight: bold; border: none; padding: 15px; border-radius: 8px; font-size: 18px; }
                button:active { background: #E6B800; }
                .fire-btn { grid-column: span 3; background: #FF3333; color: white; }
                #score-board { font-size: 20px; color: #FFCC00; font-weight: bold; margin-top: 5px; }
            </style>
        </head>
        <body>
            <div id="score-board">🎯 الكيلز (Kills): <span id="score">0</span></div>
            <canvas id="gameCanvas" width="400" height="300"></canvas>
            
            <div class="controls">
                <button id="btnLeft">⬅️ يسار</button>
                <button id="btnJump">🦘 قفز</button>
                <button id="btnRight">يمين ➡️</button>
                <button id="btnFire" class="fire-btn">🔥 إطلاق نار (FIRE)</button>
            </div>

            <script>
                const canvas = document.getElementById("gameCanvas");
                const ctx = canvas.getContext("2d");

                let player = { x: 50, y: 230, width: 25, height: 40, vy: 0, jumping: false };
                let bullets = [];
                let enemies = [];
                let score = 0;

                document.getElementById("btnLeft").addEventListener("touchstart", (e) => { e.preventDefault(); player.x -= 20; });
                document.getElementById("btnRight").addEventListener("touchstart", (e) => { e.preventDefault(); player.x += 20; });
                document.getElementById("btnJump").addEventListener("touchstart", (e) => {
                    e.preventDefault();
                    if(!player.jumping) { player.vy = -12; player.jumping = true; }
                });
                document.getElementById("btnFire").addEventListener("touchstart", (e) => {
                    e.preventDefault();
                    bullets.push({ x: player.x + 25, y: player.y + 15, speed: 7 });
                });

                function spawnEnemy() {
                    if (Math.random() < 0.02) {
                        enemies.push({ x: 400, y: 240, width: 20, height: 30, speed: 2 });
                    }
                }

                function update() {
                    player.vy += 0.6;
                    player.y += player.vy;
                    if(player.y > 230) { player.y = 230; player.vy = 0; player.jumping = false; }
                    if(player.x < 0) player.x = 0;
                    if(player.x > 375) player.x = 375;

                    bullets.forEach((b, index) => {
                        b.x += b.speed;
                        if(b.x > 400) bullets.splice(index, 1);
                    });

                    enemies.forEach((e, ei) => {
                        e.x -= e.speed;
                        if(e.x < 0) enemies.splice(ei, 1);

                        bullets.forEach((b, bi) => {
                            if(b.x > e.x && b.x < e.x + e.width && b.y > e.y && b.y < e.y + e.height) {
                                enemies.splice(ei, 1);
                                bullets.splice(bi, 1);
                                score += 1;
                                document.getElementById("score").innerText = score;
                            }
                        });
                    });

                    spawnEnemy();
                }

                function draw() {
                    ctx.clearRect(0, 0, 400, 300);
                    ctx.fillStyle = "#553311";
                    ctx.fillRect(0, 270, 400, 300);
                    ctx.fillStyle = "#2E7D32";
                    ctx.fillRect(player.x, player.y, player.width, player.height);
                    ctx.fillStyle = "#000";
                    ctx.fillRect(player.x + 20, player.y + 15, 15, 6);
                    ctx.fillStyle = "#FFD700";
                    bullets.forEach(b => ctx.fillRect(b.x, b.y, 8, 4));
                    ctx.fillStyle = "#C62828";
                    enemies.forEach(e => ctx.fillRect(e.x, e.y, e.width, e.height));
                }

                function gameLoop() {
                    update();
                    draw();
                    requestAnimationFrame(gameLoop);
                }

                gameLoop();
            </script>
        </body>
        </html>
        """
        components.html(game_html, height=520, scrolling=False)

    # الأقسام الأخرى لإدارة السيرفر
    with tab2:
        st.subheader("🕹️ محاكي قتال غزة الحربية الافتراضي (السيرفر)")
        if st.button("🔥 ابدأ معركة تجريبية في الخلفية"):
            st.info("✈️ السيرفر يرسل الآن طائرة إمداد فوق ساحة الصمود...")
            st.success("☠️ تم تحديث بيانات المعركة التجريبية بنجاح!")
            st.balloons()

    with tab3:
        st.subheader("⚙️ إدارة غرف المعارك الحالية")
        map_name = st.selectbox("🗺️ اختر خريطة المواجهة الحالية:", ["ساحة الصمود", "المدينة المدمرة"])
        air_drop_rate = st.slider("✈️ معدل نزول صناديق الإمداد:", 1, 5, 3)
        if st.button("💾 حفظ وتطبيق إعدادات الخريطة فوراً"):
            st.success("✔️ تم تحديث خريطة السيرفر بنجاح!")

    with tab4:
        st.subheader("💎 نظام شحن وتوليد العملات للّاعبين")
        player_id = st.text_input("🆔 أدخل رقم حساب اللاعب (Player ID):")
        uc_amount = st.selectbox("💵 اختر كمية الـ War Coins:", ["300 Coins", "660 Coins", "1800 Coins"])
        if st.button("⚡ إرسال العملات لحساب اللاعب"):
            st.success(f"🎉 تم بنجاح إرسال {uc_amount} إلى حساب اللاعب {player_id}!")

    with tab5:
        st.subheader("🏆 نظام تفعيل بطاقات الرويال باس الذهبي (Premium Pass)")
        p_id = st.text_input("🆔 أدخل ID اللاعب المراد ترقيته:")
        if st.button("👑 تفعيل الرويال باس فوراً"):
            st.success(f"🚀 مبروك! تم ترقية حساب اللاعب {p_id} الذهبي المطور!")

    with tab6:
        st.subheader("💬 صندوق دردشة طاقم إدارة لعبة غزة الحربية")
        for chat in st.session_state.chat_history:
            st.text(f"👤 {chat['user']}: {chat['msg']}")

    with tab7:
        st.subheader("🛡️ جدار حماية غزة الحربية (Anti-Cheat)")
        suspect_id = st.text_input("🚫 أدخل ID اللاعب المخالف:")
        if st.button("🔨 طرد وبند اللاعب المخالف"):
            st.error(f"🔒 تم طرد الحساب {suspect_id} بنجاح من اللعبة بواسطة المطور وسيم.")

st.write("---")
st.caption("حقوق التطوير والبرمجة بالكامل محفوظة للمطور وسيم © 2026 | Gaza Warfare Project")
    
