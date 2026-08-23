game_html = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <style>
        body { margin: 0; padding: 0; }
        #canvas-container { position: relative; }
        canvas { display: block; background: #000; }
        .ui-layer { position: absolute; top: 0; left: 0; }
        .interactive { pointer-events: auto; }
        .score-bar { display: flex; justify-content: space-between; }
        .menu-screen { position: absolute; top: 0; left: 0; }
        .btn { background: #38bdf8; color: white; }
        .btn:hover { background: #0ea5e9; }
    </style>
</head>
<body>
    <!-- هنا يكتمل باقي كود الـ HTML الخاص باللعبة -->
</body>
</html>
"""

# تأكد من عرض اللعبة باستخدام المكون في السطر الأخير
components.html(game_html, height=600, scrolling=True)
