import streamlit as st
import psutil
import time
import random

# --- SETUP ---
st.set_page_config(page_title="Jelly • Ecosystem", page_icon="🪼", layout="centered", initial_sidebar_state="collapsed")

# Estados Vitais
if 'saude' not in st.session_state:
    st.session_state.saude = 100
if 'sujeira' not in st.session_state:
    st.session_state.sujeira = 0
if 'last_net' not in st.session_state:
    st.session_state.last_net = psutil.net_io_counters()
if 'last_time' not in st.session_state:
    st.session_state.last_time = time.time()
if 'digestao' not in st.session_state:
    st.session_state.digestao = False

# --- CSS (A Pele e o Oceano) ---
st.markdown("""
    <style>
    .stApp { background-color: #000; overflow: hidden; transition: background 0.5s; }
    header, footer {display: none !important;}
    /* CAMADAS */
    .ocean-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
    .bio-layer { display: flex; justify-content: center; align-items: center; height: 95vh; position: relative; z-index: 10; }
    /* A JELLY */
    .jelly-body { width: 180px; height: 140px; border-radius: 50% 50% 20% 20%; background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), var(--bio-color)); box-shadow: 0 0 var(--glow-size) var(--bio-color); backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.2); animation: breathe var(--resp-speed) infinite ease-in-out; transition: all 0.5s; z-index: 15; }
    .tentacles { position: relative; top: 140px; z-index: 5; }
    .tentacle { width: 6px; height: 120px; background: var(--bio-color); position: absolute; border-radius: 10px; opacity: 0.7; box-shadow: 0 0 10px var(--bio-color); animation: sway var(--resp-speed) infinite ease-in-out; }
    .t1 { left: 50px; }
    .t2 { left: 80px; }
    .t3 { left: 110px; }
    .t4 { left: 140px; }
    /* PLÂNCTON (Rede) */
    .phyto { position: absolute; background: #00ffaa; border-radius: 50%; box-shadow: 0 0 5px #00ffaa; animation: floatUp var(--float-speed) linear infinite; }
    /* DEFESA */
    .toxin-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border: 2px solid #ff0000; opacity: 0; }
    .discharge { animation: shockwave 0.6s ease-out forwards; }
    @keyframes floatUp { 0% { transform: translateY(100vh); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(-10vh); opacity: 0; } }
    @keyframes breathe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
    @keyframes sway { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
    @keyframes shockwave { 0% { opacity: 1; border-width: 5px; transform: translate(-50%, -50%) scale(1); } 100% { opacity: 0; border-width: 0; transform: translate(-50%, -50%) scale(3); } }
    </style>
""", unsafe_allow_html=True)

# --- BIOLOGIA ---
def processar_ambiente():
    net = psutil.net_io_counters()
    t = time.time()
    dt = t - st.session_state.last_time
    if dt == 0:
        dt = 0.1
    down = max(0.5, (net.bytes_recv - st.session_state.last_net.bytes_recv) / 1024 / dt)
    st.session_state.last_net = net
    st.session_state.last_time = t
    st.session_state.sujeira = min(100, st.session_state.sujeira + 0.05)
    return down

def gerar_plancton(down):
    html = ""
    qtd = max(5, int(st.session_state.sujeira / 3))
    for _ in range(qtd):
        l, s = random.randint(0, 100), random.randint(2,6)
        html += f'<div class="phyto" style="left:{l}%; width:{s}px; height:{s}px; --float-speed:{random.uniform(2,5)}s;"></div>'
    return html

# --- CONTROLES ---
with st.sidebar:
    st.header("🪼 Controles")
    fagocitar = st.button("🦠 Fagocitose (Limpar)")
    tocar = st.button("👆 Tocar (Defesa)")

# --- LOOP (Streamlit ajustado) ---
aquarium = st.empty()
def render():
    cpu = psutil.cpu_percent(interval=1.0)
    down = processar_ambiente()
    cor, glow, msg = "#00e5ff", "40px", "ESTÁVEL"
    classe_extra, css_extra = "", ""

    if st.session_state.digestao:
        st.session_state.sujeira = max(0, st.session_state.sujeira - 10)
        cor, glow, msg = "#ffffff", "80px", "DIGERINDO..."
        st.session_state.digestao = False

    aquarium.markdown(f"""
        <style>{css_extra}</style>
        <div class='ocean-layer'>{gerar_plancton(down)}</div>
        <div class='bio-layer {classe_extra}'>
            <div class='toxin-ring'></div>
            <div class='jelly-body' style='--bio-color: {cor}; --glow-size: {glow}; --resp-speed: {max(0.5, 3 - (cpu/30))}s;'></div>
            <div class='tentacles' style='--bio-color: {cor}; --resp-speed: {max(0.5, 3 - (cpu/30))}s;'>
                <div class='tentacle t1'></div>
                <div class='tentacle t2'></div>
                <div class='tentacle t3'></div>
                <div class='tentacle t4'></div>
            </div>
            <div style='position:absolute; bottom:20px; color:#fff; font-family:monospace;'>
                {msg} | CPU: {cpu}% | NET: {down:.0f}KB/s | SUJEIRA: {st.session_state.sujeira:.0f}%
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Loop principal ---
# --- Atualização dinâmica ---
while True:
    render()
    time.sleep(1)