#!/usr/bin/env python3
"""
🦈 Predator - Simulador de Ataque para Demo da Jelly

Este script gera tráfego de rede para demonstrar o sistema de detecção
de anomalias da Jelly. Use apenas em ambiente de desenvolvimento!

Uso:
    python scripts/predator.py

O que acontece:
    1. Gera 10 threads de download simultâneos
    2. A Jelly detecta o pico via Z-Score
    3. O Nematocisto dispara e registra o evento forense
    4. A UI muda para vermelho (PÂNICO)
"""
import time
import threading
import requests
import sys

# Arquivo de teste seguro (10MB)
TEST_URL = "http://speedtest.tele2.net/10MB.zip"
NUM_THREADS = 10


def download_chunk():
    """Baixa um chunk de dados para gerar tráfego"""
    try:
        response = requests.get(TEST_URL, timeout=30)
        size_kb = len(response.content) / 1024
        print(f"  🦈 Pacote recebido: {size_kb:.0f} KB")
    except requests.RequestException as e:
        print(f"  ❌ Erro: {e}")


def attack():
    """Executa o ataque simulado"""
    print("\n" + "=" * 50)
    print("🦈 PREDATOR - Simulador de Ataque")
    print("=" * 50)
    print("\n⏳ Iniciando em 5 segundos...")
    print("   (Prepare a janela do Streamlit para observar)")
    time.sleep(5)
    
    print("\n🦈 INICIANDO FLOOD HTTP...")
    print(f"   Threads: {NUM_THREADS}")
    print(f"   Target: {TEST_URL}")
    print("-" * 50)
    
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=download_chunk, name=f"Shark-{i}")
        threads.append(t)
        t.start()
        time.sleep(0.1)  # Pequeno delay entre threads
    
    # Aguarda todas terminarem
    for t in threads:
        t.join()
    
    print("-" * 50)
    print("✅ Ataque finalizado!")
    print("\n📊 Verifique:")
    print("   1. A Jelly deve estar VERMELHA no dashboard")
    print("   2. O log do brain.py deve mostrar 'FORENSE REGISTRADA'")
    print("   3. Execute: sqlite3 jelly.db 'SELECT * FROM forensic_events;'")
    print("\n🦈 Predator fugindo... 🏊‍♂️")


if __name__ == "__main__":
    try:
        attack()
    except KeyboardInterrupt:
        print("\n\n🛑 Ataque cancelado pelo usuário.")
        sys.exit(0)
