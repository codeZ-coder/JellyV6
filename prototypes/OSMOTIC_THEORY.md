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

Onde:
*   $Q_{ion}$: Carga base do evento (ex: 404 = +10 atm, SQLi = +50 atm).
*   $M_{origem}$: Multiplicador de origem (Orgânico = 1.0, Inorgânico/Bot = 2.0+).
*   $R_{rec}$: Taxa de Recuperação Osmótica (Homeostase), ex: -5 atm/seg.
*   $\Delta t$: Tempo decorrido desde o último evento.

---

## 3. Estados de Resposta (Assimetria Defensiva)

O sistema reage de forma diferente dependendo da natureza do estímulo (Orgânico vs Inorgânico).

### Tabela de Respostas

| Estado | Gatilho | Ação do Sistema (Cnidócito) | Efeito no Alvo |
| :--- | :--- | :--- | :--- |
| **Normal** | $P(t) < Threshold$ | Nenhuma (Permeabilidade Total) | Acesso normal |
| **Contração Muscular** | $P(t) \ge Threshold$ **E** Orgânico | Rate Limiting / CAPTCHA | Lentidão, desafio cognitivo |
| **Ejeção de Nematocisto** | $P(t) \ge Threshold$ **E** Inorgânico | **Disparo Letal** | Bloqueio (L3/L4) + Contra-ataque |

### O Arsenal do Nematocisto
Quando o disparo letal ocorre, o sistema escolhe a toxina mais adequada:

1.  **Neurotoxinas (Paralisia & Bloqueio)**:
    *   **Tarpit (Paralisia)**: Mantém a conexão aberta respondendo 1 byte a cada 10s. Exaure sockets do atacante sem gastar recursos do defensor.
    *   **Blackhole**: O tráfego é descartado silenciosamente (DROP).
    *   **TCP Reset**: A conexão é terminada forçadamente.

2.  **Porinas Digitais (Lise/Colapso)**:
    *   **GZIP Bomb**: Payload comprimido que expande para gigabytes na memória do atacante.
    *   **Junks Data**: Respostas XML malformadas para quebrar parsers automatizados.

---

## 4. Evolução Futura: Jelly Swarm (Imunidade de Rebanho)

Em vez de operar isoladamente, as células (nós Jelly V6) compartilham o gradiente de pressão.

*   **Sinapse Química (Redis Pub/Sub)**: Se um nó detecta alta concentração de íons (ataque), ele publica a assinatura do atacante no canal `jelly_synapse`.
*   **Endurecimento de Membrana**: Outros nós recebem o sinal e aumentam preventivamente a pressão basal para aquele IP, bloqueando antes mesmo do primeiro pacote chegar.

---

## 5. Notas de Engenharia (Implementation Details)

Recomendações técnicas para quando iniciarmos a codificação (Fase 4):

*   **GZIP Bomb Segurança**: JAMAIS gerar a bomba dinamicamente (CPU Spike). Ter o arquivo `bomb.gzip` pré-gerado no disco e servir via stream (I/O Bound).
*   **Tarpit Performance**: Implementar via `StreamingResponse` (Python Generator) para não travar threads do worker.
*   **Armazenamento de Estado**: Usar Redis para guardar o $P(t)$ de cada IP, permitindo persistência e acesso rápido.
