# 🪼 Jelly Nervous System (JNS) - Architecture

> *"A natureza não faz nada em vão."* - Aristóteles

A **Jelly** é um Sistema de Detecção de Intrusão (IDS) biomimético que utiliza conceitos de "Calm Technology" para monitorar a saúde de servidores e dispositivos Edge. Diferente de logs tradicionais, a Jelly traduz métricas de estresse em bioluminescência (cores HSL) e reage a ameaças disparando contramedidas defensivas (Nematocistos).

---

## 🏗️ Diagrama de Arquitetura

```mermaid
graph TD
    User((Usuário/Admin))
    Hacker((Atacante))

    subgraph "Jelly Ecosystem - Docker"
        UI[Frontend: Streamlit<br/>Porta 8501]
        API[Backend: FastAPI<br/>Porta 8000]
        DB[(SQLite WAL<br/>jelly.db)]
    end

    Discord[Webhook Discord]
    OS[Sistema Operacional<br/>psutil]

    User -->|Visualiza| UI
    Hacker -.->|DDoS/Scan| OS
    UI -->|HTTP /vitals| API
    API -->|Métricas| OS
    API -->|Persiste| DB
    API -.->|Alerta| Discord
```

---

## 📋 Requisitos Funcionais

| ID | Requisito | Status |
|---|---|---|
| **RF001** | Monitorar CPU, RAM, Disco e Rede via psutil a cada 100ms | ✅ |
| **RF002** | Detectar anomalias via Z-Score (threshold > 3.0) | ✅ |
| **RF003** | Disparar Nematocisto (log forense + block IP) em anomalias críticas | ✅ |
| **RF004** | Interface biomimética com cores HSL dinâmicas (Ciano → Vermelho) | ✅ |
| **RF005** | Persistir histórico vital e eventos forenses em SQLite WAL | ✅ |
| **RF006** | Health check endpoint para Docker/Kubernetes | ✅ |

---

## 📋 Requisitos Não-Funcionais

| ID | Requisito | Implementação |
|---|---|---|
| **RNF001** | CPU < 5% em repouso | Loop otimizado + WAL |
| **RNF002** | Segurança: shell=False, sanitização de inputs | subprocess seguro |
| **RNF003** | Portabilidade: Linux/WSL/Docker | Container multi-arch |
| **RNF004** | Graceful shutdown em SIGTERM | Signal handler |

---

## 🧬 Diagrama de Classes

```mermaid
classDiagram
    class BrainState {
        -deque cpu_history
        -deque net_history
        -float max_down_kbps
        -int nematocisto_ativo
        +monitor_vitals()
    }

    class Vitals {
        +float cpu
        +float ram
        +float stress_score
        +str status_text
        +bool defense_mode
    }

    class FastAPI {
        +get_vitals() Vitals
        +health_check() dict
        +feed_jelly() dict
    }

    class Forensic {
        +registrar_evento_forense()
        +ss_tunap_snapshot()
    }

    FastAPI --> BrainState : uses
    FastAPI --> Vitals : returns
    BrainState --> Forensic : triggers
```

---

## 🔄 Diagrama de Sequência: Fluxo de Defesa

```mermaid
sequenceDiagram
    participant Net as Network Interface
    participant Brain as Jelly Brain
    participant Nema as Nematocyst
    participant DB as SQLite
    participant UI as Dashboard

    Note over Brain: Estado: ZEN (Ciano)

    Net->>Brain: Pico de Tráfego (15MB/s)
    Brain->>Brain: Calcula Z-Score = 4.8
    
    Brain->>Nema: Pressurizar()
    Nema->>Net: Captura ss -tunap
    Nema->>DB: Salva forensic_event
    
    Brain->>UI: Update: PANIC
    UI->>UI: Muda cor para Vermelho
    
    Note over Brain: Cooldown 15 ciclos
    Brain->>UI: Update: ZEN
```

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia | Função |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | API REST assíncrona |
| **Frontend** | Streamlit | Dashboard reativo |
| **Sensores** | Psutil | Coleta de métricas OS |
| **Matemática** | Statistics (StdDev) | Z-Score para anomalias |
| **Persistência** | SQLite WAL | Memória neural + forense |
| **Container** | Docker Compose | Orquestração brain + body |
| **CI/CD** | GitHub Actions | Testes automatizados |

---

## 🔮 Roadmap Evolutivo

```mermaid
gantt
    title Jelly Evolution
    dateFormat  YYYY-MM
    section Core
    Monitoramento Reativo     :done, 2026-01, 1M
    Cérebro Híbrido (Z-Score) :done, 2026-01, 1M
    Memória Persistente       :done, 2026-02, 1M
    section Future
    Honeypots Ativos          :active, 2026-03, 2M
    Smack Swarm (Multi-Jelly) :2026-05, 3M
    SaaS Dashboard Central    :2026-08, 3M
```

### Fase 5: Imunidade de Rebanho (Smack Swarm)

A evolução natural do projeto é criar múltiplas Jellys conversando entre si:

- **Jellys Edge**: Rodam em cada dispositivo (Poco X4, servidores, IoT)
- **Jelly Queen**: Dashboard central que agrega dados de todas as Jellys
- **Protocolo Smack**: Jellys compartilham threats detectados (like feromônios)

```
[Edge Jelly 1] ---> [Queen API] <--- [Edge Jelly 2]
                        |
                   [Dashboard SaaS]
```

---

## 📂 Estrutura do Projeto

```
JellyV6/
├── brain.py           # Backend FastAPI + Lógica de detecção
├── app.py             # Frontend Streamlit + UI biomimética
├── jelly.db           # Memória persistente (SQLite WAL)
├── .env               # Segredos (JELLY_DNA_SECRET)
├── Dockerfile         # Container image
├── docker-compose.yml # Orquestração
├── tests/
│   └── test_zscore.py # Testes automatizados
└── .github/
    └── workflows/
        └── ci.yml     # GitHub Actions CI
```

---

Projeto desenvolvido por **codeZ** como estudo de caso em Cybersecurity Edge e MLOps.
