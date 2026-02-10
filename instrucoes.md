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

## 8. 🚀 Deploy no GitHub (Seguro)

Antes de subir, limpe os arquivos antigos e garanta que segredos não vazem.

### Passo 1: Limpeza (Faxina)
```bash
# Remove versões antigas (Lixo)
rm brain.py app.py app_top.py app_backup.py package-lock.json

# Garante que arquivos sensíveis não estão trackeados
git rm --cached .env jelly.db -f || true
```

### Passo 2: Commit & Push
```bash
# Adiciona tudo (respeitando o .gitignore)
git add .

# Commit final
git commit -m "feat: JellyV6 NerveNet Architecture Release 🪼"

# Conecta ao seu repo remoto (Crie um repo vazio no GitHub primeiro!)
git remote add origin https://github.com/SEU_USUARIO/JellyV6.git
git branch -M main
git push -u origin main
```

> **Nota de Segurança**: O arquivo `.gitignore` já está configurado para bloquear `.env` (senhas) e `jelly.db` (histórico sensível). Pode subir sem medo!