# Jelly V6: Cyanea Capillata Digitalis 🪼

> *"A natureza não faz nada em vão."* - Aristóteles

## 🧬 Classificação Científica / Taxonomia Digital

| Categoria | Classificação Digital |
| :--- | :--- |
| **Nome Científico** | *Cyanea Capillata Digitalis* |
| **Variedade** | *Forensis Bordealis* (Subespécie de Borda) |
| **Referência Biológica** | *Cyanea capillata* (Água-viva Juba de Leão) |
| **Reino** | Software Libera (Open Source) |
| **Filo** | Data-Driven Intelligence |
| **Classe** | Secure Edge MLOps |
| **Ordem** | Anomalia Estatística |
| **Família** | Cyber-Physical Observability |
| **Gênero** | *Cyanea* (Sentinelas de tentáculos múltiplos) |
| **Espécie** | *C. Digitalis* |

---

## 📋 Prontuário do Espécime

*   **Habitat**: Ambientes de Borda (Edge Computing), redes descentralizadas e dispositivos móveis (IoT).
*   **Morfologia**: Composta por um **Cérebro** (FastAPI) e um **Corpo** (Streamlit), protegida por uma sequência de DNA específica (`X-JELLY-DNA`).
*   **Mecanismo de Defesa**: Arco reflexo baseado em **Z-Score**; injeta toxinas de log (SQLite) ao detectar flutuações anômalas no meio ambiente (Rede).
*   **Nutrição**: Fagocitose de pacotes de dados e métricas de telemetria em tempo real.

---

## 🧠 Anatomia do Sistema

O projeto é dividido em dois hemisférios que se comunicam via HTTP (Sinapses):

### 1. O Cérebro (`brain.py`) - Backend FastAPI
O centro nervoso. Não possui interface gráfica, apenas lógica pura.
*   **Neuroplasticidade (CPU)**: Utiliza médias móveis (`deque`) para "aprender" o que é uma carga normal. Se a CPU ficar em 50% por muito tempo, a Jelly se "acostuma" e para de alertar (Homeostase).
*   **Z-Score (Rede)**: Analisa o desvio padrão do tráfego. Detecta anomalias estatísticas (picos súbitos) que fogem do padrão comportamental, não apenas valores fixos.
*   **Memória de Longo Prazo**: SQLite com **WAL Mode** (Write-Ahead Logging) para garantir I/O não-bloqueante durante ataques.
*   **Nematocistos (Forense)**: Ao detectar perigo, dispara uma thread que executa `ss -tunap` (Socket Statistics), tirando um "snapshot" dos processos e IPs criminosos.

### 2. O Corpo (`app.py`) - Frontend Streamlit
A manifestação visual da saúde do sistema.
*   **Bioluminescência**: A cor da interface muda dinamicamente (**HSL**) baseada no Nível de Estresse (0-100).
    *   **Ciano/Roxo**: Zen (Baixa atividade).
    *   **Violeta**: Atividade Saudável.
    *   **Laranja**: Estresse Elevado.
    *   **Vermelho Sangue**: Pânico / Ataque Detectado.
*   **Tentáculos Visuais**: Partículas CSS que reagem à velocidade da rede.

---

## 🛡️ Mecanismos de Defesa & Metabolismo

A *Cyanea* implementa conceitos biológicos avançados aplicados à Cibersegurança:

| Conceito Biológico | Implementação Técnica | Função |
| :--- | :--- | :--- |
| **Homeostase** | Adaptive Stress Scoring | O sistema aprende o "novo normal" para evitar falso-positivos em hardware variado. |
| **Arco Reflexo** | Gatilhos Absolutos | Se CPU > 90% ou Rede > 80% do Máximo Histórico, o pânico é imediato (ignora adaptação). |
| **Nematocisto** | Forensic Logging | Captura automática de evidências (IPs, Portas, PIDs) no momento exato da anomalia. |
| **Fagocitose** | Garbage Collection | Limpeza de memória e identificação de processos parasitas. |
| **DNA** | Auth Header | Token `X-JELLY-DNA` necessário para qualquer interação com o cérebro. |

---

## 🚀 Instalação e Habitat

A *Cyanea* prefere ambientes Linux/WSL, mas sobrevive em Windows.

### 1. Preparar o Ecossistema
```bash
# Crie um ambiente virtual (Oceano Isolado)
python -m venv jelly_env
source jelly_env/bin/activate  # Linux/Mac
# jelly_env\Scripts\activate   # Windows

# Instale os nutrientes
pip install -r requirements.txt
```

*(Certifique-se de configurar o arquivo `.env` com seu `JELLY_DNA_SECRET`)*

### 2. Despertar o Cérebro (Terminal 1)
```bash
python brain.py
# O cérebro iniciará na porta 8000.
# Ele começará a criar o banco de dados 'jelly.db' e aprender seus limites de rede.
```

### 3. Materializar o Corpo (Terminal 2)
```bash
streamlit run app.py
# O corpo se conectará ao cérebro e começará a bioluminescência.
```

---

## 📂 Estrutura de Arquivos

*   `brain.py`: API, Lógica Híbrida, Banco de Dados e Forense.
*   `app.py`: Interface Reativa, CSS Biomimético e Cliente HTTP.
*   `jelly.db`: Memória persistente (Histórico Vital + Evidências Forenses).
*   `.env`: Variáveis de ambiente e Segredos Genéticos.

---

## 🔮 Roadmap Evolutivo

- [x] **Fase 1**: Monitoramento Reativo (Cores).
- [x] **Fase 2**: Cérebro Híbrido (Estatística + Adaptação).
- [x] **Fase 3**: Memória Persistente e Forense.
- [ ] **Fase 4**: Honeypots Ativos (Portas Falsas).
- [ ] **Fase 5**: Imunidade de Rebanho (Múltiplas Jellys conversando).
