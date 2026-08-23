import streamlit as st
import streamlit.components.v1 as com

st.set_page_config(page_title='🛡️ كتيبة الصمود', layout='wide')

st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;background:#06140c;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

st.title('🛡️ كتيبة الفرسان: محاكاة صمود شوارع المدينة')
st.write('🎮 أسلوب رماية تكتيكي: قُد فريقك بالعُصب الخضراء وتصدّى لآليات ومليشيات الأعداء وسط ركام وأزقة الشوارع!')

# كود اللعبة المصحح والمضمون 100% بدون أي تعليق أو شاشة بيضاء
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#0d0e12;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif;}'
h += '#game-container{position:relative;width:95vw;max-width:500px;height:68vh;max-height:520px;background:#27272a;border:4px solid #10b981;border-radius:24px;overflow:hidden;box-shadow:0 0 35px rgba(16,185,129,0.3);}'
h += 'canvas{display:block;width:100%;height:100%;}'
h += '.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.hud{display:flex;justify-content:space-between;padding:12px 15px;color:#fff;font-size:15px;font-weight:bold;background:rgba(0,0,0,0.8);border-bottom:2px solid #10b981;}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(10,15,25,0.98);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;text-align:center;padding:20px;}'
h += '.btn{background:linear-gradient(135deg,#10b981,#ef4444);color:white;border:none;padding:14px 40px;font-size:20px;font-weight:bold;border-radius:30px;cursor:pointer;box-shadow:0 5px 20px rgba(16,185,129,0.4);}'
h += '.controls-grid{display:grid;grid-template-columns:repeat(3,1fr);width:95vw;max-width:500px;margin-top:12px;gap:8px;pointer-events:auto;}'
h += '.ctrl-btn{background:#1f2937;border:2px solid #374151;color:#10b981;padding:14px;font-size:18px;font-weight:bold;border-radius:14px;text-align:center;}'
h += '#btnFire{grid-column:span 3;background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;border:none;box-shadow:0 4px 15px rgba(239,68,68,0.4);padding:16px;font-size:20px;}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer">'
h += '<div class="hud"><div id="scoreDisplay">خسائر الأعداء: 0</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#10b981;margin:0 0 10px 0;font-size:26px;text-shadow:0 0 15px #10b981;">🛡️ كتيبة الفرسان (PUBG 2D Mode)</h1><p style="color:#9ca3af;margin:0 0 25px 0;font-size:14px;line-height:1.5;">تحرك في كافة الاتجاهات وسط الركام وحطام السيارات، وقُد فريقك بالعُصب الخضراء لصد هجوم مليشيات التوغل الغازية!</p><button class="btn" onclick="startGame()">دخول الساحة والاشتباك ⚡</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;margin:0 0 10px 0;">💥 انتهت المواجهة</h1><p id="finalScore" style="font-size:17px;color:#d1d5db;margin:0 0 25px 0;"></p><button class="btn" style="background:linear-gradient(135deg,#10b981,#1f2937);" onclick="startGame()">إعادة الانتشار عسكرياً</button></div>'
h += '</div></div>'

h += '<div class="controls_zone"><div class="controls-grid">'
h += '<div class="ctrl-btn" id="btnUp">⬆️ تقدم</div><div class="ctrl-btn" id="btnLeft">◀ يمين</div><div class="ctrl-btn" id="btnRight">يسار ▶</div>'
h += '<div class="ctrl-btn" id="btnDown" style="grid-column:span 3;">⬇️ تراجع للخلف</div>'
h += '<div class="ctrl-btn" id="btnFire">🔥 إطلاق النيران (360 درجة)</div>'
h += '</div></div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");'
h += 'let player,allies,bullets,enemyBullets,enemies,obstacles,particles,score,lives,gameActive;let mvUp=false,mvDown=false,mvLeft=false,mvRight=false,isFiring=false;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setupTouch=(btn,press,release)=>{btn.addEventListener("touchstart",(e)=>{e.preventDefault();press();});btn.addEventListener("touchend",(e)=>{e.preventDefault();release();});btn.addEventListener("mousedown",press);btn.addEventListener("mouseup",release);};'
h += 'setupTouch(document.getElementById("btnUp"),()=>mvUp=true,()=>mvUp=false);setupTouch(document.getElementById("btnDown"),()=>mvDown=true,()=>mvDown=false);'
h += 'setupTouch(document.getElementById("btnLeft"),()=>mvLeft=true,()=>mvLeft=false);setupTouch(document.getElementById("btnRight"),()=>mvRight=true,()=>mvRight=false);'
h += 'setupTouch(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'

h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:canvas.width/2,y:canvas.height-80,r:14,s:4,angle:-Math.PI/2};'
h += 'allies=[{x:canvas.width/2-60,y:canvas.height-60,r:11,s:3.5,lastFire:0},{x:canvas.width/2+60,y:canvas.height-60,r:11,s:3.5,lastFire:0}];'
h += 'bullets=[];enemyBullets=[];enemies=[];particles=[];score=0;lives=3;gameActive=true;'
h += 'obstacles=[{x:40,y:120,w:70,h:35,type:"car",color:"#7f1d1d"},{x:canvas.width-120,y:200,w:80,h:40,type:"rubble",color:"#4b5563"},{x:canvas.width/2-40,y:280,w:80,h:25,type:"wall",color:"#1f2937"}];'
h += 'updateUI();animate();spawnEnemy();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="خسائر الأعداء: "+score;document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'

h += 'function spawnEnemy(){if(!gameActive)return;if(enemies.length<4){enemies.push({x:Math.random()*canvas.width,y:-20,r:12,s:1.2+Math.random()*0.8,lastFire:Date.now()});}setTimeout(spawnEnemy,1800);}'
h += 'function explode(x,y,color,count=12){for(let i=0;i<count;i++){let ang=Math.random()*Math.PI*2;particles.push({x:x,y:y,vx:Math.cos(ang)*Math.random()*4,vy:Math.sin(ang)*Math.random()*4,r:Math.random()*2.5+1,a:1,c:color});}}'

h += 'let lastPlayerFire=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);'
h += 'obstacles.forEach(o=>{ctx.fillStyle=o.color;ctx.fillRect(o.x,o.y,o.w,o.h);ctx.strokeStyle="#111";ctx.lineWidth=2;ctx.strokeRect(o.x,o.y,o.w,o.h);if(o.type==="car"){ctx.fillStyle="#111";ctx.fillRect(o.x+4,o.y-4,10,4);ctx.fillRect(o.x+o.w-14,o.y-4,10,4);}});'

h += 'let mx=0,my=0;if(mvUp)my-=player.s;if(mvDown)my+=player.s;if(mvLeft)mx-=player.s;if(mvRight)mx+=player.s;'
h += 'player.x+=mx;player.y+=my;if(mx!==0||my!==0)player.angle=Math.atan2(my,mx);'
h += 'if(player.x<15)player.x=15;if(player.x>canvas.width-15)player.x=canvas.width-15;if(player.y<15)player.y=15;if(player.y>canvas.height-15)player.y=canvas.height-15;'

h += 'obstacles.forEach(o=>{if(player.x+player.r>o.x&&player.x-player.r<o.x+o.w&&player.y+player.r>o.y&&player.y-player.r<o.y+o.h){player.x-=mx;player.y-=my;}});'

h += 'function drawP(x,y,r,angle,hasBand,isEnemy){'
h += 'ctx.fillStyle=isEnemy?"#1e1b4b":"#064e3b";ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();'
h += 'ctx.fillStyle="#fbcfe8";ctx.beginPath();ctx.arc(x,y,r-4,0,Math.PI*2);ctx.fill();'
h += 'if(hasBand){ctx.fillStyle="#22c55e";ctx.beginPath();ctx.arc(x,y,r-2,angle-0.5,angle+0.5);ctx.lineWidth=4;ctx.strokeStyle="#22c55e";ctx.stroke();}'
h += 'ctx.fillStyle="#000";ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.fillRect(0,-3,14,5);ctx.restore();}'

h += 'drawP(player.x,player.y,player.r,player.angle,true,false);'

h += 'let now=Date.now();allies.forEach(a=>{'
h += 'if(enemies.length>0){let target=enemies[0];let dx=target.x-a.x,dy=target.y-a.y;let ang=Math.atan2(dy,dx);a.x+=Math.cos(ang)*1.2;a.y+=Math.sin(ang)*1.2;'
h += 'obstacles.forEach(o=>{if(a.x+a.r>o.x&&a.x-a.r<o.x+o.w&&a.y+a.r>o.y&&a.y-a.r<o.y+o.h){a.x-=Math.cos(ang)*1.2;a.y-=Math.sin(ang)*1.2;}});'
h += 'drawP(a.x,a.y,a.r,ang,true,false);if(now-a.lastFire>600){bullets.push({x:a.x,y:a.y,vx:Math.cos(ang)*7,vy:Math.sin(ang)*7,isAlly:true});a.lastFire=now;}}else{drawP(a.x,a.y,a.r,-Math.PI/2,true,false);}});'

h += 'if(isFiring&&now-lastPlayerFire>200){bullets.push({x:player.x,y:player.y,vx:Math.cos(player.angle)*9,vy:Math.sin(player.angle)*9,isAlly:false});lastPlayerFire=now;}'

h += 'bullets.forEach((b,bi)=>{b.x+=b.vx;b.y+=b.vy;ctx.fillStyle=b.isAlly?"#4ade80":"#f59e0b";ctx.beginPath();ctx.arc(b.x,b.y,3,0,Math.PI*2);ctx.fill();'
h += 'if(b.x<0||b.x>canvas.width||b.y<0||b.y>canvas.height)bullets.splice(bi,1);'
h += 'obstacles.forEach(o=>{if(b.x>o.x&&b.x<o.x+o.w&&b.y>o.y&&b.y<o.y+o.h)bullets.splice(bi,1);});});'

h += 'enemyBullets.forEach((eb,ebi)=>{eb.x+=eb.vx;eb.y+=eb.vy;ctx.fillStyle="#ef4444";ctx.beginPath();ctx.arc(eb.x,eb.y,3,0,Math.PI*2);ctx.fill();'
h += 'if(eb.x>player.x-player.r&&eb.x<player.x+player.r&&eb.y>player.y-player.r&&eb.y<player.y+player.r){enemyBullets.splice(ebi,1);lives--;explode(player.x,player.y,"#ef4444",15);updateUI();if(lives<=0)go();}'
h += 'if(eb.x<0||eb.x>canvas.width||eb.y<0||eb.y>canvas.height)enemyBullets.splice(ebi,1);'
h += 'obstacles.forEach(o=>{if(eb.x>o.x&&eb.x<o.x+o.w&&eb.y>o.y&&eb.y<o.y+o.h)enemyBullets.splice(ebi,1);});});'

h += 'enemies.forEach((e,ei)=>{let pDx=player.x-e.x,pDy=player.y-e.y;let eAng=Math.atan2(pDy,pDx);e.x+=Math.cos(eAng)*e.s;e.y+=Math.sin(eAng)*e.s;drawP(e.x,e.y,e.r,eAng,false,true);'
h += 'if(now-e.lastFire>1600){enemyBullets.push({x:e.x,y:e.y,vx:Math.cos(eAng)*4.5,vy:Math.sin(eAng)*4.5});e.lastFire=now;}'
h += 'if(e.x>player.x-player.r&&e.x<player.x+player.r&&e.y>player.y-player.r&&e.y<player.y+player.r){enemies.splice(ei,1);lives--;explode(player.x,player.y,"#ef4444",15);updateUI();if(lives<=0)go();}'
