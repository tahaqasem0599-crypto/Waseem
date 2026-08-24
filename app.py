import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="منظومة صمود", page_icon="🇵🇸", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>صمود</title>
    <style>
        :root { --p: #00796b; --p-d: #004d40; --a: #ef6c00; }
        body { font-family: sans-serif; background: #f4f7f6; margin: 0; padding: 10px; text-align: center; }
        .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .header { background: linear-gradient(135deg, var(--p), var(--p-d)); color: white; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        .roles { display: flex; justify-content: center; gap: 10px; margin-bottom: 15px; }
        .r-btn { background: #fff; border: 2px solid #ccc; padding: 8px 15px; border-radius: 6px; cursor: pointer; font-weight: bold; }
        .r-btn.active { background: var(--p); color: #fff; border-color: var(--p); }
        .tabs { display: flex; gap: 5px; margin-bottom: 15px; background: #eee; padding: 5px; border-radius: 6px; overflow-x: auto; }
        .t-btn { background: none; border: none; padding: 10px; font-weight: bold; cursor: pointer; flex: 1; min-width: 100px; }
        .t-btn.active { background: var(--p); color: white; border-radius: 4px; }
        .content { display: none; animation: f 0.3s; text-align: right; }
        .content.active { display: block; }
        @keyframes f { from { opacity: 0; } to { opacity: 1; } }
        .f-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-bottom: 10px; }
        input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; }
        button { background: var(--p); color: white; padding: 10px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; width: 100%; }
        .cam-box { background: #222; border-radius: 8px; padding: 10px; max-width: 350px; margin: 10px auto; color: white; }
        video, img { width: 100%; border-radius: 4px; display: none; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }
        th, td { padding: 10px; border: 1px solid #eee; text-align: center; }
        th { background: var(--p); color: white; }
        tr:nth-child(even) { background: #f9f9f9; }
        .badge { padding: 4px 8px; border-radius: 12px; font-size: 11px; color: white; font-weight: bold; }
        canvas { background: #111; border-radius: 8px; max-width: 100%; touch-action: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="header"><h1>⛺ منظومة صمود التعليمية الموحدة</h1><p>من الصف الأول للتوجيهي - النسخة الموحدة بالكاميرا والحفظ التلقائي</p></div>
    <div class="roles">
        <button id="rAdmin" class="r-btn active" onclick="sRole('admin')">💼 المعلم والمشرف</button>
        <button id="rStudent" class="r-btn" onclick="sRole('student')">🎓 بوابة الطالب</button>
    </div>
    <div id="mAdmin">
        <div class="tabs">
            <button class="t-btn active" onclick="sTab(event, 't1')">📸 كاميرا والامتحانات</button>
            <button class="t-btn" onclick="sTab(event, 't2')">📝 الحضور اليومي</button>
            <button class="t-btn" onclick="sTab(event, 't3')">✏️ القرطاسية</button>
            <button class="t-btn" onclick="sTab(event, 't4')">❤️ الرعاية الطبية</button>
        </div>
        <div id="t1" class="content active">
            <div class="cam-box">
                <video id="v" autoplay playsinline></video><img id="snap">
                <div style="display:flex; gap:5px; margin-top:8px;">
                    <button onclick="stCam()" style="background:#2e7d32;">📷 تشغيل</button>
                    <button onclick="tkSnap()" style="background:#1565c0;">📸 لقطة</button>
                </div>
            </div>
            <textarea id="qrIn" placeholder="ضع كود الـ QR مالي المشفر للطالب هنا..."></textarea>
            <button onclick="pExam()" style="margin-top:5px;">🚀 فك التشفير ورصد الدرجة</button>
            <table>
                <thead><tr><th>الهوية</th><th>الاسم رباعي</th><th>الصف الدراسي</th><th>الامتحان</th><th>الدرجة</th><th>الحالة بصرية</th></tr></thead>
                <tbody id="examBody"></tbody>
            </table>
        </div>
        <div id="t2" class="content">
            <div class="f-grid">
                <input type="text" id="idAtt" placeholder="الهوية (9 أرقام)" maxlength="9">
                <input type="text" id="nameAtt" placeholder="الاسم رباعي رسمي">
                <select id="gradeAtt">
                    <option disabled selected value="">--- اختر الصف ---</option>
                    <option>الصف الأول الابتدائي</option><option>الصف الثاني الابتدائي</option><option>الصف الثالث الابتدائي</option>
                    <option>الصف الرابع الابتدائي</option><option>الصف الخامس الابتدائي</option><option>الصف السادس الابتدائي</option>
                    <option>الصف السابع الإعدادي</option><option>الصف الثامن الإعدادي</option><option>الصف التاسع الإعدادي</option>
                    <option>الصف العاشر</option><option>الصف الحادي عشر</option><option>التوجيهي (الثانوية العامة)</option>
                </select>
                <input type="text" id="tent" placeholder="رقم الخيمة">
            </div>
            <button onclick="addAtt()">✍️ توثيق الحضور</button>
            <table><thead><tr><th>الهوية</th><th>الاسم</th><th>الصف</th><th>الخيمة</th><th>التوقيت</th></tr></thead><tbody id="attBody"></tbody></table>
        </div>
        <div id="t3" class="content">
            <div class="f-grid">
                <input type="text" id="sId" placeholder="الهوية (9 أرقام)" maxlength="9">
                <input type="text" id="sName" placeholder="الاسم رباعي">
                <select id="sType"><option>حقيبة مدرسية وقرطاسية</option><option>دفاتر وأقلام</option></select>
            </div>
            <button onclick="addSup()" style="background:var(--a);">✏️ فحص وصرف الحصة</button>
            <table><thead><tr><th>الهوية</th><th>الاسم</th><th>الحصة</th><th>الفحص</th></tr></thead><tbody id="supBody"></tbody></table>
        </div>
        <div id="t4" class="content">
            <div class="f-grid">
                <input type="text" id="cId" placeholder="الهوية (9 أرقام)" maxlength="9">
                <input type="text" id="cName" placeholder="الاسم رباعي">
                <select id="cType"><option>رعاية طبية عاجلة</option><option>دعم نفسي وصدمات</option></select>
            </div>
            <textarea id="cNotes" placeholder="تفاصيل احتياج الطفل الطبية والنفسية..."></textarea>
            <button onclick="addCare()" style="background:#6a1b9a; margin-top:5px;">💾 حفظ في سجل الحماية</button>
            <table><thead><tr><th>الهوية</th><th>الاسم</th><th>الاحتياج</th><th>الملاحظات</th></tr></thead><tbody id="careBody"></tbody></table>
        </div>
    </div>
    <div id="mStudent" style="display:none;">
        <div class="tabs">
            <button class="t-btn active" onclick="sSTab(event, 'st1')">🎨 السبورة الرقمية</button>
            <button class="t-btn" onclick="sSTab(event, 'st2')">⏱️ مؤقت التركيز</button>
            <button class="t-btn" onclick="sSTab(event, 'st3')">🔊 دروس مسموعة</button>
        </div>
        <div id="st1" class="content active" style="text-align:center;">
            <canvas id="c" width="600" height="300"></canvas><br>
            <button onclick="clrC()" style="width:auto; background:#333; margin-top:5px;">🧼 مسح السبورة</button>
        </div>
        <div id="st2" class="content" style="text-align:center;">
            <div class="timer-box"><div class="timer-display" id="tVal" style="font-size:40px; font-weight:bold; color:var(--a);">25:00</div><button onclick="stT()" style="background:#2e7d32; width:auto; margin-top:5px;">▶️ ابدأ المذاكرة</button></div>
        </div>
        <div id="st3" class="content">
            <div style="background:#eee; padding:10px; margin-bottom:5px; border-radius:6px; display:flex; justify-content:space-between; align-items:center;">
                <div><strong>قوانين الحركة والسرعة في الفيزياء</strong> - التوجيهي</div>
                <button onclick="spk('قوانين الحركة لنيوتن. القانون الأول: يظل الجسم الساكن ساكناً والجسم المتحرك متحركاً ما لم تؤثر عليه قوة خارجية.')" style="width:auto;">🔊 استمع</button>
            </div>
        </div>
    </div>
</div>
<script>
    window.onload = function() { loadL(); initC(); };
    let sups = JSON.parse(localStorage.getItem('sups')) || [];
    let exams = JSON.parse(localStorage.getItem('exams')) || [];
    let stream = null, hasSnap = false;

    function sRole(r) {
        document.getElementById('rAdmin').classList.toggle('active', r === 'admin');
        document.getElementById('rStudent').classList.toggle('active', r === 'student');
        document.getElementById('mAdmin').style.display = r === 'admin' ? 'block' : 'none';
        document.getElementById('mStudent').style.display = r === 'student' ? 'block' : 'none';
        if(r === 'admin') { stopCam(); } else { setTimeout(initC, 100); }
    }
    function sTab(e, id) {
        let c = document.querySelectorAll("#mAdmin .content"); c.forEach(t => t.classList.remove('active'));
        let b = document.querySelectorAll("#mAdmin .t-btn"); b.forEach(t => t.classList.remove('active'));
        document.getElementById(id).classList.add('active'); e.currentTarget.classList.add('active');
        if(id !== 't1') stopCam();
    }
    function sSTab(e, id) {
        let c = document.querySelectorAll("#mStudent .content"); c.forEach(t => t.classList.remove('active'));
        
