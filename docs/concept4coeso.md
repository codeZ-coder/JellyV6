# Conceito Fase 5: A Organização Biológica (Jelly H-System)

> **Resumo Executivo:** Evolução da Jelly V6 de um "script de defesa" para um "Organismo Autônomo Híbrido" (H-System), integrando Observabilidade, ML leve e Governança Descentralizada.

---

## 1. Filosofia: Por que Observabilidade, não Monitoramento?

**O Problema:** Monitoramento diz *O QUE* (CPU=90%). É reativo e burro.
**A Solução:** Observabilidade diz *POR QUE* (IP X causou aumento Y na RAM). É causal e inteligente.

### 1.1. O Triângulo Dourado (A "Consciência" da Jelly)
*   **Trace (Rastreamento):** Todo request recebe um `Request-ID` único na entrada. Se a Jelly travar, sabemos exatamente em qual tentáculo foi.
*   **Causalidade:** Em vez de logs soltos, eventos correlacionados: `{Causa: Payload_SQL, Efeito: Latencia_+500ms}`.
*   **Data Lake Local:** Não descarte logs de tráfego baixo ("Invisibilidade Acidental"). Guarde amostras para entender o "normal".

---

## 2. O Cérebro: Engenharia de Dados & ML (Statocyst 2.0)

Substituir regras fixas (`if bytes > 5000`) por aprendizado dinâmico.

*   **Algoritmo "Hoje vs Ontem":** Um classificador leve (ex: Isolation Forest ou XGBoost minimalista) que aprende o que é "Normal" a cada hora.
    *   *Se o modelo consegue distinguir fácil o tráfego de agora do de ontem, há uma anomalia.*
*   **SHAP Values (Explicação):** A Jelly não apenas bloqueia; ela explica. "Bloqueado porque User-Agent raro + Payload pequeno".
*   **Chaos Llama (Treinamento Imunológico):** A Jelly ataca a si mesma aleatoriamente (injeção de falhas) para testar se seus reflexos estão afiados. Se ela não detectar o auto-ataque, ela se recalibra.

---

## 3. Dinâmica de Controle: O H-System (Hybrid System)

A Jelly é um sistema híbrido: fluxo contínuo (rede) + estados discretos (modos de defesa).

*   **Dwell Time (Histerese):** Evita o "chattering" (ligar/desligar defesa rápido demais). Se entrar em ALERTA, fica por no mínimo `T` segundos.
*   **Active Probing (Distinguibilidade):** Para provar que um IP é um bot, a Jelly injeta *micro-latência* proposital.
    *   *Humano:* Reclama/Refresh.
    *   *Bot:* Continua batendo na mesma frequência.
*   **EOG (Enriched Output Generator):** Módulo que traduz ruído de rede em "Símbolos de Ataque" claros para o núcleo processar.

---

## 4. Governança: Política dos Pinguins ("Sorria e Acene")

Atrás da tecnologia, uma postura política passivo-agressiva.

*   **Judo Digital (vs Sumo):** Não bloqueie a força bruta. Use-a.
    *   *Ataque:* Upload gigante.
    *   *Defesa:* Aceite a conexão, mas leia a 1 byte/segundo (Tarpit). O atacante trava, a Jelly não.
*   **Invisible Middle Finger:** Nunca dê erro 403/401 (que confirma existência).
    *   Dê **HTTP 200 OK** falso. Finja que aceitou a senha, finja que salvou o arquivo. Jogue tudo no `/dev/null`.
*   **Neighborhood Watch (Descentralização):** Módulos têm autonomia. O sensor de rede pode bloquear sem pedir permissão ao cérebro central se a ameaça for óbvia.

---

## Próximos Passos (Roadmap Fase 5)

1.  **Request ID:** Implementar middleware de rastreamento (`req_id`).
2.  **Tarpit Upgrade:** Melhorar o "Judo" (leitura lenta) em vez de apenas *sleep*.
3.  **Fake 200 OK:** Criar respostas falsas de sucesso para endpoints sensíveis (`/admin`, `/login`).
4.  **Statocyst ML:** Implementar um modelo simples de detecção de anomalia (Baseline Dinâmico).
