#!/usr/bin/env python3
"""
Ci — Домашній AI асистент (Universe OS)
Єдиний самовиконуваний файл для Termux та Windows
"""

import os
import sys
import json
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.error import URLError
from pathlib import Path
import base64

# ============ Конфігурація ============
HOST = "0.0.0.0"
PORT = 8790
DATA_DIR = Path.home() / ".ci-data"

# ============ Іконка (Ci Logo) ============
ICON_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAMAAAADACAYAAABS3GwHAAAACXBIWXMAAAsTAAALEwEAm" # Тимчасово скорочено для ліміту

# ============ HTML UI (Cinematic Infinite Void) ============
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Cimeika Universe</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Manrope:wght@200;300;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Manrope', 'sans-serif'], display: ['"Cinzel Decorative"', 'serif'] },
                    colors: { 'void-black': '#010103', 'ci-gold': '#FFD700' }
                }
            }
        }
    </script>
    <style>
        body, html { background-color: #010103; color: #fff; overflow: hidden; height: 100%; width: 100%; position: fixed; }
        .infinite-bg {
            position: fixed; inset: 0; z-index: 0;
            background: 
                radial-gradient(circle at 50% 115%, rgba(255, 215, 0, 0.2) 0%, transparent 60%), 
                radial-gradient(circle at 50% -15%, rgba(30, 58, 138, 0.25) 0%, transparent 70%), 
                #010103;
        }
        .glass-shell { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(40px); -webkit-backdrop-filter: blur(40px); border: 1px solid rgba(255, 255, 255, 0.08); }
        .si-orb-main { width: 100px; height: 100px; cursor: pointer; transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); filter: drop-shadow(0 0 25px rgba(59, 130, 246, 0.4)); z-index: 50; }
        .si-orb-main:active { transform: scale(0.9); }
        .chat-container { position: fixed; inset: 0; z-index: 100; background: rgba(1, 1, 3, 0.97); backdrop-filter: blur(60px); transform: translateY(100%); transition: transform 0.5s cubic-bezier(0.32, 0.72, 0, 1); display: flex; flex-direction: column; }
        .chat-container.active { transform: translateY(0); }
        .input-anchor { padding-bottom: env(safe-area-inset-bottom, 24px); background: linear-gradient(to top, #010103 85%, transparent); }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        
        /* Resonance Effect */
        .res-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border-radius: 50%; border: 1px solid rgba(255, 215, 0, 0.1); pointer-events: none; animation: ripple 8s linear infinite; }
        @keyframes ripple { 0% { width: 0; height: 0; opacity: 1; } 100% { width: 200vw; height: 200vw; opacity: 0; } }
    </style>
</head>
<body class="antialiased">
    <div class="infinite-bg"></div>
    <div class="res-ring" style="animation-delay: 0s"></div>
    <div class="res-ring" style="animation-delay: 4s"></div>

    <!-- UI LAYER -->
    <div id="main-ui" class="relative z-10 h-screen w-full flex flex-col justify-between py-12 px-6">
        
        <!-- Top Facets -->
        <div class="w-full flex justify-between gap-4">
            <div class="glass-shell flex-1 p-5 rounded-[2.5rem] cursor-pointer" onclick="openModule('legend')">
                <span class="text-[8px] tracking-[0.3em] uppercase text-white/40 block mb-1">Знання</span>
                <h2 class="font-display text-lg">Казкар</h2>
            </div>
            <div class="glass-shell flex-1 p-5 rounded-[2.5rem] cursor-pointer" onclick="openModule('event')">
                <span class="text-[8px] tracking-[0.3em] uppercase text-white/40 block mb-1">Дія</span>
                <h2 class="font-display text-lg text-blue-400">ПоДія</h2>
            </div>
        </div>

        <!-- Core (Si Axis) -->
        <div class="flex flex-col items-center gap-8">
            <div class="flex items-center gap-10">
                <div class="text-center opacity-60" onclick="openModule('calendar')">
                    <div class="w-12 h-12 rounded-2xl glass-shell flex items-center justify-center mb-2"><i data-lucide="calendar"></i></div>
                    <span class="text-[7px] uppercase tracking-widest">Ритм</span>
                </div>

                <div class="relative" onclick="toggleChat()">
                    <div class="absolute -top-6 left-1/2 -translate-x-1/2 text-[7px] uppercase tracking-[0.5em] text-ci-gold/50">Ініціація</div>
                    <!-- Using GitHub Hosted Asset for Logo -->
                    <img src="https://raw.githubusercontent.com/cimeika/assets/main/icon-512.png" alt="Ci" class="si-orb-main" onerror="this.src='https://via.placeholder.com/110/050B1A/FFD700?text=Ci'">
                </div>

                <div class="text-center opacity-60" onclick="openModule('gallery')">
                    <div class="w-12 h-12 rounded-2xl glass-shell flex items-center justify-center mb-2"><i data-lucide="image"></i></div>
                    <span class="text-[7px] uppercase tracking-widest">Образ</span>
                </div>
            </div>

            <div class="glass-shell px-6 py-2 rounded-full flex gap-4 text-[10px] font-mono border-ci-gold/10">
                <div class="flex flex-col items-center"><span class="text-[6px] text-white/30 uppercase">Resonance</span><span class="text-ci-gold">0.98 Hz</span></div>
                <div class="w-[1px] h-4 bg-white/10 self-center"></div>
                <div class="flex flex-col items-center"><span class="text-[6px] text-white/30 uppercase">Balance</span><span class="text-blue-400">74%</span></div>
            </div>
        </div>

        <!-- Bottom Facets -->
        <div class="w-full flex justify-between gap-4">
            <div class="glass-shell flex-1 p-5 rounded-[2.5rem] cursor-pointer" onclick="openModule('mood')">
                <span class="text-[8px] tracking-[0.3em] uppercase text-white/40 block mb-1">Середовище</span>
                <h2 class="font-display text-lg text-purple-400">Настрій</h2>
            </div>
            <div class="glass-shell flex-1 p-5 rounded-[2.5rem] cursor-pointer" onclick="openModule('kids')">
                <span class="text-[8px] tracking-[0.3em] uppercase text-white/40 block mb-1">Енергія</span>
                <h2 class="font-display text-lg text-pink-400">Маля</h2>
            </div>
        </div>
    </div>

    <!-- INITIATION CHAT (GEMINI POWERED) -->
    <div id="chat-overlay" class="chat-container">
        <div class="p-8 flex justify-between items-center flex-shrink-0">
            <h3 class="font-display text-2xl text-ci-gold tracking-widest">Ініціація Сі</h3>
            <button onclick="toggleChat()" class="w-10 h-10 rounded-full glass-shell flex items-center justify-center transition hover:bg-white/10">
                <i data-lucide="x" class="text-white w-5 h-5"></i>
            </button>
        </div>

        <div id="messages" class="flex-1 px-8 py-4 overflow-y-auto no-scrollbar flex flex-col gap-6">
            <div class="glass-shell p-6 rounded-3xl rounded-bl-none max-w-[85%] self-start border-l-2 border-ci-gold/40">
                <p class="text-sm font-light leading-relaxed">Очікую сигнал. Яка координата вашого стану потребує корекції?</p>
            </div>
        </div>

        <!-- STABLE INPUT AREA -->
        <div class="input-anchor flex flex-col items-center gap-6 p-6">
            <div class="w-full max-w-lg flex items-center gap-3 bg-white/5 border border-white/10 rounded-3xl p-2 focus-within:border-ci-gold/50 transition-all">
                <input id="chat-input" type="text" placeholder="Ваша думка..." 
                    class="flex-1 bg-transparent px-4 py-3 text-white outline-none text-sm placeholder:text-white/20">
                <button onclick="sendChatMessage()" class="w-12 h-12 rounded-2xl bg-ci-gold text-void-black flex items-center justify-center active:scale-90 transition">
                    <i data-lucide="send" class="w-5 h-5"></i>
                </button>
            </div>

            <div class="flex flex-col items-center gap-2">
                <button onmousedown="startVoice()" onmouseup="stopVoice()" ontouchstart="startVoice()" ontouchend="stopVoice()" 
                    class="w-16 h-16 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-700 flex items-center justify-center shadow-2xl relative active:scale-95 transition">
                    <i data-lucide="mic" class="text-white w-6 h-6"></i>
                    <div id="mic-pulse" class="absolute inset-0 rounded-full border-2 border-ci-gold opacity-0"></div>
                </button>
                <span class="text-[8px] uppercase tracking-[0.4em] text-ci-gold/50">Голосовий резонанс</span>
            </div>
        </div>
    </div>

    <!-- MODULE MODAL -->
    <div id="module-modal" class="fixed inset-0 z-[120] bg-void-black hidden flex-col p-8 backdrop-blur-3xl">
        <div class="flex justify-between items-center mb-8">
            <h2 id="modal-title" class="font-display text-2xl text-ci-gold uppercase tracking-widest"></h2>
            <button onclick="closeModule()" class="text-white/40 hover:text-white"><i data-lucide="x"></i></button>
        </div>
        <div id="modal-body" class="flex-1 overflow-y-auto"></div>
    </div>

    <script>
        const apiKey = ""; // Gemini API Key
        let isProcessing = false;

        function initApp() {
            lucide.createIcons();
            document.getElementById('chat-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') sendChatMessage(); });
        }

        function toggleChat() {
            const overlay = document.getElementById('chat-overlay');
            const isActive = overlay.classList.contains('active');
            overlay.classList.toggle('active');
            if(!isActive) setTimeout(() => document.getElementById('chat-input').focus(), 500);
            if(navigator.vibrate) navigator.vibrate(20);
        }

        async function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const text = input.value.trim();
            if(!text || isProcessing) return;

            addMessage(text, 'user');
            input.value = '';
            isProcessing = true;

            const aiResponse = await callGemini(text);
            addMessage(aiResponse, 'ai');
            isProcessing = false;
        }

        function addMessage(text, role) {
            const container = document.getElementById('messages');
            const div = document.createElement('div');
            div.className = role === 'user' 
                ? 'glass-shell p-4 rounded-3xl rounded-br-none max-w-[85%] self-end border-ci-gold/20' 
                : 'glass-shell p-5 rounded-3xl rounded-bl-none max-w-[85%] self-start border-l-2 border-ci-gold/40';
            div.innerHTML = `<p class="text-sm font-light leading-relaxed">${text}</p>`;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        async function callGemini(p) {
            try {
                const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        contents: [{parts: [{text: p}]}],
                        systemInstruction: {parts: [{text: "Ти - Сі, ядро координації Cimeika Universe. Відповідай мудро, коротко, українською мовою."}]}
                    })
                });
                const d = await res.json();
                return d.candidates[0].content.parts[0].text;
            } catch(e) { return "Сигнал перервано. Зверніться до ядра пізніше."; }
        }

        function openModule(m) {
            const modal = document.getElementById('module-modal');
            const title = document.getElementById('modal-title');
            const body = document.getElementById('modal-body');
            
            title.innerText = m;
            modal.classList.remove('hidden');
            modal.classList.add('flex');

            if(m === 'legend') {
                body.innerHTML = '<div class="glass-shell p-8 rounded-3xl"><p class="text-ci-gold/80 italic">Налаштування потоку мудрості...</p></div>';
            }
            if(navigator.vibrate) navigator.vibrate(10);
        }

        function closeModule() { document.getElementById('module-modal').classList.add('hidden'); }
        function startVoice() { document.getElementById('mic-pulse').classList.add('animate-ping', 'opacity-50'); if(navigator.vibrate) navigator.vibrate(30); }
        function stopVoice() { document.getElementById('mic-pulse').classList.remove('animate-ping', 'opacity-50'); addMessage("... голосовий паттерн прийнято ...", 'user'); sendChatMessage(); }

        window.onload = initApp;
    </script>
</body>
</html>'''

class CiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    print(f"╔═══════════════════════════════════════════╗")
    print(f"║      🏠 Ci Universe OS is LIVE            ║")
    print(f"║  URL: http://localhost:{PORT}              ║")
    print(f"╚═══════════════════════════════════════════╝")
    threading.Thread(target=lambda: webbrowser.open(f"http://localhost:{PORT}"), daemon=True).start()
    HTTPServer((HOST, PORT), CiHandler).serve_forever()

if __name__ == "__main__":
    main()
