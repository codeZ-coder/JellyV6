# 🪼 Jelly Changelog

## V6.1 "Sorria e Acene" (2026-02-16)

### 🆕 Novas Features
- **BLACKHOLE Defense** — IPs que excedem 400 atm de pressão são banidos silenciosamente
  - Resposta: `204 No Content` (vazio)
  - IP permanece na `blackhole_list` até restart
  - Cada evento é registrado no SQLite com snapshot TCP
- **Botão de Pânico** 🔴 — Controle manual de RUPTURA via Dashboard (sidebar)
  - Confirmação em dois passos para prevenir cliques acidentais
  - Endpoint: `POST /ruptura`
- **Script "Sorria e Acene"** — Simulação realista de ataque em 5 fases
  - `python tests/test_sorria_e_acene.py`

### 🔧 Correções
- Fix `NameError: url` no middleware (usava `url` em vez de `url_path`)
- Fix `NameError: reflexo_ativo` no Cnidocyte
- Fix `IndentationError` na lógica Judo Defense
- Fix `h11 Content-Length` error no BLACKHOLE (era `JSONResponse(204)`, agora `Response(204)`)
- Fix Honeypot causando RUPTURA imediata (pressão de 10x → 5x)

### ⚖️ Ajustes de Threshold
- RUPTURA: `4x → 10x` (1000 atm) — Só em emergência extrema
- BLACKHOLE: Novo nível em `4x` (400 atm)
- Honeypot: Pressão de `10x → 5x` (cai no BLACKHOLE, não RUPTURA)

### 🧹 UI/UX
- Removida barra técnica do HUD (DNA/Stress/RAM) → Foco no estado biológico
- Dashboard mais limpo, alinhado com filosofia "Modo Chucro"

### 📊 Testes
- `test_full_system.py`: 5/5 passando
- `test_sorria_e_acene.py`: Simulação passa com `🏆 SORRIA E ACENE FUNCIONOU!`
- Predator V2 (modo BOT): 20/20 requests → 204 silencioso, servidor vivo

---

## V6.0 "Cyanea Capillata Digitalis" (2026-02-14)

### Core
- FastAPI middleware com defesa osmótica em 6 camadas
- Membrana com detecção de pressão, UA fingerprint e Honeypots
- Cnidocyte com Dwell Time e período refratário
- Statocyst com Z-Score para anomalias de rede
- Turritopsis (auto-heal) com baseline de integridade
- Canary Files para detecção de intrusão
- Dashboard Streamlit com Jelly animada em SVG
