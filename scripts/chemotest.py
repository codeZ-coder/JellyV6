
import random
import time
import sys
import os

# Adiciona o diretorio raiz ao path para importar o core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.chemoreceptor import Chemoreceptor

# --- SIMULADOR DE TRÁFEGO ---

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 10; K)",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/100.0"
]

URLS = [
    "/", "/login", "/api/vitals", "/products/jelly", "/about", 
    "/contact", "/cart", "/checkout", "/img/logo.png", "/css/style.css"
]

def gerar_trafego_organico(qtd=100):
    """Cenário: Black Friday (Alta Entropia)"""
    batch = []
    for _ in range(qtd):
        batch.append({
            "ip": f"192.168.{random.randint(1,255)}.{random.randint(1,255)}",
            "url": random.choice(URLS),
            "user_agent": random.choice(USER_AGENTS)
        })
    return batch

def gerar_trafego_toxico_alvo_fixo(qtd=100):
    """Cenário: Ataque de Exaustão (Baixa Entropia)"""
    # Atacante tenta mudar o IP (via proxy barato), mas bate na mesma URL com mesmo UA
    batch = []
    ua_fixo = "Python-urllib/3.8" # Assinatura comum de bot mal feito
    url_fixa = "/api/login"
    
    for _ in range(qtd):
        # IPs variam um pouco (subnet), mas o resto é fixo
        batch.append({
            "ip": f"10.0.0.{random.randint(1, 10)}", # Pouca variação
            "url": url_fixa,
            "user_agent": ua_fixo
        })
    return batch

def gerar_trafego_botnet_burra(qtd=100):
    """Cenário: Botnet mal configurada (Zero Entropia)"""
    batch = []
    for _ in range(qtd):
        batch.append({
            "ip": "45.22.19.11", # IP Fixo
            "url": "/admin",
            "user_agent": "curl/7.68.0"
        })
    return batch

# --- EXECUÇÃO DO TESTE ---

if __name__ == "__main__":
    sensor = Chemoreceptor()

    print("\n🧪 INICIANDO BIO-ENSAIO DE TOXICIDADE 🧪\n")

    # 1. Teste Orgânico
    print("--- [CENÁRIO 1] Nutriente: Black Friday (Flash Crowd) ---")
    lote_organico = gerar_trafego_organico(100)
    resultado = sensor.analyze_batch(lote_organico)
    print(f"Entropia (H): IP={resultado['H_ip']} | URL={resultado['H_url']}")
    print(f"Vetor T: {resultado['T_vector']} -> {resultado['diagnosis']}")
    print("-" * 50)
    time.sleep(1)

    # 2. Teste Ataque Fixo
    print("\n--- [CENÁRIO 2] Toxina: Ataque de Força Bruta (Alvo Fixo) ---")
    lote_ataque = gerar_trafego_toxico_alvo_fixo(100)
    resultado = sensor.analyze_batch(lote_ataque)
    print(f"Entropia (H): IP={resultado['H_ip']} | URL={resultado['H_url']}")
    print(f"Vetor T: {resultado['T_vector']} -> {resultado['diagnosis']}")
    print("-" * 50)
    time.sleep(1)

    # 3. Teste Botnet
    print("\n--- [CENÁRIO 3] Toxina: Botnet Burra (Zero Variância) ---")
    lote_bot = gerar_trafego_botnet_burra(100)
    resultado = sensor.analyze_batch(lote_bot)
    print(f"Entropia (H): IP={resultado['H_ip']} | URL={resultado['H_url']}")
    print(f"Vetor T: {resultado['T_vector']} -> {resultado['diagnosis']}")
    print("-" * 50)

    print("\n✅ FIM DO BIO-ENSAIO")
