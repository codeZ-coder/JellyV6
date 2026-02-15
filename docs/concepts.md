# Conceitos Técnicos: Jelly V6 Ecosystem

## O Smack (Cardume de Águas-vivas)
**Definição:** Conjunto de instâncias da JellyV6 operando em uníssono. Em vez de uma arquitetura centralizada (Master-Slave), opera como uma **Mesh Network** descentralizada.

### 🛡️ Firewall Cooperativo Distribuído
O conceito central é a **Imunidade de Rebanho**. Se um nó detecta uma ameaça, ele compartilha a inteligência ("vacina") com os outros nós. A defesa deixa de ser um perímetro estático para se tornar um organismo vivo.
- **Detecção Local:** Cada Jelly processa seus próprios dados e gera alertas.
- **Propagação Global:** Alertas confirmados (via consenso ou heurística forte) são transmitidos aos pares.
- **Resposta Sincronizada:** O bloqueio de um IP ou padrão de ataque é aplicado em todo o Smack simultaneamente.

---

## Componentes Biológicos e Metáforas Técnicas

### 1. Éfiras (Relays)
**Conceito Biológico:** O estágio larval/jovem de uma medusa.
**Implementação Técnica:** Instâncias leves (Low Resource) rodando em dispositivos de borda, como smartphones Android via Termux ou Raspberry Pi.
- **Função:** Atuam como sensores avançados e "Honeypots Ativos".
- **Vantagem:** Detectam varreduras de rede e tentativas de intrusão antes que elas cheguem aos servidores principais (Medusas Adultas).
- **Protocolo:** Enviam apenas os `hashes` de assinaturas de ataque para economizar banda e bateria.

### 2. Coelenteron (A Cavidade Gástrica)
**Conceito Biológico:** A cavidade onde ocorre a digestão e circulação de nutrientes.
**Implementação Técnica:** Rede Privada Virtual (VPN) ou Túnel Criptografado (WireGuard/mTLS) que conecta todos os nós do Smack.
- **Segurança (Digestion):**
    - **Tunelamento:** Encapsula o tráfego NerveNet dentro de pacotes seguros.
    - **Criptografia:** Garante confidencialidade (IPSec/ChaCha20).
    - **Integridade:** Protege contra manipulação de mensagens.
- **Autenticação (DNA Check):** Apenas nós com o certificado digital correto (assinado pela CA do Smack) podem entrar no túnel. Isso previne ataques de Man-in-the-Middle e IP Spoofing.

### 3. Jelly Mutante (Ameaça Interna)
**Conceito Biológico:** Um organismo doente ou parasitado dentro da colônia.
**Implementação Técnica:** Um nó comprometido (Rogue Node) ou um Insider Threat.
- **Riscos:**
    - DoS Interno (Esgotamento de recursos).
    - Envenenamento de rotas/alertas (ARP/BGP Poisoning).
    - Exfiltração de dados (Vazamento via canal criptografado).

---

## Mecanismos de Defesa (Imunologia Digital)

### Apoptose Remota (Revogação de Confiança)
Se uma Jelly for identificada como comprometida (ex: comportamento anômalo persistente ou violação de integridade do binário):
1.  O sistema emite um sinal de **Revogação de Certificado**.
2.  A Jelly infectada é expulsa do Coelenteron (a VPN recusa a conexão).
3.  Ela é isolada criptograficamente, incapaz de enviar ou receber dados do Smack.

### Reação Alérgica (Isolamento de Rede)
Filtros de firewall (Mucosa) são atualizados em todos os nós saudáveis para rejeitar especificamente o tráfego vindo da Jelly doente.
- **Quarentena:** O nó infectado pode ser movido para uma VLAN isolada (Sandbox) para análise forense posterior sem risco de propagação lateral.

---

## Homeostase Regulatória (Conformidade Ativa)
**Conceito Biológico:** O organismo mantém o equilíbrio interno e rejeita partículas estranhas (conformidade com o DNA).
**Implementação Técnica:** A JellyV6 evolui de um agente de defesa para um **Agente de Conformidade**, impondo políticas de segurança ativamente.

### 1. Módulo Nematocyst (O Auditor)
Extensão do Cnidocyte focada em auditoria interna e "higiene" do servidor.
- **Verificação de Hardening:** Garante que o hospedeiro segue as "Regras da Casa".
    - *Exemplo:* Verifica se o login root via SSH está desabilitado.
- **Monitoramento de Integridade (Tripwire):**
    - A Jelly calcula o hash de arquivos críticos (`/etc/passwd`, `nginx.conf`) no nascimento.
    - Se o hash mudar sem autorização (ticket de mudança), a Jelly reverte o arquivo ou isola o processo.

### 2. Política Bio-Codificada (`policy.yaml`)
As regras de segurança são tratadas como instruções genéticas que devem ser obedecidas.

```yaml
policy_name: "Protocolo Imune Padrão"
rules:
  - id: "SSH_ROOT"
    check: "grep 'PermitRootLogin no' /etc/ssh/sshd_config"
    action: "alert_and_block"
    biological_reason: "Evitar parasitas no núcleo"
  - id: "WEAK_PASSWORDS"
    check: "check_password_complexity"
    action: "force_reset"
    biological_reason: "Membrana celular fraca"
```

### 3. Relatórios de Auditoria (Memória da Colônia)
O banco de dados `jelly.db` passa a armazenar "Logs de Saúde" para fins de conformidade (PCI-DSS, ISO 27001).
- *Exemplo:* "No dia 12/10, o servidor teve 100% de conformidade com a política de senhas."

---

## Roadmap Técnico da Implementação

1.  **Fase 1 (Atual):** Monitoramento local (Linux/WSL).
2.  **Fase 2 (Próxima):** Implementação básica de Relays em Android (Termux) reportando para um servidor central.

---

## Análise da Tríade CID (Confidencialidade, Integridade, Disponibilidade)
Para se tornar uma suíte completa de segurança (baseada em Nakamura), a JellyV6 deve cobrir todas as camadas da tríade.

| Camada | Diagnóstico Atual | Metáfora Biológica | Solução Técnica Planejada |
| :--- | :--- | :--- | :--- |
| **Confidencialidade** | ⚠️ Parcial. Dados em texto claro no `jelly.db`. | **Coelenteron** (Digestão Interna) | • Criptografia do SQLite (SQLCipher).<br>• Túnel TLS/VPN para comunicação NerveNet. |
| **Integridade** | ❌ Ausente. Não detecta alteração de binários. | **Mucosa / Immunity** (Rejeição) | • Monitoramento de Integridade de Arquivos (FIM).<br>• Verificação de assinatura do código (Tripwire). |
| **Disponibilidade** | ✅ Forte. Monitoramento de recursos e defesa ativa. | **Transdifferentiation** (Regeneração) | • Watchdog para reinício automático de processos.<br>• Defesa ativa contra DoS (bloqueio de IPs). |

---

## Matemática e História do Código (Inspiração: Simon Singh Anthology)
A "alma matemática" que justifica a eficácia biológica da JellyV6.

### 1. Statocyst Avançado: Análise de Frequência (Al-Kindi)
- **Conceito Histórico:** Al-Kindi quebrou cifras analisando a frequência de letras, não a mensagem inteira.
- **Aplicação JellyV6:** Monitorar a **frequência de Syscalls** (chamadas de sistema).
    - *Antes:* Picos de CPU.
    - *Agora:* Mudança no padrão de chamadas `read()`/`write()` indica anomalia, mesmo com CPU baixa (ataques "Low and Slow").

### 2. Módulo Chromatophore (A Cifra de Vigenère/Enigma)
- **Conceito Histórico:** A máquina Enigma rotacionava seus rotores a cada tecla, mudando a cifra. Cefalópodes mudam de cor (cromatóforos) para se camuflar.
- **Nova Funcionalidade:** **Port Hopping / Key Rotation**.
    - A Jelly altera periodicamente as portas de escuta do painel de controle ou as chaves de sessão do Coelenteron. O atacante perde o alvo se demorar a atacar.

### 3. Rhopalium Cósmico: O "Hiss" de Penzias & Wilson
- **Conceito Histórico:** A descoberta da Radiação Cósmica de Fundo (CMB) exigiu "limpar os pombos" da antena para ouvir o ruído isotrópico do universo.
- **Aplicação JellyV6:** O Rhopalium nas **Éfiras** (Android) filtra o ruído de rede:
    - **Limpeza dos Pombos (Whitelisting):** Filtrar ativamente o "material dielétrico branco" (broadcasts, updates legítimos) para ouvir o sinal real.
    - **Temperatura Basal (Low-and-Slow):** Medir a entropia mínima da rede (ex: 3 Kelvin). Um aumento sutil para 3.5K (não um pico) denota um ataque furtivo.
    - **Verificação de Isotropia:** O ruído de fundo normal vem de todas as direções (isotrópico). Se um sinal se torna direcional (vem de um único IP), é uma anomalia (Scanning/Beaconing).

### 4. Coelenteron: Chaves Assimétricas (Diffie-Hellman/RSA)
- **Conceito Histórico:** O uso de chaves públicas/privadas resolvia o problema da distribuição de chaves (Alice e Bob).
- **Refinamento JellyV6:** Cada Jelly do Smack nasce com um par de chaves (DNA Único). O Coelenteron usa autenticação mútua rigorosa, garantindo a identidade matemática de cada membro do cardume.

### 5. Módulo Cnidocil ou Statocyst Quântico (Dinheiro Quântico de Wiesner)
- **Conceito Histórico:** Informação que se destrói ao ser "observada" (lida), garantindo incopiabilidade.
- **Aplicação JellyV6:** **Canary Files** (Arquivos de Armadilha).
    - Arquivos falsos colocados no sistema. Se um atacante (ou ransomware) tentar ler ou criptografar esse arquivo ("observar"), a Jelly detecta a alteração de estado instantaneamente e dispara o alarme.

---

## Ciclo de Vida Cnidário (Escalabilidade Biológica)
Para resolver o dilema "Batata vs Servidor" (Segurança vs Complexidade), o sistema implementa **Polimorfismo**. O mesmo código pode rodar em 3 modos distintos, definidos por `JELLY_LIFE_STAGE`.

### 1. Estágio Pólipo (Mode: `POLYP`) 🥔
- **Biologia:** Sissil, fixo no chão, consome pouca energia.
- **Hardware:** "Batata" (PC antigo, IoT, Script .bat).
- **Funcionalidade:**
    - Apenas Rhopalium (Monitoramento passivo) e Cnidocyte simples (Bloqueio de IP).
    - **Sem:** API, Dashboard, Banco de Dados pesado.
    - **Output:** Logs de texto ou envio para uma Medusa mãe.

### 2. Estágio Éfira (Mode: `EPHYRA`) 📱
- **Biologia:** Medusa jovem, móvel.
- **Hardware:** Android (Termux), Raspberry Pi Zero.
- **Funcionalidade:**
    - Atua como **Relay** e **Sensor Móvel**.
    - Filtra ruído (Pigeon Cleaning) e reporta anomalias para o Smack.

### 3. Estágio Medusa (Mode: `MEDUSA`) 🪼
- **Biologia:** Forma adulta, completa e complexa.
- **Hardware:** Servidor, Cloud, Desktop potente.
- **Funcionalidade:**
    - Full Stack: FastAPI (NerveNet) + Streamlit (Interface) + SQLite (Memória).

---

## Lendas do Firewall (Inspiração: Cheswick, Bellovin & Rubin)
Lições clássicas do livro *"Firewalls and Internet Security"* biometizadas para a JellyV6.

### 1. O Modo Berferd (Bolsa Gástrica / Honeypot)
- **A Lenda:** Cheswick criou uma "Jaula" simulada para prender o hacker "Berferd", estudando seus movimentos enquanto ele tentava hackear um sistema falso e lento.
- **Biologia Jelly:** **Digestion Chamber**.
    - Em vez de bloquear o IP imediatamente, a Jelly o redireciona para um container Docker isolado (Jelly emulando vulnerabilidades).
    - O atacante perde tempo atacando o nada, enquanto a Jelly coleta inteligência (TTPs).

### 2. Protocolo Necrose (The Taking of Clark)
- **A Lenda:** A máquina "Clark" foi hackeada porque era um servidor de testes esquecido e sem patches. "Máquinas ociosas são o parquinho do Diabo."
- **Biologia Jelly:** **Amputação de Tecido Morto**.
    - O Smack monitora a "pulsação" de cada Éfira.
    - Se um nó não reportar status por X dias ou tiver software desatualizado (gangrena), ele é **revogado** (leia-se: banido da VPN) automaticamente antes que a infecção se espalhe.

### 3. Teoria do "Crunchy Shell" (A Falácia da Casca)
- **A Lenda:** Segurança antiga era "Casca dura (Firewall), miolo mole (Rede interna)". Se o hacker passasse a borda, game over.
- **Biologia Jelly:** A água-viva **não tem casca**. Ela é gelatinosa por inteiro, mas **pica em qualquer lugar**.
    - Validação do modelo **Smack (Zero Trust)**: Cada nó tem sua própria defesa (Micro-Firewall). Não existe "rede interna segura".

### 4. O Verme Teredo (Anti-Parasita)
- **A Lenda:** O protocolo Teredo encapsula IPv6 em UDP para furar NATs.
- **Biologia Jelly:** **Vermes de Mesogleia**.
    - O Rhopalium busca assinaturas de encapsulamento (ex: tráfego HTTP anômalo ou UDP 3544).
    - Se detectar um túnel não autorizado tentando sair, colapsa a conexão (Apoptose da conexão).

### 5. Cinto e Suspensórios (Belt and Suspenders)
- **A Lenda:** Usar dois métodos de segurança redundantes.
- **Biologia Jelly:** **Dupla Membrana**.
    1.  **Cinto (Kernel):** Bloqueio via `iptables`/`nftables` (rápido, bruto).
    2.  **Suspensórios (App):** Middleware FastAPI rejeita requests malformados (inteligente, granular).
    - Se uma camada falhar, a outra segura.
