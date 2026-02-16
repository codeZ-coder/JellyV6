#!/usr/bin/env python3
"""
🪼 SORRIA E ACENE — Simulação Completa do Fluxo de Defesa
=========================================================
Simula um atacante real escalando de reconhecimento até ser 
jogado no BLACKHOLE. O servidor NÃO deve morrer.

Fases:
  1. 🔍 Reconhecimento (requests normais)
  2. 🪤 Cai no Honeypot (/admin)
  3. 🔨 Força Bruta (requests rápidos)
  4. ⏳ Leva TARPIT (fica preso)
  5. 🕳️ Cai no BLACKHOLE (204 vazio)
  6. ✅ Verifica que servidor ainda VIVE

Uso:
  python tests/test_sorria_e_acene.py [--target URL]
"""

import requests
import time
import random
import sys

TARGET = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--target" else "http://localhost:8000"

# User agents realistas
UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
    "curl/7.88.1",
    "python-requests/2.31.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]

SEPARATOR = "=" * 60

def header():
    print(f"\n{SEPARATOR}")
    print("🪼 SORRIA E ACENE — Simulação de Ataque Real")
    print(f"   Alvo: {TARGET}")
    print(SEPARATOR)

def fase(num, titulo, emoji):
    print(f"\n{'─' * 50}")
    print(f"  {emoji} FASE {num}: {titulo}")
    print(f"{'─' * 50}")

def req(method, path, desc, delay=0.5, expect=None):
    """Faz request e mostra resultado bonito."""
    url = f"{TARGET}{path}"
    ua = random.choice(UAS)
    try:
        if method == "GET":
            r = requests.get(url, headers={"User-Agent": ua}, timeout=8)
        else:
            r = requests.post(url, headers={"User-Agent": ua}, timeout=8, json={"data": "test"})
        
        status = r.status_code
        # Emoji por status
        if status == 200:
            ico = "😊" if "success" in r.text else "✅"
        elif status == 204:
            ico = "🕳️"
        elif status == 401:
            ico = "🚫"
        else:
            ico = "❓"
        
        body = r.text[:80] if r.text else "(vazio)"
        print(f"  {ico} [{status}] {desc}")
        print(f"     └─ {body}")
        
        if expect and status != expect:
            print(f"     ⚠️  Esperava {expect}, recebeu {status}")
        
        time.sleep(delay)
        return status
        
    except requests.exceptions.ReadTimeout:
        print(f"  ⏳ [TIMEOUT] {desc}")
        print(f"     └─ Preso no TARPIT! (timeout 8s)")
        time.sleep(0.2)
        return "TIMEOUT"
    except requests.exceptions.ConnectionError:
        print(f"  💀 [CONN_REFUSED] {desc}")
        print(f"     └─ Servidor MORREU!")
        return "DEAD"


def main():
    header()
    results = {"allow": 0, "fake200": 0, "tarpit": 0, "blackhole": 0, "dead": False}
    
    # ═══════════════════════════════════════════════
    # FASE 1: Reconhecimento (o atacante chega de mansinho)
    # ═══════════════════════════════════════════════
    fase(1, "RECONHECIMENTO", "🔍")
    print("  O atacante testa se o servidor existe...\n")
    
    for i in range(3):
        s = req("GET", f"/feed?q={random.randint(1000,9999)}", f"Sondagem #{i+1}", delay=1.0)
        if s == 401:
            results["allow"] += 1
    
    print("\n  💭 Atacante: 'Hmm, 401... precisa de token. Vou procurar caminhos...'")
    time.sleep(1)
    
    # ═══════════════════════════════════════════════
    # FASE 2: Cai no Honeypot
    # ═══════════════════════════════════════════════
    fase(2, "HONEYPOT (Phishing Reverso)", "🪤")
    print("  O atacante tenta caminhos comuns...\n")
    
    s = req("GET", "/admin", "Tentando /admin...", delay=0.5, expect=200)
    if s == 200:
        results["fake200"] += 1
        print("\n  💭 Atacante: 'Opa! 200 OK! Admin sem senha? Que sorte!'")
        print("  🪼 Jelly:   (Sorria e Acene... IP marcado radioativo)")
    
    s = req("GET", "/wp-admin/", "Tentando /wp-admin/...", delay=0.5)
    if s == 200:
        results["fake200"] += 1
        print("  💭 Atacante: 'WordPress também?? Esse cara é noob!'")
        print("  🪼 Jelly:   (Pressão subindo... 📈)")
    
    time.sleep(1)
    
    # ═══════════════════════════════════════════════
    # FASE 3: Força Bruta (atacante fica ganancioso)
    # ═══════════════════════════════════════════════
    fase(3, "FORÇA BRUTA", "🔨")
    print("  O atacante começa a martelar o servidor...\n")
    
    for i in range(10):
        path = random.choice(["/feed", "/api/v1/data", "/login"])
        s = req("POST", f"{path}?q={random.randint(1,9999)}", f"Brute #{i+1}: POST {path}", delay=0.3)
        
        if s == "TIMEOUT":
            results["tarpit"] += 1
            print("  💭 Atacante: 'Por que tá tão lento??'")
        elif s == 204:
            results["blackhole"] += 1
            print("  🪼 Jelly:   (BLACKHOLE ativado. Silêncio total.)")
        elif s == "DEAD":
            results["dead"] = True
            break
    
    # ═══════════════════════════════════════════════
    # FASE 4: Desespero (atacante percebe que algo tá errado)
    # ═══════════════════════════════════════════════
    if not results["dead"]:
        fase(4, "DESESPERO", "😰")
        print("  O atacante insiste mesmo recebendo nada...\n")
        
        for i in range(5):
            s = req("GET", f"/feed?desperate={i}", f"Desespero #{i+1}", delay=0.2)
            if s == 204:
                results["blackhole"] += 1
            elif s == "DEAD":
                results["dead"] = True
                break
    
    # ═══════════════════════════════════════════════
    # FASE 5: Verificação — O servidor VIVE?
    # ═══════════════════════════════════════════════
    fase(5, "VERIFICAÇÃO DE VIDA", "💓")
    time.sleep(1)
    
    try:
        # Health check não passa pela defesa
        r = requests.get(f"{TARGET}/health", timeout=3)
        if r.status_code == 200:
            print("  💚 SERVIDOR VIVO! /health retornou 200 OK")
            print("  🪼 Jelly sobreviveu ao ataque sem morrer!")
            server_alive = True
        else:
            print(f"  ⚠️  /health retornou {r.status_code}")
            server_alive = True
    except:
        print("  💀 SERVIDOR MORTO! (RUPTURA aconteceu)")
        server_alive = False
        results["dead"] = True
    
    # ═══════════════════════════════════════════════
    # RELATÓRIO FINAL
    # ═══════════════════════════════════════════════
    print(f"\n{SEPARATOR}")
    print("📊 RELATÓRIO — SORRIA E ACENE")
    print(SEPARATOR)
    print(f"  🚫 Rejeições (401):     {results['allow']}")
    print(f"  😊 Fake 200 (Honeypot): {results['fake200']}")
    print(f"  ⏳ Tarpits (timeout):   {results['tarpit']}")
    print(f"  🕳️ Blackholes (204):    {results['blackhole']}")
    print(f"  💀 Servidor morreu:     {'SIM ❌' if results['dead'] else 'NÃO ✅'}")
    print(SEPARATOR)
    
    if server_alive and results["blackhole"] > 0:
        print("  🏆 RESULTADO: SORRIA E ACENE FUNCIONOU!")
        print("     Atacante foi neutralizado. Servidor intacto.")
    elif server_alive and results["tarpit"] > 0:
        print("  🥈 RESULTADO: Atacante foi retardado (TARPIT)")
        print("     Servidor vivo, mas BLACKHOLE não ativou.")
    elif results["dead"]:
        print("  💀 RESULTADO: RUPTURA ativou (servidor morreu)")
        print("     Threshold pode estar muito baixo.")
    else:
        print("  🤔 RESULTADO: Fluxo incompleto.")
    
    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    main()
