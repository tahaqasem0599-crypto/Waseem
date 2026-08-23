import streamlit as st
import streamlit.components.v1 as com

# إعدادات الصفحة
st.set_page_config(page_title='الملحمي', layout='wide')

# تحسين مظهر الواجهة بدون علامات اقتباس ثلاثية
st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

st.title('🛡️ المدرعة: الإصدار السينمائي الأخير')
st.write('🚀 النسخة المطورّة جاهزة للعمل واللعب!')

# بناء كود اللعبة بأمان كامل عبر دمج نصوص عادية
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#0f172a;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;overflow:hidden;}'
h += '#game-container{position:relative;width:95vw;max-width:500px;height:75vh;max-height:600px;background:#020617;border:3px solid #38bdf8;border-radius:16px;overflow:hidden;}'
h += 'canvas{display:block;width:100%;height:100%;}.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.score-bar{display:flex;justify-content:space-between;padding:12px 20px;color:#fff;font-size:18px;font-weight:bold;}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.95);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;}'
h += '.btn{background:#0ea5e9;color:white;border:none;padding:14px 40px;font-size:20px;font-weight:bold;border-radius:30px;cursor:pointer;margin-top:15px;}'
h += '.controls{display:flex;width:95vw;max-width:500px;justify-content:space-between;margin-top:10px;pointer-events:auto;gap:10px;}'
h += '.ctrl-btn{flex:1;background:#1e293b;border:2px solid #475569;color:white;padding:15px;font-size:18px;font-weight:bold;border-radius:12px;text-align:center;}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer"><div class="score-bar"><div id="scoreDisplay">النقاط: 0</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#38bdf8;margin:0;">🛡️ معركة المدرعة</h1><button class="btn" onclick="startGame()">إطلاق المعركة</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;">💥 انتهت المعركة</h1><button class="btn" onclick="startGame()">إعادة</button></div></div></div>'

h += '<div class="controls"><div class="ctrl-btn" id="btnLeft">⬅️ يمين</div><div class="ctrl-btn" id="btnFire" style="background:#0284c7;">🔥</div><div class="ctrl-btn" id="btnRight">يسار ➡️</div></div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");let player,bullets,enemies,score,lives,gameActive;let moveLeft=false,moveRight=false,isFiring=false;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setup=(b,p,r)=>{b.addEventListener("touchstart",(e)=>{e.preventDefault();p();});b.addEventListener("touchend",(e)=>{e.preventDefault();r();});b.addEventListener("mousedown",p);b.addEventListener("mouseup",r);};'
h += 'setup(document.getElementById("btnLeft"),()=>moveLeft=true,()=>moveLeft=false);setup(document.getElementById("btnRight"),()=>moveRight=true,()=>moveRight=false);setup(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'
h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:canvas.width/2-20,y:canvas.height-50,w:40,h:25,s:5};bullets=[];enemies=[];score=0;lives=3;gameActive=true;updateUI();animate();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="النقاط: "+score;document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'
h += 'function spawn(){if(!gameActive)return;enemies.push({x:Math.random()*(canvas.width-30),y:-30,w:30,h:30,s:2});setTimeout(spawn,1200);}setTimeout(spawn,1000);'
h += 'let last=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);if(moveLeft&&player.x>0)player.x-=player.s;if(moveRight&&player.x<canvas.width-player.w)player.x+=player.s;'
h += 'ctx.fillStyle="#38bdf8";ctx.fillRect(player.x,player.y,player.w,player.h);let now=Date.now();if(isFiring&&now-last>250){bullets.push({x:player.x+player.w/2-3,y:player.y-10,w:6,h:12,s:7});last=now;}'
h += 'ctx.fillStyle="#f59e0b";bullets.forEach((b,i)=>{b.y-=b.s;ctx.fillRect(b.x,b.y,b.w,b.h);if(b.y<0)bullets.splice(i,1);});'
h += 'enemies.forEach((e,ei)=>{e.y+=e.s;ctx.fillStyle="#ef4444";ctx.fillRect(e.x,e.y,e.w,e.h);'
h += 'if(e.x<player.x+player.w&&e.x+e.w>player.x&&e.y<player.y+player.h&&e.y+e.h>player.y){enemies.splice(ei,1);lives--;updateUI();if(lives<=0)go();}'
h += 'if(e.y>canvas.height){enemies.splice(ei,1);lives--;updateUI();if(lives<=0)go();}'
h += 'bullets.forEach((b,bi)=>{if(b.x<e.x+e.w&&b.x+b.w>e.x&&b.y<e.y+e.h&&b.y+b.h>e.y){enemies.splice(ei,1);bullets.splice(bi,1);score+=10;updateUI();}});});'
h += 'requestAnimationFrame(animate);}function go(){gameActive=false;document.getElementById("gameOverMenu").style.display="flex";}</script></body></html>'

# تشغيل اللعبة مباشرة
com.html(h, height=660, scrolling=False)
