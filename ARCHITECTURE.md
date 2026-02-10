# 🪼 Jelly Nervous System (JNS) - Architecture

> *"A natureza não faz nada em vão."* - Aristóteles

A **Jelly** é um Sistema de Detecção de Intrusão (IDS) biomimético que utiliza conceitos de "Calm Technology" para monitorar a saúde de servidores e dispositivos Edge. Diferente de logs tradicionais, a Jelly traduz métricas de estresse em bioluminescência (cores HSL) e reage a ameaças disparando contramedidas defensivas (Nematocistos).

---

## 🏗️ Diagrama de Arquitetura

```mermaid
graph TD
    User((Usuário/Admin))
    Hacker((Atacante))

    subgraph "Jelly NerveNet - Docker"
        subgraph "core/"
            NN[nervenet.py<br/>Orquestrador FastAPI]
            RH[rhopalium.py<br/>Sensores psutil]
            ST[statocyst.py<br/>Z-Score + Stress]
            CN[cnidocyte.py<br/>Defesa + Forense]
            PR[persistence.py<br/>SQLite WAL]
        end
        UI[interface/app.py<br/>Streamlit]
    end

    User -->|Visualiza| UI
    Hacker -.->|DDoS/Scan| RH
    UI -->|HTTP /vitals| NN
    NN --> RH
    NN --> ST
    NN --> CN
    CN --> PR
    ST --> PR
    NN --> PR
```

---

## 📋 Requisitos Funcionais

| ID | Requisito | Status |
|---|---|---|
| **RF001** | Monitorar CPU, RAM, Disco e Rede via psutil | ✅ |
| **RF002** | Detectar anomalias via Z-Score (threshold > 3.0) | ✅ |
| **RF003** | Disparar Nematocisto (log forense) em anomalias | ✅ |
| **RF004** | Cores separadas: Corpo (saúde interna) vs Tentáculos (rede) | ✅ |
| **RF005** | Persistir histórico e eventos forenses em SQLite WAL | ✅ |
| **RF006** | Health check endpoint para Docker/Kubernetes | ✅ |

---

## 📋 Requisitos Não-Funcionais

| ID | Requisito | Implementação |
|---|---|---|
| **RNF001** | CPU < 5% em repouso | Loop otimizado + WAL |
| **RNF002** | Segurança: shell=False | subprocess seguro |
| **RNF003** | Portabilidade | Docker multi-arch |
| **RNF004** | Graceful shutdown | Signal handler |
| **RNF005** | Modularidade | 1 arquivo = 1 responsabilidade |

---

## 🧬 Diagrama de Classes (NerveNet Modular)

```mermaid
classDiagram
    class Rhopalium {
        -last_net
        -last_time
        +read_vitals() dict
    }

    class Statocyst {
        -cpu_history: deque
        -net_history: deque
        +max_down_kbps: float
        +analyze_network(fluxo) tuple
        +analyze_cpu_stress(cpu, ram) float
    }

    class Cnidocyte {
        -nematocisto_ativo: int
        -persistence: Persistence
        +avaliar_ameaca() bool
        +get_status_text() str
    }

    class Persistence {
        -db_name: str
        +salvar_memoria(key, value)
        +carregar_memoria(key) float
        +registrar_forense_async()
        +salvar_vitals()
    }

    class NerveNet {
        +senses: Rhopalium
        +balance: Statocyst
        +defense: Cnidocyte
        +persistence: Persistence
        +processar_instinto() dict
        +get_vitals() Vitals
    }

    NerveNet --> Rhopalium
    NerveNet --> Statocyst
    NerveNet --> Cnidocyte
    NerveNet --> Persistence
    Cnidocyte --> Persistence
```

---

## 🔄 Diagrama de Sequência: Fluxo de Defesa

```mermaid
sequenceDiagram
    participant Rho as Rhopalium
    participant NN as NerveNet
    participant Stat as Statocyst
    participant Cni as Cnidocyte
    participant DB as Persistence
    participant UI as Interface

    Note over NN: Estado: ZEN (Ciano)

    Rho->>NN: read_vitals() → pico 15MB/s
    NN->>Stat: analyze_network(15000)
    Stat-->>NN: anomaly=True, z=4.8

    NN->>Cni: avaliar_ameaca(anomaly=True)
    Cni->>DB: registrar_forense_async("SATURAÇÃO")
    Cni-->>NN: reflexo=True

    NN->>DB: salvar_vitals()
    NN-->>UI: Vitals(cor_body=red, cor_tentacles=red)
    UI->>UI: Corpo vermelho + Tentáculos brilhantes

    Note over NN: Cooldown 15 ciclos
    NN-->>UI: Vitals(cor_body=cyan, cor_tentacles=cyan)
```

---

## 🎨 Bioluminescência Semântica

| Domínio | Elemento | Escala de Cor | Significado |
|---|---|---|---|
| **Corpo** (Saúde Interna) | Campânula | Ciano → Amarelo → Vermelho | CPU/RAM stress |
| **Tentáculos** (Saúde Externa) | Tentáculos | Ciano → Roxo → Branco | Atividade de rede |
| **Oceano** | Partículas Phyto | Opacidade 0-100% | Download speed |
| **Oceano** | Partículas Zoo | Opacidade 0-100% | Upload speed |
| **Fundo** | Dirt overlay | Transparente → Marrom | RAM suja |

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | API REST assíncrona |
| **Frontend** | Streamlit | Dashboard reativo |
| **Sensores** | Psutil | Coleta de métricas OS |
| **Matemática** | Statistics (StdDev) | Z-Score para anomalias |
| **Persistência** | SQLite WAL | Memória neural + forense |
| **Container** | Docker Compose | Orquestração |
| **CI/CD** | GitHub Actions | Testes automatizados |

---

## 🔮 Roadmap Evolutivo

```mermaid
gantt
    title Jelly Evolution
    dateFormat  YYYY-MM
    section Core
    Monitoramento Reativo     :done, 2026-01, 1M
    Cérebro Híbrido           :done, 2026-01, 1M
    Memória Persistente       :done, 2026-02, 1M
    NerveNet Modular          :done, 2026-02, 1M
    section Future
    Honeypots Ativos          :active, 2026-03, 2M
    Smack Swarm               :2026-05, 3M
    SaaS Dashboard            :2026-08, 3M
```

### Fase 5: Imunidade de Rebanho (Smack Swarm)

Múltiplas Jellys conversando entre si:

```
[Edge Jelly 1] ---> [Queen API] <--- [Edge Jelly 2]
                        |
                   [Dashboard SaaS]
```

---

## 📂 Estrutura do Projeto

```
JellyV6/
├── core/                  # NerveNet (Rede Nervosa)
│   ├── __init__.py
│   ├── nervenet.py        # Orquestrador FastAPI
│   ├── rhopalium.py       # Sensores
│   ├── statocyst.py       # Z-Score + Stress
│   ├── cnidocyte.py       # Defesa + Forense
│   └── persistence.py     # SQLite WAL
├── interface/
│   └── app.py             # Streamlit
├── tests/
│   └── test_zscore.py
├── scripts/
│   └── predator.py
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

Projeto desenvolvido por **codeZ** como estudo de caso em Cybersecurity Edge e MLOps.
