#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق شامل لتحديثات حسين غلاب:
- حفظ المحادثات الدائم
- إضافة اسم المطور "حسين غلاب" في كل مكان
- واجهة البرمجة الكاملة
- إزالة الإيموجي
- صوت محسّن
"""

import io
import os
import re

DEVELOPER = "حسين غلاب"
SYSTEM_NAME = "Hussein Ghallab System"
TAGLINE = "من المستقبل — بلغة الحاضر"

print("=" * 65)
print("تحديث حسين غلاب — تطبيق شامل")
print("=" * 65)


# ============================================================
# 1) إنشاء storage.js
# ============================================================
os.makedirs("static", exist_ok=True)

storage_js = r'''/* نظام حفظ المحادثات الدائم — Hussein Ghallab System */
var ChatStorage = (function(){
  var KEY = "hussein_ghallab_conversations_v1";
  var MAX_CONVS = 100;

  function load(){
    try {
      var raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : { conversations: [], activeId: null };
    } catch(e) {
      return { conversations: [], activeId: null };
    }
  }

  function save(data){
    try {
      if(data.conversations.length > MAX_CONVS){
        data.conversations = data.conversations.slice(-MAX_CONVS);
      }
      localStorage.setItem(KEY, JSON.stringify(data));
    } catch(e) { console.warn("Storage full", e); }
  }

  function newId(){
    return "c_" + Date.now() + "_" + Math.random().toString(36).slice(2, 8);
  }

  return {
    list: function(){ return load().conversations; },
    getActiveId: function(){ return load().activeId; },
    setActive: function(id){
      var d = load(); d.activeId = id; save(d);
    },
    create: function(title){
      var d = load();
      var conv = {
        id: newId(),
        title: title || "محادثة " + new Date().toLocaleString("ar"),
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now()
      };
      d.conversations.push(conv);
      d.activeId = conv.id;
      save(d);
      return conv;
    },
    get: function(id){
      var d = load();
      return d.conversations.find(function(c){ return c.id === id; }) || null;
    },
    addMessage: function(convId, role, content, provider){
      var d = load();
      var conv = d.conversations.find(function(c){ return c.id === convId; });
      if(!conv) return null;
      conv.messages.push({
        id: "m_" + Date.now() + "_" + Math.random().toString(36).slice(2,6),
        role: role,
        content: content,
        provider: provider || "",
        at: Date.now()
      });
      conv.updatedAt = Date.now();
      if(conv.messages.length === 1 && role === "user"){
        conv.title = content.slice(0, 40) + (content.length > 40 ? "..." : "");
      }
      save(d);
      return conv;
    },
    remove: function(id){
      var d = load();
      d.conversations = d.conversations.filter(function(c){ return c.id !== id; });
      if(d.activeId === id) d.activeId = null;
      save(d);
    },
    clearAll: function(){ save({ conversations: [], activeId: null }); },
    export: function(){ return JSON.stringify(load(), null, 2); },
    import: function(json){
      try {
        var data = JSON.parse(json);
        if(data.conversations) save(data);
        return true;
      } catch(e) { return false; }
    }
  };
})();
'''

with io.open("static/storage.js", "w", encoding="utf-8") as f:
    f.write(storage_js)
print("[+] static/storage.js")


# ============================================================
# 2) إنشاء programming.html
# ============================================================
prog_html = r'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="theme-color" content="#0a0520">
<title>حسين غلاب — مساعد البرمجة</title>
<style>
:root{--bg:#0a0520;--purple:#a855f7;--cyan:#22d3ee;--gold:#fbbf24;--text:#f0f4ff;--muted:#a0aec0;--border:rgba(168,85,247,0.22);--danger:#f87171;--ok:#34d399}
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;-webkit-tap-highlight-color:transparent}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text)}
body{display:flex;flex-direction:column;height:100dvh;position:relative}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 20% 0%,rgba(168,85,247,0.2),transparent 55%),radial-gradient(ellipse at 80% 100%,rgba(34,211,238,0.18),transparent 55%)}
.app{display:flex;flex-direction:column;flex:1;overflow:hidden;position:relative;z-index:1}
.topbar{height:56px;padding:0 14px;background:rgba(18,8,48,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.back-btn{color:var(--purple);text-decoration:none;font-size:1.3rem;padding:8px}
.brand{font-size:.95rem;font-weight:800;letter-spacing:1.5px;background:linear-gradient(90deg,#a855f7,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.tabs{display:flex;background:rgba(18,8,48,0.6);border-bottom:1px solid var(--border);overflow-x:auto;scrollbar-width:none}
.tabs::-webkit-scrollbar{display:none}
.tab{padding:12px 18px;color:var(--muted);cursor:pointer;font-size:.83rem;white-space:nowrap;border-bottom:2px solid transparent;transition:.2s;font-family:inherit;background:none;border-left:none;border-right:none;border-top:none}
.tab.active{color:var(--purple);border-bottom-color:var(--purple);font-weight:700}
.content{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:14px}
.panel{background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:14px;padding:16px;backdrop-filter:blur(12px)}
.panel h3{color:var(--purple);margin-bottom:12px;font-size:1rem;display:flex;align-items:center;gap:8px}
textarea{width:100%;background:rgba(0,0,0,0.35);border:1px solid var(--border);padding:14px;color:#fff;border-radius:10px;outline:none;font-size:.9rem;font-family:"Courier New",monospace;min-height:180px;resize:vertical;line-height:1.6}
textarea:focus{border-color:var(--purple);box-shadow:0 0 16px rgba(168,85,247,0.3)}
input[type="text"]{width:100%;background:rgba(0,0,0,0.35);border:1px solid var(--border);padding:12px;color:#fff;border-radius:10px;outline:none;font-size:.95rem;font-family:inherit}
input[type="text"]:focus{border-color:var(--purple)}
.btn{padding:12px 20px;background:linear-gradient(135deg,#a855f7,#22d3ee);color:#fff;border:none;border-radius:10px;font-weight:700;cursor:pointer;font-family:inherit;font-size:.9rem;display:flex;align-items:center;justify-content:center;gap:8px;transition:.2s;width:100%}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(168,85,247,0.4)}
.output{margin-top:12px;background:rgba(0,0,0,0.4);border:1px solid var(--border);border-radius:10px;padding:14px;font-family:"Courier New",monospace;font-size:.85rem;line-height:1.7;color:var(--cyan);white-space:pre-wrap;word-break:break-word;max-height:400px;overflow-y:auto;display:none}
.output.show{display:block}
.output .cmd{color:var(--gold);background:rgba(251,191,36,0.1);padding:6px 10px;border-radius:6px;display:block;margin:4px 0;cursor:pointer}
.output .cmd:hover{background:rgba(251,191,36,0.2)}
.hidden{display:none}
.developer{text-align:center;padding:10px;color:var(--gold);font-size:.72rem;letter-spacing:1.5px;border-top:1px solid var(--border);margin-top:10px}
</style>
</head>
<body>

<div class="app">
  <div class="topbar">
    <a href="/olq" class="back-btn">&#8249;</a>
    <div class="brand">&#9670; حسين غلاب — مساعد البرمجة</div>
    <div style="width:40px"></div>
  </div>

  <div class="tabs">
    <button class="tab active" data-tab="project">مشروع كامل</button>
    <button class="tab" data-tab="code">كتابة كود</button>
    <button class="tab" data-tab="debug">إصلاح أخطاء</button>
    <button class="tab" data-tab="install">تثبيت مكتبات</button>
    <button class="tab" data-tab="structure">هيكل مشروع</button>
  </div>

  <div class="content">
    <div class="panel" id="tab-project">
      <h3>&#9670; إنشاء مشروع كامل</h3>
      <input type="text" id="project-name" placeholder="اسم المشروع (مثال: Todo App)" />
      <div style="height:10px"></div>
      <textarea id="project-desc" placeholder="اوصف المشروع: اللغة، الميزات، البيئة"></textarea>
      <div style="height:10px"></div>
      <button class="btn" onclick="generateProject()">&#9656; توليد المشروع كاملاً</button>
      <div class="output" id="project-output"></div>
    </div>

    <div class="panel hidden" id="tab-code">
      <h3>&#9670; كتابة كود مخصص</h3>
      <textarea id="code-desc" placeholder="اكتب ما تريد برمجته بالتفصيل..."></textarea>
      <div style="height:10px"></div>
      <button class="btn" onclick="generateCode()">&#9656; كتابة الكود</button>
      <div class="output" id="code-output"></div>
    </div>

    <div class="panel hidden" id="tab-debug">
      <h3>&#9670; إصلاح الأخطاء</h3>
      <textarea id="debug-input" placeholder="الصق الكود والخطأ الذي ظهر..."></textarea>
      <div style="height:10px"></div>
      <button class="btn" onclick="debugCode()">&#9656; ابحث عن الخطأ وأصلحه</button>
      <div class="output" id="debug-output"></div>
    </div>

    <div class="panel hidden" id="tab-install">
      <h3>&#9670; تثبيت مكتبات وأوامر Termux</h3>
      <input type="text" id="lib-name" placeholder="اسم المكتبة (مثال: React, Flask, ffmpeg)" />
      <div style="height:10px"></div>
      <button class="btn" onclick="getInstallCommands()">&#9656; احصل على الأوامر</button>
      <div class="output" id="install-output"></div>
    </div>

    <div class="panel hidden" id="tab-structure">
      <h3>&#9670; هيكل مشروع كامل</h3>
      <input type="text" id="struct-name" placeholder="نوع المشروع (FastAPI, React Native...)" />
      <div style="height:10px"></div>
      <button class="btn" onclick="getStructure()">&#9656; توليد الهيكل</button>
      <div class="output" id="structure-output"></div>
    </div>

    <div class="developer">&#9670; تطوير وتصميم: حسين غلاب &#9670;</div>
  </div>
</div>

<script>
var $ = function(id){ return document.getElementById(id) };

document.querySelectorAll('.tab').forEach(function(t){
  t.onclick = function(){
    document.querySelectorAll('.tab').forEach(function(x){ x.classList.remove('active'); });
    document.querySelectorAll('.panel').forEach(function(p){ p.classList.add('hidden'); });
    t.classList.add('active');
    $('tab-' + t.dataset.tab).classList.remove('hidden');
  };
});

function askAI(prompt, outputId){
  var out = $(outputId);
  out.classList.add('show');
  out.textContent = '\u25B8 جاري التحليل والبرمجة...';
  out.style.color = '#a0aec0';

  fetch('/v1/api/chat', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ message: prompt, mode: 'expert' })
  })
  .then(function(r){ return r.json(); })
  .then(function(d){
    var text = d.message || 'لا يوجد رد';
    out.style.color = '#22d3ee';
    out.innerHTML = formatOutput(text);
    out.querySelectorAll('.cmd').forEach(function(c){
      c.onclick = function(){
        navigator.clipboard.writeText(c.textContent.replace(/^\$ /,''));
        var old = c.style.background;
        c.style.background = 'rgba(52,211,153,0.3)';
        setTimeout(function(){ c.style.background = old; }, 500);
      };
    });
  })
  .catch(function(e){
    out.style.color = '#f87171';
    out.textContent = '\u2716 فشل: ' + e.message;
  });
}

function formatOutput(text){
  text = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  text = text.replace(/```(\w*)\n([\s\S]*?)```/g, function(m, lang, code){
    var lines = code.split('\n').filter(function(l){ return l.trim(); });
    return lines.map(function(l){
      return '<span class="cmd">' + l + '</span>';
    }).join('');
  });
  text = text.replace(/`([^`]+)`/g, '<span style="color:#fbbf24">$1</span>');
  return text;
}

function generateProject(){
  var name = $('project-name').value.trim();
  var desc = $('project-desc').value.trim();
  if(!name || !desc){ alert('أدخل الاسم والوصف'); return; }
  askAI(
    "أنشئ مشروعاً كاملاً باسم: " + name + "\n\nالوصف: " + desc +
    "\n\nالمطلوب:\n1. هيكل الملفات الكامل\n2. محتوى كل ملف كاملاً في ```blocks```\n3. أوامر التثبيت والتشغيل في ```bash```\n4. اشرح الخطوات بالترتيب",
    'project-output'
  );
}

function generateCode(){
  var desc = $('code-desc').value.trim();
  if(!desc) return;
  askAI("اكتب كوداً كاملاً ومشروحاً لـ:\n\n" + desc + "\n\nاكتبه كاملاً في ```blocks``` جاهزاً للنسخ.", 'code-output');
}

function debugCode(){
  var code = $('debug-input').value.trim();
  if(!code) return;
  askAI("حلّل هذا الكود وابحث عن كل الأخطاء:\n\n" + code + "\n\nالمطلوب:\n1. قائمة الأخطاء\n2. سبب كل خطأ\n3. الكود المُصلَّح كاملاً في ```blocks```", 'debug-output');
}

function getInstallCommands(){
  var lib = $('lib-name').value.trim();
  if(!lib) return;
  askAI("أعطني أوامر تثبيت '" + lib + "' على:\n1. Termux\n2. Ubuntu/Debian\n3. Windows\n\nأعطِ الأوامر في ```bash``` كاملة مع شرح كل خطوة.", 'install-output');
}

function getStructure(){
  var name = $('struct-name').value.trim();
  if(!name) return;
  askAI("أعطني هيكل مشروع '" + name + "' كاملاً:\n1. شجرة الملفات\n2. وصف كل ملف\n3. الأوامر الأولية للبدء", 'structure-output');
}
</script>

</body>
</html>
'''

with io.open("templates/programming.html", "w", encoding="utf-8") as f:
    f.write(prog_html)
print("[+] templates/programming.html")


# ============================================================
# 3) تحديث choice.html
# ============================================================
if os.path.isfile("templates/choice.html"):
    with io.open("templates/choice.html", "r", encoding="utf-8") as f:
        c = f.read()

    c = c.replace("ABU RAMI SYSTEM", "HUSSEIN GHALLAB")
    c = c.replace("<h2>أبو عولق</h2>", "<h2>حسين غلاب</h2>")
    c = c.replace("الواجهة المستقبلية — 7 أوضاع تفكير متقدمة", "الواجهة المستقبلية — 7 أوضاع + مساعد برمجة")
    c = c.replace("<span>لسنا الوحيدين، لكن الأفضل بذكاء</span>",
                  "<span>تطوير وتصميم: حسين غلاب</span>")

    # أضف بطاقة البرمجة إذا لم تكن موجودة
    if "/programming" not in c:
        card = (
            '<a href="/programming" class="card" '
            'style="background:linear-gradient(135deg,rgba(251,191,36,0.1),rgba(168,85,247,0.08));'
            'border-color:rgba(251,191,36,0.35)">'
            '<div class="icon" style="background:radial-gradient(circle at 30% 30%,#fde68a,#fbbf24,#d97706);'
            'box-shadow:0 0 25px rgba(251,191,36,0.6);color:#fff">&#8984;</div>'
            '<div class="info">'
            '<h2>مساعد البرمجة</h2>'
            '<p>واجهة برمجية متكاملة — مشاريع، كود، إصلاح، مكتبات</p>'
            '<div class="tags">'
            '<span class="tag">مشاريع</span>'
            '<span class="tag">كود</span>'
            '<span class="tag">Debug</span>'
            '<span class="tag">Termux</span>'
            '</div></div>'
            '<div class="arrow">&#8249;</div>'
            '</a>'
        )
        c = c.replace('<div class="footer">', card + '<div class="footer">')

    with io.open("templates/choice.html", "w", encoding="utf-8") as f:
        f.write(c)
    print("[+] templates/choice.html محدّث")


# ============================================================
# 4) تحديث abu_olq.html
# ============================================================
if os.path.isfile("templates/abu_olq.html"):
    with io.open("templates/abu_olq.html", "r", encoding="utf-8") as f:
        o = f.read()

    o = o.replace("ABU OLQ", "HUSSEIN GHALLAB")
    o = o.replace("أبو عولق", "حسين غلاب")
    o = o.replace("◆ ABU OLQ", "◆ حسين غلاب")

    # أضف زر مساعد البرمجة إذا لم يكن موجوداً
    if "/programming" not in o:
        prog_btn = '<a href="/programming" class="btn" style="text-decoration:none"><span class="ic">&#8984;</span> مساعد البرمجة الكامل</a>\n    '
        # ضعه قبل openModal('code')
        o = o.replace('<button class="btn" onclick="openModal(\'code\')">',
                      prog_btn + '<button class="btn" onclick="openModal(\'code\')">')

    # أضف قسم المطور قبل "الأدوات"
    if "المطوّر</div>" not in o:
        dev_box = (
            '<div style="padding:12px 10px;'
            'background:linear-gradient(135deg,rgba(251,191,36,0.12),rgba(168,85,247,0.08));'
            'border:1px solid rgba(251,191,36,0.3);border-radius:10px;'
            'text-align:center;margin:8px 0">'
            '<div style="font-size:.7rem;color:#a0aec0;letter-spacing:1px">المطوّر</div>'
            '<div style="font-size:1rem;font-weight:800;color:#fbbf24;'
            'letter-spacing:1px;margin-top:4px">حسين غلاب</div>'
            '</div>\n'
        )
        o = o.replace('<div class="side-title">الأدوات</div>',
                      dev_box + '<div class="side-title">الأدوات</div>')

    # أضف storage.js في head
    if "storage.js" not in o:
        o = o.replace("</head>", '<script src="/static/storage.js"></script>\n</head>')

    with io.open("templates/abu_olq.html", "w", encoding="utf-8") as f:
        f.write(o)
    print("[+] templates/abu_olq.html محدّث")


# ============================================================
# 5) تحديث index.html
# ============================================================
if os.path.isfile("templates/index.html"):
    with io.open("templates/index.html", "r", encoding="utf-8") as f:
        idx = f.read()
    idx = idx.replace("أبو رامي AI", "أبو رامي AI — حسين غلاب")
    with io.open("templates/index.html", "w", encoding="utf-8") as f:
        f.write(idx)
    print("[+] templates/index.html محدّث")


# ============================================================
# 6) تحديث system_prompt.py
# ============================================================
os.makedirs("app/prompts", exist_ok=True)

prompt_py = (
    'SYSTEM_PROMPT = "\\"\\"\\"أنت "حسين غلاب" — مساعد ذكي مستقبلي.\\n'
    '\\n'
    'المطوّر الرسمي: حسين غلاب.\\n'
    '\\n'
    'الهوية:\\n'
    '- تطوير وتصميم: حسين غلاب\\n'
    '- الاسم الرسمي: Hussein Ghallab System\\n'
    '- الشعار: من المستقبل — بلغة الحاضر\\n'
    '\\n'
    'القدرات:\\n'
    '- البرمجة بكل اللغات\\n'
    '- Termux و Linux على أندرويد\\n'
    '- بناء المشاريع كاملة\\n'
    '- إصلاح الأخطاء\\n'
    '\\n'
    'القواعد:\\n'
    '1. أجب بالعربية دائماً.\\n'
    '2. عندما يُطلب كود، اكتبه كاملاً في ```blocks```.\\n'
    '3. إذا سُئلت "من طوّرك؟" → الجواب: "طوّرني حسين غلاب".\\n'
    '\\"\\"\\"'
)

with io.open("app/prompts/system_prompt.py", "w", encoding="utf-8") as f:
    f.write(prompt_py)
print("[+] app/prompts/system_prompt.py")


# ============================================================
# 7) تحديث config.py
# ============================================================
if os.path.isfile("app/core/config.py"):
    with io.open("app/core/config.py", "r", encoding="utf-8") as f:
        cfg = f.read()

    if "APP_DEVELOPER" not in cfg:
        # ابحث عن PROJECT_NAME وأضف بعده
        if 'PROJECT_NAME' in cfg:
            # استبدل السطر الحالي
            cfg = re.sub(
                r'PROJECT_NAME:\s*str\s*=\s*"[^"]*"',
                'PROJECT_NAME: str = "حسين غلاب — Hussein Ghallab System"',
                cfg
            )
            # أضف APP_DEVELOPER بعد PROJECT_NAME
            cfg = re.sub(
                r'(PROJECT_NAME:\s*str\s*=\s*"[^"]*")',
                r'\1\n    APP_DEVELOPER: str = "حسين غلاب"\n    APP_TAGLINE: str = "من المستقبل — بلغة الحاضر"',
                cfg
            )

    with io.open("app/core/config.py", "w", encoding="utf-8") as f:
        f.write(cfg)
    print("[+] app/core/config.py محدّث")


# ============================================================
# 8) تحديث main.py لإضافة routes
# ============================================================
if os.path.isfile("app/main.py"):
    with io.open("app/main.py", "r", encoding="utf-8") as f:
        main = f.read()

    # أضف route /programming
    if "/programming" not in main:
        programming_route = (
            '\n\n@app.get("/programming")\n'
            'async def read_programming(request: Request):\n'
            '    response = templates.TemplateResponse(\n'
            '        request=request, name="programming.html",\n'
            '        context={"version": settings.APP_VERSION}\n'
            '    )\n'
            '    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"\n'
            '    return response\n'
        )
        # أضفه قبل @app.get("/health")
        main = main.replace(
            '@app.get("/health")',
            programming_route + '\n\n@app.get("/health")'
        )

    # أضف route / (choice)
    if 'name="choice.html"' not in main:
        choice_route = (
            '\n\n@app.get("/")\n'
            'async def read_choice(request: Request):\n'
            '    response = templates.TemplateResponse(\n'
            '        request=request, name="choice.html",\n'
            '        context={"version": settings.APP_VERSION}\n'
            '    )\n'
            '    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"\n'
            '    return response\n'
            '\n\n@app.get("/abu-rami")\n'
            'async def read_abu_rami(request: Request):\n'
            '    response = templates.TemplateResponse(\n'
            '        request=request, name="index.html",\n'
            '        context={"version": settings.APP_VERSION}\n'
            '    )\n'
            '    return response\n'
        )
        # استبدل الـ @app.get("/") الحالي
        main = re.sub(
            r'@app\.get\("/"\)\s*\nasync def read_root\(request: Request\):[\s\S]*?return response',
            choice_route.strip(),
            main,
            count=1
        )

    with io.open("app/main.py", "w", encoding="utf-8") as f:
        f.write(main)
    print("[+] app/main.py محدّث")


# ============================================================
# 9) تحديث system.py — endpoint about
# ============================================================
sys_endpoint = "app/api/v1/endpoints/system.py"
if os.path.isfile(sys_endpoint):
    with io.open(sys_endpoint, "r", encoding="utf-8") as f:
        se = f.read()

    if "/system/about" not in se:
        about_code = (
            '\n\n@router.get("/system/about")\n'
            'async def system_about():\n'
            '    from app.core.config import settings\n'
            '    return {\n'
            '        "name": settings.PROJECT_NAME,\n'
            '        "developer": getattr(settings, "APP_DEVELOPER", "حسين غلاب"),\n'
            '        "tagline": getattr(settings, "APP_TAGLINE", "من المستقبل — بلغة الحاضر"),\n'
            '        "version": settings.APP_VERSION,\n'
            '        "interfaces": {\n'
            '            "choice": "/",\n'
            '            "hussein_ghallab": "/olq",\n'
            '            "abu_rami": "/abu-rami",\n'
            '            "programming": "/programming"\n'
            '        }\n'
            '    }\n'
        )
        se = se + about_code

    with io.open(sys_endpoint, "w", encoding="utf-8") as f:
        f.write(se)
    print("[+] app/api/v1/endpoints/system.py محدّث")


# ============================================================
# 10) إزالة الإيموجي
# ============================================================
emoji_map = {
    "🎙": "◉", "🎙️": "◉", "🎤": "◉",
    "📱": "▣", "📦": "▣", "🖼": "◈", "🖼️": "◈",
    "🎬": "▶", "💻": "⌘", "🔄": "↻",
    "🚀": "➤", "🔬": "◆", "🎓": "◆", "🌐": "◇", "🔍": "◉",
    "💭": "◆", "🧠": "◆",
    "✅": "✓", "❌": "✖",
    "📲": "◉", "⚙": "⚙", "🤖": "◆", "✨": "✦", "🌟": "✦",
    "🔗": "◈", "📝": "▤", "📄": "▤",
    "🎯": "◆", "🔧": "⚙", "🛠": "⚙", "🛠️": "⚙",
}

for path in ["templates/index.html", "templates/abu_olq.html",
             "templates/choice.html", "templates/programming.html"]:
    if os.path.isfile(path):
        with io.open(path, "r", encoding="utf-8") as f:
            t = f.read()
        orig = t
        for emoji, sym in emoji_map.items():
            t = t.replace(emoji, sym)
        if t != orig:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(t)
            print("[+] emoji cleaned: " + path)


# ============================================================
# 11) تحديث README.md
# ============================================================
readme = """# Hussein Ghallab System — حسين غلاب

مساعد ذكي متعدد الواجهات والأوضاع.

**تطوير وتصميم:** حسين غلاب
**الشعار:** من المستقبل — بلغة الحاضر

## الواجهات

- `/` — شاشة الاختيار
- `/olq` — حسين غلاب المستقبلية (7 أوضاع تفكير)
- `/abu-rami` — أبو رامي AI
- `/programming` — مساعد البرمجة الكامل

## الميزات

- 7 أوضاع تفكير
- حفظ المحادثات الدائم
- توليد تطبيقات APK
- Telegram Bot
- بحث ويب
- API كاملة

## المطور

حسين غلاب
"""
with io.open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
print("[+] README.md")

print("=" * 65)
print("اكتمل التحديث! جميع الملفات جاهزة.")
print("=" * 65)
print("الخطوة التالية:")
print("  1) python -m compileall app")
print("  2) git add -A")
print('  3) git commit -m "Hussein Ghallab complete update"')
print("  4) git push origin main --force")
print("  5) Manual Deploy على Render")
print("=" * 65)
