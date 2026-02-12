# Teoria da Defesa Osmótica (Bio-Inspired Cyberdefense)

> **Documento de Conceito - Fase 4 (Honeypots Ativos)**
> Baseado na fisiologia da *Cyanea capillata* e princípios de termodinâmica celular.

## 1. O Conceito: Pressão Dinâmica vs. Bloqueio Estático

Diferente de firewalls tradicionais que operam em lógica binária (Allow/Deny), o modelo de **Defesa Osmótica** opera em um gradiente de "Pressão" (Suspeita/Entropia).

### Anatomia da Célula de Defesa
*   **Membrana Semipermeável**: Interface pública do sistema (API Gateway / Reverse Proxy).
*   **Íons (Cargas)**: Requisições HTTP com características suspeitas (SQLi, 404, User-Agent anômalo).
*   **Pressão Osmótica ($P$)**: O acúmulo de "tensão" no sistema causado pelos íons.
*   **Homeostase**: Capacidade natural do sistema de dissipar pressão ao longo do tempo (decay).
*   **Nematocisto**: Mecanismo de resposta letal (gatilho de defesa).

---

## 2. Modelagem Matemática ($P(t)$)

A integridade da membrana em um instante $t$ é dada pela função de Pressão Dinâmica (Leaky Bucket with Weights):

$$
P(t) = \max\left(0, P(t-1) + (Q_{ion} \cdot M_{origem}) - (R_{rec} \cdot \Delta t)\right)
$$

---

## 3. Estados de Resposta (Assimetria Defensiva)

| Estado | Gatilho | Ação do Sistema (Cnidócito) | Efeito no Alvo |
| :--- | :--- | :--- | :--- |
| **Normal** | $P(t) < Threshold$ | Nenhuma (Permeabilidade Total) | Acesso normal |
| **Contração Muscular** | $P(t) \ge Threshold$ **E** Orgânico | Rate Limiting / CAPTCHA | Lentidão, desafio cognitivo |
| **Ejeção de Nematocisto** | $P(t) \ge Threshold$ **E** Inorgânico | **Disparo Letal** | Bloqueio (L3/L4) + Contra-ataque |

### O Arsenal do Nematocisto

1.  **Neurotoxinas (Paralisia & Bloqueio)**:
    *   **Fluxo de Cálcio ($Ca^{2+}$)**: Tarpit Ativo. Responde 1 byte a cada 10s. Causa "cãibra" (thread locking) no cliente atacante.
    *   **Blackhole**: O tráfego é descartado silenciosamente (DROP).
    *   **TCP Reset**: A conexão é terminada forçadamente.

2.  **Porinas Digitais (Lise/Colapso)**:
    *   **GZIP Bomb**: Payload comprimido que expande para gigabytes na memória do atacante.
    *   **Junks Data**: Respostas XML malformadas para quebrar parsers automatizados.

---

## 4. Evolução Futura: Jelly Swarm (Imunidade de Rebanho)

*   **Sinapse Química (Redis Pub/Sub)**: Compartilha assinaturas de ataque entre nós (Gossip Protocol).
*   **Endurecimento de Membrana**: Aumento preventivo de pressão global.

---

## 5. Notas de Engenharia & Resiliência

### 💀 Tentáculos Destacados (Fossilized Persistence)
O sistema deve sobreviver à morte do processo Python (App Crash ou Reboot).

*   **Kernel-Level Rules**: Regras de `iptables` ou eBPF persistidas no sistema operacional.
*   **Fossilização**: Ao detectar ataque crítico, o sistema salva as regras (`iptables-save > /etc/iptables/rules.v4`) para que os tentáculos continuem queimando mesmo se o "cérebro" (NerveNet) estiver desligado.

### 🧪 Fluxo de Cálcio (Async Tarpit)
Implementação de Tarpit com `StreamingResponse`:

```python
async def fluxo_de_calcio():
    """Simula o fluxo descontrolado de íons. Envia lixo infinitamente."""
    while True:
        yield b"Ca2+" # O 'íon' digital
        await asyncio.sleep(5) # A 'contração' contínua
```
