Jelly V6.1 "Sorria e Acene" - Release Walkthrough
🌟 O Que Mudou?
A versão 6.1 foca na filosofia de defesa "Judo": usar a força do atacante contra ele mesmo, sem derrubar o servidor.

1. Defesa em Camadas (Escalada)
Nível	Pressão	Ação	Efeito
🟢	0-50	ALLOW	Acesso normal
🟡	50-100	ACTIVE_PROBE	Injeção de micro-latência
🟠	100-200	CONTRACT	Lentidão proposital (2s delay)
🔴	200-400	TARPIT	Retenção de conexão (5s sleep)
⚫	400+	BLACKHOLE	NOVO: Drop silencioso (204 No Content). Atacante some no vácuo.
☠️	1000+	RUPTURA	Auto-reinício (Turritopsis) apenas em emergência extrema.
2. "Sorria e Acene" (Honeypot + Blackhole)
Cenário: Atacante acessa /admin.
Reação Antiga: RUPTURA imediata (servidor morria).
Reação V6.1:
Retorna 200 OK falso (Sorria 😊)
Marca IP com 500 atm (Blacklist)
Próximos requests recebem 204 No Content vazio (Acene 👋)
Servidor continua vivo e operante.
3. Observabilidade Forense
Toda ação de BLACKHOLE agora grava um snapshot no SQLite:

sql
SELECT * FROM forensic_events WHERE trigger_type = 'BLACKHOLE';
Contém: Timestamp, IP, Pressão e Snapshot TCP (ss -tunap).

4. Controle Manual
Bata o ponto no Dashboard:

Botão de Pânico 🔴: Força RUPTURA manual se você vir algo estranho.
HUD Limpo: Removemos as métricas sujas, foco no estado biológico.
🧪 Como Validar
Simulação completa de um ataque real:

bash
python tests/test_sorria_e_acene.py
Resultado esperado: 🏆 RESULTADO: SORRIA E ACENE FUNCIONOU!

"A natureza não faz nada em vão. Ela fez a água-viva ser simples, mas letal." 🪼