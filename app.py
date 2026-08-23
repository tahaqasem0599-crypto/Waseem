import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="المدرعة 101: الإصدار الملحمي", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    body, .main, .block-container { background-color: #02040a; color: #38bdf8; direction: rtl; text-align: center; padding: 0; }
    iframe { border: none; border-radius: 15px; box-shadow: 0 0 50px rgba(56, 189, 248, 0.4); }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ وحدة الطوارئ المدرعة: الإصدار السينمائي الأخير 🇵🇸")
st.write("تم إضافة النيازك الجوية، دروع الحماية، ومحرك الأكشن المطور لجني الأرباح بدون توقف!")

# محرك الألعاب المتكامل والأخير (HTML5 Canvas + Shield System + Meteor Storm + Storage)
game_html = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; background: #02040a; font-family: sans-serif; overflow: hidden; display: flex; justify-content: center; align-items: center; height: 100vh; color: white; }
        #canvas-container { position: relative; width: 360px; height: 540px; border: 3px solid #38bdf8; border-radius: 12px; overflow: hidden; background: #070a13; }
        canvas { display: block; background: #04060c; }
        .ui-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 15px; box-sizing: border-box; pointer-events: none; }
        .interactive { pointer-events: auto; }
        .score-bar { display: flex; justify-content: space-between; font-size: 16px; font-weight: bold; color: #38bdf8; text-shadow: 0 0 8px rgba(56,189,248,0.6); }
        .menu-screen { position: absolute; width: 100%; height: 100%; background: rgba(2, 4, 10, 0.95); display: flex; flex-direction: column; justify-content: center; align-items: center; top: 0; left: 0; }
        .btn { background: #38bdf8; color: #02040a; border: none; padding: 14px 35px; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; margin: 10px; box-shadow: 0 0 20px rgba(56, 189, 248, 0.5); transition: 0.2s; }
        .btn:hover { background: #0ea5e9; transform: scale(1.05); }
        .hidden { display: none !important; }
        .controls-hint { color: #94a3b8; font-size: 12px; margin-top: 15px; text-align: center; }
    </style>
</head>
<body>

<div id="canvas-container">
    <canvas id="gameCanvas" width="360" height="540"></canvas>
    
    <div class="ui-layer">
        <div class="score-bar">
            <div>⚙️ التدمير: <span id="ui-score">0</span></div>
            <div id="shield-indicator" style="color: #34d399; display:none;">🛡️ الدرع نشط!</div>
            <div style="color: #FFD700;">💎 الماس: <span id="ui-diamonds">130</span></div>
        </div>
        <div class="controls-hint">💡 انقر للتبديل بين المسارات وإطلاق ليزر النيون تلقائياً!</div>
    </div>

    <!-- شاشة البدء -->
    <div id="main-menu" class="menu-screen">
        <h2 style="color: #38bdf8; font-size: 26px; text-shadow: 0 0 15px rgba(56,189,248,0.4);">المدرعة: خط الدفاع الأخير</h2>
        <p style="color: #66fcf1; font-size: 14px; font-weight: bold; margin-bottom: 5px;">الإصدار السينمائي المتكامل 🎬</p>
        <p style="color: #94a3b8; font-size: 13px; margin: 10px 25px; text-align:center; line-height:1.5;">دمر روبوتات الغزو، تفادَ النيازك الساقطة، والقط درع الطاقة للبقاء على قيد الحياة والربح بدون نت!</p>
        <button class="btn interactive" onclick="startGame()">تشغيل المحرك والقتال ⚔️</button>
    </div>

    <!-- شاشة الخسارة -->
    <div id="game-over-screen" class="menu-screen hidden">
        <h2 style="color: #ef4444; font-size: 24px;">💥 تحطمت دروع المركبة!</h2>
        <p id="ad-text" style="color: #cbd5e1; font-size:14px;">شاهد الدعم التكتيكي (الإعلان) لإعادة الشحن وكسب 50 ماسة</p>
        <button id="ad-btn" class="btn interactive" onclick="playRewardedAd()">إعادة التموين الفوري 💰</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    let diamonds = localStorage.getItem('waseem_diamonds') ? parseInt(localStorage.getItem('waseem_diamonds')) : 130;
    document.getElementById('ui-diamonds').innerText = diamonds;

    let gameActive = false;
    let audioCtx = null;
    let gameLoopId = null;
    
    let vehicle = { x: 40, y: 380, width: 65, height: 35, targetY: 380, speed: 12, hasShield: false, shieldTime: 0 };
    let lasers = [];
    let enemies = [];
    let meteors = [];
    let powerups = [];
    let score = 0;

    function initAudio() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            startMusicLoop();
        }
    }

    function startMusicLoop() {
        setInterval(() => {
            if (!gameActive) return;
            playTone(95, "triangle", 0.2, 0.15);
            setTimeout(() => playTone(130, "triangle", 0.2, 0.15), 250);
        }, 450);
    }

    function playTone(freq, type, duration, vol) {
        if (!audioCtx) return;
        try {
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = type; osc.frequency.value = freq;
            gain.gain.setValueAtTime(vol, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + duration);
        } catch(e){}
    }

    function startGame() {
        initAudio();
        document.getElementById('main-menu').classList.add('hidden');
        document.getElementById('game-over-screen').classList.add('hidden');
        gameActive = true;
        score = 0;
        enemies = [];
        lasers = [];
        meteors = [];
        powerups = [];
        vehicle.y = 380;
        vehicle.targetY = 380;
        vehicle.hasShield = false;
        document.getElementById('ui-score').innerText = score;
        document.getElementById('shield-indicator').style.display = "none";
        
        canvas.addEventListener('touchstart', handleAction);
        canvas.addEventListener('mousedown', handleAction);
        
        if(!gameLoopId) gameLoopId = requestAnimationFrame(updateGame);
    }

    function handleAction(e) {
        if (!gameActive) return;
        vehicle.targetY = (vehicle.targetY === 380) ? 240 : 380;
        playTone(580, "sawtooth", 0.08, 0.1);
        lasers.push({ x: vehicle.x + vehicle.width, y: vehicle.y + 15, speed: 13, width: 22, height: 4 });
        e.preventDefault();
    }

    function updateGame() {
        if (!gameActive) { gameLoopId = null; return; }
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // رسم الطريق الفخم
        ctx.fillStyle = "#090d16"; ctx.fillRect(0, 190, canvas.width, 260);
        ctx.fillStyle = "#1e293b"; ctx.fillRect(0, 315, canvas.width, 6);

        // حركة المركبة الانسيابية
        let dy = vehicle.targetY - vehicle.y;
        if (Math.abs(dy) > 2) vehicle.y += Math.sign(dy) * vehicle.speed;

        // إدارة مؤقت درع الحماية
        if (vehicle.hasShield) {
            vehicle.shieldTime--;
            if (vehicle.shieldTime <= 0) {
                vehicle.hasShield = false;
                document.getElementById('shield-indicator').style.display = "none";
            }
        }

        // رسم المدرعة الفخمة
        ctx.fillStyle = "#1e293b"; ctx.fillRect(vehicle.x, vehicle.y, vehicle.width, vehicle.height);
        ctx.fillStyle = "#38bdf8"; ctx.fillRect(vehicle.x + 45, vehicle.y + 5, 20, 10);
        ctx.fillStyle = "#ef4444"; ctx.fillRect(vehicle.x + 5, vehicle.y + 12, 10, 10);

        // رسم فقاعة درع الحماية إذا كانت نشطة
        if (vehicle.hasShield) {
            ctx.strokeStyle = "#34d399"; ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(vehicle.x + vehicle.width/2, vehicle.y + vehicle.height/2, 45, 0, 2*Math.PI);
            ctx.stroke();
        }

        // تحديث وحركة سلاح الليزر
        for (let i = lasers.length - 1; i >= 0; i--) {
            let l = lasers[i]; l.x += l.speed;
            ctx.fillStyle = "#22c55e"; ctx.fillRect(l.x, l.y, l.width, l.height);
            if (l.x > 360) lasers.splice(i, 1);
        }

        // توليد حركة النيازك الجوية الساقطة من الأعلى
        if (Math.random() < 0.015 && meteors.length < 2) {
            meteors.push({ x: Math.random() * 200 + 100, y: -20, speedY: 5, speedX: -2, radius: 12 });
        }

        // تحديث ورسم النيازك
        for (let i = meteors.length - 1; i >= 0; i--) {
            let m = meteors[i]; m.y += m.speedY; m.x += m.speedX;
            ctx.fillStyle = "#f97316"; ctx.beginPath(); ctx.arc(m.x, m.y, m.radius, 0, 2*Math.PI); ctx.fill();
            
            // تصادم النيزك مع المركبة
            let distVehicle = Math.hypot((vehicle.x + vehicle.width/2) - m.x, (vehicle.y + vehicle.height/2) - m.y);
            if (distVehicle < m.radius + 20) {
                meteors.splice(i, 1);
                if (vehicle.hasShield) {
                    playTone(200, "sine", 0.1, 0.2);
                } else {
                    endGame();
                }
                continue;
            }
            if (m.y > 540) meteors.splice(i, 1);
        }

        // توليد أيقونات درع الحماية العشوائية في الشارع
        if (Math.random() < 0.005 && powerups.length < 1) {
            let lanes =;
            powerups.push({ x: 360, y: lanes[Math.floor(Math.random()*2)] + 5, width: 25, height: 25 });
        }

        // تحديث ورسم الدروع والتقاطها
        for (let i = powerups.length - 1; i >= 0; i--) {
            let p = powerups[i]; p.x -= 4;
            ctx.fillStyle = "#34d399"; ctx.fillRect(p.x, p.y, p.width, p.height); // مربع أخضر نيون للدرع
            
            if (p.x < vehicle.x + vehicle.width && p.x + p.width > vehicle.x && p.y < vehicle.y + vehicle.height && p.y + p.height > vehicle.y) {
            
