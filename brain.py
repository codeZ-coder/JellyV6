import psutil
import time
import statistics
import sqlite3
import subprocess
import threading
import os
from collections import deque
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
load_dotenv()
JELLY_DNA_SECRET = os.getenv("JELLY_DNA_SECRET", "default_secret_dev")
DB_NAME = os.getenv("DB_NAME", "jelly.db")

# Limites Absolutos inicias (serão sobrescritos pela memória)
LIMIT_CPU_PANIC = 90.0

# --- PERSISTÊNCIA AVANÇADA (WAL + FORENSE) ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    # OTIMIZAÇÃO: Write-Ahead Logging permite leitura/escrita simultânea
    conn.execute("PRAGMA journal_mode=WAL;") 
    conn.execute("PRAGMA synchronous=NORMAL;")
    c = conn.cursor()
    
    # 1. Histórico Vital (Expandido)
    c.execute('''CREATE TABLE IF NOT EXISTS vitals_history
                 (timestamp REAL, cpu REAL, ram REAL, disk REAL, 
                  stress REAL, z_score REAL, down_kbps REAL, up_kbps REAL)''')
                  
    # 2. Eventos Forenses (O "Ferrão")
    c.execute('''CREATE TABLE IF NOT EXISTS forensic_events
                 (timestamp REAL, trigger_type TEXT, details TEXT, raw_snapshot TEXT)''')
                 
    # 3. Memória Neural (Key-Value para aprendizado persistente)
    c.execute('''CREATE TABLE IF NOT EXISTS neuro_memory
                 (key TEXT PRIMARY KEY, value REAL)''')
                 
    conn.commit()
    conn.close()

app = FastAPI(title="Jelly Brain", description="Cérebro Híbrido: Forense & WAL")
init_db()

# --- FUNÇÕES DE BD (Helpers) ---
def salvar_memoria(key: str, value: float):
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT OR REPLACE INTO neuro_memory VALUES (?, ?)", (key, value))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro Memória: {e}")

def carregar_memoria(key: str, default: float) -> float:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.execute("SELECT value FROM neuro_memory WHERE key=?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else default
    except Exception as e:
        return default

def registrar_evento_forense(trigger: str, details: str):
    """
    Executa ss -tunap e salva no banco.
    Deve ser rodado em thread separada para não bloquear a API.
    """
    try:
        # Captura conexões de rede (Socket Statistics)
        # -t: tcp, -u: udp, -n: numeric (fast), -a: all, -p: process
        result = subprocess.run(['ss', '-tunap'], capture_output=True, text=True, shell=False)
        snapshot = result.stdout
        
        conn = sqlite3.connect(DB_NAME)
        conn.execute("INSERT INTO forensic_events VALUES (?, ?, ?, ?)", 
                     (time.time(), trigger, details, snapshot))
        conn.commit()
        conn.close()
        print(f"🕵️‍♂️ FORENSE REGISTRADA: {trigger}")
    except Exception as e:
        print(f"❌ Erro Forense: {e}")

# --- ESTADO GLOBAL ---
class BrainState:
    def __init__(self):
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()
        self.last_save = 0
        
        # Históricos
        self.cpu_history = deque(maxlen=60)
        self.net_history = deque(maxlen=30)
        
        self.nematocisto_ativo = 0 
        
        # Carrega o Recorde Pessoal do banco
        self.max_down_kbps = carregar_memoria("max_down_kbps", 5000.0)
        print(f"🧠 Memória Carregada: Recorde de Rede = {self.max_down_kbps/1024:.1f} MB/s")

brain_state = BrainState()

class Vitals(BaseModel):
    cpu: float
    ram: float
    down_kbps: float
    up_kbps: float
    instinct_color: str
    status_text: str
    resp_speed: float
    defense_mode: bool
    disk_percent: float
    stress_score: float

# --- MIDDLEWARE ---
@app.middleware("http")
async def sistema_imunologico(request: Request, call_next):
    if request.url.path in ["/docs", "/openapi.json"]: return await call_next(request)
    token = request.headers.get("X-JELLY-DNA")
    if token != JELLY_DNA_SECRET:
        return JSONResponse(status_code=401, content={"erro": "REJEIÇÃO_IMUNOLÓGICA"})
    return await call_next(request)

# --- CÓRTEX 1: REDE (Com Forense) ---
def analisar_rede(novo_fluxo):
    brain_state.net_history.append(novo_fluxo)
    
    # 0. APRENDIZADO
    if novo_fluxo > brain_state.max_down_kbps:
        brain_state.max_down_kbps = novo_fluxo
        # Persiste o novo recorde imediatamente
        # (Idealmente seria assíncrono, mas WAL é rápido o suficiente para um único insert)
        salvar_memoria("max_down_kbps", novo_fluxo)
        
    # 1. GATILHO DE SATURAÇÃO (Absoluto Dinâmico)
    limite_panico = brain_state.max_down_kbps * 0.8
    if novo_fluxo > limite_panico:
        # Dispara Forense em background se não estiver em cooldown
        if brain_state.nematocisto_ativo == 0:
            threading.Thread(target=registrar_evento_forense, 
                             args=("SATURACAO_REDE", f"Flow: {novo_fluxo:.0f} > Lim: {limite_panico:.0f}")).start()
        return True, 100.0 
        
    # 2. Z-SCORE (Estatístico)
    if len(brain_state.net_history) < 10: return False, 0.0
    media = statistics.mean(brain_state.net_history)
    desvio = statistics.stdev(brain_state.net_history)
    if desvio < 50: desvio = 50 
    z_score = (novo_fluxo - media) / desvio
    
    if z_score > 3.0:
        if brain_state.nematocisto_ativo == 0:
            threading.Thread(target=registrar_evento_forense, 
                             args=("ANOMALIA_Z_SCORE", f"Z: {z_score:.2f} (Flow: {novo_fluxo:.0f})")).start()
        return True, z_score
        
    return False, z_score

# --- CÓRTEX 2: CPU ---
def analisar_stress_cpu(cpu, ram):
    if cpu > LIMIT_CPU_PANIC or ram > 95: return 100.0
    brain_state.cpu_history.append(cpu)
    if len(brain_state.cpu_history) < 10: return max(cpu, ram)
    media_recente = statistics.mean(brain_state.cpu_history)
    diff = cpu - media_recente
    stress_relativo = max(0, diff * 2.0)
    score = (max(cpu, ram) * 0.4) + (stress_relativo * 0.6)
    return min(100, score)

# --- PROCESSAMENTO ---
def processar_instinto(cpu, ram, down, disk):
    anomalia_rede, z_val = analisar_rede(down)
    
    if anomalia_rede:
        brain_state.nematocisto_ativo = 15 
        
    reflexo_ativo = brain_state.nematocisto_ativo > 0
    if reflexo_ativo: brain_state.nematocisto_ativo -= 1

    if reflexo_ativo:
        stress_final = 100.0
        # Definindo mensagem de alerta
        limite_atual = brain_state.max_down_kbps * 0.8
        tipo = "SATURAÇÃO" if down > limite_atual else f"ANOMALIA Z:{z_val:.1f}"
        status = f"⚠️ ALERTA: {tipo}"
        cor, speed = "#ff0000", 0.2
    else:
        stress_final = analisar_stress_cpu(cpu, ram)
        if stress_final < 30: cor, status, speed = "#00e5ff", "ZEN", 5.0
        elif stress_final < 60: cor, status, speed = "#aa00ff", "ADAPTADO", 2.0
        elif stress_final < 85: cor, status, speed = "#ffaa00", "ESTRESSE", 1.0
        else: cor, status, speed = "#ff4400", "SOBRECARGA", 0.1

    return cor, status, speed, reflexo_ativo, stress_final, z_val

@app.post("/feed")
def feed_jelly():
    return {"status": "accepted", "msg": "Fagocitose Iniciada", "nutrients": "processed"}

@app.get("/vitals", response_model=Vitals)
def get_vitals():
    net = psutil.net_io_counters()
    t = time.time()
    dt = t - brain_state.last_time
    if dt == 0: dt = 0.1
    
    down = (net.bytes_recv - brain_state.last_net.bytes_recv) / 1024 / dt
    up = (net.bytes_sent - brain_state.last_net.bytes_sent) / 1024 / dt
    
    brain_state.last_net = net
    brain_state.last_time = t
    
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    cor, txt, speed, reflex, score, z_val = processar_instinto(cpu, ram, down, disk)
    
    # Persistência Rotineira (A cada 60s)
    if t - brain_state.last_save > 60:
        try:
            conn = sqlite3.connect(DB_NAME)
            # Sem WAL aqui explícito pois já definimos no init, mas boa prática manter conexões curtas
            c = conn.cursor()
            c.execute("INSERT INTO vitals_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                      (t, cpu, ram, disk, score, z_val, down, up))
            conn.commit()
            conn.close()
            brain_state.last_save = t
            print(f"💾 Memória: Stress={score:.1f} | Rede Z={z_val:.1f}")
        except Exception as e:
            print(f"Erro SQLite: {e}")

    return Vitals(
        cpu=cpu, ram=ram, disk_percent=disk, stress_score=score,
        down_kbps=down, up_kbps=up, instinct_color=cor,
        status_text=txt, resp_speed=speed, defense_mode=reflex
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
