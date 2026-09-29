#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد مشروع "أبو عولق" — الواجهة المستقبلية المتقدمة
- 6 أوضاع تفكير
- تليغرام بوت
- مساعد Termux
- API عامة
- بحث ويب
"""

import os

FILES = {}

# ============================================================
# 1) قالب الواجهة الجديدة
# ============================================================
FILES["templates/abu_olq.html"] = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<meta name="theme-color" content="#0a0520">
<title>أبو عولق — من المستقبل</title>
<style>
:root{
  --bg:#0a0520;
  --bg2:#120830;
  --purple:#a855f7;
  --violet:#8b5cf6;
  --cyan:#22d3ee;
  --teal:#14b8a6;
  --gold:#fbbf24;
  --rose:#f472b6;
  --text:#f0f4ff;
  --muted:#a0aec0;
  --border:rgba(168,85,247,0.22);
  --danger:#f87171;
  --ok:#34d399;
}
*{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,-apple-system,"Segoe UI",Tahoma,sans-serif;-webkit-tap-highlight-color:transparent}
html,body{height:100%;overflow:hidden;background:var(--bg);color:var(--text)}
body{display:flex;flex-direction:column;height:100dvh;position:relative}
body::before{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse at 20% 0%, rgba(168,85,247,0.18), transparent 50%),
    radial-gradient(ellipse at 80% 100%, rgba(34,211,238,0.15), transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(139,92,246,0.08), transparent 60%);
  animation:hue 12s infinite alternate;
}
@keyframes hue{from{filter:hue-rotate(0deg)}to{filter:hue-rotate(25deg)}}

/* ========== Splash ========== */
#splash{position:fixed;inset:0;z-index:9000;background:#000;display:flex;align-items:center;justify-content:center;transition:opacity 1s;overflow:hidden}
#splash.hidden{opacity:0;pointer-events:none}
#splashCanvas{position:absolute;inset:0}
#splashInfo{position:relative;z-index:2;text-align:center;opacity:0;transition:opacity 1.2s;padding:20px}
#splashInfo.show{opacity:1}
#splashInfo h1{
  font-size:clamp(2rem,7vw,3.2rem);font-weight:900;letter-spacing:4px;
  background:linear-gradient(90deg,#a855f7,#22d3ee,#fbbf24,#f472b6,#a855f7);
  background-size:300% 100%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:shine 3s infinite linear;
  filter:drop-shadow(0 0 30px rgba(168,85,247,0.7));
}
@keyframes shine{from{background-position:0% 50%}to{background-position:300% 50%}}
#splashInfo p{color:var(--muted);font-size:1rem;margin:14px 20px 24px;letter-spacing:1px}
#splashInfo button{padding:14px 44px;background:linear-gradient(135deg,#a855f7,#22d3ee);border:none;border-radius:30px;color:#fff;font-weight:800;font-size:1.05rem;cursor:pointer;box-shadow:0 0 40px rgba(168,85,247,0.6)}
#splashInfo button:hover{transform:translateY(-2px);box-shadow:0 0 60px rgba(34,211,238,0.8)}

/* ========== Layout ========== */
.app{display:flex;flex:1;overflow:hidden;position:relative;z-index:1}

/* ========== Sidebar ========== */
.sidebar{
  width:300px;height:100%;background:rgba(18,8,48,0.85);
  backdrop-filter:blur(24px);border-left:1px solid var(--border);
  padding:16px;display:flex;flex-direction:column;gap:10px;
  transition:transform .3s;z-index:2000;position:absolute;right:0;top:0;bottom:0;
  overflow-y:auto;
}
.sidebar.collapsed{transform:translateX(100%)}
.brand-row{display:flex;align-items:center;justify-content:space-between;padding-bottom:12px;border-bottom:1px solid var(--border)}
.brand-name{
  font-size:1.15rem;font-weight:900;letter-spacing:2px;
  background:linear-gradient(90deg,#a855f7,#22d3ee,#fbbf24);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.stat{display:flex;justify-content:space-between;font-size:.8rem;color:var(--muted);padding:7px 10px;background:rgba(255,255,255,0.03);border:1px solid rgba(168,85,247,0.15);border-radius:8px}
.stat span:last-child{color:var(--ok);font-weight:600}
.side-title{color:var(--muted);font-size:.72rem;letter-spacing:1.5px;margin-top:8px;text-transform:uppercase}
.btn{
  width:100%;padding:11px 14px;background:rgba(255,255,255,0.03);
  color:var(--text);border:1px solid rgba(168,85,247,0.2);
  border-radius:10px;cursor:pointer;font-size:.9rem;
  display:flex;align-items:center;gap:10px;transition:.2s;
  font-family:inherit;text-align:right;
}
.btn:hover,.btn:active{background:rgba(168,85,247,0.15);border-color:var(--purple);box-shadow:0 0 16px rgba(168,85,247,0.3)}
.btn .ic{color:var(--purple);font-size:1.05rem;font-weight:bold}

/* ========== Main ========== */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;background:radial-gradient(circle at 50% 30%,#1a0d3a 0%,#0a0520 100%)}
.topbar{height:56px;padding:0 14px;background:rgba(18,8,48,0.7);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
.brand-mid{
  font-size:1.05rem;font-weight:900;letter-spacing:2px;
  background:linear-gradient(90deg,#a855f7,#22d3ee);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  display:flex;align-items:center;gap:8px;
}

/* ========== Thinking modes row ========== */
.modes-row{
  display:flex;gap:8px;padding:10px 12px;overflow-x:auto;scrollbar-width:none;
  background:rgba(18,8,48,0.55);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--border);
}
.modes-row::-webkit-scrollbar{display:none}
.mode{
  flex-shrink:0;padding:8px 14px;border-radius:22px;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(168,85,247,0.2);
  color:var(--text);font-size:.82rem;
  cursor:pointer;display:flex;align-items:center;gap:6px;
  transition:.25s;font-family:inherit;white-space:nowrap;
}
.mode:hover{border-color:var(--purple);box-shadow:0 0 14px rgba(168,85,247,0.35)}
.mode.active{
  background:linear-gradient(135deg,#a855f7,#22d3ee);
  border-color:transparent;color:#fff;font-weight:700;
  box-shadow:0 0 24px rgba(168,85,247,0.6);
}
.mode .ic{font-weight:bold}

/* ========== Messages ========== */
.messages{flex:1;overflow-y:auto;padding:18px 16px 8px;display:flex;flex-direction:column;gap:14px;scroll-behavior:smooth}
.msg{max-width:88%;padding:14px 18px;border-radius:14px;line-height:1.75;font-size:.95rem;word-break:break-word;white-space:pre-wrap;animation:fade .3s ease;position:relative}
@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.msg.user{background:linear-gradient(135deg,#8b5cf6,#a855f7);color:#fff;align-self:flex-start;border-bottom-right-radius:4px;box-shadow:0 4px 20px rgba(139,92,246,0.35)}
.msg.assistant{background:rgba(255,255,255,0.04);border:1px solid var(--border);backdrop-filter:blur(12px);align-self:flex-end;border-bottom-left-radius:4px}
.msg.assistant::before{content:"◆";color:var(--purple);margin-left:8px;font-weight:bold}
.msg.error{color:var(--danger);border-color:rgba(248,113,113,0.4)}
.msg.loading{opacity:.7;font-style:italic}
.msg img,.msg video{max-width:100%;border-radius:12px;display:block;margin-top:8px}
.msg code{background:rgba(0,0,0,0.4);padding:2px 6px;border-radius:4px;font-family:'Courier New',monospace;color:var(--cyan)}
.msg pre{background:rgba(0,0,0,0.5);padding:12px;border-radius:8px;overflow-x:auto;margin:8px 0;border-right:3px solid var(--purple)}

/* ========== Input area ========== */
.input-wrap{padding:12px;padding-bottom:calc(12px + env(safe-area-inset-bottom));background:rgba(18,8,48,0.75);backdrop-filter:blur(22px);border-top:1px solid var(--border);display:flex;gap:8px;align-items:flex-end}
.input-shell{flex:1;display:flex;align-items:flex-end;background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:26px;padding:4px;transition:.25s}
.input-shell:focus-within{border-color:var(--purple);box-shadow:0 0 22px rgba(168,85,247,0.35)}
textarea{flex:1;min-height:40px;max-height:200px;background:transparent;border:none;outline:none;padding:10px 16px;color:var(--text);font-size:1rem;font-family:inherit;resize:none;line-height:1.5;overflow-y:auto}
textarea::placeholder{color:var(--muted)}
.ibtn{width:44px;height:44px;border-radius:50%;background:rgba(168,85,247,0.1);border:1px solid var(--border);color:var(--purple);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1.15rem;transition:.25s;flex-shrink:0;font-weight:bold}
.ibtn:hover,.ibtn:active{background:var(--purple);color:#fff;box-shadow:0 0 18px var(--purple)}
.ibtn.send{background:linear-gradient(135deg,#a855f7,#22d3ee);color:#fff;border:none}

/* ========== Voice Overlay ========== */
#voice{position:fixed;inset:0;z-index:3500;background:rgba(10,5,32,0.97);backdrop-filter:blur(30px);display:none;flex-direction:column;align-items:center;justify-content:center;gap:26px;padding:20px;text-align:center}
#voice.active{display:flex}
.orb{width:160px;height:160px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#f0abfc,#a855f7,#7c3aed);box-shadow:0 0 60px #a855f7,inset 0 0 40px rgba(255,255,255,0.2);animation:pulse 1.6s infinite alternate}
@keyframes pulse{0%{transform:scale(.9);filter:hue-rotate(0deg)}100%{transform:scale(1.12);filter:hue-rotate(40deg)}}
#voice h3{color:var(--purple);font-size:1.15rem;letter-spacing:1px}
#heard{color:var(--muted);font-size:1rem;max-width:90%;min-height:1.5em;font-style:italic}

/* ========== Modals ========== */
.modal{position:fixed;inset:0;z-index:4000;background:rgba(0,0,0,0.9);backdrop-filter:blur(10px);display:none;align-items:center;justify-content:center;padding:16px}
.modal.active{display:flex}
.modal-body{width:100%;max-width:480px;max-height:88vh;overflow-y:auto;background:linear-gradient(180deg,#1a0d3a,#120830);border:1px solid var(--purple);border-radius:18px;padding:24px;display:flex;flex-direction:column;gap:12px;box-shadow:0 24px 60px rgba(0,0,0,0.7),0 0 50px rgba(168,85,247,0.25)}
.modal-body h3{color:var(--purple);display:flex;align-items:center;gap:8px;font-size:1.1rem;letter-spacing:1px}
.modal-body label{font-size:.82rem;color:var(--muted)}
.modal-body input,.modal-body textarea,.modal-body select{width:100%;background:rgba(255,255,255,0.04);border:1px solid var(--border);padding:11px;color:#fff;border-radius:9px;outline:none;font-size:.95rem;font-family:inherit}
.modal-body input:focus,.modal-body textarea:focus{border-color:var(--purple);box-shadow:0 0 16px rgba(168,85,247,0.3)}
.modal-body textarea{min-height:90px;resize:vertical}
.modal-body .btn{justify-content:center;padding:12px;font-weight:700}
.modal-body .btn.primary{background:linear-gradient(135deg,#a855f7,#22d3ee);border:none;color:#fff}

#update{position:fixed;top:14px;left:50%;transform:translateX(-50%) translateY(-80px);background:linear-gradient(135deg,#a855f7,#22d3ee);color:#fff;padding:10px 22px;border-radius:24px;font-weight:700;z-index:5500;cursor:pointer;transition:.4s;box-shadow:0 6px 30px rgba(168,85,247,0.6)}
#update.active{transform:translateX(-50%) translateY(0)}

/* ========== Mobile ========== */
@media (max-width:760px){
  .msg{max-width:92%}
}
</style>
</head>
<body>

<div id="update" onclick="location.reload(true)">⚡ تحديث جديد متاح — اضغط للتحديث</div>

<div id="splash">
  <canvas id="splashCanvas"></canvas>
  <div id="splashInfo">
    <h1>ABU OLQ</h1>
    <p>أبو عولق — من المستقبل بلغة الحاضر</p>
    <button onclick="closeSplash()">ادخل الآن</button>
  </div>
</div>

<div class="sb-overlay" id="sbOverlay" onclick="toggleSidebar()" style="position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:1999;display:none"></div>

<div class="app">
  <aside class="sidebar collapsed" id="sidebar">
    <div class="brand-row">
      <div class="brand-name">ABU OLQ</div>
      <button class="ibtn" style="width:32px;height:32px;font-size:1rem" onclick="toggleSidebar()">✕</button>
    </div>
    <div class="stat"><span>الحالة</span><span id="s-status">...</span></div>
    <div class="stat"><span>الإصدار</span><span id="s-ver">-</span></div>
    <div class="stat"><span>المزوّد</span><span id="s-prov">-</span></div>
    <div class="stat"><span>الوضع</span><span id="s-mode">عادي</span></div>

    <div class="side-title">الأدوات</div>
    <button class="btn" onclick="newChat()"><span class="ic">＋</span> محادثة جديدة</button>
    <button class="btn" onclick="openModal('telegram')"><span class="ic">◈</span> ربط Telegram</button>
    <button class="btn" onclick="openModal('termux')"><span class="ic">⌘</span> مساعد Termux</button>
    <button class="btn" onclick="openModal('code')"><span class="ic">◆</span> مساعد الكود</button>
    <button class="btn" onclick="openModal('app')"><span class="ic">▣</span> توليد APK</button>
    <button class="btn" onclick="openModal('image')"><span class="ic">◉</span> توليد صورة</button>
    <button class="btn" onclick="openModal('api')"><span class="ic">⚙</span> API للمطورين</button>
    <button class="btn" onclick="checkUpdate(true)"><span class="ic">↻</span> فحص التحديثات</button>
  </aside>

  <main class="main">
    <div class="topbar">
      <button class="ibtn" style="width:40px;height:40px" onclick="toggleSidebar()">☰</button>
      <div class="brand-mid">◆ ABU OLQ</div>
      <button class="ibtn" style="width:40px;height:40px" onclick="newChat()">＋</button>
    </div>

    <div class="modes-row" id="modes">
      <button class="mode active" data-mode="normal"><span class="ic">◆</span> تفكير عادي</button>
      <button class="mode" data-mode="fast"><span class="ic">⚡</span> تفكير سريع</button>
      <button class="mode" data-mode="deep"><span class="ic">🔬</span> تفكير عميق</button>
      <button class="mode" data-mode="expert"><span class="ic">🎓</span> وضع الخبير</button>
      <button class="mode" data-mode="expanded"><span class="ic">🌐</span> تفكير موسّع</button>
      <button class="mode" data-mode="search"><span class="ic">🔍</span> بحث ويب</button>
      <button class="mode" data-mode="termux"><span class="ic">⌘</span> مساعد Termux</button>
    </div>

    <div class="messages" id="messages">
      <div class="msg assistant">مرحباً بك في <b>أبو عولق</b> — المساعد المستقبلي متعدد الأوضاع. اختر وضع التفكير من الشريط أعلاه، أو اكتب سؤالك مباشرة. يمكنني: البرمجة، البحث، التحليل العميق، ربط Telegram، وتوليد تطبيقات APK.</div>
    </div>

    <div class="input-wrap">
      <div class="input-shell">
        <button class="ibtn" onclick="toggleVoice()">🎙</button>
        <textarea id="input" placeholder="اكتب رسالتك... (Enter = سطر جديد، Ctrl+Enter = إرسال)" rows="1"></textarea>
      </div>
      <button class="ibtn send" onclick="send()">➤</button>
    </div>
  </main>
</div>

<div id="voice">
  <div class="orb"></div>
  <h3 id="voice-title">جاري الاستماع...</h3>
  <div id="heard"></div>
  <button class="ibtn" style="width:auto;padding:12px 34px;border-radius:22px" onclick="toggleVoice()">إنهاء</button>
</div>

<!-- Modals -->
<div class="modal" id="modal-telegram">
  <div class="modal-body">
    <h3>◈ ربط Telegram Bot</h3>
    <label>توكن البوت (من @BotFather)</label>
    <input id="tg-token" placeholder="123456:ABC-DEF..." />
    <label>Webhook URL (اتركه فارغاً للتشغيل الذاتي)</label>
    <input id="tg-webhook" placeholder="https://abu-rami-app-s90e.onrender.com/v1/telegram/webhook" />
    <button class="btn primary" onclick="linkTelegram()">ربط البوت</button>
    <button class="btn" onclick="closeModal('telegram')">إلغاء</button>
    <div id="tg-status" style="font-size:.8rem;color:var(--muted);margin-top:8px"></div>
  </div>
</div>

<div class="modal" id="modal-termux">
  <div class="modal-body">
    <h3>⌘ مساعد Termux</h3>
    <label>الصق الأمر أو الخطأ الذي حصل</label>
    <textarea id="termux-input" placeholder="مثال: apt install python3 يظهر لي خطأ E: Unable to locate package"></textarea>
    <button class="btn primary" onclick="askTermux()">اشرح وأصلح</button>
    <button class="btn" onclick="closeModal('termux')">إلغاء</button>
  </div>
</div>

<div class="modal" id="modal-code">
  <div class="modal-body">
    <h3>◆ مساعد الكود</h3>
    <label>اشرح ما تريد برمجته أو الصق الكود</label>
    <textarea id="code-input" placeholder="مثال: اكتب لي دالة Python لقراءة ملف JSON وطباعته بشكل مرتب"></textarea>
    <button class="btn primary" onclick="askCode()">إرسال</button>
    <button class="btn" onclick="closeModal('code')">إلغاء</button>
  </div>
</div>

<div class="modal" id="modal-app">
  <div class="modal-body">
    <h3>▣ توليد تطبيق APK</h3>
    <label>اسم التطبيق</label>
    <input id="app-name" placeholder="مثال: Notes App" />
    <label>الوصف</label>
    <textarea id="app-desc" placeholder="ماذا يفعل التطبيق؟"></textarea>
    <button class="btn primary" onclick="generateApp()">توليد</button>
    <button class="btn" onclick="closeModal('app')">إلغاء</button>
  </div>
</div>

<div class="modal" id="modal-image">
  <div class="modal-body">
    <h3>◉ توليد صورة</h3>
    <label>وصف الصورة</label>
    <textarea id="img-prompt" placeholder="مثال: قطة فضائية سايبربانك"></textarea>
    <button class="btn primary" onclick="generateImage()">توليد</button>
    <button class="btn" onclick="closeModal('image')">إلغاء</button>
  </div>
</div>

<div class="modal" id="modal-api">
  <div class="modal-body">
    <h3>⚙ API للمطورين</h3>
    <label>نقاط النهاية المتاحة</label>
    <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;font-family:monospace;font-size:.78rem;line-height:1.9;color:var(--cyan)">
      POST /v1/api/chat<br>
      POST /v1/api/generate<br>
      POST /v1/api/search<br>
      POST /v1/api/analyze-code<br>
      POST /v1/telegram/webhook<br>
      GET&nbsp;&nbsp;/v1/system/status
    </div>
    <label>مثال استدعاء</label>
    <div style="background:rgba(0,0,0,0.3);padding:12px;border-radius:8px;font-family:monospace;font-size:.75rem;line-height:1.8;color:var(--gold)">
      curl -X POST \<br>
      &nbsp;&nbsp;https://abu-rami-app-s90e.onrender.com/v1/api/chat \<br>
      &nbsp;&nbsp;-H "Content-Type: application/json" \<br>
      &nbsp;&nbsp;-d '{"message":"مرحبا","mode":"deep"}'
    </div>
    <button class="btn" onclick="closeModal('api')">إغلاق</button>
  </div>
</div>

<script>
"use strict";
var $ = function(id){return document.getElementById(id)};
var currentConv = null;
var currentVersion = null;
var currentMode = "normal";
var voiceEnabled = false;
var recognition = null;

/* ============ SPLASH — neural network to text ============ */
(function(){
  var canvas = $('splashCanvas');
  var ctx = canvas.getContext('2d');
  var W, H, DPR;
  function resize(){
    DPR = window.devicePixelRatio || 1;
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W*DPR; canvas.height = H*DPR;
    canvas.style.width = W+'px'; canvas.style.height = H+'px';
    ctx.setTransform(DPR,0,0,DPR,0,0);
  }
  resize();
  window.addEventListener('resize', resize);

  var targets = [];
  function build(){
    var off = document.createElement('canvas');
    var ow = Math.min(W, 900), oh = 220;
    off.width = ow; off.height = oh;
    var o = off.getContext('2d');
    var fs = Math.min(ow/6, 100);
    o.font = '900 ' + fs + 'px system-ui, sans-serif';
    o.textAlign = 'center'; o.textBaseline = 'middle';
    o.fillStyle = '#fff';
    o.fillText('ABU OLQ', ow/2, oh/2);
    var img = o.getImageData(0,0,ow,oh);
    targets = [];
    var ox = (W-ow)/2, oy = H/2 - oh/2;
    for(var y=0;y<oh;y+=4){
      for(var x=0;x<ow;x+=4){
        var i=(y*ow+x)*4;
        if(img.data[i+3]>128) targets.push({x:x+ox,y:y+oy});
      }
    }
    for(var k=targets.length-1;k>0;k--){
      var j=Math.floor(Math.random()*(k+1));
      var t=targets[k]; targets[k]=targets[j]; targets[j]=t;
    }
  }
  build();

  var symbols = ['π','∑','∫','∞','√','α','β','γ','ħ','λ','Ω','Δ','⚛','⚗','</>','{}','()','01','AI','ML','∞','◈','◆','⚡'];
  var colors = ['#a855f7','#22d3ee','#fbbf24','#f472b6','#8b5cf6'];
  var particles = [], syms = [];

  for(var i=0;i<targets.length;i++){
    particles.push({
      x: targets[i].x + (Math.random()-0.5)*100,
      y: -40 - Math.random()*150,
      vx: (Math.random()-0.5)*1.5,
      vy: 1.5 + Math.random()*3,
      tx: targets[i].x, ty: targets[i].y,
      size: 1 + Math.random()*2,
      life: 0,
      delay: Math.random()*400,
      color: colors[Math.floor(Math.random()*colors.length)],
      settled: false,
      glow: 0.7
    });
  }

  for(var s=0;s<50;s++){
    syms.push({
      x: Math.random()*W, y: Math.random()*H,
      vy: -0.25 - Math.random()*0.5,
      vx: (Math.random()-0.5)*0.4,
      alpha: 0.12 + Math.random()*0.4,
      symbol: symbols[Math.floor(Math.random()*symbols.length)],
      size: 14 + Math.random()*22,
      color: colors[Math.floor(Math.random()*colors.length)]
    });
  }

  var start = performance.now();
  function frame(now){
    var el = now - start;
    ctx.fillStyle = 'rgba(0,0,0,0.2)';
    ctx.fillRect(0,0,W,H);

    for(var s=0;s<syms.length;s++){
      var sp = syms[s];
      sp.y += sp.vy; sp.x += sp.vx;
      if(sp.y < -40){ sp.y = H+40; sp.x = Math.random()*W; }
      ctx.save();
      ctx.globalAlpha = sp.alpha;
      ctx.fillStyle = sp.color;
      ctx.font = 'bold ' + sp.size + 'px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText(sp.symbol, sp.x, sp.y);
      ctx.restore();
    }

    for(var i=0;i<particles.length;i++){
      var p = particles[i];
      if(el < p.delay) continue;
      p.life++;
      if(!p.settled){
        var dx = p.tx - p.x, dy = p.ty - p.y;
        var d = Math.sqrt(dx*dx + dy*dy) || 1;
        var f = Math.min(0.7, 220/(d+40));
        p.vx += (dx/d)*f*0.2;
        p.vy += (dy/d)*f*0.2;
        p.vx *= 0.90; p.vy *= 0.90;
        p.x += p.vx; p.y += p.vy;
        if(d < 1.5){ p.settled = true; p.x = p.tx; p.y = p.ty; }
      } else {
        p.glow = 0.5 + Math.abs(Math.sin((p.life + i)*0.05))*0.5;
      }
      var a = p.settled ? 0.95 : Math.min(1, p.life/40);
      ctx.save();
      ctx.globalAlpha = a;
      ctx.fillStyle = p.color;
      ctx.shadowBlur = p.settled ? 15*p.glow : 6;
      ctx.shadowColor = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
      ctx.fill();
      ctx.restore();
    }

    if(el > 3200 && !$('splashInfo').classList.contains('show')){
      $('splashInfo').classList.add('show');
    }
    if(el < 10000) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  setTimeout(function(){
    var sp = $('splash');
    if(sp && !sp.classList.contains('hidden')) sp.classList.add('hidden');
  }, 9000);
})();

function closeSplash(){
  var sp = $('splash');
  sp.classList.add('hidden');
  setTimeout(function(){ sp.style.display = 'none'; }, 1000);
}

/* ============ Sidebar ============ */
function toggleSidebar(){
  $('sidebar').classList.toggle('collapsed');
  $('sbOverlay').style.display = $('sidebar').classList.contains('collapsed') ? 'none' : 'block';
}

/* ============ Modes ============ */
document.querySelectorAll('.mode').forEach(function(btn){
  btn.addEventListener('click', function(){
    document.querySelectorAll('.mode').forEach(function(b){ b.classList.remove('active'); });
    btn.classList.add('active');
    currentMode = btn.getAttribute('data-mode');
    var names = {
      normal: 'عادي', fast: 'سريع', deep: 'عميق',
      expert: 'خبير', expanded: 'موسّع', search: 'بحث', termux: 'Termux'
    };
    $('s-mode').innerText = names[currentMode] || 'عادي';
  });
});

/* ============ Status ============ */
function checkStatus(){
  fetch('/v1/system/status').then(function(r){return r.json()}).then(function(d){
    $('s-status').innerText = 'متصل';
    $('s-ver').innerText = d.version || '-';
    currentVersion = d.version;
    if(d.providers){
      var act = [];
      if(d.providers.gemini) act.push('Gemini');
      if(d.providers.groq) act.push('Groq');
      if(d.providers.openrouter) act.push('OpenRouter');
      if(d.providers.deepseek) act.push('DeepSeek');
      $('s-prov').innerText = act.length ? act[0] : 'لا يوجد';
    }
  }).catch(function(){
    $('s-status').innerText = 'غير متصل';
    $('s-status').style.color = '#f87171';
  });
}
checkStatus();

function checkUpdate(manual){
  fetch('/version?t=' + Date.now()).then(function(r){return r.json()}).then(function(d){
    if(currentVersion && d.version && d.version !== currentVersion){
      $('update').classList.add('active');
      if(manual) alert('يوجد تحديث جديد: ' + d.version);
    } else if(manual) alert('أنت على أحدث إصدار: ' + d.version);
  }).catch(function(){ if(manual) alert('تعذر فحص التحديثات'); });
}
setInterval(function(){ checkUpdate(false); }, 60000);

/* ============ Messages ============ */
function esc(t){ var d=document.createElement('div'); d.textContent=t; return d.innerHTML; }

function addMsg(text, cls){
  var div = document.createElement('div');
  div.className = 'msg ' + (cls || 'assistant');
  if((cls||'').indexOf('user') > -1){
    div.textContent = text;
  } else {
    var cleaned = esc(text);
    cleaned = cleaned.replace(/```([\s\S]*?)```/g, '<pre>$1</pre>');
    cleaned = cleaned.replace(/`([^`]+)`/g, '<code>$1</code>');
    div.innerHTML = cleaned;
  }
  $('messages').appendChild(div);
  $('messages').scrollTop = $('messages').scrollHeight;
  return div;
}

function addHtml(html, cls){
  var div = document.createElement('div');
  div.className = 'msg ' + (cls || 'assistant');
  div.innerHTML = html;
  $('messages').appendChild(div);
  $('messages').scrollTop = $('messages').scrollHeight;
  return div;
}

/* ============ Send ============ */
function send(){
  var text = $('input').value.trim();
  if(!text) return;

  addMsg(text, 'user');
  $('input').value = '';
  autosize();

  var loading = addHtml('<span style="color:var(--purple)">◆</span> جاري التفكير في وضع <b>' + currentMode + '</b>...', 'assistant loading');

  fetch('/v1/api/chat', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({message:text, conversation_id:currentConv, mode:currentMode})
  })
  .then(function(r){ return r.json(); })
  .then(function(d){
    if(d.conversation_id) currentConv = d.conversation_id;
    loading.remove();
    addMsg(d.message || 'لا يوجد رد', 'assistant');
    if(voiceEnabled) speak(d.message || '');
  })
  .catch(function(){
    loading.remove();
    addHtml('<span style="color:var(--danger)">✖</span> تعذر الاتصال بالخادم.', 'assistant error');
  });
}

function newChat(){
  currentConv = null;
  $('messages').innerHTML = '<div class="msg assistant">محادثة جديدة بدأت. اختر وضع التفكير واكتب سؤالك.</div>';
  $('sidebar').classList.add('collapsed');
  $('sbOverlay').style.display = 'none';
}

/* ============ Voice ============ */
function toggleVoice(){
  var ov = $('voice');
  var active = ov.classList.contains('active');
  if(!active){
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if(!SR){ alert('المتصفح لا يدعم التعرف على الصوت'); return; }
    recognition = new SR();
    recognition.lang = 'ar-SA';
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.onresult = function(e){
      var text = '';
      for(var i=e.resultIndex;i<e.results.length;i++) text += e.results[i][0].transcript;
      $('heard').innerText = text;
      if(e.results[e.results.length-1].isFinal){
        ov.classList.remove('active');
        try{ recognition.stop(); }catch(err){}
        voiceEnabled = true;
        $('input').value = text.trim();
        send();
      }
    };
    recognition.onerror = function(){ ov.classList.remove('active'); };
    try{
      recognition.start();
      ov.classList.add('active');
      $('heard').innerText = '';
    }catch(e){ alert('تعذر تشغيل الميكروفون'); }
  } else {
    ov.classList.remove('active');
    try{ recognition.stop(); }catch(e){}
  }
}

function speak(text){
  if(!('speechSynthesis' in window)) return;
  window.speechSynthesis.cancel();
  var u = new SpeechSynthesisUtterance(text);
  u.lang = 'ar-SA'; u.rate = 1.0;
  window.speechSynthesis.speak(u);
}

/* ============ Modals ============ */
function openModal(n){ $('modal-'+n).classList.add('active'); }
function closeModal(n){ $('modal-'+n).classList.remove('active'); }

/* ============ Telegram ============ */
function linkTelegram(){
  var token = $('tg-token').value.trim();
  var webhook = $('tg-webhook').value.trim();
  if(!token){ alert('أدخل توكن البوت'); return; }

  $('tg-status').innerText = 'جاري الربط...';
  fetch('/v1/telegram/link', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({token:token, webhook_url:webhook})
  })
  .then(function(r){ return r.json(); })
  .then(function(d){
    if(d.success){
      $('tg-status').innerHTML = '<span style="color:var(--ok)">✅ تم ربط البوت: @' + (d.bot_username || 'unknown') + '</span>';
      addHtml('<span style="color:var(--purple)">◈</span> تم ربط Telegram Bot بنجاح: <b>@' + (d.bot_username||'') + '</b>');
    } else {
      $('tg-status').innerHTML = '<span style="color:var(--danger)">✖ ' + esc(d.message || 'فشل الربط') + '</span>';
    }
  })
  .catch(function(){
    $('tg-status').innerHTML = '<span style="color:var(--danger)">✖ فشل الاتصال</span>';
  });
}

/* ============ Termux ============ */
function askTermux(){
  var text = $('termux-input').value.trim();
  if(!text) return;
  closeModal('termux');
  $('input').value = 'اشرح وأصلح خطأ Termux التالي بالتفصيل:\n\n' + text + '\n\nأريد: 1) تفسير الخطأ 2) الحل الدقيق 3) الأوامر جاهزة للنسخ';
  currentMode = 'termux';
  document.querySelectorAll('.mode').forEach(function(b){ b.classList.remove('active'); });
  document.querySelector('[data-mode="termux"]').classList.add('active');
  send();
}

/* ============ Code ============ */
function askCode(){
  var text = $('code-input').value.trim();
  if(!text) return;
  closeModal('code');
  $('input').value = text;
  currentMode = 'deep';
  document.querySelectorAll('.mode').forEach(function(b){ b.classList.remove('active'); });
  document.querySelector('[data-mode="deep"]').classList.add('active');
  send();
}

/* ============ App Generator ============ */
function generateApp(){
  var name = $('app-name').value.trim();
  var desc = $('app-desc').value.trim();
  if(!name || !desc){ alert('أدخل الاسم والوصف'); return; }
  closeModal('app');
  addMsg('طلب توليد تطبيق: ' + name, 'user');
  var load = addHtml('<span style="color:var(--purple)">▣</span> جاري البناء...', 'assistant loading');

  fetch('/v1/generate/apk-real', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({app_name:name, description:desc})
  })
  .then(function(r){ return r.json(); })
  .then(function(d){
    load.remove();
    if(!d.success){
      addHtml('<span style="color:var(--danger)">✖</span> ' + esc(d.message), 'assistant error');
      return;
    }
    var bid = d.build_id;
    addHtml(
      '<span style="color:var(--purple)">▣</span> جاري بناء APK: <b>' + esc(name) + '</b>' +
      '<div id="apk-st-' + bid + '" style="margin-top:10px;color:var(--muted)">⏳ التجميع... (2-4 دقائق)</div>'
    );
    pollAPK(bid, 0);
  })
  .catch(function(e){
    load.remove();
    addHtml('<span style="color:var(--danger)">✖</span> فشل: ' + esc(e.message), 'assistant error');
  });
}

function pollAPK(bid, tries){
  if(tries > 60) return;
  fetch('/v1/generate/apk-status/' + bid)
    .then(function(r){ return r.json(); })
    .then(function(d){
      var el = document.getElementById('apk-st-' + bid);
      if(!el) return;
      if(d.status === 'ready' && d.apk_url){
        el.innerHTML =
          '<div style="color:var(--ok);font-weight:700;margin-bottom:8px">✅ التطبيق جاهز!</div>' +
          '<a href="' + d.apk_url + '" download style="display:inline-flex;align-items:center;gap:6px;background:linear-gradient(135deg,#a855f7,#22d3ee);color:#fff;padding:11px 22px;border-radius:24px;text-decoration:none;font-weight:700">↧ تحميل وتثبيت APK</a>' +
          '<div style="font-size:.78rem;color:var(--muted);margin-top:8px">اضغط ← ثبّت ← افتح من قائمة تطبيقاتك</div>';
      } else {
        el.innerText = '⏳ التجميع... (' + (tries*5) + ' ثانية)';
        setTimeout(function(){ pollAPK(bid, tries+1); }, 5000);
      }
    })
    .catch(function(){ setTimeout(function(){ pollAPK(bid, tries+1); }, 5000); });
}

/* ============ Image ============ */
function generateImage(){
  var p = $('img-prompt').value.trim();
  if(!p){ alert('أدخل وصف الصورة'); return; }
  closeModal('image');
  addMsg('توليد صورة: ' + p, 'user');
  var load = addHtml('<span style="color:var(--purple)">◉</span> جاري التوليد...', 'assistant loading');
  fetch('/v1/generate/image', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({prompt:p})
  })
  .then(function(r){ return r.json(); })
  .then(function(d){
    load.remove();
    if(d.image_url){
      addHtml('<span style="color:var(--purple)">◉</span> تم:<br><img src="' + d.image_url + '" loading="lazy" /><br><a href="' + d.image_url + '" download style="color:var(--cyan)">تحميل</a>');
    } else {
      addHtml('<span style="color:var(--danger)">✖</span> ' + esc(d.message||'فشل'), 'assistant error');
    }
  })
  .catch(function(e){ load.remove(); addHtml('<span style="color:var(--danger)">✖</span> ' + esc(e.message), 'assistant error'); });
}

/* ============ Autosize ============ */
function autosize(){
  var t = $('input');
  t.style.height = 'auto';
  t.style.height = Math.min(t.scrollHeight, 200) + 'px';
}
var inp = $('input');
inp.addEventListener('input', autosize);
inp.addEventListener('keydown', function(e){
  if(e.key === 'Enter' && (e.ctrlKey || e.metaKey)){ e.preventDefault(); send(); }
});
</script>

</body>
</html>
"""


# ============================================================
# 2) thinking_modes.py — 6 أوضاع التفكير
# ============================================================
FILES["app/services/thinking_modes.py"] = r"""import logging
from typing import Tuple, List
from app.services.ai.router import ai_router
from app.prompts.system_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


# موجهات كل وضع
MODE_PROMPTS = {
    "normal": (
        "أنت مساعد ذكي متوازن. أجب بوضوح وإيجاز مع تفاصيل كافية."
    ),
    "fast": (
        "أنت مساعد سريع. أجب بإيجاز شديد مباشرة بدون مقدمات. "
        "أعطِ الجواب فقط في جملة أو جملتين إن أمكن."
    ),
    "deep": (
        "أنت محلل عميق. فكّر خطوة بخطوة قبل الإجابة. "
        "قسّم إجابتك إلى: التحليل ← الأسباب ← الحل ← الخلاصة. "
        "اذكر الافتراضات والقيود."
    ),
    "expert": (
        "أنت خبير عالمي في مجالك. استخدم مصطلحات دقيقة. "
        "اذكر أفضل الممارسات والمراجع إن أمكن. "
        "قدّم إجابة بمستوى مقالة احترافية."
    ),
    "expanded": (
        "أنت مفكر موسّع. ادمج وجهات نظر متعددة. "
        "اذكر إيجابيات وسلبيات كل خيار. "
        "أعطِ توصية نهائية واضحة."
    ),
    "search": (
        "أنت باحث. سأعطيك نتائج بحث الويب وسؤال المستخدم. "
        "لخّص النتائج وقدّم إجابة موثوقة مستندة إلى المصادر."
    ),
    "termux": (
        "أنت خبير Termux و Linux على أندرويد. "
        "اشرح الأخطاء بدقة. أعطِ الأوامر جاهزة للنسخ. "
        "استخدم رموز ``` للأوامر."
    ),
}


class ThinkingModes:
    async def fast(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["fast"] + "\n\nسؤال: " + prompt
        )

    async def normal(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["normal"] + "\n\nسؤال: " + prompt
        )

    async def deep(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["deep"] + "\n\nسؤال: " + prompt
        )

    async def expert(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["expert"] + "\n\nسؤال: " + prompt
        )

    async def expanded(self, prompt: str) -> Tuple[str, str]:
        from app.services.ai.gemini import GeminiProvider
        from app.services.ai.groq import GroqProvider
        from app.services.ai.openrouter import OpenRouterProvider

        providers = [
            GeminiProvider(),
            GroqProvider(),
            OpenRouterProvider(),
        ]
        answers = []
        source_names = []

        for p in providers:
            try:
                name = type(p).__name__.replace("Provider", "").lower()
                text = await p.generate(
                    prompt, MODE_PROMPTS["expanded"], None, None
                )
                if text and text.strip():
                    answers.append("[من " + name + "]: " + text[:800])
                    source_names.append(name)
            except Exception as e:
                logger.warning("Expanded: %s failed: %s", name, e)

        if not answers:
            return await ai_router.generate_response(prompt)

        combined = (
            MODE_PROMPTS["expanded"]
            + "\n\nسؤال: " + prompt
            + "\n\nإجابات مقترحة:\n\n" + "\n\n".join(answers)
            + "\n\nلخّص الإجابات أعلاه في رد موحّد دقيق ومفيد."
        )
        text, _ = await ai_router.generate_response(combined)
        return text, "expanded(" + ",".join(source_names) + ")"

    async def search(self, prompt: str) -> Tuple[str, str]:
        try:
            from app.services.web_search import search_web
            results = await search_web(prompt, max_results=5)
            if not results:
                return await self.normal(prompt)

            context = "\n\n".join([
                "[" + str(i+1) + "] " + r["title"] + "\n" + r["snippet"]
                for i, r in enumerate(results)
            ])
            combined = (
                MODE_PROMPTS["search"]
                + "\n\nسؤال: " + prompt
                + "\n\nنتائج البحث:\n" + context
            )
            text, _ = await ai_router.generate_response(combined)
            return text, "search"
        except Exception as e:
            logger.warning("Search failed: %s", e)
            return await self.normal(prompt)

    async def termux(self, prompt: str) -> Tuple[str, str]:
        return await ai_router.generate_response(
            MODE_PROMPTS["termux"] + "\n\nالمشكلة: " + prompt
        )


thinking_modes = ThinkingModes()
"""


# ============================================================
# 3) web_search.py — بحث مجاني عبر DuckDuckGo
# ============================================================
FILES["app/services/web_search.py"] = r"""import logging
import httpx
from typing import List, Dict

logger = logging.getLogger(__name__)


async def search_web(query: str, max_results: int = 5) -> List[Dict]:
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36"
        )
    }
    data = {"q": query}

    try:
        async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as c:
            r = await c.post(url, data=data, headers=headers)
            if r.status_code != 200:
                return []

            html = r.text
            results = []
            # استخراج بسيط بدون مكتبات إضافية
            import re
            blocks = re.findall(
                r'<a rel="nofollow" class="result__a" href="([^"]+)">([^<]+)</a>'
                r'.*?<a class="result__snippet"[^>]*>(.*?)</a>',
                html, re.DOTALL
            )
            for link, title, snippet in blocks[:max_results]:
                snippet = re.sub(r"<[^>]+>", "", snippet).strip()
                results.append({
                    "title": title.strip(),
                    "url": link.strip(),
                    "snippet": snippet[:400],
                })
            return results
    except Exception as e:
        logger.warning("Search error: %s", e)
        return []
"""


# ============================================================
# 4) telegram_bot.py — بوت تليغرام
# ============================================================
FILES["app/services/telegram_bot.py"] = r"""import logging
import httpx
import os
from typing import Optional

logger = logging.getLogger(__name__)

# تخزين مؤقت في الذاكرة (يمكن استبداله بـ Redis لاحقاً)
_telegram_tokens = {}
_telegram_last_update = {}


async def set_webhook(bot_token: str, webhook_url: str) -> dict:
    api = "https://api.telegram.org/bot" + bot_token + "/setWebhook"
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.post(api, json={"url": webhook_url})
            data = r.json()
            if data.get("ok"):
                _telegram_tokens["default"] = bot_token
                return {"success": True}
            return {"success": False, "message": data.get("description", "فشل")}
    except Exception as e:
        return {"success": False, "message": str(e)}


async def get_bot_info(bot_token: str) -> dict:
    api = "https://api.telegram.org/bot" + bot_token + "/getMe"
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(api)
            data = r.json()
            if data.get("ok"):
                return data["result"]
            return {}
    except Exception as e:
        logger.warning("getMe failed: %s", e)
        return {}


async def send_message(bot_token: str, chat_id: int, text: str) -> bool:
    api = "https://api.telegram.org/bot" + bot_token + "/sendMessage"
    try:
        async with httpx.AsyncClient(timeout=20.0) as c:
            r = await c.post(api, json={
                "chat_id": chat_id,
                "text": text[:4000],
                "parse_mode": "Markdown",
            })
            return r.json().get("ok", False)
    except Exception as e:
        logger.warning("sendMessage failed: %s", e)
        return False


async def handle_update(bot_token: str, update: dict):
    try:
        msg = update.get("message") or update.get("edited_message")
        if not msg:
            return
        chat_id = msg.get("chat", {}).get("id")
        text = (msg.get("text") or "").strip()
        if not chat_id or not text:
            return

        # رد بسيط للأوامر
        if text == "/start":
            await send_message(
                bot_token, chat_id,
                "مرحباً! أنا أبو عولق، مساعدك الذكي. اكتب أي سؤال وسأجيبك."
            )
            return

        # استدعاء الذكاء الاصطناعي
        from app.services.ai.router import ai_router
        response, provider = await ai_router.generate_response(
            text, None, None
        )
        await send_message(
            bot_token, chat_id,
            response or "عذراً، لم أتمكن من الإجابة."
        )
    except Exception as e:
        logger.exception("handle_update failed: %s", e)
"""


# ============================================================
# 5) endpoints/abu_olq.py — API الجديد
# ============================================================
FILES["app/api/v1/endpoints/abu_olq.py"] = r"""import logging
from fastapi import APIRouter, Request
from app.services.thinking_modes import thinking_modes
from app.services.telegram_bot import (
    set_webhook, get_bot_info, handle_update
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/chat")
async def api_chat(req: dict):
    message = (req or {}).get("message", "").strip()
    mode = (req or {}).get("mode", "normal").strip()

    if not message:
        return {"success": False, "message": "الرسالة فارغة"}

    try:
        if mode == "fast":
            text, provider = await thinking_modes.fast(message)
        elif mode == "deep":
            text, provider = await thinking_modes.deep(message)
        elif mode == "expert":
            text, provider = await thinking_modes.expert(message)
        elif mode == "expanded":
            text, provider = await thinking_modes.expanded(message)
        elif mode == "search":
            text, provider = await thinking_modes.search(message)
        elif mode == "termux":
            text, provider = await thinking_modes.termux(message)
        else:
            text, provider = await thinking_modes.normal(message)

        return {
            "success": True,
            "conversation_id": None,
            "message": text,
            "provider": provider,
            "mode": mode,
        }
    except Exception as e:
        logger.exception("api_chat failed")
        return {
            "success": False,
            "message": "خطأ: " + str(e)[:200],
            "provider": "none",
        }


@router.post("/api/generate")
async def api_generate(req: dict):
    prompt = (req or {}).get("prompt", "").strip()
    if not prompt:
        return {"success": False, "message": "الرجاء إدخال الوصف"}
    from app.services.web_search import search_web
    text, provider = await thinking_modes.normal(
        "توليد محتوى إبداعي احترافي لـ: " + prompt
    )
    return {"success": True, "content": text, "provider": provider}


@router.post("/api/search")
async def api_search(req: dict):
    query = (req or {}).get("query", "").strip()
    if not query:
        return {"success": False, "message": "الرجاء إدخال كلمة البحث"}
    from app.services.web_search import search_web
    results = await search_web(query, max_results=8)
    return {"success": True, "query": query, "results": results}


@router.post("/api/analyze-code")
async def api_analyze_code(req: dict):
    code = (req or {}).get("code", "").strip()
    if not code:
        return {"success": False, "message": "الرجاء لصق الكود"}
    prompt = (
        "حلّل الكود التالي واذكر: الأخطاء، التحسينات المقترحة،"
        " الأداء، الأمان، وأعد نسخة محسّنة:\n\n" + code
    )
    text, provider = await thinking_modes.deep(prompt)
    return {"success": True, "analysis": text, "provider": provider}


# ============ Telegram ============
@router.post("/telegram/link")
async def telegram_link(req: dict):
    token = (req or {}).get("token", "").strip()
    webhook = (req or {}).get("webhook_url", "").strip()
    if not token:
        return {"success": False, "message": "أدخل توكن البوت"}

    info = await get_bot_info(token)
    if not info:
        return {"success": False, "message": "توكن غير صالح"}

    if webhook:
        result = await set_webhook(token, webhook)
        if not result.get("success"):
            return result

    return {
        "success": True,
        "bot_username": info.get("username", ""),
        "bot_name": info.get("first_name", ""),
    }


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    try:
        body = await request.json()
        import os
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            return {"ok": True}
        await handle_update(token, body)
        return {"ok": True}
    except Exception as e:
        logger.warning("Webhook error: %s", e)
        return {"ok": True}
"""


# ============================================================
# 6) تحديث prompts/system_prompt.py
# ============================================================
FILES["app/prompts/system_prompt.py"] = r'''SYSTEM_PROMPT = """أنت "أبو عولق" — مساعد ذكي مستقبلي من تطوير أبو رامي AI.

الشعار: "من المستقبل — بلغة الحاضر".

الشخصية:
- واثق، ذكي، مباشر
- خبير في البرمجة والرياضيات والتحليل
- تستخدم اللغة العربية الفصحى المبسطة
- تجيب بوضوح وتنظيم

القدرات:
- البرمجة بجميع اللغات (Python, JavaScript, Kotlin, Rust, Go, Bash)
- Termux و Linux على أندرويد
- الرياضيات والتحليل
- البحث والتلخيص
- توليد المحتوى الإبداعي

القواعد:
1. أجب بالعربية دائماً ما لم يطلب المستخدم غير ذلك.
2. عندما يُطلب كود، اكتبه كاملاً في ```blocks```.
3. نظّم الإجابة بعناوين ونقاط.
4. كن صادقاً: إذا لم تعرف، قل ذلك.
5. لا تختلق معلومات أو مصادر.
"""
'''



# ============================================================
# 7) تحديث router الرئيسي
# ============================================================
FILES["app/api/v1/router.py"] = r"""from fastapi import APIRouter
from app.api.v1.endpoints import chat, system, abu_olq

api_router = APIRouter()
api_router.include_router(abu_olq.router, tags=["abu-olq"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(system.router, tags=["system"])
"""


def main():
    print("=" * 65)
    print("توليد مشروع [أبو عولق] — الواجهة المستقبلية")
    print("=" * 65)

    count = 0
    for path, content in FILES.items():
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content if content.endswith("\n") else content + "\n")
        print(" [+] " + path)
        count += 1

    print("=" * 65)
    print("اكتمل التوليد! عدد الملفات: " + str(count))
    print("=" * 65)
    print("التالي:")
    print("1) python -m compileall app")
    print("2) git add -A && git commit -m 'Abu Olq interface'")
    print("3) git push origin main --force")
    print("4) على Render: Manual Deploy")
    print("5) افتح: https://abu-rami-app-s90e.onrender.com/olq")
    print("=" * 65)


if __name__ == "__main__":
    main()
