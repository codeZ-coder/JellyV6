# Guia de Execucao: Jelly V6 (NerveNet Architecture)

A Jelly V6 opera como um organismo modular com **NerveNet** (Rede Nervosa Difusa).
Backend (Brain/FastAPI) e Frontend (Body/Streamlit) rodam separados.

---

## 1. Configurar Ambiente

```bash
# Criar ambiente virtual
python3 -m venv jelly_env
source jelly_env/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configurar Variaveis de Ambiente

```bash
# Copiar o exemplo e editar
cp .env.example .env
# Edite o .env com uma chave forte para JELLY_DNA_SECRET
```

## 3. Iniciar a NerveNet (Backend)

```bash
# Terminal 1
uvicorn core.nervenet:app --host 0.0.0.0 --port 8000
```

Voce vera: `Memoria Carregada: Recorde de Rede = X MB/s`

Acesse a documentacao da API em: http://localhost:8000/docs

## 4. Iniciar a Interface (Frontend)

```bash
# Terminal 2
streamlit run interface/app.py
```

Acesse no navegador: http://localhost:8501

## 5. Com Docker (Alternativo)

```bash
docker compose up --build -d

# Brain API: http://localhost:8000/docs
# Dashboard: http://localhost:8501
```

Nota: O Docker Compose ja configura `BRAIN_URL` para comunicacao entre containers.

---

## 6. Testes Automatizados

```bash
# Rodar todos os testes
pytest tests/ -v
```

Os testes cobrem:
- `test_zscore.py`: Statocyst (Z-Score), Cnidocyte (Defesa), Stress de CPU
- `test_osmotic.py`: Chemoreceptor (Entropia Shannon), OsmoticMembrane (Pressao/Buffer)

## 7. Testes de Stress (Predator V2)

Com o backend rodando (passo 3), abra outro terminal:

```bash
# Testar deteccao de bots (baixa entropia, alta frequencia)
python scripts/predator.py --mode bot

# Testar falsos positivos (alta entropia, delay humano)
python scripts/predator.py --mode human

# Testar Z-Score de rede (download volumetrico)
python scripts/predator.py --mode ddos
```

## 8. Consultar Banco

```bash
# Ver eventos forenses
sqlite3 jelly.db "SELECT timestamp, trigger_type, details FROM forensic_events;"

# Ver recorde de rede (memoria neural)
sqlite3 jelly.db "SELECT * FROM neuro_memory;"
```

---

## 9. Deploy no GitHub

```bash
# Verificar que arquivos sensiveis nao estao tracked
git status

# Adicionar tudo (respeitando .gitignore)
git add .
git commit -m "feat: JellyV6 NerveNet MVP"

# Conectar ao repo remoto (crie um repo vazio no GitHub primeiro)
git remote add origin https://github.com/SEU_USUARIO/JellyV6.git
git branch -M main
git push -u origin main
```

Nota de Seguranca: O `.gitignore` bloqueia `.env` (senhas), `*.db` (historico) e `assets/toxin.gz` (payload). Pode subir sem medo.

---

## Estrutura do Projeto

```
JellyV6/
  core/              # Backend (Brain)
    nervenet.py      # Orquestrador FastAPI
    rhopalium.py     # Sensores (psutil)
    statocyst.py     # Z-Score e Stress
    cnidocyte.py     # Defesa e Forense
    membrane.py      # Pressao Osmotica por IP
    chemo.py         # Entropia de Shannon
    persistence.py   # SQLite WAL
  interface/
    app.py           # Frontend Streamlit
  scripts/
    predator.py      # Simulador de ataque
  prototypes/        # Experimentos e POCs
  tests/             # Testes automatizados
  docs/              # Documentacao
  .env.example       # Template de variaveis
  docker-compose.yml # Orquestracao Docker
  requirements.txt   # Dependencias Python
```
