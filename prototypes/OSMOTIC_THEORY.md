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

A integridade da membrana em um instante $t$ é dada pela função de Pressão Dinâmica:

$$
P(t) = \left( \sum_{i=0}^{n} Q_{ion} \cdot M_{origem} \right) - (R_{rec} \cdot \Delta t)
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
Quando o disparo letal ocorre, duas toxinas são liberadas:

1.  **Neurotoxinas (Bloqueio)**:
    *   `Blackhole Route`: O tráfego do atacante é descartado silenciosamente.
    *   `TCP Reset`: A conexão é terminada forçadamente.

2.  **Porinas Digitais (Contra-ataque)**:
    *   **GZIP Bomb**: Payload de 10GB compactado em 1KB para exaurir RAM do atacante.
    *   **Tarpit**: Mantém a conexão aberta infinitamente, gastando sockets do atacante.
    *   **Junks Data**: Respostas XML malformadas para quebrar parsers automatizados.

---

## 4. Evolução Futura

*   [ ] **Fator de Imunidade de Rebanho**: Compartilhar $P(t)$ entre nós da rede (Jelly Swarm).
*   [ ] **Adaptação Evolutiva**: Ajustar $Q_{ion}$ automaticamente baseando-se em novos vetores de ataque (Machine Learning).
