# Plano de Implementacao: Refinamentos Biologicos (Fase 2)

> **Status:** Planejamento
> **Foco:** Eficiencia Energetica, Reflexo Imediato e Sinal de Ruptura.

## Objetivo
Implementar tres conceitos biologicos para completar o organismo Jelly V6, baseados em Nakamura e na biologia de cnidarios:
1. **Inercia do Nado:** Suavizar o consumo de CPU em repouso.
2. **Gosto Acido:** Bloquear ataques obvios imediatamente, sem buffer.
3. **Ruptura de Mesogleia:** Sinalizar pressao critica para reinicio (imortalidade).

---

## Mudancas Propostas

### 1. Inercia do Nado (Eficiencia)
**Arquivo:** `core/nervenet.py`
- Substituir o `sleep` fixo (degraus) por uma **Media Movel** (Inercia).
- Como `nervenet.py` e uma API reativa (sem loop while-true), a inercia sera aplicada ao **Rate Limiting Adaptativo** no middleware `sistema_imunologico`.
- Se o sistema esta calmo, resposta rapida. Se esta sob ataque, o delay aumenta gradualmente (nao subitamente) para economizar energia.
- Na pratica: ajustar o campo `resp_speed` retornado em `/vitals` usando media movel sobre os ultimos N ciclos.

### 2. Gosto Acido (Reflexo Imediato)
**Arquivo:** `core/membrane.py`
- No metodo `process_request`, **antes** de adicionar ao buffer:
    - Checar patterns sujos na URL: `../`, `%00`, `SELECT`, `UNION`, `<script`.
    - Se detectado:
        - `self.pressure_map[ip] = self.threshold * 3` (Pressao instantanea).
        - Retornar `action="NEMATOCYST", diagnosis="ACIDEZ_IMEDIATA"`.
- Isso bloqueia **Single-Packet Exploits** sem esperar a analise estatistica.

### 3. Conexao Mente-Corpo (Muscle-Skin Link)
**Arquivo:** `core/cnidocyte.py`
- Adicionar `osmotic_alert` ao metodo `avaliar_ameaca`:
    ```python
    def avaliar_ameaca(..., osmotic_alert=None):
        if osmotic_alert in ["NEMATOCYST", "RUPTURA_MESOGLEIA"]:
            self.nematocisto_ativo = 15
            return True
    ```

**Arquivo:** `core/nervenet.py`
- Passar o resultado de `membrane.process_request` para `defense.avaliar_ameaca` dentro do middleware.

### 4. Sinal de Ruptura (Turritopsis)
**Arquivo:** `core/membrane.py`
- No retorno de `process_request`:
    - Se `pressure > threshold * 4`: retornar `action="RUPTURA_MESOGLEIA"`.

**Arquivo:** `core/nervenet.py`
- No middleware `sistema_imunologico`:
    - Se action for `RUPTURA_MESOGLEIA`:
        - Logar `CRITICAL: RUPTURA DE MESOGLEIA DETECTADA!`.
        - `os.kill(os.getpid(), signal.SIGTERM)` (Auto-reinicio pelo Docker).

---

## Plano de Verificacao

### Testes Automatizados
1. **Teste de Acidez:**
    - Script `curl` enviando `GET /?q=../etc/passwd`.
    - Esperado: Bloqueio imediato (Nematocisto) e log "ACIDEZ_IMEDIATA".

2. **Teste de Ruptura:**
    - Script `predator.py` modificado para enviar 1000 requests rapidos (Burst).
    - Esperado: O container Jelly deve morrer (Exit code) e o Docker deve reinicia-lo (restart policy).

3. **Teste de Inercia (Manual):**
    - Observar o campo `resp_speed` no JSON de `/vitals` enquanto varia a carga. Deve mudar suavemente (ex: 5.0 -> 4.8 -> 4.5) e nao pular (5.0 -> 1.0).
