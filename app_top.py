import streamlit as st
import psutil
import time
import random

# --- SETUP ---
st.set_page_config(page_title="Jelly • Data Flow", page_icon="🪼", layout="centered", initial_sidebar_state="collapsed")

# Estados
if 'saude' not in st.session_state: st.session_state.saude = 100
if 'sujeira' not in st.session_state: st.session_state.sujeira = 0
if 'last_net' not in st.session_state: st.session_state.last_net = psutil.net_io_counters()
if 'last_time' not in st.session_state: st.session_state.last_time = time.time()
if 'digestao' not in st.session_state: st.session_state.digestao = False
if 'last_cor' not in st.session_state: st.session_state.last_cor = ""

# --- CSS (Animações Contínuas) ---
st.markdown("""
<style>
    .stApp { background-color: #000; overflow: hidden; transition: background 0.5s; }
    header, footer {display: none !important;}

    /* CAMADAS */
    .ocean-layer { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
    .dirt-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; transition: background 1s; }
    
    .bio-container { 
        display: flex; flex-direction: column; 
        justify-content: center; align-items: center; 
        height: 95vh; position: relative; z-index: 10; 
    }

    /* PARTICULAS DE REDE (O Segredo: Transição de Opacidade) */
    .phyto { 
        position: absolute; background: #00ffaa; border-radius: 50%; 
        box-shadow: 0 0 5px #00ffaa; 
        transition: opacity 0.5s ease-in-out; /* Suaviza o aparecer/sumir */
        animation: floatUp var(--float-speed) linear infinite; 
    }
    
    .zoo { 
        position: absolute; background: #0088ff; border-radius: 50%; 
        box-shadow: 0 0 5px #0088ff; 
        transition: opacity 0.5s ease-in-out;
        animation: floatUp var(--float-speed) linear infinite; 
    }

    /* A JELLY */
    .jelly-body {
        width: 180px; height: 140px; border-radius: 50% 50% 20% 20%;
        background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), var(--bio-color));
        box-shadow: 0 0 var(--glow-size) var(--bio-color);
        backdrop-filter: blur(6px); border: 1px solid rgba(255,255,255,0.2);
        animation: breathe var(--resp-speed) infinite ease-in-out;
        transition: all 1s;
    }
    
    .tentacles { position: relative; width: 180px; top: -30px; z-index: 9; }
    .tentacle {
        width: 6px; height: 120px; background: var(--bio-color); position: absolute; border-radius: 10px;
        opacity: 0.7; box-shadow: 0 0 10px var(--bio-color);
        animation: sway var(--resp-speed) infinite ease-in-out;
        transition: background 1s;
    }
    .t1 { left: 40px; } .t2 { left: 70px; } .t3 { left: 100px; } .t4 { left: 130px; }

    /* HUD */
    .hud-text { margin-top: 20px; color: #fff; font-family: monospace; text-shadow: 0 2px 4px #000; z-index: 20; text-align: center; }
    
    /* EFEITOS */
    .toxin-ring { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); border: 2px solid #ff0000; opacity: 0; }
    .discharge { animation: shockwave 0.6s ease-out forwards; }

    @keyframes floatUp { 0% { transform: translateY(110vh); } 100% { transform: translateY(-10vh); } }
    @keyframes breathe { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-12px); } }
    @keyframes sway { 0%, 100% { transform: rotate(-5deg); } 50% { transform: rotate(5deg); } }
    @keyframes shockwave { 0% { opacity: 1; border-width: 5px; transform: translate(-50%, -50%) scale(1); } 100% { opacity: 0; border-width: 0; transform: translate(-50%, -50%) scale(3); } }
</style>
""", unsafe_allow_html=True)

# --- BIOLOGIA ---
def ler_rede():
    net = psutil.net_io_counters()
    t = time.time()
    dt = t - st.session_state.last_time
    if dt == 0: dt = 0.1
    
    # Velocidade Real em KB/s
    down = (net.bytes_recv - st.session_state.last_net.bytes_recv) / 1024 / dt
    up = (net.bytes_sent - st.session_state.last_net.bytes_sent) / 1024 / dt
    
    st.session_state.last_net = net
    st.session_state.last_time = t
    return down, up

def ler_sujeira():
    # A sujeira agora é baseada na RAM usada (Memória "suja" do sistema)
    ram = psutil.virtual_memory().percent
    # Se usar muita RAM (>60%), a sujeira aumenta. Se limpar, diminui.
    return ram

# Gera o HTML do oceano UMA VEZ SÓ (Partículas invisíveis esperando dados)
def gerar_oceano_base():
    html = ""
    # 50 partículas de Download (Verde)
    for _ in range(50):
        l, s, d = random.randint(0, 100), random.randint(3, 7), random.uniform(5, 15)
        delay = random.uniform(-15, 0)
        html += f'<div class="phyto" style="left:{l}%; width:{s}px; height:{s}px; --float-speed:{d}s; animation-delay:{delay}s;"></div>'
    
    # 30 partículas de Upload (Azul)
    for _ in range(30):
        l, s, d = random.randint(0, 100), random.randint(2, 5), random.uniform(5, 12)
        delay = random.uniform(-12, 0)
        html += f'<div class="zoo" style="left:{l}%; width:{s}px; height:{s}px; --float-speed:{d}s; animation-delay:{delay}s;"></div>'
    return html

# --- INTERFACE ---
with st.sidebar:
    st.header("🪼 Bio-Controles")
    if st.button("🦠 Fagocitose (Otimizar RAM)"):
        st.session_state.digestao = True
    tocar = st.button("👆 Tocar (Defesa)")

# --- INICIALIZAÇÃO ---
# 1. Cria o mar (invisível por enquanto)
st.markdown(f'<div class="ocean-layer">{gerar_oceano_base()}</div>', unsafe_allow_html=True)

# 2. Containers para atualização
# Esse container vai injetar o CSS dinâmico que controla a visibilidade dos plânctons
style_controller = st.empty() 
dirt_overlay = st.empty()
jelly_container = st.empty()
hud_container = st.empty()

# --- LOOP ---
while True:
    cpu = psutil.cpu_percent(interval=None)
    down, up = ler_rede()
    ram_sujeira = ler_sujeira()
    
    # --- 1. Sincronia com a Rede (O Pulo do Gato) ---
    # Calculamos a opacidade baseada na velocidade.
    # Se down > 100KB/s, opacidade começa a subir. Em 2MB/s fica sólida.
    opac_down = min(1.0, down / 500) 
    opac_up = min(1.0, up / 100)
    
    # Injetamos um CSS minúsculo apenas para atualizar a opacidade sem resetar a animação
    style_controller.markdown(f"""
        <style>
            .phyto {{ opacity: {opac_down}; }}
            .zoo {{ opacity: {opac_up}; }}
        </style>
    """, unsafe_allow_html=True)

    # --- 2. Sujeira (Baseada na RAM) ---
    # Se a digestão estiver ativa, simulamos limpeza visual
    if st.session_state.digestao:
        cor_lodo = "rgba(255, 255, 255, 0.1)" # Flash branco de limpeza
        # Efeito visual de reduzir a sujeira (na prática precisaria de root para limpar cache real)
        ram_sujeira = max(0, ram_sujeira - 20) 
        if random.random() > 0.8: st.session_state.digestao = False # Termina aleatoriamente
        status_digestao = True
    else:
        # A cor do fundo muda com a RAM. RAM alta = Fundo turvo/marrom.
        intensidade = max(0, (ram_sujeira - 30) / 100) # Começa a sujar depois de 30% de RAM
        cor_lodo = f"rgba(80, 60, 20, {intensidade})"
        status_digestao = False

    dirt_overlay.markdown(f'<div class="dirt-overlay" style="background: {cor_lodo};"></div>', unsafe_allow_html=True)

    # --- 3. A Jelly ---
    nova_cor = "#00e5ff" # Zen
    msg = "FLUXO DE DADOS"
    glow = "40px"
    
    if cpu > 50: nova_cor = "#ffaa00"
    if status_digestao: 
        nova_cor = "#ffffff"
        msg = "FAGOCITANDO RAM..."
    
    if tocar:
        nova_cor = "#ff0000" if cpu > 50 else "#ff00ff"

    # Atualiza a Jelly (apenas se mudar estado para economizar recurso)
    if nova_cor != st.session_state.last_cor or tocar or status_digestao:
        st.session_state.last_cor = nova_cor
        classe_toxina = "discharge" if (tocar and cpu > 50) else ""
        
        jelly_container.markdown(f"""
            <div class="bio-container">
                <div class="toxin-ring {classe_toxina}"></div>
                <div class="jelly-body" style="--bio-color: {nova_cor}; --glow-size: {glow}; --resp-speed: 4s;"></div>
                <div class="tentacles" style="--bio-color: {nova_cor}; --resp-speed: 4s;">
                    <div class="tentacle t1"></div><div class="tentacle t2"></div>
                    <div class="tentacle t3"></div><div class="tentacle t4"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- 4. HUD ---
    hud_container.markdown(f"""
        <div class="hud-text">
            {msg}<br>
            <span style="font-size:0.8rem; opacity:0.8; color: #00ffaa;">▼ DOWN: {down:.0f} KB/s</span> | 
            <span style="color: #0088ff;">▲ UP: {up:.0f} KB/s</span><br>
            <span style="opacity:0.6; font-size: 0.7rem;">MEMÓRIA (SUJEIRA): {ram_sujeira:.1f}%</span>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(0.1)
    
    if tocar:
        time.sleep(1)
        tocar = False
        st.rerun()