"""
🪼 Jelly V6 - Chemoreceptor Module (Sensor Químico)
Analisa a DIVERSIDADE (Entropia de Shannon) de um lote de tráfego
para distinguir nutrientes (humanos) de toxinas (botnets).

Stateless: Recebe um batch de dados e retorna matemática pura.
"""
import math
from collections import Counter
from typing import List, Dict


class Chemoreceptor:
    """
    Analisa a DIVERSIDADE (Entropia de Shannon) de um lote de tráfego.
    
    Conceito: Se 100 requisições vêm de 100 IPs diferentes → Entropia Alta (Humano).
              Se 100 requisições vêm de 1 IP só → Entropia Zero (Ataque DoS).
    """
    def __init__(self):
        # Pesos calibrados para detectar repetição
        self.W1_IP = 0.5   # Baixa variação de IP = Ataque clássico
        self.W2_URL = 0.3  # Baixa variação de URL = Brute force/Flood
        self.W3_UA = 0.2   # Baixa variação de UA = Botnet preguiçosa
        
    def _shannon_entropy(self, data: List[str]) -> float:
        """Quanto maior o valor, mais variado (humano) é o lote."""
        if not data: return 0.0
        
        total = len(data)
        counts = Counter(data)
        entropy = 0.0
        
        for count in counts.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
                
        return entropy

    def analyze_batch(self, batch: List[Dict]) -> dict:
        """
        Recebe um buffer de requisições (ex: últimas 50).
        Retorna o Vetor de Toxicidade baseado na distribuição do lote.
        """
        if not batch or len(batch) < 2:
            # Se não tem amostra suficiente, assume neutro
            return {"toxicity": 0.0, "diagnosis": "AMOSTRA_INSUFICIENTE"}

        # 1. Extração dos compostos químicos
        ips = [r.get("ip", "") for r in batch]
        urls = [r.get("url", "") for r in batch]
        uas = [r.get("user_agent", "") for r in batch]

        # 2. Entropia (Diversidade do lote)
        h_ip = self._shannon_entropy(ips)
        h_url = self._shannon_entropy(urls)
        h_ua = self._shannon_entropy(uas)

        # 3. Toxicidade (Inverso da Diversidade)
        # Se a entropia é baixa (repetição), a toxicidade é alta.
        # Threshold de 0.5 evita divisão por zero e ignora micro-repetições
        t_ip = (1.0 / h_ip) if h_ip > 0.5 else 10.0
        t_url = (1.0 / h_url) if h_url > 0.5 else 10.0
        t_ua = (1.0 / h_ua) if h_ua > 0.5 else 10.0

        vector_T = (self.W1_IP * t_ip) + (self.W2_URL * t_url) + (self.W3_UA * t_ua)

        # 4. Diagnóstico Clínico
        diagnosis = "NUTRIENTE_ORGANICO"
        if vector_T > 5.0:
            diagnosis = "TOXINA_LETAL_BOTNET"  # Muita repetição
        elif vector_T > 2.5:
            diagnosis = "ALTA_TOXICIDADE_ALVO_FIXO"  # Repetição moderada

        return {
            "toxicity": round(vector_T, 2),
            "entropies": {
                "IP": round(h_ip, 2),
                "URL": round(h_url, 2),
                "UA": round(h_ua, 2)
            },
            "diagnosis": diagnosis
        }
