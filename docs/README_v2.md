# Jelly V6: Cyanea Capillata Digitalis 🪼

[![CI](https://github.com/codeZ-coder/JellyV6/actions/workflows/ci.yml/badge.svg)](https://github.com/codeZ-coder/JellyV6/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20WSL%20%7C%20Docker-lightgrey)](./docker-compose.yml)
[![Status](https://img.shields.io/badge/status-dev-orange)](.)

> *"A natureza não faz nada em vão."* — Aristóteles

---

### ⚡ TL;DR (Resumo Técnico)
**Jelly V6** é um agente de **Observabilidade de Sistemas** e defesa cibernética leve. Atualmente desenvolvido em ambiente **Linux (WSL/Docker)**, ele monitora recursos (CPU/RAM), detecta anomalias via Z-Score (estatística) e oferece uma interface visual interativa inspirada em sistemas biológicos.

*Meta futura: Portabilidade para dispositivos de borda (Android/Termux) atuando como Relays de defesa.*

---

### 📑 Sumário
- [Taxonomia Digital](#-classificação-científica--taxonomia-digital)
- [Arquitetura (NerveNet)](#️-arquitetura-nervenet)
- [Smack SaaS (Defesa Cooperativa)](#-smack-saas-a-defesa-cooperativa)
- [Bioluminescência (Status)](#-bioluminescência-system-status)
- [Instalação (Quick Start)](#-quick-start)
- [Segurança & Ética](#-segurança-e-uso-responsável)
- [Roadmap](#-roadmap-evolutivo)

---

## 🧬 Classificação Científica / Taxonomia Digital

| Categoria | Classificação Digital |
| :--- | :--- |
| **Nome Científico** | *Cyanea Capillata Digitalis* |
| **Variedade** | *Forensis Laboratorial* (Ambiente Linux) |
| **Filo** | Data-Driven Intelligence |
| **Classe** | System Resource Observability |
| **Ordem** | Anomalia Estatística |
| **Família** | Linux-Based Systems |

---

## 🏗️ Arquitetura NerveNet

O sistema imita o sistema nervoso descentralizado de um cnidário:

```mermaid
graph LR
    A[Linux Kernel] -->|psutil| R[Rhopalium<br/>Sensores]
    R --> N[NerveNet<br/>FastAPI]
    N --> S[Statocyst<br/>Z-Score]
    N --> C[Cnidocyte<br/>Defesa]
    N --> P[Persistence<br/>SQLite WAL]
    N -->|HTTP /vitals| I[Interface<br/>Streamlit]
```

### 🧠 Anatomia do Sistema (Módulos)

| Módulo | Arquivo | Responsabilidade |
| :--- | :--- | :--- |
| **NerveNet** | `core/nervenet.py` | Orquestrador: API FastAPI + Endpoints |
| **Rhopalium** | `core/rhopalium.py` | Sentidos: Coleta de métricas do OS (psutil) |
| **Statocyst** | `core/statocyst.py` | Equilíbrio: Cálculo de Z-Score e Stress |
| **Cnidocyte** | `core/cnidocyte.py` | Defesa: Mecanismo de resposta e forense |
| **Persistence** | `core/persistence.py` | Memória: Banco de dados SQLite (WAL Mode) |
| **Interface** | `interface/app.py` | Corpo: Dashboard interativo em Streamlit |

---

## 🦈 Smack SaaS: A Defesa Cooperativa

> *"Nenhum de nós é tão inteligente quanto todos nós."* — Provérbio Japonês

Em biologia, um grupo de águas-vivas é chamado de **Smack**. Na JellyV6, o Smack é a implementação de nossa **Defesa Cooperativa Distribuída**.

Diferente de Botnets tradicionais que operam em hierarquia rígida (Master/Slave), o Jelly Smack opera como uma rede descentralizada (**Mesh Network**).

### 🛡️ O Conceito de Firewall Cooperativo

Inspirado na arquitetura de enxame, múltiplas instâncias da JellyV6 comunicam-se entre si para compartilhar inteligência de ameaças em tempo real.

1.  **Relays (Éfiras):** Instâncias leves (ex: Android/Termux) atuam como sensores de borda. Se detectam um padrão de ataque (ex: port scanning), geram uma assinatura.
2.  **O Coelenteron (Túnel Seguro):** A comunicação entre os nós trafega por uma VPN criptografada (WireGuard/mTLS), garantindo que apenas Jellys autenticadas compartilhem dados.
3.  **Imunidade de Rebanho:** Se um nó detecta um IP malicioso, ele "vacina" o restante do Smack. O bloqueio é propagado instantaneamente para todos os outros nós, criando bolsões de segurança dinâmicos.

---

## 🔵 Bioluminescência (System Status)

O sistema comunica seu estado de saúde (Health Check) através de padrões de cores:

| Componente | 🟢 Homeostase (Normal) | 🟡 Alerta (Stress) | 🔴 Pânico (Crítico) |
| :--- | :---: | :---: | :---: |
| **Corpo (Soma)**<br>*(CPU/RAM)* | **Ciano**<br>`Eficiente` | **Amarelo**<br>`Processamento Intenso` | **Vermelho**<br>`Sobrecarga` |
| **Tentáculos**<br>*(Rede)* | **Ciano**<br>`Estável` | **Roxo**<br>`Congestionamento` | **Branco**<br>`Perda de Sinal/Ataque` |

---

## 🚀 Quick Start

### 1. Configuração do DNA (.env)
⚠️ **Nunca comite suas chaves reais.** Crie um arquivo `.env` baseado no exemplo abaixo:

```bash
# .env.example (Copie este conteúdo para .env)
JELLY_DNA_SECRET=changeme_dev_key
JELLY_LOG_LEVEL=INFO
JELLY_DB_PATH=jelly.db
```

### 2. Rodando com Docker (Recomendado)

```bash
git clone https://github.com/codeZ-coder/JellyV6.git
cd JellyV6
docker compose up --build -d

# 🧠 Brain API: http://localhost:8000/docs
# 🪼 Dashboard: http://localhost:8501
```

### 3. Rodando Localmente (Linux/WSL)

```bash
# Configurar ambiente virtual
python3 -m venv jelly_env
source jelly_env/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar (em terminais separados)
# Terminal A:
uvicorn core.nervenet:app --host 0.0.0.0 --port 8000

# Terminal B:
streamlit run interface/app.py
```

---

## 🧪 Testes & Stress

```bash
# Rodar testes unitários
pytest tests/ -v

# ⚠️ Simulação de Ataque (Predator)
# Simula um DDoS local para testar o Z-Score
python scripts/predator.py
```

---

## 🔒 Segurança e Uso Responsável

### 🛡️ Boas Práticas
*   Mantenha o arquivo `.env` no seu `.gitignore`.
*   Em produção, altere a `JELLY_DNA_SECRET` para um hash forte.

### ⚠️ Aviso Legal
> Esta ferramenta foi desenvolvida estritamente para fins de testes em ambientes controlados (Localhost/WSL). O uso não autorizado contra alvos de terceiros é ilegal e antiético.

---

## 🔮 Roadmap Evolutivo

**Visão de Longo Prazo: O Ecossistema Smack**
> *"A experiência de um indivíduo fortalece a sobrevivência da espécie."*

- [x] **Fase 1**: Monitoramento de Recursos Linux (WSL/Server)
- [x] **Fase 2**: Refinamento do Z-Score e Persistência Forense
- [x] **Fase 3**: Modularização da Arquitetura (NerveNet)
- [ ] **Fase 4**: Adaptação para Android (Termux) atuando como Relays (Éfiras)
- [ ] **Fase 5**: Implementação do Smack SaaS (Gossip Protocol via Coelenteron/VPN)
- [ ] **Fase 6**: Reescrever o Núcleo (NerveNet) em **Go** ou **Rust** para performance "Bare Metal" 🚀

---

<div align="center">
  <b>Desenvolvido por codeZ 🪼</b><br>
  <i>Secure Edge MLOps • Bio-Inspired Cybersecurity</i>
</div>
