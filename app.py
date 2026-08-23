import streamlit as st
import streamlit.components.v1 as com

st.set_page_config(page_title='كتيبة الصمود', layout='wide')

st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;background:#031e10;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

st.title('🛡️ معركة الديار: كتيبة الفرسان المطورة')
st.write('🎮 قد فرقتك الحاملة للعُصب الخضراء، وتصدّى لمليشيات وآليات الأعداء لمنع التوغل في شوارع المدينة!')

# كود المحاكاة الجماعي المطور بالكامل وبألوان العصب الخضراء للأفراد
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#011a0e;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif;}'
h += '#game-container{position:relative;width:95vw;max-width:480px;height:72vh;max-height:560px;background:linear-gradient(to bottom, #022a16, #000c06);border:4px solid #10b981;border-radius:24px;overflow:hidden;box-shadow:0 0 35px rgba(16,185,129,0.35);}'
h += 'canvas{display:block;width:100%;height:100%;}'
h += '.heavy-shake{animation:heavyShake 0.22s ease-in-out;}'
h += '@keyframes heavyShake{0%{transform:translate(3px,2px);}13%{transform:translate(-2px,-3px);}26%{transform:translate(-4px,1px);}40%{transform:translate(1px,3px);}55%{transform:translate(-2px,-1px);}}'
h += '.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.hud{display:flex;justify-content:space-between;padding:15px;color:#fff;font-size:16px;font-weight:bold;background:rgba(0,0,0,0.7);border-bottom:3px solid #10b981;box-shadow:0 4px 10px rgba(0,0,0,0.4);}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(1,20,10,0.98);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;text-align:center;padding:20px;}'
h += '.btn{background:linear-gradient(135deg,#10b981,#ef4444);color:white;border:none;padding:16px 45px;font-size:22px;font-weight:bold;border-radius:40px;cursor:pointer;box-shadow:0 5px 25px rgba(16,185,129,0.4);}'
h += '.btn:active{transform:scale(0.96);}.controls{display:flex;width:95vw;max-width:480px;justify-content:space-between;margin-top:15px;pointer-events:auto;gap:12px;}'
h += '.ctrl-btn{flex:1;background:#044e2e;border:2px solid #10b981;color:#fff;padding:18px;font-size:20px;font-weight:bold;border-radius:18px;text-align:center;}'
h += '#btnFire{background:linear-gradient(135deg,#ef4444,#b91c1c);border:none;flex:1.5;box-shadow:0 4px 20px rgba(239,68,68,0.5);font-size:22px;}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer">'
h += '<div class="hud"><div id="scoreDisplay">خسائر المليشيات: 0</div><div id="levelDisplay" style="color:#f59e0b;">الأحياء الآمنة: 1</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#10b981;margin:0 0 10px 0;font-size:30px;text-shadow:0 0 15px #10b981;">🛡️ معركة الصمود الجماعي</h1><p style="color:#a7f3d0;margin:0 0 25px 0;font-size:15px;line-height:1.5;">قُد كتيبتك الحاملة للعُصب الخضراء، ونفذوا كمائن الردع لصد زحف الفصائل والمليشيات الغازية!</p><button class="btn" onclick="startGame()">تعبئة وإطلاق المعركة ⚡</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;margin:0 0 10px 0;font-size:26px;">💥 اخترق العدو خطوط الدفاع</h1><p id="finalScore" style="font-size:18px;color:#d1d5db;margin:0 0 25px 0;"></p><button class="btn" style="background:linear-gradient(135deg,#10b981,#043e22);" onclick="startGame()">إعادة تنظيم الصفوف</button></div>'
h += '</div></div>'

h += '<div class="controls"><div class="ctrl-btn" id="btnLeft">◀ يمين</div><div class="ctrl-btn" id="btnFire">نيران المؤازرة 🔥</div><div class="ctrl-btn" id="btnRight">يسار ▶</div></div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");const container=document.getElementById("game-container");'
h += 'let player,allies,bullets,enemies,particles,shrapnels,score,lives,level,gameActive;let moveLeft=false,moveRight=false,isFiring=false;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setup=(b,p,r)=>{b.addEventListener("touchstart",(e)=>{e.preventDefault();p();});b.addEventListener("touchend",(e)=>{e.preventDefault();r();});b.addEventListener("mousedown",p);b.addEventListener("mouseup",r);};'
h += 'setup(document.getElementById("btnLeft"),()=>moveLeft=true,()=>moveLeft=false);setup(document.getElementById("btnRight"),()=>moveRight=true,()=>moveRight=false);setup(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'

h += 'function triggerShake(){container.classList.add("heavy-shake");setTimeout(()=>container.classList.remove("heavy-shake"),220);}'

h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:canvas.width/2-24,y:canvas.height-65,w:48,h:32,s:7.5};'
h += 'allies=[{x:canvas.width/2-100,y:canvas.height-45,w:18,h:24,side:-1},{x:canvas.width/2+80,y:canvas.height-45,w:18,h:24,side:1}];'
h += 'bullets=[];enemies=[];particles=[];shrapnels=[];score=0;lives=3;level=1;gameActive=true;updateUI();animate();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="خسائر المليشيات: "+score;document.getElementById("levelDisplay").innerText="الأحياء الآمنة: "+level;document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'

h += 'function spawn(){if(!gameActive)return;let size=Math.random()*12+25;let speed=Math.random()*1.2+(1.5+level*0.4);'
h += 'enemies.push({x:Math.random()*(canvas.width-size),y:-size,w:size,h:size,s:speed,hp:Math.ceil(level/2),maxHp:Math.ceil(level/2)});'
h += 'setTimeout(spawn,Math.max(400,1200-level*100));}'
h += 'setTimeout(spawn,1000);'

h += 'function explode(x,y,color,count=15,speed=6){triggerShake();for(let i=0;i<count;i++){particles.push({x:x,y:y,vx:(Math.random()-0.5)*speed,vy:(Math.random()-0.5)*speed,r:Math.random()*3.5+1,a:1,c:color});}}'
h += 'function triggerAmbush(x,y){for(let i=0;i<5;i++){let angle=Math.PI+(i*Math.PI)/4;shrapnels.push({x:x,y:y,vx:Math.cos(angle)*6,vy:Math.sin(angle)*6,w:6,h:6});}}'

h += 'let last=0;let lastAllyFire=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);'
h += 'if(moveLeft&&player.x>40)player.x-=player.s;if(moveRight&&player.x<canvas.width-player.w-40)player.x+=player.s;'
h += 'allies[0].x=player.x-60;allies[1].x=player.x+player.w+40;'

h += 'ctx.fillStyle="#047857";ctx.fillRect(player.x,player.y+10,player.w,player.h-10);ctx.fillStyle="#10b981";ctx.fillRect(player.x+8,player.y,player.w-16,10);ctx.fillStyle="#ef4444";ctx.fillRect(player.x+player.w/2-4,player.y-12,8,12);'

h += 'allies.forEach(a=>{ctx.fillStyle="#15803d";ctx.fillRect(a.x,a.y,a.w,a.h);ctx.fillStyle="#4ade80";ctx.fillRect(a.x,a.y,a.w,6);ctx.fillStyle="#000";ctx.fillRect(a.x+4,a.y+10,4,4);ctx.fillRect(a.x+12,a.y+10,4,4);});'

h += 'let now=Date.now();if(isFiring&&now-last>200){bullets.push({x:player.x+player.w/2-3,y:player.y-12,w:6,h:16,s:11,isAlly:false});last=now;}'
h += 'if(now-lastAllyFire>600){allies.forEach(a=>{bullets.push({x:a.x+a.w/2-2,y:a.y,w:4,h:12,s:8,isAlly:true});});lastAllyFire=now;}'

h += 'bullets.forEach((b,i)=>{b.y-=b.s;ctx.fillStyle=b.isAlly?"#4ade80":"#f59e0b";ctx.fillRect(b.x,b.y,b.w,b.h);if(b.y<0)bullets.splice(i,1);});'
h += 'ctx.fillStyle="#ffea00";shrapnels.forEach((s,si)=>{s.x+=s.vx;s.y+=s.vy;ctx.fillRect(s.x,s.y,s.w,s.h);if(s.x<0||s.x>canvas.width||s.y<0||s.y>canvas.height)shrapnels.splice(si,1);});'

h += 'enemies.forEach((e,ei)=>{e.y+=e.s;ctx.fillStyle="#374151";ctx.fillRect(e.x,e.y,e.w,e.h);ctx.fillStyle="#ef4444";ctx.fillRect(e.x,e.y-6,e.w*(e.hp/e.maxHp),4);'
h += 'if(e.x<player.x+player.w&&e.x+e.w>player.x&&e.y<player.y+player.h&&e.y+e.h>player.y){enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#ef4444",25,8);lives--;updateUI();if(lives<=0)go();}'
h += 'allies.forEach(a=>{if(e.x<a.x+a.w&&e.x+e.w>a.x&&e.y<a.y+a.h&&e.y+e.h>a.y){enemies.splice(ei,1);explode(a.x+a.w/2,a.y+a.h/2,"#ef4444",20,6);score+=5;updateUI();}});'
h += 'if(e.y>canvas.height){enemies.splice(ei,1);lives--;explode(canvas.width/2,canvas.height,"#ff0000",30,10);updateUI();if(lives<=0)go();}'
h += 'bullets.forEach((b,bi)=>{if(b.x<e.x+e.w&&b.x+b.w>e.x&&b.y<e.y+e.h&&b.y+b.h>e.y){bullets.splice(bi,1);e.hp--;explode(b.x,b.y,"#10b981",6,3);if(e.hp<=0){enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#374151",18,5);triggerAmbush(e.x+e.w/2,e.y+e.h/2);score+=10;if(score%60===0){level++;}updateUI();}}});'
h += 'shrapnels.forEach((s,si)=>{if(s.x<e.x+e.w&&s.x+s.w>e.x&&s.y<e.y+e.h&&s.y+s.h>e.y){shrapnels.splice(si,1);enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#ffea00",15,5);score+=10;updateUI();}});});'

h += 'particles.forEach((p,index)=>{p.x+=p.vx;p.y+=p.vy;p.a-=0.025;ctx.save();ctx.globalAlpha=p.a;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.restore();if(p.a<=0)particles.splice(index,1);});'
h += 'requestAnimationFrame(animate);}function go(){gameActive=false;document.getElementById("gameOverMenu").style.display="flex";document.getElementById("finalScore").innerText="عدد آليات ومليشيات العدو المدمرة: "+score;}</script></body></html>'

com.html(h, height=640, scrolling=False)
