#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import http.server
import threading
import webbrowser
import sys
import os

# ---------------------------------------------------------
# Flask Wrapper (Required for cloud hosts like pella.app)
# ---------------------------------------------------------
try:
    from flask import Flask, Response
    app = Flask(__name__)

    @app.route("/")
    def _index():
        return Response(PAGE, mimetype="text/html")

    @app.route("/health")
    def _health():
        return "ok"
except ImportError:
    app = None

# ---------------------------------------------------------
# The Game (HTML + CSS + JS)
# ---------------------------------------------------------
PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>Talking Photo Pal 🐾</title>
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#28213a; --paper:#fff8ec;
  --display:'Baloo 2','Comic Sans MS','Chalkboard SE','Marker Felt',system-ui,sans-serif;
  --body:'Nunito','Trebuchet MS',Verdana,system-ui,sans-serif;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;height:100%;overflow:hidden}
body{font-family:var(--body);touch-action:manipulation;user-select:none;-webkit-user-select:none}
button{font-family:inherit}

/* ================= STAGE & ROOM ================= */
#stage{position:fixed;inset:0;overflow:hidden;--px:0;--py:0}
#room{position:absolute;inset:0;background:linear-gradient(180deg,#2fae9d 0%,#5cc9b6 55%,#7ad9c4 76%,#7ad9c4 100%)}
#room::before{content:'';position:absolute;inset:0 0 24% 0;opacity:.5;
  background-image:radial-gradient(rgba(255,255,255,.20) 3px,transparent 3.5px);background-size:36px 36px}
.plx{transform:translate(calc(var(--px,0)*var(--d,6)*1px),calc(var(--py,0)*var(--d,6)*.6px))}

#floor{position:absolute;left:0;right:0;bottom:0;height:24%;
  background:repeating-linear-gradient(90deg,#e2a45e 0 88px,#d8994f 88px 92px);
  box-shadow:inset 0 6px 14px rgba(70,40,10,.35)}
#rug{position:absolute;left:50%;bottom:2.5%;width:min(74vmin,470px);height:11vmin;transform:translateX(-50%);
  border-radius:50%;background:radial-gradient(ellipse,#ffd166 0 34%,#ff8b6b 35% 62%,#ef6f61 63% 100%);
  box-shadow:0 6px 14px rgba(60,30,10,.25);opacity:.95}

#window{position:absolute;left:5%;top:11%;width:27vmin;height:31vmin;min-width:150px;min-height:170px;
  border:10px solid #fff8ec;border-radius:16px;overflow:hidden;z-index:2;
  box-shadow:0 0 0 5px rgba(40,33,58,.85),0 14px 24px rgba(0,0,0,.22);
  background:linear-gradient(180deg,#8fd8ff,#e8f9ff 80%)}
#window::before,#window::after{content:'';position:absolute;background:#fff8ec;z-index:4}
#window::before{left:50%;top:0;bottom:0;width:7px;transform:translateX(-50%)}
#window::after{top:50%;left:0;right:0;height:7px;transform:translateY(-50%)}
.sun{position:absolute;left:14%;top:14%;width:32%;aspect-ratio:1;border-radius:50%;
  background:radial-gradient(circle,#fff3a6 30%,#ffd94d 70%);box-shadow:0 0 26px #ffd94d}
.sun i{position:absolute;inset:-42%;border-radius:50%;
  background:repeating-conic-gradient(rgba(255,215,80,.35) 0 9deg,transparent 9deg 26deg);
  animation:spin 38s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.moon{display:none;position:absolute;right:16%;top:14%;width:30%;aspect-ratio:1;border-radius:50%;
  background:radial-gradient(circle at 34% 32%,#fffdf2,#e4e0c9 75%);box-shadow:0 0 22px rgba(255,250,220,.8)}
.moon::after{content:'';position:absolute;left:22%;top:44%;width:18%;aspect-ratio:1;border-radius:50%;background:rgba(160,155,130,.5)}
.star{display:none;position:absolute;width:4px;height:4px;border-radius:50%;background:#fffbe6;animation:tw 2.2s infinite}
@keyframes tw{50%{opacity:.2}}
.cloud{position:absolute;background:#fff;border-radius:99px;opacity:.92;width:46%;height:15%;animation:drift 26s linear infinite}
.cloud::after{content:'';position:absolute;left:24%;top:-52%;width:46%;height:100%;background:#fff;border-radius:50%}
.c1{top:26%}.c2{top:58%;animation-duration:38s;animation-delay:-14s;transform:scale(.7)}
@keyframes drift{from{left:-55%}to{left:110%}}
.night #window{background:linear-gradient(180deg,#17224d,#3b3f70)}
.night .sun{display:none}.night .moon{display:block}.night .star{display:block}

#frame{position:absolute;right:7%;top:13%;width:15vmin;height:17vmin;min-width:92px;min-height:104px;z-index:2;
  background:linear-gradient(160deg,#ffe3ec,#cdefff);border:9px solid #fff8ec;border-radius:10px;
  box-shadow:0 0 0 4px rgba(40,33,58,.85),0 12px 20px rgba(0,0,0,.2);
  display:flex;align-items:center;justify-content:center;font-size:clamp(26px,6vmin,44px);
  animation:sway 7s ease-in-out infinite;transform-origin:top center}
@keyframes sway{0%,100%{rotate:-2deg}50%{rotate:2.4deg}}
.glow{position:absolute;right:-10%;top:-16%;width:52vmin;height:52vmin;pointer-events:none;
  background:radial-gradient(circle,rgba(255,214,140,.55),transparent 65%);opacity:.55}
.night .glow{opacity:.95}
.night #room{filter:brightness(.9)}
.mote{position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;opacity:0;top:72%;pointer-events:none;animation:rise linear infinite}
@keyframes rise{0%{opacity:0;transform:translateY(0)}15%{opacity:.5}85%{opacity:.35}100%{opacity:0;transform:translateY(-46vh)}}

/* ================= CHARACTER ================= */
#charWrap{position:absolute;left:50%;bottom:6.5%;width:min(56vmin,360px);transform:translateX(-50%);z-index:20}
#charWrap.enter{animation:popin .8s cubic-bezier(.3,1.7,.45,1)}
@keyframes popin{from{transform:translateX(-50%) translateY(6vh) scale(0)}}
#charWrap.jumping{animation:jump .72s cubic-bezier(.35,.7,.35,1)}
@keyframes jump{
  0%{transform:translateX(-50%) translateY(0) rotate(0)}
  42%{transform:translateX(-50%) translateY(-17vmin) rotate(190deg)}
  78%{transform:translateX(-50%) translateY(0) rotate(360deg)}
  100%{transform:translateX(-50%) translateY(0) rotate(360deg)}}
#charShadow{position:absolute;left:50%;bottom:-5%;width:88%;height:10%;transform:translateX(-50%);z-index:-1;
  background:radial-gradient(ellipse,rgba(35,20,45,.36),transparent 70%);border-radius:50%}
#char{width:100%;aspect-ratio:1/1.06;cursor:pointer;will-change:transform;transform-origin:50% 100%}
#char.wiggle{animation:wig .17s ease-in-out infinite}
@keyframes wig{0%,100%{rotate:-3deg}50%{rotate:3deg}}
#char.shake{animation:shk .5s ease}
@keyframes shk{20%{translate:-9px 0}40%{translate:8px 0}60%{translate:-6px 0}80%{translate:5px 0}}
#face{position:relative;width:100%;height:100%;overflow:hidden;background:#cfd8e4;
  border-radius:46% 54% 52% 48%/54% 46% 52% 48%;
  animation:blob 11s ease-in-out infinite alternate;
  box-shadow:0 0 0 6px var(--paper),0 22px 38px rgba(20,15,35,.32)}
@keyframes blob{
  0%{border-radius:46% 54% 52% 48%/54% 46% 52% 48%}
  50%{border-radius:53% 47% 44% 56%/48% 57% 45% 55%}
  100%{border-radius:44% 56% 55% 45%/57% 44% 55% 47%}}
#char.listen #face{box-shadow:0 0 0 6px var(--paper),0 22px 38px rgba(20,15,35,.32),0 0 0 13px rgba(255,90,90,.35)}
#face img{width:100%;height:100%;object-fit:cover;display:none}
#catFace{position:absolute;inset:0}
#catFace svg{width:100%;height:100%;display:block}
.catEyes{transform-box:fill-box;transform-origin:center;animation:blink 4.4s infinite}
@keyframes blink{0%,91%,100%{transform:scaleY(1)}94.5%{transform:scaleY(.08)}}
#mouth{position:absolute;left:50%;top:59%;width:36%;height:30%;transform-origin:50% 0;overflow:hidden;
  transform:translateX(-50%) scale(1,.07);
  background:radial-gradient(120% 130% at 50% 0%,#7c2f3e 0%,#3c1220 72%);
  border-radius:14% 14% 50% 50%/12% 12% 88% 88%;box-shadow:inset 0 5px 9px rgba(0,0,0,.45)}
#mouth .tongue{position:absolute;bottom:-12%;left:18%;width:64%;height:58%;
  background:radial-gradient(120% 100% at 50% 0,#ff8fa3,#e4647c);border-radius:50% 50% 0 0/70% 70% 0 0}
.blush{position:absolute;top:47%;width:16%;height:9%;background:#ff97a8;border-radius:50%;filter:blur(3px);opacity:0;transition:opacity .4s}
.blush.l{left:9%}.blush.r{right:9%}
#face.blushing .blush{opacity:.75}

/* speech bubble */
#bubble{position:absolute;left:50%;bottom:105%;max-width:min(66vw,264px);width:max-content;z-index:30;pointer-events:none;
  background:#fff;border:3px solid var(--ink);border-radius:18px;padding:10px 14px;text-align:center;
  font-family:var(--display);font-weight:700;font-size:clamp(14px,3.6vw,18px);color:var(--ink);
  box-shadow:0 6px 0 rgba(40,33,58,.18);transform:translateX(-50%) scale(0);transform-origin:50% 135%;
  transition:transform .32s cubic-bezier(.3,1.9,.5,1)}
#bubble.show{transform:translateX(-50%) scale(1)}
#bubble::after{content:'';position:absolute;left:50%;bottom:-11px;width:15px;height:15px;background:#fff;
  border:3px solid var(--ink);border-top:none;border-left:none;transform:translateX(-50%) rotate(45deg)}

/* ================= HUD ================= */
header{position:absolute;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;gap:10px;padding:12px 14px;flex-wrap:wrap}
.chip{display:flex;align-items:center;gap:8px;background:var(--paper);border:3px solid var(--ink);border-radius:999px;
  padding:5px 7px 5px 16px;box-shadow:0 4px 0 rgba(40,33,58,.28);
  font-family:var(--display);font-weight:800;font-size:clamp(15px,4vw,20px);color:var(--ink)}
#nameTxt{outline:none;min-width:36px;max-width:150px;white-space:nowrap;overflow:hidden;border-radius:8px}
#nameTxt:focus{background:#fff3c9}
.smallBtn{width:40px;height:40px;border-radius:50%;border:3px solid var(--ink);background:var(--paper);
  font-size:17px;cursor:pointer;box-shadow:0 3px 0 rgba(40,33,58,.32);transition:transform .1s,box-shadow .1s}
.smallBtn:active{transform:translateY(2px);box-shadow:none}
.smallBtn.on{background:#ffd166}
#meters{margin-left:auto;display:flex;gap:10px}
.meter{display:flex;align-items:center;gap:6px;background:rgba(255,248,236,.94);border:3px solid var(--ink);
  border-radius:999px;padding:5px 10px;font-size:15px}
.meter i{display:block;width:clamp(56px,13vw,108px);height:12px;border-radius:99px;background:#e8dcc8;overflow:hidden}
.meter b{display:block;height:100%;border-radius:99px;transition:width .5s}
#hungerFill{background:linear-gradient(90deg,#ff9f68,#ff6b5e)}
#funFill{background:linear-gradient(90deg,#7be0a1,#3ec46d)}
.meter.low i{animation:blinkW 1s infinite}
@keyframes blinkW{50%{opacity:.4}}

#hint{position:absolute;top:70px;left:50%;transform:translateX(-50%);z-index:49;pointer-events:none;text-align:center;
  background:rgba(40,33,58,.72);color:#fff8ec;font-size:12px;font-weight:700;padding:6px 14px;border-radius:99px;opacity:.9}

/* ================= DOCK ================= */
#dock{position:absolute;left:50%;bottom:max(14px,env(safe-area-inset-bottom));transform:translateX(-50%);
  display:flex;gap:clamp(8px,2vw,18px);z-index:50}
.act{position:relative;display:flex;flex-direction:column;align-items:center;gap:1px;cursor:pointer;
  width:clamp(66px,17.5vw,92px);padding:9px 4px 7px;border-radius:24px;color:#3a2b20;
  background:var(--c);border:4px solid rgba(30,25,50,.28);
  box-shadow:0 7px 0 var(--cd),0 14px 20px rgba(0,0,0,.26);
  font-family:var(--display);transition:transform .08s,box-shadow .08s}
.act em{font-style:normal;font-size:clamp(24px,6vw,34px);filter:drop-shadow(0 2px 0 rgba(0,0,0,.15))}
.act span{font-weight:800;font-size:clamp(11px,2.6vw,14px);letter-spacing:.4px}
.act:active{transform:translateY(6px);box-shadow:0 1px 0 var(--cd),0 4px 8px rgba(0,0,0,.2)}
#feedBtn{--c:#ff6b5e;--cd:#c94a3f}
#milkBtn{--c:#5ec8f2;--cd:#3a9ec7}
#talkBtn{--c:#ffcc4d;--cd:#d3a02c}
#fartBtn{--c:#b48cf2;--cd:#8a63cf}
.act.rec{--c:#ff4757;--cd:#a02330;border-color:#8c1e2b}
.act.rec::after{content:'';position:absolute;inset:-9px;border-radius:30px;border:4px solid rgba(255,71,87,.65);animation:pulse 1s infinite}
@keyframes pulse{0%{transform:scale(.92);opacity:1}100%{transform:scale(1.18);opacity:0}}

#recChip{position:absolute;left:50%;bottom:140px;transform:translateX(-50%) scale(0);z-index:55;
  background:#ff4757;color:#fff;font-family:var(--display);font-weight:800;font-size:14px;
  border:3px solid var(--ink);border-radius:99px;padding:6px 16px;transition:transform .25s cubic-bezier(.3,1.7,.5,1)}
#recChip.show{transform:translateX(-50%) scale(1)}

#sayPanel{position:absolute;left:50%;bottom:140px;transform:translateX(-50%) scale(0);transform-origin:bottom center;
  display:flex;gap:8px;z-index:55;transition:transform .28s cubic-bezier(.3,1.7,.5,1)}
#sayPanel.open{transform:translateX(-50%) scale(1)}
#sayInput{width:min(56vw,300px);border:3px solid var(--ink);border-radius:99px;padding:10px 16px;
  font-family:var(--body);font-weight:700;font-size:15px;background:#fff;color:var(--ink);outline:none}
#sayGo{border:3px solid var(--ink);border-radius:99px;background:#ffd166;font-family:var(--display);
  font-weight:800;padding:0 18px;cursor:pointer;font-size:15px}

/* fx layers */
#fx{position:absolute;inset:0;pointer-events:none;z-index:44}
.pt{position:absolute;pointer-events:none;will-change:transform,opacity;font-size:calc(21px*var(--s,1));animation:floatUp .95s ease-out forwards}
@keyframes floatUp{0%{opacity:1;transform:translate(0,0) rotate(0)}100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(var(--r)) scale(.45)}}
.flyer{position:fixed;z-index:45;pointer-events:none;font-size:clamp(34px,9vw,52px);margin:-24px 0 0 -22px;
  transform:translate(0,0) rotate(0);transition:transform .6s cubic-bezier(.5,-.18,.55,1.12);
  filter:drop-shadow(0 4px 4px rgba(0,0,0,.25))}

/* overlays */
#dropOverlay{position:absolute;inset:0;z-index:90;display:none;align-items:center;justify-content:center;
  background:rgba(40,33,58,.55);border:8px dashed #ffd166;font-family:var(--display);font-weight:800;
  color:#fff;font-size:clamp(22px,6vw,40px)}
#dropOverlay.show{display:flex}
#welcome{position:absolute;inset:0;z-index:100;display:none;align-items:center;justify-content:center;background:rgba(30,26,48,.6);padding:18px}
#welcome.show{display:flex}
#welcome .card{background:var(--paper);border:4px solid var(--ink);border-radius:26px;padding:28px 26px;max-width:430px;
  text-align:center;box-shadow:0 14px 0 rgba(40,33,58,.3);animation:popin .6s cubic-bezier(.3,1.7,.5,1)}
#welcome h1{font-family:var(--display);font-size:clamp(24px,6vw,34px);margin:0 0 8px;color:var(--ink)}
#welcome p{font-weight:700;color:#5c5470;margin:0 0 20px;font-size:15px}
#welcome button{display:block;width:100%;margin:10px 0;padding:13px;border-radius:16px;cursor:pointer;
  border:3px solid var(--ink);font-family:var(--display);font-weight:800;font-size:17px;box-shadow:0 5px 0 rgba(40,33,58,.35)}
#welcome button:active{transform:translateY(3px);box-shadow:none}
#wUpload{background:#ffd166;color:var(--ink)}
#wDefault{background:#fff;color:var(--ink)}
</style>
</head>
<body>
<div id="stage">
  <div id="room">
    <div class="glow plx" style="--d:3"></div>
    <div id="window" class="plx" style="--d:10">
      <div class="sun"><i></i></div>
      <div class="moon"></div>
      <span class="star" style="left:18%;top:22%"></span><span class="star" style="left:64%;top:14%;animation-delay:.7s"></span>
      <span class="star" style="left:40%;top:38%;animation-delay:1.3s"></span><span class="star" style="left:80%;top:46%;animation-delay:.4s"></span>
      <div class="cloud c1"></div><div class="cloud c2"></div>
    </div>
    <div id="frame" class="plx" style="--d:6">🐾</div>
    <div id="floor"></div>
    <div id="rug"></div>
  </div>

  <div id="charWrap">
    <div id="bubble"></div>
    <div id="charShadow"></div>
    <div id="char">
      <div id="face">
        <div id="catFace">
          <svg viewBox="0 0 200 200" aria-hidden="true">
            <defs><linearGradient id="fur" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#aec0d4"/><stop offset="1" stop-color="#8fa2ba"/></linearGradient></defs>
            <path d="M42 74 L18 12 L86 44 Z" fill="#8fa2ba"/>
            <path d="M46 62 L32 26 L72 46 Z" fill="#ffb3c1"/>
            <path d="M158 74 L182 12 L114 44 Z" fill="#8fa2ba"/>
            <path d="M154 62 L168 26 L128 46 Z" fill="#ffb3c1"/>
            <circle cx="100" cy="114" r="76" fill="url(#fur)"/>
            <path d="M76 46 q24 -13 48 0" stroke="#7d92ab" stroke-width="9" fill="none" stroke-linecap="round"/>
            <path d="M84 62 q16 -9 32 0" stroke="#7d92ab" stroke-width="8" fill="none" stroke-linecap="round"/>
            <ellipse cx="100" cy="134" rx="42" ry="30" fill="#eef3f9"/>
            <g class="catEyes">
              <ellipse cx="71" cy="96" rx="14" ry="16" fill="#fff"/>
              <ellipse cx="129" cy="96" rx="14" ry="16" fill="#fff"/>
              <circle cx="73" cy="98" r="7.5" fill="#2b2b3a"/><circle cx="127" cy="98" r="7.5" fill="#2b2b3a"/>
              <circle cx="76" cy="95" r="2.6" fill="#fff"/><circle cx="130" cy="95" r="2.6" fill="#fff"/>
            </g>
            <path d="M91 112 h18 l-9 11 z" fill="#ff8fa3"/>
            <path d="M36 122 L10 116 M36 132 L8 132 M36 142 L12 150" stroke="#7d92ab" stroke-width="3.4" stroke-linecap="round"/>
            <path d="M164 122 L190 116 M164 132 L192 132 M164 142 L188 150" stroke="#7d92ab" stroke-width="3.4" stroke-linecap="round"/>
          </svg>
        </div>
        <img id="photo" alt="character">
        <div class="blush l"></div><div class="blush r"></div>
        <div id="mouth"><div class="tongue"></div></div>
      </div>
    </div>
  </div>

  <div id="fx"></div>

  <header>
    <div class="chip">
      <span id="nameTxt" contenteditable="true" spellcheck="false">Mochi</span>
      <button class="smallBtn" id="camBtn" title="Upload a photo">📷</button>
    </div>
    <div id="meters">
      <div class="meter" id="mHunger"><span>🍗</span><i><b id="hungerFill"></b></i></div>
      <div class="meter" id="mFun"><span>🎈</span><i><b id="funFill"></b></i></div>
    </div>
    <button class="smallBtn" id="sayToggle" title="Type something to say">💬</button>
    <button class="smallBtn" id="musicBtn" title="Music">🎵</button>
    <button class="smallBtn" id="muteBtn" title="Sound">🔊</button>
  </header>

  <div id="hint">tap the pal · double-tap = jump · F feed · M milk · T talk · P toot · Space = boop</div>
  <div id="recChip">● REC 0s</div>
  <div id="sayPanel">
    <input id="sayInput" maxlength="90" placeholder="Type something for me to say…">
    <button id="sayGo">SAY IT</button>
  </div>

  <nav id="dock">
    <button class="act" id="feedBtn"><em>🍔</em><span>Feed</span></button>
    <button class="act" id="milkBtn"><em>🥛</em><span>Milk</span></button>
    <button class="act" id="talkBtn"><em>🎤</em><span>Talk</span></button>
    <button class="act" id="fartBtn"><em>💨</em><span>Toot</span></button>
  </nav>

  <div id="dropOverlay"><div>📸 Drop the photo!</div></div>
  <div id="welcome">
    <div class="card">
      <h1>🐾 Talking Photo Pal</h1>
      <p>Pick your star — <b>any photo</b> becomes a living, talking goofball that repeats everything you say.</p>
      <button id="wUpload">📷 Upload a photo</button>
      <button id="wDefault">🐱 Play with Mochi the cat</button>
    </div>
  </div>
</div>
<input type="file" id="fileInput" accept="image/*" hidden>

<script>
'use strict';
const $=s=>document.querySelector(s);
const rand=(a,b)=>a+Math.random()*(b-a);
const pick=a=>a[(Math.random()*a.length)|0];
const clamp=(v,a,b)=>v<a?a:v>b?b:v;

const stage=$('#stage'),room=$('#room'),charEl=$('#char'),charWrap=$('#charWrap'),
face=$('#face'),mouth=$('#mouth'),photoImg=$('#photo'),catFace=$('#catFace'),
bubble=$('#bubble'),shadowEl=$('#charShadow'),fxLayer=$('#fx'),
hungerFill=$('#hungerFill'),funFill=$('#funFill'),mHunger=$('#mHunger'),mFun=$('#mFun'),
nameTxt=$('#nameTxt'),fileInput=$('#fileInput'),
feedBtn=$('#feedBtn'),milkBtn=$('#milkBtn'),talkBtn=$('#talkBtn'),fartBtn=$('#fartBtn'),
camBtn=$('#camBtn'),muteBtn=$('#muteBtn'),musicBtn=$('#musicBtn'),sayToggle=$('#sayToggle'),
sayPanel=$('#sayPanel'),sayInput=$('#sayInput'),sayGo=$('#sayGo'),
recChip=$('#recChip'),welcome=$('#welcome'),dropOverlay=$('#dropOverlay');

const S={name:'Mochi',hunger:82,fun:80,photo:null,busy:false,chewing:false};
try{const d=JSON.parse(localStorage.getItem('ttpal')||'null');
  if(d){S.name=d.n||'Mochi';S.hunger=d.h??82;S.fun=d.f??80;S.photo=d.p||null;}}catch(e){}

let AC=null,master=null,NOISE=null,muted=false;
function ac(){
  if(!AC){AC=new (window.AudioContext||window.webkitAudioContext)();
    master=AC.createGain();master.gain.value=.9;master.connect(AC.destination);}
  if(AC.state==='suspended')AC.resume();return AC;}
function getNoise(c){if(!NOISE){NOISE=c.createBuffer(1,c.sampleRate,c.sampleRate);
  const ch=NOISE.getChannelData(0);for(let i=0;i<ch.length;i++)ch[i]=Math.random()*2-1;}return NOISE;}
function env(g,t,a,peak,d){g.gain.setValueAtTime(0.0001,t);
  g.gain.linearRampToValueAtTime(peak,t+a);g.gain.exponentialRampToValueAtTime(0.0001,t+d);}
function tone(o){const c=ac(),t=c.currentTime+(o.when||0),os=c.createOscillator(),g=c.createGain();
  os.type=o.type||'sine';os.frequency.setValueAtTime(o.f,t);
  if(o.f2)os.frequency.exponentialRampToValueAtTime(Math.max(o.f2,1),t+o.dur);
  env(g,t,o.attack||.01,o.vol||.2,o.dur);os.connect(g);g.connect(master);
  os.start(t);os.stop(t+o.dur+.05);}
function noise(o){const c=ac(),t=c.currentTime+(o.when||0),s=c.createBufferSource();
  s.buffer=getNoise(c);s.loop=true;const fl=c.createBiquadFilter();fl.type=o.type||'bandpass';
  fl.frequency.setValueAtTime(o.f||1000,t);if(o.slide)fl.frequency.exponentialRampToValueAtTime(o.slide,t+o.dur);
  fl.Q.value=o.q||1;const g=c.createGain();env(g,t,.005,o.vol||.2,o.dur);
  s.connect(fl);fl.connect(g);g.connect(master);s.start(t);s.stop(t+o.dur+.05);}
const SFX={
  pop(){tone({f:620,f2:190,type:'square',dur:.12,vol:.16});},
  giggle(){[0,.09,.18,.29].forEach((w,i)=>tone({f:rand(700,900)+i*60,f2:rand(300,430),dur:.09,vol:.15,when:w}));},
  crunch(){noise({dur:.08,vol:.3,f:2400,q:2});noise({dur:.06,vol:.2,f:1500,q:2,when:.02});},
  gulp(){tone({f:340,f2:70,dur:.28,vol:.24});},
  whoosh(){noise({dur:.35,vol:.16,f:300,slide:2600,q:.8});},
  thud(){tone({f:150,f2:55,dur:.14,vol:.3});},
  eek(){tone({f:880,f2:1400,type:'square',dur:.12,vol:.1});},
  buzz(){tone({f:160,f2:118,type:'sawtooth',dur:.3,vol:.14});},
  ding(){tone({f:1046,type:'triangle',dur:.5,vol:.14});tone({f:1568,type:'triangle',dur:.6,vol:.09,when:.08});},
  mew(){tone({f:520,f2:880,type:'triangle',dur:.18,vol:.18});tone({f:880,f2:430,type:'triangle',dur:.22,vol:.18,when:.16});},
  sad(){tone({f:330,f2:180,type:'triangle',dur:.4,vol:.16});},
  fart(){const c=ac(),t=c.currentTime,o=c.createOscillator(),g=c.createGain(),fl=c.createBiquadFilter();
    o.type='sawtooth';o.frequency.setValueAtTime(115,t);o.frequency.exponentialRampToValueAtTime(48,t+.6);
    fl.type='lowpass';fl.frequency.value=420;
    const lfo=c.createOscillator(),lg=c.createGain();lfo.frequency.value=26;lg.gain.value=.45;
    lfo.connect(lg);lg.connect(g.gain);
    g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.5,t+.05);
    g.gain.setValueAtTime(.5,t+.35);g.gain.exponentialRampToValueAtTime(.0001,t+.62);
    o.connect(fl);fl.connect(g);g.connect(master);
    o.start(t);lfo.start(t);o.stop(t+.65);lfo.stop(t+.65);
    noise({dur:.5,vol:.07,f:300,type:'lowpass'});}
};

const LINES={
  idle:['Pet me! 🐾','Whatcha doing?','Say something to me!','*happy noises* ✨','Boop my nose!','Best day ever!','I love this room 🏠'],
  hungry:['Feed me pleeease 🍗','My tummy is rumbling…','Snack break? 🥺','I could eat a whole pizza 🍕'],
  bored:['Play with me! 🎈','I\'m boooored…','Poke me, I dare you 👉','Entertain me, human'],
  pat:['Hehe, that tickles!','Right on the head, yes!','Purrrr 💕','More head pats please!'],
  belly:['NOT the belly! 😆','Hehehehe!!','I\'m ticklish there!!','Okay okay, truce! 🏳️'],
  feet:['Hey! My toes! 🦶','Watch the feet!','Brrr, cold paws!'],
  annoyed:['Personal space!! 😤','Six pokes?! Seriously?!','I\'m telling my lawyer 🙄','Okaaay, time out!'],
  yum:['Mmm, delicious! 😋','Nom nom nom!','10 out of 10! ⭐','Got any more? 🤤'],
  drink:['Ahh, refreshing! 🥛','Glug glug glug~','Milk? YES please','Do I have a moustache? 🥸'],
  fart:['Excuse me!! 💨','Oops. That was the chair.','…pretend you didn\'t hear that','Better out than in 😌'],
  hello:['Ta-da! I\'m {n}! 🎉','Ooooh, I feel alive! ✨','Nice photo. I look GREAT 😎','{n} has entered the chat!'],
  encore:['Hehe! Say it again! 😂','What a voice! 🎶','I sound GREAT ✨','Classic. 😌']
};

let bubbleT=null;
function say(txt,ms){ms=ms||2600;bubble.textContent=txt;bubble.classList.add('show');
  clearTimeout(bubbleT);bubbleT=setTimeout(()=>bubble.classList.remove('show'),ms);}
function spawnBurst(x,y,emojis,n,spread){n=n||6;spread=spread||90;
  for(let i=0;i<n;i++){const s=document.createElement('span');s.className='pt';
    s.textContent=pick(emojis);s.style.left=x+'px';s.style.top=y+'px';
    s.style.setProperty('--dx',rand(-spread,spread)+'px');
    s.style.setProperty('--dy',rand(-150,-60)+'px');
    s.style.setProperty('--r',rand(-45,45)+'deg');
    s.style.setProperty('--s',rand(.7,1.5).toFixed(2));
    fxLayer.appendChild(s);s.addEventListener('animationend',()=>s.remove());}}
function charCenter(){const r=face.getBoundingClientRect();
  return{x:r.left+r.width/2,y:r.top+r.height*.45};}
function hearts(){const c=charCenter();spawnBurst(c.x,c.y,['💖','💕','✨'],7,120);}
function confetti(){for(let i=0;i<3;i++)setTimeout(()=>{
  spawnBurst(rand(innerWidth*.25,innerWidth*.75),rand(innerHeight*.25,innerHeight*.55),
    ['🎉','✨','⭐','💖','🎈'],10,190);},i*160);}
let blushT=null;
function blush(ms){face.classList.add('blushing');clearTimeout(blushT);
  blushT=setTimeout(()=>face.classList.remove('blushing'),ms||1200);}

const P={sx:1,sy:1,vsx:0,vsy:0,rot:0,vr:0};
let listening=false;
function kickS(ax,ay,ar){P.vsx+=ax||0;P.vsy+=ay||0;P.vr+=ar||0;}
function spr(o,k,vk,target,dt,st,da){o[vk]+=(target-o[k])*st*dt;o[vk]*=Math.exp(-da*dt);o[k]+=o[vk]*dt;}

let mouthGoal=.06,mouthCur=.06;
let talkMode=null,talkAnalyser=null,talkData=null,lastTalkKick=0,lastT=performance.now();
function frame(ts){
  const dt=Math.min(.05,(ts-lastT)/1000)||.016;lastT=ts;
  if(!talkMode&&!S.chewing)mouthGoal+=(0.06-mouthGoal)*Math.min(1,dt*5);
  if(talkMode==='tts')mouthGoal=.18+.55*Math.abs(Math.sin(ts*.02)+.4*Math.sin(ts*.013));
  if(talkMode==='audio'&&talkAnalyser){talkAnalyser.getByteTimeDomainData(talkData);
    let s=0;for(let i=0;i<talkData.length;i+=4){const v=(talkData[i]-128)/128;s+=v*v;}
    mouthGoal=clamp(.08+Math.sqrt(s/(talkData.length/4))*5,.08,1);}
  if(talkMode&&ts-lastTalkKick>150){lastTalkKick=ts;kickS(rand(-.05,.05),rand(-.1,-.03),rand(-2.5,2.5));}
  mouthCur+=(mouthGoal-mouthCur)*Math.min(1,dt*18);
  mouth.style.transform='translateX(-50%) scale('+(1+mouthCur*.15).toFixed(3)+','+mouthCur.toFixed(3)+')';
  const br=Math.sin(ts*.0021);
  const droop=(S.hunger<25||S.fun<18)?1:0;
  spr(P,'sx','vsx',1-br*.012,dt,170,9);
  spr(P,'sy','vsy',1+br*.02-droop*.04,dt,170,9);
  spr(P,'rot','vr',(listening?5:0)+br*.7+droop*2.6,dt,110,8);
  charEl.style.transform='rotate('+P.rot.toFixed(2)+'deg) scale('+P.sx.toFixed(3)+','+P.sy.toFixed(3)+')';
  shadowEl.style.transform='translateX(-50%) scaleX('+(1+br*.02).toFixed(3)+')';
  requestAnimationFrame(frame);
}

function meters(){hungerFill.style.width=S.hunger+'%';funFill.style.width=S.fun+'%';
  mHunger.classList.toggle('low',S.hunger<30);mFun.classList.toggle('low',S.fun<30);}
let saveT=null;
function save(){clearTimeout(saveT);saveT=setTimeout(()=>{try{
  localStorage.setItem('ttpal',JSON.stringify({n:S.name,h:Math.round(S.hunger),f:Math.round(S.fun),p:S.photo}));
}catch(e){}},400);}

function react(zone,px,py){
  if(zone==='head'){SFX.giggle();spawnBurst(px,py,['💖','✨'],4);say(pick(LINES.pat));S.fun=clamp(S.fun+5,0,100);blush(1200);}
  else if(zone==='belly'){SFX.giggle();kickS(rand(-.1,.1),-.35,rand(-5,5));
    spawnBurst(px,py,['😆','✨'],3);say(pick(LINES.belly));S.fun=clamp(S.fun+6,0,100);}
  else{SFX.eek();kickS(0,-.5,rand(-6,6));spawnBurst(px,py,['🦶','💢'],3);say(pick(LINES.feet));}
  meters();save();}
function annoyed(){say(pick(LINES.annoyed));charEl.classList.add('shake');SFX.buzz();
  const c=charCenter();spawnBurst(c.x,c.y-60,['😤','💢'],4,70);
  setTimeout(()=>charEl.classList.remove('shake'),520);}
function jump(){if(S.busy||charWrap.classList.contains('jumping'))return;
  charWrap.classList.add('jumping');SFX.whoosh();
  setTimeout(()=>{kickS(.3,-.2);SFX.thud();
    const r=face.getBoundingClientRect();
    spawnBurst(r.left+r.width/2,r.bottom-10,['💨'],4,80);},520);
  setTimeout(()=>charWrap.classList.remove('jumping'),740);
  S.fun=clamp(S.fun+3,0,100);meters();save();}

let lastTap=0,tapTimes=[];
charEl.addEventListener('pointerdown',e=>{
  e.preventDefault();ac();
  if(S.busy){kickS(.05,-.1);return;}
  const r=face.getBoundingClientRect();
  const rel=clamp((e.clientY-r.top)/r.height,0,1);
  const x=clamp((e.clientX-r.left)/r.width-.5,-.5,.5);
  kickS(-x*.45,-.4,x*7);SFX.pop();
  const now=performance.now();
  if(now-lastTap<300){lastTap=0;jump();return;}
  lastTap=now;
  react(rel<.34?'head':rel<.72?'belly':'feet',e.clientX,e.clientY);
  tapTimes.push(now);tapTimes=tapTimes.filter(t=>now-t<2200);
  if(tapTimes.length>=6){tapTimes=[];annoyed();}
});

function mouthPoint(){const r=face.getBoundingClientRect();
  return{x:r.left+r.width/2,y:r.top+r.height*.66};}
function flyToMouth(emoji,fromBtn,done){
  const fr=fromBtn.getBoundingClientRect(),mp=mouthPoint();
  const el=document.createElement('div');el.className='flyer';el.textContent=emoji;
  el.style.left=(fr.left+fr.width/2)+'px';el.style.top=(fr.top+fr.height/2)+'px';
  fxLayer.appendChild(el);
  const dx=mp.x-(fr.left+fr.width/2),dy=mp.y-(fr.top+fr.height/2);
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    el.style.transform='translate('+dx+'px,'+dy+'px) scale(.55) rotate(-18deg)';}));
  setTimeout(()=>{el.remove();done();},620);}
function chew(n,done){if(n<=0)return done();
  SFX.crunch();mouthGoal=.95;kickS(rand(-.05,.05),-.1);
  setTimeout(()=>{mouthGoal=.15;setTimeout(()=>chew(n-1,done),120);},150);}
function gulp(done){SFX.gulp();mouthGoal=.5;kickS(-.06,-.25,-3);
  setTimeout(()=>{mouthGoal=.06;kickS(.05,.12,2);done();},300);}
function feed(){if(S.busy)return;S.busy=true;
  const food=pick(['🍔','🍕','🌭','🍗','🍩','🍣','🥪']);
  flyToMouth(food,feedBtn,()=>{S.chewing=true;
    chew(3,()=>{S.chewing=false;gulp(()=>{
      S.hunger=clamp(S.hunger+26,0,100);S.fun=clamp(S.fun+4,0,100);meters();
      say(pick(LINES.yum));blush(1500);hearts();S.busy=false;save();});});});}
function milk(){if(S.busy)return;S.busy=true;
  flyToMouth('🍼',milkBtn,()=>{S.chewing=true;let g=0;
    const iv=setInterval(()=>{SFX.gulp();mouthGoal=g%2?.2:.75;kickS(0,-.08);g++;
      if(g>=4){clearInterval(iv);S.chewing=false;mouthGoal=.06;
        S.hunger=clamp(S.hunger+12,0,100);S.fun=clamp(S.fun+10,0,100);meters();
        say(pick(LINES.drink));blush(1400);S.busy=false;save();}},240);});}
function toot(){if(S.busy)return;S.busy=true;
  say('uh oh… 🫣');charEl.classList.add('wiggle');
  setTimeout(()=>{charEl.classList.remove('wiggle');SFX.fart();
    const r=face.getBoundingClientRect();
    spawnBurst(r.left+r.width*.5,r.top+r.height*.92,['💨','☁️','🟢'],8,140);
    setTimeout(()=>say(pick(LINES.fart)),380);
    S.fun=clamp(S.fun+6,0,100);meters();
    setTimeout(()=>{S.busy=false;save();},900);},700);}

let rec=null,recStream=null,recTimer=null,recInt=null,recStart=0;
async function toggleTalk(){
  ac();
  if(rec){stopRec();return;}
  if(typeof MediaRecorder==='undefined'){say('No mic here — type to me! 💬');openSay();return;}
  try{recStream=await navigator.mediaDevices.getUserMedia({audio:true});}
  catch(err){say('Mic blocked 🙉 — type to me instead!');openSay();return;}
  rec=new MediaRecorder(recStream);const chunks=[];
  rec.ondataavailable=e=>{if(e.data&&e.data.size)chunks.push(e.data);};
  rec.onstop=async()=>{recStream.getTracks().forEach(t=>t.stop());
    talkBtn.classList.remove('rec');recChip.classList.remove('show');
    clearInterval(recInt);listening=false;charEl.classList.remove('listen');
    try{const buf=await new Blob(chunks).arrayBuffer();
      const ab=await ac().decodeAudioData(buf);
      if(ab.duration<.25)say('I heard… nothing 🤔');else playChipmunk(ab);
    }catch(e){say('Hmm, could not play that 🙈');}};
  rec.start();recStart=Date.now();listening=true;charEl.classList.add('listen');
  talkBtn.classList.add('rec');recChip.classList.add('show');
  say('I\'m listening… speak! 👂');kickS(0,-.08);
  recInt=setInterval(()=>{recChip.textContent='● REC '+Math.min(10,((Date.now()-recStart)/1000)|0)+'s';},200);
  recTimer=setTimeout(stopRec,10000);}
function stopRec(){clearTimeout(recTimer);if(rec&&rec.state!=='inactive')rec.stop();}
function playChipmunk(buf){const c=ac();
  const src=c.createBufferSource();src.buffer=buf;src.playbackRate.value=1.45;
  const an=c.createAnalyser();an.fftSize=256;talkData=new Uint8Array(an.fftSize);
  const g=c.createGain();g.gain.value=1.6;
  src.connect(an);an.connect(g);g.connect(master);
  talkAnalyser=an;talkMode='audio';
  src.onended=()=>{if(talkMode==='audio'){talkMode=null;talkAnalyser=null;mouthGoal=.06;
    if(Math.random()<.6)setTimeout(()=>say(pick(LINES.encore)),250);kickS(.08,-.15);}};
  src.start();}
function speak(t){if(!('speechSynthesis'in window))return;
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(t);u.pitch=2;u.rate=1.08;u.volume=muted?0:1;
  u.onstart=()=>{talkMode='tts';};
  u.onend=u.onerror=()=>{if(talkMode==='tts')talkMode=null;};
  talkMode='tts';speechSynthesis.speak(u);}
function openSay(){sayPanel.classList.add('open');sayInput.focus();}
function doSay(){const t=sayInput.value.trim();if(!t)return;
  sayInput.value='';sayPanel.classList.remove('open');
  const short=t.length>60?t.slice(0,60)+'…':t;
  say(short,1400+t.length*70);speak(t);kickS(0,-.1);ac();}

const MELODY=[0,2,4,7,4,2,0,2,4,7,8,7,4,2,4,2];
const SCALE=[262,294,330,392,440,494,523,587,659];
let musicOn=false,musicTimer=null,step=0;
function musicTick(){if(!musicOn)return;
  const n=SCALE[MELODY[step%MELODY.length]%SCALE.length];
  tone({f:n,type:'triangle',dur:.24,vol:.045});
  if(step%4===0)tone({f:n/2,dur:.4,vol:.05});
  if(step%2===1)noise({dur:.05,vol:.014,f:6000,type:'highpass'});
  step++;musicTimer=setTimeout(musicTick,280);}

function downscale(file,max){max=max||640;
  return new Promise((res,rej)=>{const url=URL.createObjectURL(file),im=new Image();
    im.onload=()=>{const k=Math.min(1,max/Math.max(im.width,im.height));
      const c=document.createElement('canvas');
      c.width=Math.max(1,Math.round(im.width*k));c.height=Math.max(1,Math.round(im.height*k));
      c.getContext('2d').drawImage(im,0,0,c.width,c.height);
      URL.revokeObjectURL(url);res(c.toDataURL('image/jpeg',.86));};
    im.onerror=rej;im.src=url;});}
function setPhoto(url,celebrate){S.photo=url;photoImg.src=url;photoImg.style.display='block';
  catFace.style.display='none';save();
  if(celebrate){confetti();SFX.ding();
    say(pick(LINES.hello).replaceAll('{n}',S.name),3200);blush(2000);}}
async function useFile(f){if(!f)return;
  try{hideWelcome();const url=await downscale(f);setPhoto(url,true);}
  catch(e){say('Hmm, that picture did not load 🙈');}}
function hideWelcome(){welcome.classList.remove('show');
  try{localStorage.setItem('ttp_seen','1');}catch(e){}}

feedBtn.onclick=feed;milkBtn.onclick=milk;talkBtn.onclick=toggleTalk;fartBtn.onclick=toot;
camBtn.onclick=()=>fileInput.click();
fileInput.onchange=()=>useFile(fileInput.files[0]);
muteBtn.onclick=()=>{muted=!muted;ac();master.gain.value=muted?0:.9;
  muteBtn.textContent=muted?'🔇':'🔊';};
musicBtn.onclick=()=>{ac();musicOn=!musicOn;musicBtn.classList.toggle('on',musicOn);
  if(musicOn){step=0;musicTick();}else clearTimeout(musicTimer);};
sayToggle.onclick=()=>{sayPanel.classList.toggle('open');if(sayPanel.classList.contains('open'))sayInput.focus();};
sayGo.onclick=doSay;
sayInput.addEventListener('keydown',e=>{if(e.key==='Enter')doSay();});
$('#wUpload').onclick=()=>{hideWelcome();fileInput.click();};
$('#wDefault').onclick=()=>{hideWelcome();SFX.mew();
  say('Hi, I\'m Mochi! 🐱 Tap 📷 to put YOUR photo here!');};
nameTxt.textContent=S.name;
nameTxt.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();nameTxt.blur();}});
nameTxt.addEventListener('blur',()=>{
  S.name=(nameTxt.textContent||'').trim().replace(/\s+/g,' ').slice(0,16)||'Pal';
  nameTxt.textContent=S.name;save();});

let dragDepth=0;
stage.addEventListener('dragover',e=>e.preventDefault());
stage.addEventListener('dragenter',e=>{e.preventDefault();dragDepth++;dropOverlay.classList.add('show');});
stage.addEventListener('dragleave',()=>{if(--dragDepth<=0){dragDepth=0;dropOverlay.classList.remove('show');}});
stage.addEventListener('drop',e=>{e.preventDefault();dragDepth=0;dropOverlay.classList.remove('show');
  useFile(e.dataTransfer.files[0]);});
document.addEventListener('paste',e=>{
  const it=[...((e.clipboardData&&e.clipboardData.items)||[])].find(i=>i.type.startsWith('image/'));
  if(it)useFile(it.getAsFile());});

addEventListener('keydown',e=>{
  if(e.target===sayInput||e.target===nameTxt)return;
  const k=e.key.toLowerCase();
  if(k==='f')feed();else if(k==='m')milk();else if(k==='t')toggleTalk();
  else if(k==='p')toot();
  else if(k===' '){e.preventDefault();
    const r=face.getBoundingClientRect();
    charEl.dispatchEvent(new PointerEvent('pointerdown',
      {clientX:r.left+r.width/2,clientY:r.top+r.height*.2,bubbles:true}));}});

stage.addEventListener('pointermove',e=>{
  room.style.setProperty('--px',((e.clientX/innerWidth)-.5).toFixed(3));
  room.style.setProperty('--py',((e.clientY/innerHeight)-.5).toFixed(3));});

document.addEventListener('pointerdown',()=>ac(),{once:true});

if(S.photo)setPhoto(S.photo,false);
meters();
charWrap.classList.add('enter');
requestAnimationFrame(t=>{lastT=t;frame(t);});

for(let i=0;i<7;i++){const m=document.createElement('i');m.className='mote';
  m.style.left=rand(5,95)+'%';m.style.animationDuration=rand(7,14).toFixed(1)+'s';
  m.style.animationDelay=(-rand(0,12)).toFixed(1)+'s';room.appendChild(m);}

const hr=new Date().getHours();if(hr<6||hr>=19)stage.classList.add('night');

if(!S.photo&&!localStorage.getItem('ttp_seen'))welcome.classList.add('show');
else setTimeout(()=>say('Hi! I\'m '+S.name+'! 👋'),1100);

setInterval(()=>{if(document.hidden)return;
  S.hunger=clamp(S.hunger-.35,0,100);S.fun=clamp(S.fun-.25,0,100);meters();save();},1300);

setInterval(()=>{if(S.busy||talkMode||document.hidden||Math.random()>.7)return;
  const pool=S.hunger<30?LINES.hungry:S.fun<25?LINES.bored:LINES.idle;
  say(pick(pool));if(Math.random()<.3)SFX.mew();kickS(rand(-.04,.04),-.06);},9000);
setInterval(()=>{if(!S.busy&&!talkMode&&!document.hidden)
  kickS(rand(-.06,.06),rand(-.05,-.02),rand(-3,3));},5200);
</script>
</body>
</html>
"""

# ---------------------------------------------------------
# Local Server (For running on your own PC)
# ---------------------------------------------------------
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html", "/health"):
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404, "Not found")

    def log_message(self, *_args):  
        pass

def main():
    # Uses PORT provided by Pella (or 8787 locally)
    port = int(os.environ.get("PORT", 8787))
    
    # Binds to 0.0.0.0 on cloud, 127.0.0.1 locally
    host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    
    try:
        srv = http.server.ThreadingHTTPServer((host, port), Handler)
    except OSError as e:
        print(f"Could not start server on port {port}: {e}")
        sys.exit(1)

    print(f"\n  🐾  TALKING PHOTO PAL is live →  http://{host}:{port}\n")
    
    # Only auto-open browser if running locally on our own PC
    if host == "127.0.0.1":
        threading.Timer(0.6, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
        
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n  Bye! 👋")

if __name__ == "__main__":
    main()