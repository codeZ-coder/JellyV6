import streamlit as st
import time
import random
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv()
# DEFINE O DNA (Simbiose)
JELLY_DNA_SECRET = os.getenv("JELLY_DNA_SECRET", "default_secret_dev")
HEADERS = {"X-JELLY-DNA": JELLY_DNA_SECRET} 

BRAIN_URL = os.getenv("BRAIN_URL", "http://localhost:8000")

st.set_page_config(page_title="Jelly • Passive Viewer", page_icon="🪼", layout="centered", initial_sidebar_state="collapsed")

# Estados Vitais (UI Only)
if 'last_cor_body' not in st.session_state: st.session_state.last_cor_body = "#00e5ff"
if 'last_cor_tentacles' not in st.session_state: st.session_state.last_cor_tentacles = "#00e5ff"

if 'fail_count' not in st.session_state: st.session_state.fail_count = 0

# --- CSS (Atualizado: corpo e tentáculos com cores independentes) ---
st.markdown("""
<style>
    .stApp { background-color: #050505; overflow: hidden; transition: background 0.5s; }
    header, footer {display: none !important;}
    .ocean-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
    .dirt-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; transition: background 0.5s; }
    .bio-container { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 80vh; position: relative; z-index: 10; }
    .phyto { position: absolute; background: #00ffaa; border-radius: 50%; box-shadow: 0 0 6px #00ffaa; transition: opacity 0.2s; animation: floatUp var(--float-speed) linear infinite; }
    .zoo { position: absolute; background: #0088ff; border-radius: 50%; box-shadow: 0 0 6px #0088ff; transition: opacity 0.2s; animation: floatUp var(--float-speed) linear infinite; }
    .jelly-body {
        width: 180px; height: 140px; border-radius: 50% 50% 20% 20%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), var(--body-color));
        box-shadow: 0 0 var(--glow-size) var(--tentacle-color);
        backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.2);
        animation: breathe var(--resp-speed) infinite ease-in-out;
        transform: rotate(var(--balance-angle));
        transition: all 0.5s; z-index: 20;
    }
    .tentacles { position: relative; width: 180px; top: -50px; z-index: 10; }
    .tentacle {
        width: 8px; height: 130px; background: var(--tentacle-color); position: absolute; border-radius: 0 0 10px 10px;
        opacity: 0.6; box-shadow: 0 0 10px var(--tentacle-color);
        animation: sway var(--resp-speed) infinite ease-in-out;
        transition: background 0.5s;
    }
    .t1 { left: 45px; } .t2 { left: 75px; } .t3 { left: 105px; } .t4 { left: 135px; }
    .hud-text { margin-top: -20px; color: #fff; font-family: monospace; text-shadow: 0 2px 4px #000; z-index: 30; text-align: center; }
    .toxin-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border: 3px solid #ff0000; opacity: 0; z-index: 25; }
    .discharge { animation: shockwave 0.5s ease-out forwards; }
    @keyframes floatUp { 0% { transform: translateY(110vh); } 100% { transform: translateY(-10vh); } }
    @keyframes breathe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
    @keyframes sway { 0%, 100% { transform: rotate(-3deg); } 50% { transform: rotate(3deg); } }
    @keyframes shockwave { 0% { opacity: 1; border-width: 5px; transform: translate(-50%, -50%) scale(1); } 100% { opacity: 0; border-width: 0; transform: translate(-50%, -50%) scale(3.5); } }
</style>
""", unsafe_allow_html=True)

def gerar_oceano_base():
    html = ""
    for _ in range(50):
        l, s, d = random.randint(0, 100), random.randint(3, 8), random.uniform(4, 10)
        delay = random.uniform(-10, 0)
        html += f'<div class="phyto" style="left:{l}%; width:{s}px; height:{s}px; --float-speed:{d}s; animation-delay:{delay}s;"></div>'
    for _ in range(30):
        l, s, d = random.randint(0, 100), random.randint(2, 6), random.uniform(5, 12)
        delay = random.uniform(-12, 0)
        html += f'<div class="zoo" style="left:{l}%; width:{s}px; height:{s}px; --float-speed:{d}s; animation-delay:{delay}s;"></div>'
    return html


# --- INICIALIZAÇÃO ---
st.markdown(f'<div class="ocean-layer">{gerar_oceano_base()}</div>', unsafe_allow_html=True)
style_controller = st.empty() 
dirt_overlay = st.empty()
jelly_container = st.empty()
hud_container = st.empty()

# --- LOOP DA VIDA ---
while True:
    try:
        # 1. Sinapse com a NerveNet (COM AUTH)
        response = requests.get(f"{BRAIN_URL}/vitals", headers=HEADERS, timeout=0.5)
        
        if response.status_code == 401:
             raise Exception("REJECTED_DNA")
             
        data = response.json()
        
        down = data.get('down_kbps', 0)
        up = data.get('up_kbps', 0)
        cpu = data.get('cpu', 0)
        ram = data.get('ram', 0)
        disk = data.get('disk_percent', 0)
        stress_score = data.get('stress_score', 0)
        status_txt = data.get('status_text', "OFFLINE")

        # Cores separadas do NerveNet
        cor_body = data.get('cor_body', '#00e5ff')
        cor_tentacles = data.get('cor_tentacles', '#00e5ff')

        # Lógica de Equilíbrio (Estatocistos)
        angulo_inclinacao = 0
        if disk > 50:
            fator_cheio = (disk - 50) / 40
            angulo_inclinacao = int(fator_cheio * 30)
        css_angle = f"{angulo_inclinacao}deg"
        
        # Metabolismo
        sleep_interval = float(data.get('resp_speed', 5.0))
        
        # SUCESSO: Reseta contador de falhas
        st.session_state.fail_count = 0
        
        css_resp_speed = f"{sleep_interval}s"
        
        reflex_active = data.get('defense_mode', False) 
        
    except Exception as e:
        st.session_state.fail_count += 1
        status_txt = "SINAPSE PERDIDA"
        cor_body = "#333333"
        cor_tentacles = "#333333"
        sleep_interval = 2.0
        css_resp_speed = "2s"
        css_angle = "0deg"
        down, up, cpu, ram, disk, reflex_active = 0, 0, 0, 0, 0, False
        stress_score = 0
        
        # AUTO-RERUN (Desfibrilador)
        if st.session_state.fail_count >= 5:
            st.session_state.fail_count = 0
            time.sleep(1)
            st.rerun()
    
    # 2. Cronobiologia (Ocelos - Ritmo Circadiano)
    hora = datetime.now().hour
    eh_noite = hora >= 18 or hora < 6
    
    if eh_noite:
        bg_color = "#000000"
        glow_size = "60px"
        ocean_opac = 0.8
    else:
        bg_color = "#1a1a2e"
        glow_size = "20px"
        ocean_opac = 0.4

    # 3. Processamento Visual de Rede
    opac_down = min(1.0, down / 200) 
    opac_up = min(1.0, up / 100)
    
    style_controller.markdown(f"""
        <style>
            .stApp {{ background-color: {bg_color}; transition: background 2s; }}
            .phyto {{ opacity: {opac_down * ocean_opac}; }}
            .zoo {{ opacity: {opac_up * ocean_opac}; }}
        </style>
    """, unsafe_allow_html=True)

    # 4. Sujeira
    intensidade_sujeira = max(0, (ram - 30) / 100)
    cor_lodo = f"rgba(80, 70, 30, {intensidade_sujeira})"
    dirt_overlay.markdown(f'<div class="dirt-overlay" style="background: {cor_lodo};"></div>', unsafe_allow_html=True)

    # 5. Defesa
    classe_toxina = "discharge" if reflex_active else ""
    if reflex_active: status_txt = "⚡ REFLEXO DE DEFESA ⚡"

    # 6. Render Jelly (Corpo e Tentáculos com cores independentes)
    jelly_container.markdown(f"""
        <div class="bio-container">
            <div class="toxin-ring {classe_toxina}"></div>
            <div class="jelly-body" style="--body-color: {cor_body}; --tentacle-color: {cor_tentacles}; --glow-size: {glow_size}; --resp-speed: {css_resp_speed}; --balance-angle: {css_angle};"></div>
            <div class="tentacles" style="--tentacle-color: {cor_tentacles}; --resp-speed: {css_resp_speed};">
                <div class="tentacle t1"></div><div class="tentacle t2"></div>
                <div class="tentacle t3"></div><div class="tentacle t4"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 7. HUD - Biomimético & Seguro
    hostname = os.environ.get('HOSTNAME', 'Edge Node')
    hud_container.markdown(f"""
        <div class="hud-text">
            <h2 style="color: {cor_body}; filter: drop-shadow(0 0 5px {cor_body});">{status_txt}</h2>
            <p style="opacity: 0.7; font-size: 0.9em;">
                🧬 DNA Verified | ⚡ Stress: {stress_score:.1f}% | 📦 RAM: {ram}%
            </p>
            <div style="font-size: 0.8em; color: #555; margin-top: 5px;">
                Edge Instance: {hostname} <br>
                <span style="color: #00ffaa;">▼ {down:.0f} KB/s</span> | <span style="color: #0088ff;">▲ {up:.0f} KB/s</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 8. Metabolismo Variável (O coração do script)
    time.sleep(sleep_interval)
