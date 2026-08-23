import streamlit as st
import streamlit.components.v1 as com

# 1. إعدادات الصفحة وتحسين العرض
st.set_page_config(
    page_title="الملحمي",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. تحسين مظهر واجهة Streamlit وإلغاء الفراغات
st.markdown("""
    <style>
        body, .main, .block-container { 
            padding: 0 !important; 
            margin: 0 !important;
            background-color: #0f172a;
        }
        iframe { 
            border: none; 
            border-radius: 12px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ المدرعة: الإصدار السينمائي الأخير")
st.write("🚀 النسخة المطورّة جاهزة للعمل واللعب بجودة عالية وبدون توقف!")

# 3. تقسيم كود الـ HTML إلى أجزاء لمنع خطأ علامات الاقتباس الثلاثية نهائياً
html_start = """<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; user-select: none; }
        body { 
            margin: 0; padding: 0; 
            background: #0f172a; 
            font-family: system-ui, sans-serif;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            min-height: 100vh; overflow: hidden;
        }
        #game-container { 
            position: relative; 
            width: 95vw; max-width: 500px;
            height: 75vh; max-height: 600px;
            background: #020617; 
            border: 3px solid #38bdf8; border-radius: 16px;
            overflow: hidden; box-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
        }
        canvas { display: block; width: 100%; height: 100%; }
        .ui-layer { 
            position: absolute; top: 0; left: 0; 
            width: 100%; height: 100%; pointer-events: none; 
        }
        .score-bar { 
            display: flex; justify-content: space-between; 
            padding: 12px 20px; color: #fff;
            font-size: 18px; font-weight: bold;
            background: linear-gradient(to bottom, rgba(15,23,42,0.8), transparent);
        }
        .menu-screen { 
            position: absolute; top: 0; left: 0; 
            width: 100%; height: 100%; 
            background: rgba(15, 23, 42, 0.95);
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            color: white; pointer-events: auto;
            text-align: center; padding: 20px;
        }
        .btn { 
            background: linear-gradient(135deg, #38bdf8, #0ea5e9); 
            color: white; border: none;
            padding: 14px 40px; font-size: 20px; font-weight: bold;
            border-radius: 30px; cursor: pointer;
            transition: transform 0.1s; margin-top: 15px;
        }
        .btn:active { transform: scale(0.95); }
        .controls {
            display: flex; width: 95vw; max-width: 500px;
            justify-content: space-between; margin-top: 10px;
            pointer-events: auto; gap: 10px;
        }
        .ctrl-btn {
            flex: 1; background: #1e293b; border: 2px solid #475569;
            color: white; padding: 15px; font-size: 18px; font-weight: bold;
            border-radius: 12px; text-align: center;
        }
    </style>
</head>
<body>"""

html_body = """    <div id="game-container">
        <canvas id="gameCanvas"></canvas>
        <div class="ui-layer">
            <div class="score-bar">
                <div id="scoreDisplay">النقاط: 0</div>
                <div id="liveDisplay">❤️ ❤️ ❤️</div>
            </div>
            
            <div id="mainMenu" class="menu-screen">
                <h1 style="color: #38bdf8; margin: 0 0 10px 0; font-size: 28px;">🛡️ معركة المدرعة الملحمية</h1>
                <p style="color: #94a3b8; margin: 0 0 20px 0; font-size: 14px;">دمر مدرعات الأعداء وحافظ على طاقتك!</p>
                <button class="btn" onclick="startGame()">إطلاق المعركة</button>
            </div>

            <div id="gameOverMenu" class="menu-screen" style="display: none;">
                <h1 style="color: #ef4444; margin-bottom: 5px;">💥 انتهت المعركة</h1>
                <p id="finalScore" style="font-size: 18px; color: #cbd5e1;"></p>
                <button class="btn" style="background: #ef4444;" onclick="startGame()">إعادة المحاولة</button>
            </div>
        </div>
    </div>

    <div class="controls">
        <div class="ctrl-btn" id="btnLeft">⬅️ يمين</div>
        <div class="ctrl-btn" id="btnFire" style="background: #0284c7; border-color: #38bdf8;">🔥 إطلاق</div>
        <div class="ctrl-btn" id="btnRight">يسار ➡️</div>
    </div>"""

html_script = """    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        
        let player, bullets, enemies, particles, score, lives, gameActive;
        let moveLeft = false, moveRight = false, isFiring = false;

        function resize() {
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        const setupTouch = (btn, pressCallback, releaseCallback) => {
            btn.addEventListener('touchstart', (e) => { e.preventDefault(); pressCallback(); });
            btn.addEventListener('touchend', (e) => { e.preventDefault(); releaseCallback(); });
            btn.addEventListener('mousedown', pressCallback);
            btn.addEventListener('mouseup', releaseCallback);
        };
        setupTouch(document.getElementById('btnLeft'), () => moveLeft = true, () => moveLeft = false);
        setupTouch(document.getElementById('btnRight'), () => moveRight = true, () => moveRight = false);
        setupTouch(document.getElementById('btnFire'), () => isFiring = true, () => isFiring = false);

        window.addEventListener('keydown', (e) => {
            if(e.key === 'ArrowLeft' || e.key === 'a') moveLeft = true;
            if(e.key === 'ArrowRight' || e.key === 'd') moveRight = true;
            if(e.key === ' ' || e.key === 'Enter') isFiring = true;
        });
        window.addEventListener('keyup', (e) => {
            if(e.key === 'ArrowLeft' || e.key === 'a') moveLeft = false;
            if(e.key === 'ArrowRight' || e.key === 'd') moveRight = false;
            if(e.key === ' ' || e.key === 'Enter') isFiring = false;
        });

        function startGame() {
            resize();
            document.getElementById('mainMenu').style.display = 'none';
            document.getElementById('gameOverMenu').style.display = 'none';
            
            player = { x: canvas.width / 2 - 20, y: canvas.height - 50, width: 40, height: 25, speed: 5 };
            bullets = [];
            enemies = [];
            particles = [];
            score = 0;
            lives = 3;
            gameActive = true;
            
            updateUI();
            animate();
        }

        function updateUI() {
            document.getElementById('scoreDisplay').innerText = `النقاط: ${score}`;
            document.getElementById('liveDisplay').innerText = '❤️ '.repeat(lives);
        }

        function spawnEnemy() {
            if (!gameActive) return;
            let size = Math.random() * 20 + 20;
            enemies.push({
                x: Math.random() * (canvas.width - size),
                y: -size,
                width: size,
                height: size,
                speed: Math.random() * 1.5 + 1.5
            });
            setTimeout(spawnEnemy, Math.max(600, 1500 - score * 10));
        }

        function createExplosion(x, y, color) {
            for(let i=0; i<10; i++) {
                particles.push({
                    x: x, y: y,
                    vx: (Math.random() - 0.5) * 4,
                    vy: (Math.random() - 0.5) * 4,
                    radius: Math.random() * 3 + 1,
                    alpha: 1,
                    color: color
                });
            }
        }

        let lastFire = 0;
        function animate() {
            if (!gameActive) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (moveLeft && player.x > 0) player.x -= player.speed;
            if (moveRight && player.x < canvas.width - player.width) player.x += player.speed;

            ctx.fillStyle = '#38bdf8';
            ctx.fillRect(player.x, player.y, player.width, player.height);
            ctx.fillStyle = '#0ea5e9';
            ctx.fillRect(player.x + player.width/2 - 5, player.y - 10, 10, 10);

            let now = Date.now();
            if (isFiring && now - lastFire > 250) {
                bullets.push({ x: player.x + player.width / 2 - 3, y: player.y - 10, width: 6, height: 12, speed: 7 });
                lastFire = now;
            }

            bullets.forEach((bullet, index) => {
                bullet.y -= bullet.speed;
                ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
                if (bullet.y < 0) bullets.splice(index, 1);
            });

            enemies.forEach((enemy, eIndex) => {
                enemy.y += enemy.speed;
                
                ctx.fillStyle = '#ef4444';
                ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
                ctx.fillStyle = '#991b1b';
                ctx.fillRect(enemy.x + 4, enemy.y + 4, enemy.width - 8, enemy.height - 8);

                if (enemy.x < player.x + player.width && enemy.x + enemy.width > player.x &&
                    enemy.y < player.y + player.height && enemy.y + enemy.height > player.y) {
                    enemies.splice(eIndex, 1);
                    createExplosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2, '#ef4444');
                    lives--;
                    updateUI();
                    if(lives <= 0) gameOver();
                }

