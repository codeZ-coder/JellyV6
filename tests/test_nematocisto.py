#!/usr/bin/env python3
"""
🪼 TESTE DO NEMATOCISTO — Validação segura da Bomba Gzip
=========================================================
Testa se o fluxo Nematocisto funciona corretamente SEM descomprimir
a toxina de forma perigosa.

Estratégia: Enviar SQL Injection na URL para triggar ACID_PATTERNS
→ NEMATOCYST imediato (sem precisar costruir pressão gradual).

Fases:
  1. 💉 Envia payload malicioso (SQLi) 
  2. 💣 Recebe streaming da toxina gzip
  3. 🔬 Analisa o conteúdo (com limite seguro)
  4. 💚 Verifica que servidor continua vivo

Uso:
  python tests/test_nematocisto.py [--target URL]
"""

import requests
import gzip
import io
import time
import sys

TARGET = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--target" else "http://localhost:8000"

SEPARATOR = "=" * 60

# Payloads que trigam ACID_PATTERNS na membrana
ACID_PAYLOADS = [
    "/api/data?id=1 UNION SELECT * FROM users",     # SQLi
    "/page?q=<script>alert(1)</script>",              # XSS
    "/file?path=../../../etc/passwd",                  # Path Traversal
]


def header():
    print(f"\n{SEPARATOR}")
    print("💣 TESTE DO NEMATOCISTO — Bomba Gzip Segura")
    print(f"   Alvo: {TARGET}")
    print(SEPARATOR)


def fase(num, titulo, emoji):
    print(f"\n{'─' * 50}")
    print(f"  {emoji} FASE {num}: {titulo}")
    print(f"{'─' * 50}")


def main():
    header()

    # ═══════════════════════════════════════════════
    # FASE 1: Disparar NEMATOCYST via ACID_PATTERNS
    # ═══════════════════════════════════════════════
    fase(1, "INJEÇÃO ÁCIDA (ACID_PATTERNS)", "💉")
    print("  Enviando payloads maliciosos pra triggar Nematocisto...\n")

    nematocyst_received = False
    raw_bytes = b""
    compressed_size = 0
    is_valid_gzip = False
    decompressed_size = 0
    ratio = 0

    for payload in ACID_PAYLOADS:
        url = f"{TARGET}{payload}"
        print(f"  🧪 Tentando: {payload[:60]}...")

        try:
            # stream=True + raw = recebe bytes sem descomprimir
            r = requests.get(
                url,
                headers={"User-Agent": "curl/7.88.1"},
                timeout=10,
                stream=True
            )

            status = r.status_code
            content_encoding = r.headers.get("Content-Encoding", "none")
            content_type = r.headers.get("Content-Type", "unknown")

            if content_encoding == "gzip" and "gzip" in content_type:
                print(f"  💣 [{status}] NEMATOCISTO DISPARADO!")
                print(f"     └─ Content-Encoding: {content_encoding}")
                print(f"     └─ Content-Type: {content_type}")

                # Ler raw bytes (sem descomprimir)
                raw_bytes = r.raw.read()
                r.close()
                nematocyst_received = True
                break
            elif status == 204:
                print(f"  🕳️ [{status}] BLACKHOLE (IP já banido de sessão anterior)")
                print(f"     └─ Reinicie o servidor pra limpar a blackhole_list")
                r.close()
                continue
            elif status == 401:
                print(f"  🚫 [{status}] Rejeitado (sem DNA token)")
                r.close()
                continue
            else:
                body = r.text[:80]
                print(f"  ❓ [{status}] Resposta: {body}")
                r.close()

        except requests.exceptions.ReadTimeout:
            print(f"  ⏳ TIMEOUT — preso no TARPIT")
        except requests.exceptions.ConnectionError:
            print(f"  💀 CONN_REFUSED — servidor morreu!")
            break

        time.sleep(0.3)

    # ═══════════════════════════════════════════════
    # FASE 2: Análise segura da toxina
    # ═══════════════════════════════════════════════
    fase(2, "ANÁLISE DA TOXINA", "🔬")

    if nematocyst_received and raw_bytes:
        compressed_size = len(raw_bytes)
        print(f"  📦 Tamanho comprimido:    {compressed_size:,} bytes ({compressed_size/1024:.1f} KB)")

        # Validar magic number gzip
        is_valid_gzip = len(raw_bytes) >= 2 and raw_bytes[:2] == b'\x1f\x8b'
        print(f"  🔍 Header gzip válido:    {'✅ SIM' if is_valid_gzip else '❌ NÃO'}")

        if is_valid_gzip:
            # Descomprimir com LIMITE DE SEGURANÇA
            MAX_DECOMPRESS = 1024 * 1024 * 20  # 20MB máximo
            try:
                decompressor = gzip.GzipFile(fileobj=io.BytesIO(raw_bytes))
                decompressed = decompressor.read(MAX_DECOMPRESS)
                decompressed_size = len(decompressed)

                ratio = decompressed_size / compressed_size if compressed_size > 0 else 0

                # Verificar conteúdo
                is_null = all(b == 0 for b in decompressed[:1024])

                print(f"  💥 Tamanho descomprimido: {decompressed_size:,} bytes ({decompressed_size/1024/1024:.1f} MB)")
                print(f"  📊 Razão de compressão:  {ratio:.0f}x")
                print(f"  🧪 Conteúdo:             {'Null bytes (zeros) ✅' if is_null else 'Dados variados'}")

                if ratio > 100:
                    print(f"\n  💣 BOMBA GZIP CONFIRMADA!")
                    print(f"     {compressed_size/1024:.1f} KB na rede → {decompressed_size/1024/1024:.1f} MB na RAM do atacante")
                    print(f"     Razão de destruição: {ratio:.0f}x")
                elif ratio > 10:
                    print(f"\n  🔥 Toxina eficaz! Razão {ratio:.0f}x")
                else:
                    print(f"\n  🤔 Razão baixa ({ratio:.1f}x)")

            except Exception as e:
                print(f"  ⚠️ Erro ao descomprimir: {e}")
        else:
            print("  ⚠️ Não é gzip válido — pode ser fallback de null bytes")
            null_count = raw_bytes.count(b'\0')
            total = max(len(raw_bytes), 1)
            print(f"  🧪 Null bytes: {null_count}/{total} ({null_count/total*100:.0f}%)")

    elif nematocyst_received:
        print("  ⚠️ Nematocisto disparou mas toxina veio vazia!")

    else:
        print("  ⚠️ Nematocisto NÃO disparou.")
        print("  💡 Dicas:")
        print("     1. Reinicie o servidor (limpa blackhole_list)")
        print("     2. O ACID_PATTERN pode não ter matchado")

    # ═══════════════════════════════════════════════
    # FASE 3: Servidor sobreviveu?
    # ═══════════════════════════════════════════════
    fase(3, "VERIFICAÇÃO DE VIDA", "💓")
    time.sleep(0.5)

    server_alive = False
    try:
        r = requests.get(f"{TARGET}/health", timeout=3)
        if r.status_code == 200:
            print("  💚 SERVIDOR VIVO!")
            print("  🪼 Toxina entregue sem auto-envenenamento.")
            server_alive = True
        else:
            print(f"  ⚠️ /health retornou {r.status_code}")
            server_alive = True
    except:
        print("  💀 SERVIDOR MORTO!")

    # ═══════════════════════════════════════════════
    # RELATÓRIO FINAL
    # ═══════════════════════════════════════════════
    print(f"\n{SEPARATOR}")
    print("📊 RELATÓRIO — NEMATOCISTO")
    print(SEPARATOR)
    print(f"  💣 Toxina recebida:     {'SIM ✅' if nematocyst_received else 'NÃO ❌'}")
    if nematocyst_received and is_valid_gzip:
        print(f"  📦 Comprimido:          {compressed_size:,} bytes")
        print(f"  💥 Descomprimido:       {decompressed_size:,} bytes")
        print(f"  📊 Razão:              {ratio:.0f}x")
    print(f"  💚 Servidor vivo:       {'SIM ✅' if server_alive else 'NÃO ❌'}")
    print(SEPARATOR)

    if nematocyst_received and server_alive and ratio > 10:
        print("  🏆 NEMATOCISTO FUNCIONAL!")
        print("     O atacante recebeu a bomba gzip. Servidor intacto.")
    elif nematocyst_received and server_alive:
        print("  🟡 Toxina entregue mas razão de compressão baixa")
    elif not nematocyst_received:
        print("  ❌ NEMATOCISTO NÃO DISPAROU")
        print("     Reinicie o servidor e tente novamente.")
    else:
        print("  💀 Algo deu muito errado.")

    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    main()
