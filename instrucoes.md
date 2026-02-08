Guia de Execução: Jelly V6 (Architecture Refactor)
A transição para arquitetura Client-Server foi concluída! Agora a Jelly tem um Cérebro independente.

1. Instalar Dependências
Atualizamos o 
requirements.txt
. Instale as novas libs:

bash
pip install -r requirements.txt
(Ou instale manualmente: pip install fastapi uvicorn requests)

2. Iniciar o Cérebro (Server)
Este processo deve rodar continuamente em background. Ele protege o sistema mesmo sem UI.

bash
# Executar no Terminal 1
--> uvicorn brain:app --reload --host 0.0.0.0 --port 8000
Você verá logs como: Uvicorn running on http://0.0.0.0:8000.

3. Iniciar o Corpo (Client)
A interface visual agora é apenas um visualizador.

bash
# Executar no Terminal 2
--> streamlit run app.py
Como Testar
Conexão: Abra a UI. Se ela mostrar "CONEXÃO PERDIDA COM CÉREBRO", verifique se o passo 2 está rodando.
Persistência: Feche a aba do navegador (ou pare o terminal 2). O Terminal 1 (
brain.py
) deve continuar monitorando sem erros.
Stress: Rode um teste de stress de CPU e veja a Jelly mudar de cor.

------------------------------------------------- v2

Jelly V6 Biológico (Guia de Sobrevivência)
A Jelly V6 evoluiu para um organismo Client-Server Seguro, Híbrido e Forense. Aqui está o passo a passo para "ligar" sua nova vida digital.

0. O Grande Reset (Importante!) ☢️
Como o Cérebro mudou sua estrutura neural (novas tabelas SQL), precisamos limpar a memória antiga. No terminal WSL:

bash
rm jelly.db
(Se não fizer isso, o cérebro vai travar tentando ler memórias incompatíveis)

1. Subindo o Cérebro (Server) 🧠
O cérebro agora roda em uvicorn com suporte a multithreading para não engasgar durante ataques. No Terminal 1:

bash
uvicorn brain:app --host 0.0.0.0 --port 8000 --reload
Você verá:

🧠 Memória Carregada: Recorde de Rede = 4.9 MB/s (Começa humilde)

2. Subindo o Corpo (Frontend) 🪼
A interface agora é leve, passiva e biomimética. No Terminal 2:

bash
streamlit run app.py
Acesse no navegador (geralmente http://localhost:8501).

3. O Que Observar (Checklist de Vida) ✅
🎨 A. Biomimética Visual (HSL)
Estado Zen: Se seu PC estiver calmo, a Jelly estará Ciano (Azul Piscina) e pulsando devagar (5s).
Estresse Emocional: Abra 10 abas do Chrome ou compile algo pesado.
O Cérebro calcula o Stress Score.
A Jelly mudará suavemente para Roxo -> Magenta -> Vermelho.
A pulsação vai acelerar (taquicardia visual).
📈 B. Aprendizado de Rede (Neuroplasticidade)
Teste de Campo: Faça um download pesado ou rode um SpeedTest.
O Aprendizado: O Cérebro vai detectar que o fluxo aumentou.
Olhe o log do terminal do Cérebro: Ele não vai gritar "Pânico" se for só um download rápido. Ele vai aprender que você aguenta essa velocidade.
O novo max_down_record será salvo no banco.
🕵️‍♂️ C. O Ferrão Forense (Segurança)
Simulação de Ataque: Se você conseguir saturar sua rede acima de 80% do novo recorde (difícil, mas possível):
A Jelly ficará Vermelha Sólida.
O HUD mostrará: ⚠️ DEFESA: SATURAÇÃO.
Nos Bastidores: O Cérebro executará ss -tunap silenciosamente e salvará o snapshot na tabela forensic_events.
🖥️ D. HUD Secure Edge
No topo da tela, verifique o HUD estilo "Cyberpunk Bio":
Status: Zen / Adaptado / Estresse
Info: DNA Verified | RAM | Stress %
Instance: O nome do seu host (ex: DESKTOP-XYZ ou Ubuntu).
4. Comandos de Manutenção (SQL)
Para ver o que a Jelly andou gravando:

Ver eventos forenses:

bash
sqlite3 jelly.db "SELECT timestamp, trigger_type, details FROM forensic_events;"
Ver o Recorde de Rede atual:

bash
sqlite3 jelly.db "SELECT * FROM neuro_memory;"
Divirta-se com seu novo organismo digital! 🪼🚀