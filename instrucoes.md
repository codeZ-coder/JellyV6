# Guia de Execução: Jelly V6 (NerveNet Architecture)

A Jelly V6 foi refatorada para uma arquitetura modular **NerveNet** (Rede Nervosa Difusa).

## 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

## 2. Iniciar a NerveNet (Server) 🧠

```bash
# Terminal 1
uvicorn core.nervenet:app --host 0.0.0.0 --port 8000
```

Você verá: `Memória Carregada: Recorde de Rede = X MB/s`

## 3. Iniciar a Interface (Client) 🪼

```bash
# Terminal 2
streamlit run interface/app.py
```

Acesse no navegador: http://localhost:8501

## 4. Com Docker (Alternativo)

```bash
docker-compose up -d
# Brain: http://localhost:8000/docs
# Body:  http://localhost:8501
```

## 5. Como Testar

- **Conexão**: Abra a UI. Se mostrar "SINAPSE PERDIDA", verifique se o passo 2 está rodando.
- **Stress**: Rode um teste de stress de CPU e veja o **corpo** da Jelly mudar de cor.
- **Rede**: Rode `python scripts/predator.py` e veja os **tentáculos** mudarem de cor.
- **Cores**: Corpo = saúde interna (CPU/RAM). Tentáculos = saúde externa (Rede).

## 6. Testes Automatizados

```bash
pytest tests/ -v
```

## 7. Consultar Banco

```bash
# Ver eventos forenses
sqlite3 jelly.db "SELECT timestamp, trigger_type, details FROM forensic_events;"

# Ver recorde de rede
sqlite3 jelly.db "SELECT * FROM neuro_memory;"
```