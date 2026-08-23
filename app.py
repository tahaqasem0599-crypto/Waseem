import streamlit as st
import streamlit.components.v1 as com

st.set_page_config(page_title='🛡️ كتيبة الصمود', layout='wide')

# إلغاء الفراغات نهائياً
st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;background:#0d0e12;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

# كود اللعبة البسيط والسريع جداً لضمان الفتح الفوري بدون شاشة بيضاء
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#0d0e12;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif;}'
h += '#game-container{position:relative;width:95vw;max-width:480px;height:65vh;max-height:500px;background:#27272a;border:4px solid #10b981;border-radius:20px;overflow:hidden;box-shadow:0 0 25px rgba(16,185,129,0.3);}'
h += 'canvas{display:block;width:100%;height:100%;}.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.hud{display:flex;justify-content:space-between;padding:12px;color:#fff;font-size:16px;font-weight:bold;background:rgba(0,0,0,0.8);border-bottom:2px solid #10b981;}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(10,15,25,0.98);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;text-align:center;padding:20px;}'
h += '.btn{background:linear-gradient(135deg,#10b981,#ef4444);color:white;border:none;padding:14px 40px;font-size:20px;font-weight:bold;border-radius:30px;cursor:pointer;box-shadow:0 5px 20px rgba(16,185,129,0.4);}'
h += '.controls-grid{display:grid;grid-template-columns:repeat(3,1fr);width:95vw;max-width:480px;margin-top:10px;gap:8px;pointer-events:auto;}'
h += '.ctrl-btn{background:#1f2937;border:2px solid #374151;color:#10b981;padding:15px;font-size:18px;font-weight:bold;border-radius:14px;text-align:center;}'
h += '#btnFire{grid-column:span 3;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border:none;padding:16px;font-size:20px;}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer">'
h += '<div class="hud"><div id="scoreDisplay">خسائر الأعداء: 0</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#10b981;margin:0 0 10px 0;font-size:26px;">🛡️ كتيبة الفرسان (PUBG 2D)</h1><p style="color:#9ca3af;margin:0 0 25px 0;font-size:14px;">قد فريق العُصب الخضراء وتصدّى للمليشيات وسط الركام!</p><button class="btn" onclick="startGame()">ابدأ المعركة ⚡</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;margin:0 0 10px 0;">💥 انتهت المواجهة</h1><button class="btn" onclick="startGame()">إعادة الانتشار</button></div>'
h += '</div></div>'

h += '<div class="controls-grid">'
h += '<div class="ctrl-btn" id="btnUp">⬆️ تقدم</div><div class="ctrl-btn" id="btnLeft">◀ يمين</div><div class="ctrl-btn" id="btnRight">يسار ▶</div>'
h += '<div class="ctrl-btn" id="btnDown" style="grid-column:span 3;">⬇️ تراجع</div>'
h += '<div class="ctrl-btn" id="btnFire">🔥 إطلاق النيران التكتيكي</div>'
h += '</div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");'
h += 'let player,bullets,enemyBullets,enemies,obstacles,score,lives,gameActive;let mvUp=false,mvDown=false,mvLeft=false,mvRight=false,isFiring=false;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setupTouch=(btn,press,release)=>{btn.addEventListener("touchstart",(e)=>{e.preventDefault();press();});btn.addEventListener("touchend",(e)=>{e.preventDefault();release();});btn.addEventListener("mousedown",press);btn.addEventListener("mouseup",release);};'
h += 'setupTouch(document.getElementById("btnUp"),()=>mvUp=true,()=>mvUp=false);setupTouch(document.getElementById("btnDown"),()=>mvDown=true,()=>mvDown=false);'
h += 'setupTouch(document.getElementById("btnLeft"),()=>mvLeft=true,()=>mvLeft=false);setupTouch(document.getElementById("btnRight"),()=>mvRight=true,()=>mvRight=false);'
h += 'setupTouch(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'

h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:canvas.width/2,y:canvas.height-60,r:14,s:4,angle:-Math.PI/2};'
h += 'bullets=[];enemyBullets=[];enemies=[];score=0;lives=3;gameActive=true;'
h += 'obstacles=[{x:40,y:100,w:60,h:30,c:"#7f1d1d"},{x:canvas.width-100,y:180,w:70,h:35,c:"#4b5563"}];'
h += 'updateUI();animate();spawnEnemy();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="خسائر الأعداء: "+score;document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'

h += 'function spawnEnemy(){if(!gameActive)return;if(enemies.length<3){enemies.push({x:Math.random()*canvas.width,y:-20,r:12,s:1.5,lastFire:Date.now()});}setTimeout(spawnEnemy,2000);}'

h += 'function drawP(x,y,r,angle,hasBand,isEnemy){'
h += 'ctx.fillStyle=isEnemy?"#1e1b4b":"#064e3b";ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();'
h += 'ctx.fillStyle="#fbcfe8";ctx.beginPath();ctx.arc(x,y,r-4,0,Math.PI*2);ctx.fill();'
h += 'if(hasBand){ctx.fillStyle="#22c55e";ctx.beginPath();ctx.arc(x,y,r-2,angle-0.4,angle+0.4);ctx.lineWidth=4;ctx.strokeStyle="#22c55e";ctx.stroke();}'
h += 'ctx.fillStyle="#000";ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.fillRect(0,-2,12,4);ctx.restore();}'

h += 'let lastPlayerFire=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);'
h += 'obstacles.forEach(o=>{ctx.fillStyle=o.c;ctx.fillRect(o.x,o.y,o.w,o.h);});'

h += 'let mx=0,my=0;if(mvUp)my-=player.s;if(mvDown)my+=player.s;if(mvLeft)mx-=player.s;if(mvRight)mx+=player.s;'
h += 'player.x+=mx;player.y+=my;if(mx!==0||my!==0)player.angle=Math.atan2(my,mx);'
h += 'if(player.x<15)player.x=15;if(player.x>canvas.width-15)player.x=canvas.width-15;if(player.y<15)player.y=15;if(player.y>canvas.height-15)player.y=canvas.height-15;'

h += 'drawP(player.x,player.y,player.r,player.angle,true,false);'
h += 'drawP(player.x-40,player.y+20,player.r-2,player.angle,true,false);drawP(player.x+40,player.y+20,player.r-2,player.angle,true,false);'

h += 'let now=Date.now();if(isFiring&&now-lastPlayerFire>250){bullets.push({x:player.x,y:player.y,vx:Math.cos(player.angle)*8,vy:Math.sin(player.angle)*8});bullets.push({x:player.x-40,y:player.y+20,vx:Math.cos(player.angle)*8,vy:Math.sin(player.angle)*8});bullets.push({x:player.x+40,y:player.y+20,vx:Math.cos(player.angle)*8,vy:Math.sin(player.angle)*8});lastPlayerFire=now;}'

h += 'bullets.forEach((b,bi)=>{b.x+=b.vx;b.y+=b.vy;ctx.fillStyle="#f59e0b";ctx.fillRect(b.x,b.y,4,4);if(b.x<0||b.x>canvas.width||b.y<0||b.y>canvas.height)bullets.splice(bi,1);});'
h += 'enemyBullets.forEach((eb,ebi)=>{eb.x+=eb.vx;eb.y+=eb.vy;ctx.fillStyle="#ef4444";ctx.fillRect(eb.x,eb.y,4,4);if(eb.x>player.x-14&&eb.x<player.x+14&&eb.y>player.y-14&&eb.y<player.y+14){enemyBullets.splice(ebi,1);lives--;updateUI();if(lives<=0)go();};if(eb.x<0||eb.x>canvas.width||eb.y<0||eb.y>canvas.height)enemyBullets.splice(ebi,1);});'

h += 'enemies.forEach((e,ei)=>{let dx=player.x-e.x,dy=player.y-e.y;let eAng=Math.atan2(dy,dx);e.x+=Math.cos(eAng)*e.s;e.y+=Math.sin(eAng)*e.s;drawP(e.x,e.y,e.r,eAng,false,true);'
h += 'if(now-e.lastFire>1500){enemyBullets.push({x:e.x,y:e.y,vx:Math.cos(eAng)*4,vy:Math.sin(eAng)*4});e.lastFire=now;}'
h += 'bullets.forEach((b,bi)=>{if(b.x>e.x-12&&b.x<e.x+12&&b.y>e.y-12&&b.y<e.y+12){bullets.splice(bi,1);enemies.splice(ei,1);score+=10;updateUI();}});});'

h += 'requestAnimationFrame(animate);}function go(){gameActive=false;document.getElementById("gameOverMenu").style.display="flex";}</script></body></html>'

com.html(h, height=620, scrolling=False)
