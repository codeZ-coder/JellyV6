#!/usr/bin/env python3
"""
🦈 Predator V2 - Simulador de Ataque Multi-Vetor
Suporta ataques volumétricos (Layer 3/4) e de aplicação (Layer 7)
para testar a Membrana Osmótica da Jelly V6.

Uso:
    python scripts/predator.py --mode bot    (Testa detecção de bots)
    python scripts/predator.py --mode human  (Testa falsos positivos)
    python scripts/predator.py --mode ddos   (Testa Z-Score de rede)
"""
import time
import threading
import requests
import random
import argparse
import sys
from fake_useragent import UserAgent

# Configurações
TARGET_API = "http://localhost:8000/feed"
TEST_URL_VOLUMETRIC = "http://speedtest.tele2.net/10MB.zip"

def attack_volumetric():
    """Modo Original: Gera tráfego de rede para testar Z-Score (psutil)"""
    print(f"🦈 Iniciando Ataque Volumétrico (Target: {TEST_URL_VOLUMETRIC})")
    def download():
        try:
            requests.get(TEST_URL_VOLUMETRIC, timeout=10)
        except: pass
    
    threads = []
    for _ in range(10):
        t = threading.Thread(target=download)
        t.start()
        threads.append(t)
    
    for t in threads: t.join()
    print("✅ Ataque Volumétrico Finalizado")

def attack_bot():
    """Modo Bot: Baixa entropia, alta frequência, User-Agent fixo"""
    print(f"🤖 Iniciando Ataque BOT (Alvo: {TARGET_API})")
    print("   -> Comportamento: Repetitivo, Rápido, UA Fixo")
    
    headers = {"User-Agent": "BadBot/1.0 (Scanning)"}
    
    for i in range(20):
        try:
            # URL fixa, Payload fixo -> Entropia Zero
            r = requests.post(TARGET_API, json={"data": "lixo"}, headers=headers, timeout=2)
            print(f"[{i+1}/20] Status: {r.status_code} | Time: {r.elapsed.total_seconds():.2f}s")
            if r.status_code == 401:
                print("   🛡️ Bloqueado por Token (Normal)")
            elif "gzip" in r.headers.get("Content-Encoding", ""):
                print("   💀 GZIP BOMB DETECTADA! (Nematocisto Ativo)")
                break
        except requests.exceptions.ReadTimeout:
            print("   ⏳ Timeout (Tarpit/Contração Muscular?)")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
        
        time.sleep(0.05) # Muito rápido

def attack_human():
    """Modo Humano: Alta entropia, delay aleatório, User-Agent dinâmico"""
    print(f"🧑 Iniciando Simulação HUMANA (Alvo: {TARGET_API})")
    print("   -> Comportamento: Aleatório, Lento, UA Dinâmico")
    
    try:
        ua = UserAgent()
    except:
        ua = None # Fallback se library não existir

    for i in range(10):
        try:
            # Varia URL e UA para aumentar entropia
            headers = {"User-Agent": ua.random if ua else f"Mozilla/5.0 (Random-{random.randint(1,1000)})"}
            query = f"?q={random.randint(1,10000)}"
            
            r = requests.post(TARGET_API + query, json={"data": "obs"}, headers=headers, timeout=5)
            print(f"[{i+1}/10] Status: {r.status_code}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            
        time.sleep(random.uniform(0.5, 2.0)) # Delay humano

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jelly Predator V2")
    parser.add_argument("--mode", choices=["bot", "human", "ddos"], default="bot", help="Modo de ataque")
    args = parser.parse_args()
    
    print("\n" + "="*40)
    print(f"🦈 PREDATOR V2 - Mode: {args.mode.upper()}")
    print("="*40 + "\n")
    
    try:
        if args.mode == "ddos":
            attack_volumetric()
        elif args.mode == "bot":
            attack_bot()
        elif args.mode == "human":
            attack_human()
    except KeyboardInterrupt:
        print("\n🛑 Interrompido.")
