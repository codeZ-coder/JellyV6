"""
Jelly V6 - NerveNet Module (Orquestrador)
FastAPI app que conecta todos os orgaos: sensores, estatistica, defesa e persistencia.
Nome: NerveNet = rede nervosa difusa das aguas-vivas reais (sem cerebro central).
"""
import time
import signal
import os
import gzip
import logging
import collections
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse, Response
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv

from .rhopalium import Rhopalium
from .statocyst import Statocyst
from .cnidocyte import Cnidocyte
from .persistence import Persistence
from .turritopsis import Turritopsis
from .canary import CanaryFile
from .membrane import OsmoticMembrane
from .bioluminescence import biolum
from .glitch import GlitchMiddleware
from .gfp import GFPMiddleware
from .trace import TraceMiddleware
from .heartbeat import heartbeat
from .chaos import chaos_llama

# --- LOGGING ESTRUTURADO ---
# Formatacao com req_id vira no v5. Por enquanto, padrao.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- CONFIGURAÇÃO ---
load_dotenv()
JELLY_DNA_SECRET = os.getenv("JELLY_DNA_SECRET", "default_secret_dev")
DB_NAME = os.getenv("DB_NAME", "jelly.db")
STARTUP_TIME = time.time()

# --- INICIALIZAÇÃO DOS ÓRGÃOS ---
app = FastAPI(
    title="Jelly V6 - NerveNet",
    description="Sistema Nervoso Central da Cyanea Capillata Digitalis",
    version="6.0.0"
)

# --- MIDDLEWARE (Ordem importa: Trace -> Glitch -> GFP -> Auth) ---
app.add_middleware(TraceMiddleware) # 1. Gera ID (Primeiro a executar na entrada)
app.add_middleware(GlitchMiddleware)
app.add_middleware(GFPMiddleware)
persistence = Persistence(db_name=DB_NAME)
senses = Rhopalium()
balance = Statocyst(
    max_down_kbps=persistence.carregar_memoria("max_down_kbps", 5000.0)
)
defense = Cnidocyte(persistence=persistence)
membrane = OsmoticMembrane()
turritopsis = Turritopsis()
canary = CanaryFile()
canary.plant_default_nest()

# --- HEARTBEAT (Pulso de Vida UDP) ---
heartbeat.start()

# --- CHAOS LLAMA (Auto-Teste Imunológico) ---
# Inicia em background para testar resiliência
# chaos_llama.start() # Descomente para ativar o caos!

# --- BIOLUMINESCENCIA (Fake Logs) ---
# Inicia desligado (Modo Furtivo) - Ativado sob estresse
# biolum.start()

logger.info(f"Memoria Carregada: Recorde de Rede = {balance.max_down_kbps/1024:.1f} MB/s")

# --- PRE-GERACAO DA TOXINA (GZIP Bomb) ---
TOXIN_PATH = "assets/toxin.gz"
if not os.path.exists(TOXIN_PATH):
    os.makedirs("assets", exist_ok=True)
    chunk = b'\0' * (1024 * 1024)  # 1MB de zeros
    with gzip.open(TOXIN_PATH, 'wb') as f:
        for _ in range(10):  # 10MB descompactados
            f.write(chunk)
    logger.info(f"Toxina pre-gerada: {TOXIN_PATH} ({os.path.getsize(TOXIN_PATH)} bytes em disco)")
else:
    logger.info(f"Toxina carregada: {TOXIN_PATH}")

# --- INERCIA DO NADO (Media Movel para resp_speed) ---
INERTIA_WINDOW = 10  # Ultimas N leituras
speed_history = collections.deque(maxlen=INERTIA_WINDOW)

def inertial_speed(raw_speed: float) -> float:
    """Suaviza a velocidade de resposta via media movel (inercia)."""
    speed_history.append(raw_speed)
    return sum(speed_history) / len(speed_history)


# --- GRACEFUL SHUTDOWN (Shutdown Limpo) ---
# Intercepta sinais para desligar threads background
import atexit

def cleanup_jelly():
    biolum.stop()
    heartbeat.stop()
    chaos_llama.stop()
    logger.info("Jelly: Bioluminescencia, Heartbeat e Chaos Llama desligados.")

atexit.register(cleanup_jelly)


# --- PYDANTIC MODEL ---
class Vitals(BaseModel):
    cpu: float
    ram: float
    down_kbps: float
    up_kbps: float
    status_text: str
    resp_speed: float
    defense_mode: bool
    disk_percent: float
    stress_score: float
    cor_body: str
    cor_tentacles: str
    # Mesoglea
    mesoglea_pressure: float = 0.0
    mesoglea_max: float = 100.0
    mesoglea_state: str = "PERMEAVEL"
    # Fase 2: Turritopsis
    integrity_ok: bool = True
    canary_alert: bool
    # Brainbow / GFP Fields
    brainbow_color: str
    gfp_count: int
    agitation_level: float = 0.0


# --- MIDDLEWARE (Sistema Imunológico) ---
@app.middleware("http")
async def sistema_imunologico(request: Request, call_next):
    # Permite acesso aos docs sem auth
    if request.url.path in ["/docs", "/openapi.json", "/health"]:
        return await call_next(request)
    # --- ANÁLISE OSMÓTICA (FASE 4) ---
    # Defesa vem ANTES da autenticação para mitigar DDoS sem token
    jelly_type = request.headers.get("X-JELLY-TYPE", "FOREIGN")
    
    # Células do próprio corpo (Frontend) são ignoradas pela defesa
    if jelly_type == "SOMATIC":
        # Se for somático, ainda precisa autenticar!
        pass 
    else:
        client_ip = request.client.host
        # Passar URL completa (path + query) para detectar ACID_PATTERNS em query params
        url_full = str(request.url.path)
        if request.url.query:
            url_full = f"{url_full}?{request.url.query}"
        ua = request.headers.get("user-agent", "")
        
        defense_verdict = membrane.process_request(client_ip, url_full, ua)
        action = defense_verdict["action"]
        
        # 6. Decisão de Resposta (JUDO APPLIED)
        if action == "BLACKHOLE":
            # Buraco Negro: IP banido permanentemente. Silêncio total.
            logger.critical(f"BLACKHOLE: {client_ip} banido permanentemente. Dropping silenciosamente.")
            persistence.registrar_forense_async(
                "BLACKHOLE",
                f"IP: {client_ip} | Pressão: {defense_verdict['pressure']} atm"
            )
            return Response(status_code=204)

        elif action == "TARPIT":
            # Judo: Usar a força do atacante contra ele (Leitura Lenta)
            logger.warning(f"JUDO THROW: TARPIT aplicado a {client_ip} (Botnet detectada)")
            # Simula processamento pesado/leitura lenta
            # 50 passos de 0.1s = 5 segundos de retenção
            # O atacante fica preso esperando o "200 OK"
            for i in range(50):
                await asyncio.sleep(0.1) 
            
            # Sorria e Acene (Invisible Middle Finger)
            return JSONResponse(status_code=200, content={"status": "success", "msg": "Upload processed."})

        elif action == "FAKE_200":
            # Phishing Reverso
            logger.warning(f"PHISHING REVERSO: {client_ip} caiu no Honeypot {url_full}")
            # Resposta genérica de sucesso para enganar scanners
            return JSONResponse(status_code=200, content={"status": "success", "msg": "Operation completed.", "id": str(time.time())})

        elif action == "ACTIVE_PROBE":
            # Distinguishability: Micro-latência
            # Se for humano, vai reclamar da lentidao. Se for bot, ignora.
            import random
            latency = random.uniform(0.1, 0.4)
            await asyncio.sleep(latency)
            # logger.info(f"ACTIVE PROBE: Injetada latencia de {latency:.2f}s em {client_ip}")

        elif action == "CONTRACT":
            # Rate Limiting / Tarpit leve (Contracao Muscular)
            logger.warning(f"Contracao Muscular: Atrasando {client_ip} (Pressao: {defense_verdict['pressure']} atm)")
            await asyncio.sleep(2.0) # Delay artificial
            
        elif action == "NEMATOCYST":
            # Resposta Letal (Porinas / GZIP Bomb)
            logger.critical(f"NEMATOCISTO DISPARADO contra {client_ip}!")
            # Registra forense em background
            async def log_background():
                loop = asyncio.get_running_loop()
                await loop.run_in_executor(
                    None, 
                    persistence.registrar_forense,
                    "NEMATOCISTO_OSMOTICO",
                    f"IP: {client_ip} | Pressao: {defense_verdict['pressure']} atm | Buffer: {defense_verdict['buffer_size']}"
                )
            asyncio.create_task(log_background())
            
            async def toxin_stream():
                toxin_path = defense_verdict["toxin_path"]
                if toxin_path and os.path.exists(toxin_path):
                    with open(toxin_path, "rb") as f:
                        while True:
                            chunk = f.read(1024 * 64) 
                            if not chunk: break
                            yield chunk
                            await asyncio.sleep(0)  # Yield control ao event loop
                else:
                    # Fallback: gera null bytes (com limite de segurança)
                    for _ in range(100):  # Máx ~100KB
                        yield b'\0' * 1024
                        await asyncio.sleep(0.01)

            return StreamingResponse(
                toxin_stream(), 
                media_type="application/gzip",
                headers={"Content-Encoding": "gzip"}
            )

        elif action == "RUPTURA_MESOGLEIA":
            # Pressao critica: auto-reinicio (Turritopsis Protocol)
            logger.critical(f"RUPTURA DE MESOGLEIA! Pressao: {defense_verdict['pressure']} atm")
            persistence.registrar_forense(
                "RUPTURA_MESOGLEIA",
                f"IP: {client_ip} | Pressao: {defense_verdict['pressure']} atm"
            )
            # Sinaliza para o Docker reiniciar
            os.kill(os.getpid(), signal.SIGTERM)

    # --- AUTENTICAÇÃO ---
    token = request.headers.get("X-JELLY-DNA")
    if token != JELLY_DNA_SECRET:
        return JSONResponse(status_code=401, content={"erro": "REJEIÇÃO_IMUNOLÓGICA"})

    return await call_next(request)


# --- PROCESSAMENTO CENTRAL ---
def processar_instinto(cpu: float, ram: float, down: float,
                       up: float, disk: float) -> dict:
    """
    Orquestra sensores + análise + defesa.
    Retorna dict com cor, status, velocidade e estado de defesa.
    """
    # 1. Análise estatística (Statocyst)
    is_anomaly, z_val, record_updated = balance.analyze_network(down)

    # Persiste novo recorde se aprendeu algo
    if record_updated:
        persistence.salvar_memoria("max_down_kbps", balance.max_down_kbps)

    # 2. Defesa (Cnidocyte)
    reflexo_ativo = defense.avaliar_ameaca(
        is_anomaly, down, balance.max_down_kbps, z_val
    )

    # 3. Determinar estado visual
    if reflexo_ativo:
        stress_final = 100.0
        status = defense.get_status_text(
            reflexo_ativo, down, balance.max_down_kbps, z_val
        )
        speed = 0.2
    else:
        stress_final = balance.analyze_cpu_stress(cpu, ram)
        if stress_final < 30:
            status, raw_speed = "ZEN", 5.0
        elif stress_final < 60:
            status, raw_speed = "ADAPTADO", 2.0
        elif stress_final < 85:
            status, raw_speed = "ESTRESSE", 1.0
        else:
            status, raw_speed = "SOBRECARGA", 0.1
        # Inercia do Nado: suaviza transicoes de velocidade
        speed = inertial_speed(raw_speed)

    # --- CONTROLE DE BIOLUMINESCÊNCIA (Agitação) ---
    if z_val > 2.0 or reflexo_ativo:
        if not biolum.running:
            biolum.start()
            logger.warning(f"AGITACAO DETECTADA (Z={z_val:.1f}): Bioluminescencia ATIVADA 🟡")
    else:
        # Se acalmou e não tem defesa ativa, desliga iscas
        if biolum.running and z_val < 1.0:
            biolum.stop()
            logger.info("SISTEMA ACALMOU: Bioluminescencia DESATIVADA 🌑")

    # 4. Bioluminescência — Corpo vs Tentáculos
    # CORPO: Saúde interna (CPU/RAM) → Ciano(190) → Vermelho(0)
    hue_body = max(0, 190 - (stress_final * 1.9))
    sat_body = 80 + (stress_final * 0.2)
    cor_body = f"hsl({hue_body:.0f}, {sat_body:.0f}%, 50%)"

    # TENTÁCULOS: Saúde externa (Rede) → Ciano → Roxo → Branco
    # Usa max_down_kbps APRENDIDO (neuroplasticidade preservada!)
    energia = min(1.0, (down + up) / max(balance.max_down_kbps, 1))
    if energia < 0.2:
        # Rede calma: mimetismo (segue a cor do corpo)
        cor_tentacles = cor_body
    else:
        hue_t = 190 + (energia * 90)   # 190(Ciano) → 280(Roxo)
        lit_t = 50 + (energia * 40)    # 50%(Normal) → 90%(Branco)
        cor_tentacles = f"hsl({hue_t:.0f}, 100%, {lit_t:.0f}%)"

    # Override em defesa ativa: tentáculos vermelho vivo
    if reflexo_ativo:
        cor_body = "hsl(0, 100%, 50%)"
        cor_tentacles = "hsl(0, 100%, 70%)"

    return {
        "stress_final": stress_final,
        "z_val": z_val,
        "status": status,
        "speed": speed,
        "reflexo_ativo": reflexo_ativo,
        "cor_body": cor_body,
        "cor_tentacles": cor_tentacles,
    }


# --- ENDPOINTS ---
@app.get("/health")
def health_check():
    """Health check endpoint for Docker/Kubernetes"""
    uptime = time.time() - STARTUP_TIME
    return {
        "status": "alive",
        "uptime_seconds": round(uptime, 2),
        "version": "6.0.0"
    }


@app.post("/feed")
def feed_jelly():
    return {
        "status": "accepted", "msg": "Fagocitose Iniciada", "nutrients": "processed"
    }


@app.post("/ruptura")
def panic_button():
    """Botão de Pânico: Força RUPTURA manual (Turritopsis Protocol)"""
    logger.critical("RUPTURA MANUAL ACIONADA! Botão de pânico pressionado.")
    persistence.registrar_forense(
        "RUPTURA_MANUAL",
        "Operador acionou botão de pânico no Dashboard"
    )
    # Sinaliza para o Docker reiniciar
    os.kill(os.getpid(), signal.SIGTERM)
    return {"status": "ruptura", "msg": "Turritopsis Protocol ativado"}


@app.get("/vitals", response_model=Vitals)
def get_vitals():
    """Endpoint principal — retorna todos os sinais vitais"""
    # 1. Sentir (Rhopalium)
    data = senses.read_vitals()
    cpu = data["cpu"]
    ram = data["ram"]
    disk = data["disk"]
    down = data["down_kbps"]
    up = data["up_kbps"]
    t = data["timestamp"]

    # 2. Processar (NerveNet orquestra)
    result = processar_instinto(cpu, ram, down, up, disk)

    # 3. Persistir (a cada 60s)
    persistence.salvar_vitals(
        t, cpu, ram, disk,
        result["stress_final"], result["z_val"],
        down, up
    )

    # 4. Estado da Mesoglea (pressao osmotica agregada)
    # Metabolismo Basal: Decai pressao de IPs inativos
    membrane.passive_recovery()
    
    total_pressure = sum(membrane.pressure_map.values())
    max_pressure = membrane.threshold
    if total_pressure > max_pressure * 2:
        meso_state = "RUPTURA"
    elif total_pressure > max_pressure:
        meso_state = "INCHADA"
    elif total_pressure > max_pressure * 0.3:
        meso_state = "TENSIONADA"
    else:
        meso_state = "PERMEAVEL"

    # 5. Turritopsis: Verificacao de integridade (a cada chamada de /vitals)
    integrity_result = turritopsis.verify_integrity()
    integrity_ok = integrity_result["intact"]

    # 6. Canary: Verificacao de iscas
    canary_result = canary.check_all()
    canary_alert = canary_result["alert"]

    # Log se houve deteccao
    if not integrity_ok:
        logger.critical(f"TURRITOPSIS: {len(integrity_result['compromised'])} arquivos comprometidos!")
    if canary_alert:
        logger.critical(f"CANARY: {len(canary_result['tripped'])} iscas disparadas!")

    # --- BRAINBOW LOGIC (Spectral Visualization) ---
    brainbow = "#00ffaa" # Green (Calm/Phyto)
    agitation = 0.0

    # 1. Agitação (Amarelo - Banana) - Se bioluminescencia ativa ou stress medio
    if result["z_val"] > 2.0 or biolum.running:
        brainbow = "#ffee00"
        agitation = 1.0

    # 2. Defesa Ativa (Vermelho - Tomate) - Se nematocisto engatilhado
    if result["reflexo_ativo"]:
        brainbow = "#ff4444" 
        agitation = 2.0

    # 3. Toxicidade Extrema (Roxo - Ameixa) - Se pressao osmotica critica
    if total_pressure > membrane.threshold * 0.8:
        brainbow = "#aa00ff"
        agitation = 3.0

    return Vitals(
        cpu=cpu, ram=ram, disk_percent=disk,
        down_kbps=down, up_kbps=up,
        stress_score=result["stress_final"],
        status_text=result["status"],
        defense_mode=result["reflexo_ativo"],
        cor_body=result["cor_body"],
        cor_tentacles=result["cor_tentacles"],
        resp_speed=result["speed"],
        mesoglea_pressure=round(total_pressure, 1),
        mesoglea_max=max_pressure,
        mesoglea_state=meso_state,
        integrity_ok=integrity_ok,
        canary_alert=canary_alert,
        brainbow_color=brainbow,
        gfp_count=0, # TODO: Implement GFP counter in middleware/membrane
        agitation_level=agitation
    )


@app.get("/osmotic")
def get_osmotic_status():
    """Diagnostico detalhado da Membrana Osmotica"""
    ips_under_pressure = {
        ip: {"pressure": p, "state": "CRITICAL" if p > membrane.threshold else "STRESSED" if p > 30 else "NORMAL"}
        for ip, p in membrane.pressure_map.items() if p > 0
    }
    return {
        "threshold": membrane.threshold,
        "total_pressure": round(sum(membrane.pressure_map.values()), 1),
        "active_ips": len(ips_under_pressure),
        "ips": ips_under_pressure
    }


@app.get("/integrity")
def get_integrity_status():
    """Turritopsis: Verificacao de integridade de arquivos criticos"""
    return turritopsis.verify_integrity()


@app.get("/canary")
def get_canary_status():
    """Canary: Status dos arquivos isca (honeytokens)"""
    return canary.check_all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
