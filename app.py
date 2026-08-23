import streamlit as st
import streamlit.components.v1 as com

st.set_page_config(page_title='كتيبة الصمود - محاكاة الشوارع', layout='wide')

st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;background:#020b05;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

st.title('🇵🇸 معركة المدينة: محاكاة حرب الشوارع')
st.write('🎮 الإصدار المطور: دافع عن شوارع المدينة المليئة بالمدنيين، السيارات، والأنقاض ضد اقتحام الميليشيات المهاجمة!')

# كود المحاكاة المطور برسم شوارع كاملة، سيارات، مدنيين، وجنود بعصب خضراء
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#03140a;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif;}'
h += '#game-container{position:relative;width:95vw;max-width:480px;height:72vh;max-height:560px;background:#27272a;border:4px solid #10b981;border-radius:24px;overflow:hidden;box-shadow:0 0 35px rgba(16,185,129,0.35);}'
h += 'canvas{display:block;width:100%;height:100%;}'
h += '.heavy-shake{animation:heavyShake 0.22s ease-in-out;}'
h += '@keyframes heavyShake{0%{transform:translate(3px,2px);}13%{transform:translate(-2px,-3px);}26%{transform:translate(-4px,1px);}40%{transform:translate(1px,3px);}}'
h += '.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.hud{display:flex;justify-content:space-between;padding:15px;color:#fff;font-size:15px;font-weight:bold;background:rgba(0,0,0,0.85);border-bottom:3px solid #10b981;}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(2,15,8,0.98);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;text-align:center;padding:20px;}'
h += '.btn{background:linear-gradient(135deg,#10b981,#ef4444);color:white;border:none;padding:16px 45px;font-size:22px;font-weight:bold;border-radius:40px;cursor:pointer;box-shadow:0 5px 25px rgba(16,185,129,0.4);}'
h += '.controls{display:flex;width:95vw;max-width:480px;justify-content:space-between;margin-top:15px;pointer-events:auto;gap:12px;}'
h += '.ctrl-btn{flex:1;background:#064e3b;border:2px solid #10b981;color:#fff;padding:18px;font-size:20px;font-weight:bold;border-radius:18px;text-align:center;}'
h += '#btnFire{background:linear-gradient(135deg,#ef4444,#b91c1c);border:none;flex:1.5;box-shadow:0 4px 20px rgba(239,68,68,0.5);font-size:22px;}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer">'
h += '<div class="hud"><div id="scoreDisplay">خسائر الميليشيات: 0</div><div id="civilDisplay" style="color:#38bdf8;">المدنيون بأمان: 100%</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#10b981;margin:0 0 10px 0;font-size:28px;text-shadow:0 0 15px #10b981;">🛡️ الدفاع عن شوارع المدينة</h1><p style="color:#a7f3d0;margin:0 0 25px 0;font-size:14px;line-height:1.5;">احمِ المارة والمدنيين، وتصدى مع فرقتك ذات العُصب الخضراء لآليات وجنود الميليشيات الغازية وسط ركام السيارات!</p><button class="btn" onclick="startGame()">بدء المحاكاة والمواجهة ⚡</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;margin:0 0 10px 0;font-size:26px;">💥 انتهت معركة الشارع</h1><p id="finalScore" style="font-size:18px;color:#d1d5db;margin:0 0 25px 0;"></p><button class="btn" style="background:linear-gradient(135deg,#10b981,#043e22);" onclick="startGame()">إعادة الكَرّة</button></div>'
h += '</div></div>'

h += '<div class="controls"><div class="ctrl-btn" id="btnLeft">◀ يمين</div><div class="ctrl-btn" id="btnFire">🔥 نيران صد</div><div class="ctrl-btn" id="btnRight">يسار ▶</div></div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");const container=document.getElementById("game-container");'
h += 'let player,allies,civilians,cars,bullets,enemies,particles,score,lives,civilHealth,gameActive;let moveLeft=false,moveRight=false,isFiring=false;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setup=(b,p,r)=>{b.addEventListener("touchstart",(e)=>{e.preventDefault();p();});b.addEventListener("touchend",(e)=>{e.preventDefault();r();});b.addEventListener("mousedown",p);b.addEventListener("mouseup",r);};'
h += 'setup(document.getElementById("btnLeft"),()=>moveLeft=true,()=>moveLeft=false);setup(document.getElementById("btnRight"),()=>moveRight=true,()=>moveRight=false);setup(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'

h += 'function triggerShake(){container.classList.add("heavy-shake");setTimeout(()=>container.classList.remove("heavy-shake"),220);}'

h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:canvas.width/2-15,y:canvas.height-75,w:30,h:45,s:6};'
h += 'allies=[{x:canvas.width/2-75,y:canvas.height-65,w:22,h:35},{x:canvas.width/2+55,y:canvas.height-65,w:22,h:35}];'
h += 'civilians=[];cars=[];bullets=[];enemies=[];particles=[];score=0;lives=3;civilHealth=100;gameActive=true;'
h += 'for(let i=0;i<4;i++){cars.push({x:Math.random()>0.5?15:canvas.width-55,y:100+i*110,w:38,h:55,color:Math.random()>0.5?"#7f1d1d":"#3f3f46"});}'
h += 'updateUI();animate();spawnCivilians();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="خسائر الميليشيات: "+score;document.getElementById("civilDisplay").innerText="المدنيون بأمان: "+civilHealth+"%";document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'

h += 'function spawnCivilians(){if(!gameActive)return;if(civilians.length<3){civilians.push({x:Math.random()*(canvas.width-140)+70,y:Math.random()*(canvas.height-200)+100,w:14,h:20,vx:(Math.random()-0.5)*2});}setTimeout(spawnCivilians,3000);}'
h += 'function spawn(){if(!gameActive)return;let size=26;let speed=Math.random()*1.2+1.5;enemies.push({x:Math.random()*(canvas.width-140)+70,y:-size,w:size,h:38,s:speed,hp:1,maxHp:1});setTimeout(spawn,1100);}setTimeout(spawn,1000);'

h += 'function explode(x,y,color,count=12){triggerShake();for(let i=0;i<count;i++){particles.push({x:x,y:y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,r:Math.random()*3+1,a:1,c:color});}}'

h += 'let last=0;let lastAllyFire=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);'
h += 'if(moveLeft&&player.x>65)player.x-=player.s;if(moveRight&&player.x<canvas.width-player.w-65)player.x+=player.s;'
h += 'allies[0].x=player.x-55;allies[1].x=player.x+player.w+30;'

h += 'ctx.fillStyle="#4b5563";ctx.fillRect(0,0,60,canvas.height);ctx.fillRect(canvas.width-60,0,60,canvas.height);'
h += 'ctx.fillStyle="#3f3f46";for(let i=0;i<canvas.height;i+=90){ctx.fillRect(5,i+10,50,60);ctx.fillRect(canvas.width-55,i+10,50,60);}'
h += 'ctx.strokeStyle="#71717a";ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(canvas.width/2,0);ctx.lineTo(canvas.width/2,canvas.height);ctx.stroke();'

h += 'cars.forEach(c=>{ctx.fillStyle=c.color;ctx.fillRect(c.x,c.y,c.w,c.h);ctx.fillStyle="#18181b";ctx.fillRect(c.x+2,c.y+5,c.w-4,10);ctx.fillRect(c.x+2,c.y+c.h-15,c.w-4,10);ctx.fillStyle="#facc15";ctx.fillRect(c.x+4,c.y,4,2);ctx.fillRect(c.x+c.w-8,c.y,4,2);});'

h += 'civilians.forEach((civ,idx)=>{civ.x+=civ.vx;if(civ.x<65||civ.x>canvas.width-65-civ.w)civ.vx*=-1;ctx.fillStyle="#fbcfe8";ctx.beginPath();ctx.arc(civ.x+civ.w/2,civ.y+4,civ.w/2,0,Math.PI*2);ctx.fill();ctx.fillStyle="#2563eb";ctx.fillRect(civ.x,civ.y+8,civ.w,civ.h-8);});'

h += 'function drawSoldier(x,y,w,h,hasGreenBand,isEnemy){'
h += 'ctx.fillStyle=isEnemy?"#1e1b4b":"#064e3b";ctx.fillRect(x+w/4,y+h/3,w/2,h/2);'
h += 'ctx.fillStyle="#fbcfe8";ctx.beginPath();ctx.arc(x+w/2,y+h/5,w/4,0,Math.PI*2);ctx.fill();'
h += 'if(hasGreenBand){ctx.fillStyle="#22c55e";ctx.fillRect(x+w/4,y+h/9,w/2,4);}'
h += 'if(isEnemy){ctx.fillStyle="#ef4444";ctx.fillRect(x+w/4,y+h/9,w/2,4);}'
h += 'ctx.fillStyle=isEnemy?"#000":"#15803d";ctx.fillRect(x,y+h/3,w/4,h/3);ctx.fillRect(x+w*3/4,y+h/3,w/4,h/3);}'

h += 'drawSoldier(player.x,player.y,player.w,player.h,true,false);'
h += 'allies.forEach(a=>drawSoldier(a.x,a.y,a.w,a.h,true,false));'

h += 'let now=Date.now();if(isFiring&&now-last>220){bullets.push({x:player.x+player.w/2-2,y:player.y,w:4,h:12,s:10,isAlly:false});last=now;}'
h += 'if(now-lastAllyFire>700){allies.forEach(a=>{bullets.push({x:a.x+a.w/2-2,y:a.y,w:3,h:10,s:8,isAlly:true});});lastAllyFire=now;}'

h += 'bullets.forEach((b,i)=>{b.y-=b.s;ctx.fillStyle=b.isAlly?"#4ade80":"#f59e0b";ctx.fillRect(b.x,b.y,b.w,b.h);if(b.y<0)bullets.splice(i,1);});'

h += 'enemies.forEach((e,ei)=>{e.y+=e.s;drawSoldier(e.x,e.y,e.w,e.h,false,true);'
h += 'civilians.forEach((civ,cIdx)=>{if(e.x<civ.x+civ.w&&e.x+e.w>civ.x&&e.y<civ.y+civ.h&&e.y+e.h>civ.y){civilians.splice(cIdx,1);civilHealth=Math.max(0,civilHealth-20);explode(civ.x,civ.y,"#ef4444",10);updateUI();if(civilHealth<=0)go();}});'
h += 'if(e.x<player.x+player.w&&e.x+e.w>player.x&&e.y<player.y+player.h&&e.y+e.h>player.y){enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#ef4444",20);lives--;updateUI();if(lives<=0)go();}'
h += 'if(e.y>canvas.height){enemies.splice(ei,1);lives--;explode(canvas.width/2,canvas.height,"#ff0000",25);updateUI();if(lives<=0)go();}'
h += 'bullets.forEach((b,bi)=>{if(b.x<e.x+e.w&&b.x+b.w>e.x&&b.y<e.y+e.h&&b.y+b.h>e.y){bullets.splice(bi,1);e.hp--;explode(b.x,b.y,"#22c55e",4);if(e.hp<=0){enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#475569",15);score+=10;updateUI();}}});});'

