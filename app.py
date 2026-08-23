import streamlit as st
import streamlit.components.v1 as com

st.set_page_config(page_title='معركة الصمود - نمط كونترا', layout='wide')

st.markdown('<style>body,.main,.block-container{padding:0!important;margin:0!important;background:#06140c;}iframe{border:none;width:100%;}</style>', unsafe_allow_html=True)

st.title('🛡️ كتيبة الصمود: حرب الشوارع (نمط كونترا)')
st.write('🎮 تحرك، اقفز فوق السيارات والأنقاض، وأطلق النار لتطهير شوارع المدينة من الميليشيات الغازية!')

# كود اللعبة بنمط كونترا وببجي ثنائي الأبعاد (تحرك جانبي، قفز، منصات وسيارات)
h = '<!DOCTYPE html><html lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">'
h += '<style>*{box-sizing:border-box;user-select:none;}body{margin:0;padding:0;background:#090d16;display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif;}'
h += '#game-container{position:relative;width:95vw;max-width:550px;height:65vh;max-height:480px;background:linear-gradient(to bottom,#111827,#1f2937);border:4px solid #10b981;border-radius:20px;overflow:hidden;box-shadow:0 0 35px rgba(16,185,129,0.3);}'
h += 'canvas{display:block;width:100%;height:100%;}'
h += '.ui-layer{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}'
h += '.hud{display:flex;justify-content:space-between;padding:12px 15px;color:#fff;font-size:15px;font-weight:bold;background:rgba(0,0,0,0.75);border-bottom:2px solid #10b981;}'
h += '.menu-screen{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(10,15,30,0.98);display:flex;flex-direction:column;justify-content:center;align-items:center;color:white;pointer-events:auto;text-align:center;padding:20px;}'
h += '.btn{background:linear-gradient(135deg,#10b981,#ef4444);color:white;border:none;padding:14px 40px;font-size:20px;font-weight:bold;border-radius:30px;cursor:pointer;box-shadow:0 5px 20px rgba(16,185,129,0.4);}'
h += '.controls{display:flex;width:95vw;max-width:550px;justify-content:space-between;margin-top:12px;pointer-events:auto;gap:8px;}'
h += '.ctrl-btn{flex:1;background:#1f2937;border:2px solid #374151;color:#10b981;padding:16px;font-size:18px;font-weight:bold;border-radius:14px;text-align:center;}'
h += '#btnFire{background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff;flex:1.3;box-shadow:0 4px 15px rgba(239,68,68,0.4);}'
h += '#btnJump{background:linear-gradient(135deg,#2563eb,#1d4ed8);color:#fff;flex:1.1;box-shadow:0 4px 15px rgba(37,99,235,0.4);}</style></head><body>'

h += '<div id="game-container"><canvas id="gameCanvas"></canvas><div class="ui-layer">'
h += '<div class="hud"><div id="scoreDisplay">خسائر الأعداء: 0</div><div id="liveDisplay">❤️ ❤️ ❤️</div></div>'
h += '<div id="mainMenu" class="menu-screen"><h1 style="color:#10b981;margin:0 0 10px 0;font-size:28px;text-shadow:0 0 15px #10b981;">🛡️ فرسان الصمود (Contra Mode)</h1><p style="color:#9ca3af;margin:0 0 25px 0;font-size:14px;line-height:1.5;">تحرك في الشوارع، اقفز فوق السيارات المحطمة، وتصدى مع جنود العُصب الخضراء لهجوم الميليشيات!</p><button class="btn" onclick="startGame()">دخول ساحة المعركة ⚡</button></div>'
h += '<div id="gameOverMenu" class="menu-screen" style="display:none;"><h1 style="color:#ef4444;margin:0 0 10px 0;">💥 تضررت فرقتك</h1><p id="finalScore" style="font-size:18px;color:#d1d5db;margin:0 0 25px 0;"></p><button class="btn" style="background:linear-gradient(135deg,#10b981,#1f2937);" onclick="startGame()">إعادة تنظيم الصفوف</button></div>'
h += '</div></div>'

h += '<div class="controls"><div class="ctrl-btn" id="btnLeft">◀ يمين</div><div class="ctrl-btn" id="btnRight">يسار ▶</div><div class="ctrl-btn" id="btnJump">🦘 قفز</div><div class="ctrl-btn" id="btnFire">🔥 إطلاق</div></div>'

h += '<script>const canvas=document.getElementById("gameCanvas");const ctx=canvas.getContext("2d");'
h += 'let player,bullets,enemyBullets,enemies,cars,particles,score,lives,gameActive;let moveLeft=false,moveRight=false,isFiring=false;const gravity=0.5;const groundY=380;'
h += 'function resize(){canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;}window.addEventListener("resize",resize);resize();'
h += 'const setup=(b,p,r)=>{b.addEventListener("touchstart",(e)=>{e.preventDefault();p();});b.addEventListener("touchend",(e)=>{e.preventDefault();r();});b.addEventListener("mousedown",p);b.addEventListener("mouseup",r);};'
h += 'setup(document.getElementById("btnLeft"),()=>moveLeft=true,()=>moveLeft=false);setup(document.getElementById("btnRight"),()=>moveRight=true,()=>moveRight=false);setup(document.getElementById("btnFire"),()=>isFiring=true,()=>isFiring=false);'
h += 'document.getElementById("btnJump").addEventListener("touchstart",(e)=>{e.preventDefault();jump();});document.getElementById("btnJump").addEventListener("mousedown",jump);'

h += 'function jump(){if(player&&!player.isJumping){player.vy=-10;player.isJumping=true;}}'

h += 'function startGame(){resize();document.getElementById("mainMenu").style.display="none";document.getElementById("gameOverMenu").style.display="none";'
h += 'player={x:50,y:groundY-40,w:24,h:40,vx:0,vy:0,isJumping:false,facing:1};bullets=[];enemyBullets=[];enemies=[];particles=[];score=0;lives=3;gameActive=true;'
h += 'cars=[{x:180,y:groundY-30,w:70,h:30,color:"#4b5563"},{x:360,y:groundY-30,w:70,h:30,color:"#7f1d1d"}];'
h += 'updateUI();animate();spawnEnemy();}'
h += 'function updateUI(){document.getElementById("scoreDisplay").innerText="خسائر الأعداء: "+score;document.getElementById("liveDisplay").innerText="❤️ ".repeat(lives);}'

h += 'function spawnEnemy(){if(!gameActive)return;if(enemies.length<3){enemies.push({x:canvas.width+20,y:groundY-40,w:24,h:40,s:1.5+Math.random(),lastFire:Date.now()});}setTimeout(spawnEnemy,2000);}'

h += 'function explode(x,y,color,count=10){for(let i=0;i<count;i++){particles.push({x:x,y:y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,r:Math.random()*3+1,a:1,c:color});}}'

h += 'let lastPlayerFire=0;function animate(){if(!gameActive)return;ctx.clearRect(0,0,canvas.width,canvas.height);'
h += 'ctx.fillStyle="#374151";ctx.fillRect(0,groundY,canvas.width,canvas.height-groundY);ctx.fillStyle="#1f2937";ctx.fillRect(0,groundY,canvas.width,6);'

h += 'cars.forEach(c=>{ctx.fillStyle=c.color;ctx.fillRect(c.x,c.y,c.w,c.h);ctx.fillStyle="#111";ctx.fillRect(c.x+8,c.y+c.h-8,14,14);ctx.fillRect(c.x+c.w-22,c.y+c.h-8,14,14);});'

h += 'if(moveLeft){player.x-=4;player.facing=-1;}if(moveRight){player.x+=4;player.facing=1;}if(player.x<0)player.x=0;if(player.x>canvas.width-player.w)player.x=canvas.width-player.w;'

h += 'player.vy+=gravity;player.y+=player.vy;let onPlatform=false;'
h += 'cars.forEach(c=>{if(player.x+player.w>c.x&&player.x<c.x+c.w&&player.y+player.h>=c.y&&player.y+player.h-player.vy<=c.y+10&&player.vy>=0){player.y=c.y-player.h;player.vy=0;player.isJumping=false;onPlatform=true;}});'
h += 'if(!onPlatform&&player.y>=groundY-player.h){player.y=groundY-player.h;player.vy=0;player.isJumping=false;}'

h += 'function drawSoldier(x,y,w,h,hasBand,isEnemy,face){'
h += 'ctx.fillStyle=isEnemy?"#312e81":"#064e3b";ctx.fillRect(x,y+h/3,w,h*2/3);ctx.fillStyle="#fbcfe8";ctx.beginPath();ctx.arc(x+w/2,y+h/6,w/3,0,Math.PI*2);ctx.fill();'
h += 'if(hasBand){ctx.fillStyle="#22c55e";ctx.fillRect(x+2,y+4,w-4,4);}'
h += 'ctx.fillStyle="#000";let gunX=face===1?x+w:x-8;ctx.fillRect(gunX,y+h/2,8,4);}'

h += 'drawSoldier(player.x,player.y,player.w,player.h,true,false,player.facing);'

h += 'let now=Date.now();if(isFiring&&now-lastPlayerFire>250){bullets.push({x:player.facing===1?player.x+player.w:player.x,y:player.y+player.h/2,vx:player.facing*8,vy:0});lastPlayerFire=now;}'

h += 'bullets.forEach((b,bi)=>{b.x+=b.vx;ctx.fillStyle="#f59e0b";ctx.fillRect(b.x,b.y,6,3);if(b.x<0||b.x>canvas.width)bullets.splice(bi,1);});'
h += 'enemyBullets.forEach((eb,ebi)=>{eb.x+=eb.vx;ctx.fillStyle="#ef4444";ctx.fillRect(eb.x,eb.y,6,3);'
h += 'if(eb.x>player.x&&eb.x<player.x+player.w&&eb.y>player.y&&eb.y<player.y+player.h){enemyBullets.splice(ebi,1);lives--;explode(player.x+player.w/2,player.y+player.h/2,"#ef4444",15);updateUI();if(lives<=0)go();}'
h += 'if(eb.x<0||eb.x>canvas.width)enemyBullets.splice(ebi,1);});'

h += 'enemies.forEach((e,ei)=>{e.x-=e.s;drawSoldier(e.x,e.y,e.w,e.h,false,true,-1);'
h += 'let ecPlatform=false;cars.forEach(c=>{if(e.x+e.w>c.x&&e.x<c.x+c.w&&e.y+e.h>=c.y&&e.y+e.h<=c.y+10){e.y=c.y-e.h;ecPlatform=true;}});if(!ecPlatform)e.y=groundY-e.h;'
h += 'if(now-e.lastFire>1500){enemyBullets.push({x:e.x,y:e.y+e.h/2,vx:-5,vy:0});e.lastFire=now;}'
h += 'if(e.x<-20){enemies.splice(ei,1);lives--;updateUI();if(lives<=0)go();}'
h += 'bullets.forEach((b,bi)=>{if(b.x>e.x&&b.x<e.x+e.w&&b.y>e.y&&b.y<e.y+e.h){bullets.splice(bi,1);enemies.splice(ei,1);explode(e.x+e.w/2,e.y+e.h/2,"#10b981",15);score+=10;updateUI();}});});'

h += 'particles.forEach((p,index)=>{p.x+=p.vx;p.y+=p.vy;p.a-=0.03;ctx.save();ctx.globalAlpha=p.a;ctx.fillStyle=p.c;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);ctx.fill();ctx.restore();if(p.a<=0)particles.splice(index,1);});'
h += 'requestAnimationFrame(animate);}function go(){gameActive=false;document.getElementById("gameOverMenu").style.display="flex";document.getElementById("finalScore").innerText="عدد الأعداء الذين تم تحييدهم: "+score;}</script></body></html>'

com.html(h, height=620, scrolling=False)
