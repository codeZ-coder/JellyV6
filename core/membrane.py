"""
🪼 Jelly V6 - Osmotic Membrane Module (Defesa)
Gerencia a pressão osmótica por IP e decide a resposta defensiva.
Usa um buffer de requisições para alimentar o Chemoreceptor (batch).

Stateful: Mantém pressão por IP + buffer temporal de requests.
Thread-safe: Usa Lock para proteger estado compartilhado.
"""
import time
import threading
from collections import deque
from typing import Dict
from .chemo import Chemoreceptor


class OsmoticMembrane:
    """
    Membrana semipermeável com buffer de requisições.
    Acumula requests e analisa a distribuição do lote periodicamente.
    """
    def __init__(self, threshold=100, decay_rate=5, buffer_size=50, buffer_ttl=30.0):
        self.pressure_map: Dict[str, float] = {}
        self.last_update_map: Dict[str, float] = {}
        self.threshold = threshold
        self.decay_rate = decay_rate
        self.chemo = Chemoreceptor()
        
        # Buffer de requisições (janela deslizante)
        self.request_buffer: deque = deque(maxlen=buffer_size)
        self.buffer_ttl = buffer_ttl  # Tempo de vida dos requests no buffer (segundos)
        self.last_batch_result: dict = {"toxicity": 0.0, "diagnosis": "AMOSTRA_INSUFICIENTE"}
        self.last_analysis_time: float = 0
        self.analysis_interval: float = 3.0  # Analisa a cada 3 segundos
        
        # Contadores forenses
        self.nematocyst_count: int = 0
        self.contract_count: int = 0

        # BLACKHOLE: IPs permanentemente banidos (silencioso)
        self.blackhole_list: set = set()

        # Thread safety
        self._lock = threading.Lock()

        # Caminho da toxina (GZIP Bomb)
        self.toxin_path = "assets/toxin.gz"

    def _osmotic_recovery(self, ip: str):
        """Aplica homeostase (recuperação natural) ao IP. Deve ser chamado dentro do lock."""
        now = time.time()
        last_time = self.last_update_map.get(ip, now)
        delta = now - last_time
        
        # Recupera decay_rate atm por segundo
        if delta > 1.0:
            recovery = int(delta) * self.decay_rate
            current_pressure = self.pressure_map.get(ip, 0)
            new_pressure = max(0, current_pressure - recovery)
            self.pressure_map[ip] = new_pressure
            
            # Limpa IPs que voltaram a zero (garbage collection)
            if new_pressure == 0:
                self.pressure_map.pop(ip, None)
                self.last_update_map.pop(ip, None)
                return
            
            self.last_update_map[ip] = now

    def passive_recovery(self):
        """
        Metabolismo Basal: Decai a pressão de TODOS os IPs.
        Chamado periodicamente pelo sistema (ex: get_vitals) para limpar
        pressão residual de atacantes que pararam de enviar requests.
        """
        with self._lock:
            now = time.time()
            # Copia chaves para permitir modificação durante iteração
            for ip in list(self.pressure_map.keys()):
                self._osmotic_recovery(ip)

    def _purge_expired(self):
        """Remove requests expirados do buffer (TTL). Deve ser chamado dentro do lock."""
        now = time.time()
        while self.request_buffer and (now - self.request_buffer[0]["timestamp"] > self.buffer_ttl):
            self.request_buffer.popleft()

    def _analyze_buffer(self):
        """Analisa o buffer de requisições acumuladas (batch). Deve ser chamado dentro do lock."""
        now = time.time()
        if now - self.last_analysis_time < self.analysis_interval:
            return  # Ainda não é hora
        
        # Purga requests antigos antes de analisar
        self._purge_expired()
        
        if len(self.request_buffer) >= 2:
            self.last_batch_result = self.chemo.analyze_batch(
                list(self.request_buffer)
            )
            self.last_analysis_time = now

    # Padrões de ataque óbvios (Reflexo Imediato / Gosto Ácido)
    ACID_PATTERNS = ["../", "..\\", "%00", "%2e%2e", "UNION ", "SELECT ", "<script", "javascript:", "onerror="]
    
    # Caminhos Isca (Honeypots) - Sorria e Acene
    HONEYPOT_PATHS = ["/admin", "/login", "/config", "/.env", "/backup", "/phpmyadmin"]

    def process_request(self, ip: str, url: str, ua: str) -> dict:
        """
        Processa uma requisição (thread-safe):
        0. Gosto Ácido: Bloqueia exploits óbvios instantaneamente
        1. Adiciona ao buffer
        2. Analisa batch periodicamente
        3. Aplica pressão baseada na toxicidade do LOTE
        4. Decide ação
        """
        with self._lock:
            # 0.0. BLACKHOLE CHECK (IP já banido? Silêncio total)
            if ip in self.blackhole_list:
                return {
                    "action": "BLACKHOLE",
                    "pressure": 9999,
                    "diagnosis": "IP_BANIDO_PERMANENTE",
                    "buffer_size": 0,
                    "toxin_path": None
                }

            # 0.1. HONEYPOT (Phishing Reverso)
            # Se tocar na isca, finge sucesso (200 OK) mas marca o IP
            for honey in self.HONEYPOT_PATHS:
                if url.startswith(honey):
                    self.pressure_map[ip] = self.threshold * 5 # Marca radioativo -> BLACKHOLE
                    self.last_update_map[ip] = time.time()
                    return {
                        "action": "FAKE_200",
                        "pressure": self.pressure_map[ip],
                        "diagnosis": "PHISHING_REVERSO_SUCESSO",
                        "buffer_size": 0,
                        "toxin_path": None
                    }

            # 0.2. GOSTO ÁCIDO — Reflexo imediato
            # Decodifica URL-encoding para detectar payloads ofuscados
            from urllib.parse import unquote
            url_decoded = unquote(url).upper()
            for pattern in self.ACID_PATTERNS:
                if pattern.upper() in url_decoded:
                    self.pressure_map[ip] = self.threshold * 3
                    self.last_update_map[ip] = time.time()
                    self.nematocyst_count += 1
                    return {
                        "action": "NEMATOCYST",
                        "pressure": self.pressure_map[ip],
                        "diagnosis": {"diagnosis": "ACIDEZ_IMEDIATA", "toxicity": 99.0, "pattern": pattern},
                        "buffer_size": len(self.request_buffer),
                        "toxin_path": self.toxin_path
                    }

            # 1. Alimentar o buffer
            self.request_buffer.append({
                "ip": ip,
                "url": url,
                "user_agent": ua,
                "timestamp": time.time()
            })

            # 2. Homeostase
            self._osmotic_recovery(ip)
            
            # 3. Quimiorecepção
            self._analyze_buffer()
            toxicity = self.last_batch_result.get("toxicity", 0.0)
            diagnosis = self.last_batch_result.get("diagnosis", "AMOSTRA_INSUFICIENTE")
            
            # 4. Calcular pressão
            if diagnosis == "AMOSTRA_INSUFICIENTE":
                pressure_buildup = 1
            elif diagnosis == "NUTRIENTE_ORGANICO":
                pressure_buildup = 0
            elif diagnosis == "ALTA_TOXICIDADE_ALVO_FIXO":
                pressure_buildup = int(toxicity * 3)
            else:
                pressure_buildup = int(toxicity * 8)

            # 5. Atualiza Pressão
            current_pressure = self.pressure_map.get(ip, 0) + pressure_buildup
            self.pressure_map[ip] = current_pressure
            self.last_update_map[ip] = time.time()
            
            # 6. Decisão de Resposta (JUDO APPLIED)
            action = "ALLOW"
            
            if current_pressure > self.threshold * 10:
                # RUPTURA: Só em caso EXTREMO (1000+ atm)
                action = "RUPTURA_MESOGLEIA"
                self.nematocyst_count += 1

            elif current_pressure > self.threshold * 4:
                # BLACKHOLE: Bane IP silenciosamente (400+ atm)
                action = "BLACKHOLE"
                self.blackhole_list.add(ip)
                self.nematocyst_count += 1

            elif current_pressure > self.threshold * 2:
                if diagnosis in ("TOXINA_LETAL_BOTNET", "ALTA_TOXICIDADE_ALVO_FIXO"):
                    action = "TARPIT" if "BOTNET" in diagnosis else "NEMATOCYST"
                    self.nematocyst_count += 1
                else:
                    action = "CONTRACT"
                    self.contract_count += 1
                     
            elif current_pressure > self.threshold:
                action = "CONTRACT"
                self.contract_count += 1

            elif current_pressure > self.threshold * 0.5:
                action = "ACTIVE_PROBE"

            return {
                "action": action,
                "pressure": current_pressure,
                "diagnosis": self.last_batch_result,
                "buffer_size": len(self.request_buffer),
                "toxin_path": self.toxin_path if action == "NEMATOCYST" else None
            }
