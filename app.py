import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون واسعة ومتطورة ومناسبة لكافة الشاشات محمولاً وكمبيوتراً
st.set_page_config(page_title="منظومة صمود العالمية - من أول للتوجيهي", page_icon="🇵🇸", layout="wide")

# كود القرية البرمجية المتكاملة الموحدة الشامل لكافة المراحل الدراسية والكاميرا
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منظومة صمود العالمية - البوابة الموحدة الشاملة</title>
    <style>
        :root { --primary: #00796b; --primary-dark: #004d40; --secondary: #0288d1; --accent: #ef6c00; --bg: #f4f7f6; --card-bg: #ffffff; --text: #333333; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--bg); margin: 0; padding: 15px; color: var(--text); }
        .container { max-width: 1200px; margin: 0 auto; background: var(--card-bg); padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        
        .header-panel { text-align: center; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: white; padding: 25px; border-radius: 10px; margin-bottom: 25px; position: relative; }
        .header-panel h1 { margin: 0; font-size: 26px; }
        .header-panel p { margin: 5px 0 0 0; opacity: 0.9; font-size: 14px; }
        .flag-badge { position: absolute; top: 15px; left: 20px; font-size: 24px; }

        .role-section { background: #eceff1; padding: 10px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: center; gap: 15px; font-weight: bold; }
        .role-btn { background: #ffffff; color: #333; border: 2px solid #ccc; padding: 10px 25px; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .role-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }

        .tabs { display: flex; justify-content: space-around; margin-bottom: 25px; border-bottom: 2px solid #ddd; background: #fafafa; padding: 6px; border-radius: 8px; flex-wrap: wrap; gap: 5px; }
        .tab-btn { background: none; color: #555; border: none; padding: 12px 15px; font-size: 14px; font-weight: bold; cursor: pointer; flex: 1; transition: 0.3s; border-radius: 6px; min-width: 140px; display: flex; align-items: center; justify-content: center; gap: 8px; }
        .tab-btn.active { background-color: var(--primary); color: white; box-shadow: 0 2px 8px rgba(0,121,107,0.3); }
        .tab-content { display: none; animation: fadeIn 0.4s ease; }
        .tab-content.active { display: block; }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 15px; }
        label { font-weight: bold; display: block; margin-bottom: 6px; color: #444; text-align: right; }
        input, select, textarea { width: 100%; padding: 11px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; background: #fafafa; }
        
        .btn { background-color: var(--primary); color: white; padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: bold; width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }
        .btn:hover { background-color: var(--primary-dark); }
        .btn-accent { background-color: var(--accent); } .btn-accent:hover { background-color: #b35000; }
        .btn-purple { background-color: #6a1b9a; } .btn-purple:hover { background-color: #4a148c; }
        
        .camera-box { background: #222; border: 3px solid #444; border-radius: 10px; padding: 15px; text-align: center; max-width: 450px; margin: 15px auto; color: white; }
        video { width: 100%; height: auto; border-radius: 6px; display: none; background: #000; transform: scaleX(-1); }
        .snapshot-preview { width: 100%; height: auto; border-radius: 6px; display: none; border: 2px dashed #00796b; margin-top: 10px; }

        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-box { background: #e0f2f1; padding: 20px; border-radius: 8px; text-align: center; border-bottom: 4px solid var(--primary); }
        .stat-box p { margin: 8px 0 0 0; font-size: 24px; font-weight: bold; color: var(--primary); }
        .table-responsive { overflow-x: auto; margin-top: 15px; border-radius: 8px; border: 1px solid #eee; }
        table { width: 100%; border-collapse: collapse; font-size: 14px; background: #fff; }
        th, td { padding: 12px; border: 1px solid #eee; text-align: center; }
        th { background-color: var(--primary); color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; color: white; }
        .canvas-container { text-align: center; margin-top: 15px; }
        canvas { background: #111; border: 3px solid #333; border-radius: 8px; cursor: crosshair; touch-action: none; max-width: 100%; }
        .timer-box { background: #fff3e0; border: 2px solid #ffe0b2; padding: 20px; border-radius: 10px; text-align: center; max-width: 400px; margin: 15px auto; }
        .timer-display { font-size: 44px; font-weight: bold; color: #e65100; font-family: monospace; }
        .audio-card { background: #f9f9f9; padding: 15px; margin-bottom: 10px; border-radius: 4px; border-right: 5px solid #2e7d32; display: flex; justify-content: space-between; align-items: center; }
        .certificate-card { background: #fffde7; border: 3px dashed #fbc02d; padding: 30px; border-radius: 12px; text-align: center; margin-top: 25px; display: none; }
        .map-container { background: #e3f2fd; border: 2px solid #90caf9; border-radius: 8px; height: 220px; margin-top: 15px; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; overflow: hidden; }
        .map-dot { position: absolute; width: 14px; height: 14px; background: red; border-radius: 50%; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { transform: scale(0.9); opacity: 1; } 50% { transform: scale(1.3); opacity: 0.6; } 100% { transform: scale(0.9); opacity: 1; } }
        .export-panel { background: #f3e5f5; border: 1px dashed #ab47bc; padding: 15px; border-radius: 8px; margin-top: 20px; text-align: center; }
    </style>
</head>
<body>

<div class="container">
    <div class="header-panel">
        <span class="flag-badge">🇵🇸</span>
        <h1>⛺ منظومة صمود العالمية الموحدة (الشرنقة الرقمية الكاملة)</h1>
        <p>دعم شامل وموحد لكافة المراحل الدراسية الفلسطينية من الصف الأول الابتدائي وحتى التوجيهي</p>
    </div>

    <div class="role-section">
        <button id="btnRoleAdmin" class="role-btn active" onclick="switchRole('admin')">💼 بوابة المشرف والمعلم الإدارية</button>
        <button id="btnRoleStudent" class="role-btn" onclick="switchRole('student')">🎓 بوابة الطالب والخدمات التفاعلية</button>
    </div>

    <!-- ==================== بوابات الإدارة والمشرفين ==================== -->
    <div id="adminModule" class="module-wrapper">
        <div class="tabs" id="adminTabs">
            <button class="tab-btn active" onclick="switchTab(event, 'examSyncTab')">🔒 كاميرا وفك كبسولات الامتحانات</button>
            <button class="tab-btn" onclick="switchTab(event, 'attendanceTab')">📝 الحضور اليومي المعتمد</button>
            <button class="tab-btn" onclick="switchTab(event, 'suppliesTab')">✏️ حوكمة القرطاسية</button>
            <button class="tab-btn" onclick="switchTab(event, 'careTab')">❤️ ملفات الرعاية السريّة</button>
            <button class="tab-btn" onclick="switchTab(event, 'mapTab')">🗺️ رادار الخرائط والتقارير</button>
        </div>

        <!-- تبويب استقبال الامتحانات والتوثيق البصري بالكاميرا -->
        <div id="examSyncTab" class="tab-content active">
            <h4 style="text-align: right; color: var(--primary); margin-bottom: 5px;">📸 نظام التوثيق البصري ومسح الـ QR للامتحانات الميدانية:</h4>
            
            <div class="camera-box">
                <div id="cameraStatus" style="font-size:13px; margin-bottom:10px; color:#a9dfbf;">📷 كاميرا الامتحانات مغلقة حالياً</div>
                <video id="webcam" autoplay playsinline></video>
                <img id="snapshot" class="snapshot-preview" alt="معاينة الصورة الموثقة">
                
                <div style="display:flex; gap:10px; margin-top:12px;">
                    <button onclick="startCamera()" style="background:#239b56; color:white; border:none; padding:8px; border-radius:4px; flex:1; font-weight:bold; cursor:pointer;">🟢 تشغيل الكاميرا</button>
                    <button onclick="takeSnapshot()" style="background:#1f618d; color:white; border:none; padding:8px; border-radius:4px; flex:1; font-weight:bold; cursor:pointer;">📸 لقطة التوثيق</button>
                    <button onclick="stopCamera()" style="background:#922b21; color:white; border:none; padding:8px; border-radius:4px; flex:1; font-weight:bold; cursor:pointer;">🛑 إيقاف</button>
                </div>
            </div>

            <div class="form-group" style="text-align: right; margin-top: 20px;">
                <label>📥 رصد يدوي / إدخال نص كبسولة الطالب المشفرة:</label>
                <textarea id="qrInput" style="width:100%; height:60px; padding:10px;" placeholder="ضع النص المشفر المستخرج من كود الـ QR مالي للطالب هنا..."></textarea>
                <button class="btn" style="margin-top:10px;" onclick="processExamPayload()">🚀 فك التشفير ومزامنة الدرجة والتوثيق</button>
            </div>
            
            <div class="stats-grid" style="margin-top:20px;">
            
