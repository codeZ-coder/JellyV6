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
HEADERS = {"X-JELLY-DNA": JELLY_DNA_SECRET, "X-JELLY-TYPE": "SOMATIC"} 

BRAIN_URL = os.getenv("BRAIN_URL", "http://localhost:8000")

st.set_page_config(page_title="Jelly • Passive Viewer", page_icon="🪼", layout="centered", initial_sidebar_state="collapsed")

# Estados Vitais (UI Only)
if 'last_cor_body' not in st.session_state: st.session_state.last_cor_body = "#00e5ff"
if 'last_cor_tentacles' not in st.session_state: st.session_state.last_cor_tentacles = "#00e5ff"
if 'ion_positions' not in st.session_state: st.session_state.ion_positions = []

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
        position: relative;
    }
    /* MESOGLEA — Camada Osmótica Viva */
    .mesoglea {
        position: absolute; top: -15px; left: -15px; right: -15px; bottom: -15px;
        border-radius: 50% 50% 30% 30%;
        border: var(--meso-thickness) solid var(--meso-color);
        box-shadow: 0 0 var(--meso-glow) var(--meso-color), inset 0 0 var(--meso-glow) var(--meso-color-inner);
        opacity: var(--meso-opacity);
        animation: mesoglea-pulse var(--meso-pulse-speed) infinite ease-in-out;
        pointer-events: none; z-index: 15;
        transition: all 0.8s;
    }
    .ion-particle {
        position: absolute; width: 4px; height: 4px; border-radius: 50%;
        background: var(--meso-color); box-shadow: 0 0 6px var(--meso-color);
        animation: ion-drift var(--ion-speed) infinite ease-in-out;
        pointer-events: none; z-index: 16;
    }
    @keyframes mesoglea-pulse {
        0%, 100% { transform: scale(1); opacity: var(--meso-opacity); }
        50% { transform: scale(1.05); opacity: calc(var(--meso-opacity) * 0.7); }
    }
    @keyframes ion-drift {
        0% { transform: translate(0, 0) scale(1); opacity: 0.8; }
        25% { transform: translate(10px, -15px) scale(1.2); opacity: 1; }
        50% { transform: translate(-5px, -25px) scale(0.8); opacity: 0.6; }
        75% { transform: translate(-15px, -10px) scale(1.1); opacity: 0.9; }
        100% { transform: translate(0, 0) scale(1); opacity: 0.8; }
    }
    .tentacles { position: relative; width: 180px; top: -30px; height: 100px; z-index: 15; pointer-events: none; }
    .tentacle {
        width: 8px; height: 130px; background: var(--tentacle-color); position: absolute; border-radius: 0 0 10px 10px;
        opacity: 0.7; box-shadow: 0 0 10px var(--tentacle-color);
        animation: sway var(--resp-speed) infinite ease-in-out;
        transition: background 0.5s;
    }
    .t1 { left: 45px; } .t2 { left: 75px; } .t3 { left: 105px; } .t4 { left: 135px; }
    .hud-text { margin-top: 10px; color: #fff; font-family: monospace; text-shadow: 0 2px 4px #000; z-index: 30; text-align: center; }
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
footer_container = st.empty()

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

        # Mesoglea (Fase 4)
        meso_pressure = data.get('mesoglea_pressure', 0)
        meso_max = data.get('mesoglea_max', 100)
        meso_state = data.get('mesoglea_state', 'PERMEAVEL')

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
        meso_pressure, meso_max, meso_state = 0, 100, 'PERMEAVEL'
        
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

    # 5.5 MESOGLEA — Cálculo Visual da Pressão Osmótica
    meso_ratio = min(1.0, meso_pressure / max(meso_max, 1))
    
    if meso_state == "RUPTURA":
        meso_color = "rgba(255, 30, 30, 0.9)"
        meso_color_inner = "rgba(255, 60, 60, 0.4)"
        meso_thickness = "4px"
        meso_glow = "25px"
        meso_opacity = 1.0
        meso_pulse = "0.4s"
        num_ions = 8
    elif meso_state == "INCHADA":
        meso_color = "rgba(255, 120, 30, 0.8)"
        meso_color_inner = "rgba(255, 160, 60, 0.3)"
        meso_thickness = "3px"
        meso_glow = "18px"
        meso_opacity = 0.85
        meso_pulse = "0.8s"
        num_ions = 5
    elif meso_state == "TENSIONADA":
        meso_color = "rgba(255, 200, 60, 0.5)"
        meso_color_inner = "rgba(255, 220, 100, 0.15)"
        meso_thickness = "2px"
        meso_glow = "10px"
        meso_opacity = 0.5
        meso_pulse = "1.5s"
        num_ions = 2
    else:
        meso_color = "rgba(0, 229, 255, 0.1)"
        meso_color_inner = "rgba(0, 229, 255, 0.05)"
        meso_thickness = "1px"
        meso_glow = "3px"
        meso_opacity = 0.1
        meso_pulse = "4s"
        num_ions = 0

    # Gerar/Persistir posições dos íons (session_state evita teleporte)
    if len(st.session_state.ion_positions) != num_ions:
        # Regenera SÓ quando muda o estado (num_ions diferente)
        st.session_state.ion_positions = []
        for i in range(num_ions):
            radius = 110 + random.randint(-10, 20)
            x = 90 + int(radius * 0.5 * (1 if i % 2 == 0 else -1))
            y = 70 + int(radius * 0.4 * (1 if i % 3 == 0 else -1))
            speed = round(random.uniform(2, 5), 1)
            delay = round(random.uniform(-3, 0), 1)
            st.session_state.ion_positions.append({"x": x, "y": y, "speed": speed, "delay": delay})

    ions_html = ""
    for ion in st.session_state.ion_positions:
        ions_html += f'<div class="ion-particle" style="left:{ion["x"]}px; top:{ion["y"]}px; --meso-color:{meso_color}; --ion-speed:{ion["speed"]}s; animation-delay:{ion["delay"]}s;"></div>'

    # 6. Render Jelly (Corpo + Mesoglea + Tentáculos)
    # 6. Render Jelly (Corpo + Mesoglea + Tentáculos)
    # Obs: HTML compactado em uma linha para garantir que o Streamlit renderize como HTML puro
    jelly_html = f'<div class="bio-container"><div class="toxin-ring {classe_toxina}"></div><div class="jelly-body" style="--body-color: {cor_body}; --tentacle-color: {cor_tentacles}; --glow-size: {glow_size}; --resp-speed: {css_resp_speed}; --balance-angle: {css_angle};"><div class="mesoglea" style="--meso-color:{meso_color}; --meso-color-inner:{meso_color_inner}; --meso-thickness:{meso_thickness}; --meso-glow:{meso_glow}; --meso-opacity:{meso_opacity}; --meso-pulse-speed:{meso_pulse};"></div>{ions_html}</div><div class="tentacles" style="--tentacle-color: {cor_tentacles}; --resp-speed: {css_resp_speed};"><div class="tentacle t1"></div><div class="tentacle t2"></div><div class="tentacle t3"></div><div class="tentacle t4"></div></div></div>'
    jelly_container.markdown(jelly_html, unsafe_allow_html=True)

    # 7. HUD - Biomimético & Seguro
    hostname = os.environ.get('HOSTNAME', 'Edge Node')
    # Ícone da Mesoglea para o HUD
    meso_icon = "🫧" if meso_state == "PERMEAVEL" else "🟡" if meso_state == "TENSIONADA" else "🟠" if meso_state == "INCHADA" else "🔴"

    # Mover infos técnicas para session_state ou caption discreto
    hud_container.markdown(f"""
        <div class="hud-text">
            <h2 style="color: {cor_body}; filter: drop-shadow(0 0 5px {cor_body});">{status_txt}</h2>
            <p style="opacity: 0.7; font-size: 0.9em;">
                🧬 DNA Verified | ⚡ Stress: {stress_score:.1f}% | 📦 RAM: {ram}%
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Info técnica discreta no rodapé (Usando footer_container para update in-place)
    footer_container.markdown(f"""
        <div style="text-align: center; color: #555; font-size: 0.8em; margin-top: 10px;">
            {hostname} | ▼ {down:.0f} KB/s ▲ {up:.0f} KB/s | {meso_icon} Mesoglea: {meso_pressure:.0f}/{meso_max:.0f} atm
        </div>
    """, unsafe_allow_html=True)

    # 8. Metabolismo Variável (O coração do script)
    time.sleep(sleep_interval)
