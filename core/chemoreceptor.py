
import math
from collections import Counter
from typing import List, Dict

class Chemoreceptor:
    """
    Analisa a estrutura química (entropia) do tráfego para distinguir
    nutrientes (usuários reais) de toxinas (botnets/ataques).
    """
    def __init__(self):
        # Pesos do Vetor de Toxicidade (Ajuste fino)
        # Bots tentam enganar IPs, mas falham em URL/UA
        self.W1_IP = 0.5
        self.W2_URL = 0.3
        self.W3_UA = 0.2
        
    def _shannon_entropy(self, data: List[str]) -> float:
        """Calcula a Entropia de Shannon (H) de uma lista."""
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
        Recebe uma lista de requests (dicionários) e retorna o Vetor de Toxicidade.
        """
        if not batch: return {"toxicity": 0.0, "diagnosis": "VÁCUO"}

        # 1. Extração dos compostos químicos
        ips = [r.get("ip", "") for r in batch]
        urls = [r.get("url", "") for r in batch]
        uas = [r.get("user_agent", "") for r in batch]

        # 2. Cálculo das Entropias (H)
        h_ip = self._shannon_entropy(ips)
        h_url = self._shannon_entropy(urls)
        h_ua = self._shannon_entropy(uas)

        # 3. Cálculo do Vetor de Toxicidade (T = w * (1/H))
        # Tratamento de divisão por zero: Se H < 0.1, considera toxicidade MÁXIMA (10.0)
        t_ip = (1.0 / h_ip) if h_ip > 0.1 else 10.0
        t_url = (1.0 / h_url) if h_url > 0.1 else 10.0
        t_ua = (1.0 / h_ua) if h_ua > 0.1 else 10.0

        vector_T = (self.W1_IP * t_ip) + (self.W2_URL * t_url) + (self.W3_UA * t_ua)

        # 4. Diagnóstico Clínico
        diagnosis = "NUTRIENTE_ORGANICO"
        if vector_T > 6.0:
            diagnosis = "TOXINA_LETAL_BOTNET"
        elif vector_T > 3.0:
            diagnosis = "ALTA_TOXICIDADE_ALVO_FIXO" # Provável ataque L7 focado

        return {
            "T_vector": round(vector_T, 2),
            "H_ip": round(h_ip, 2),
            "H_url": round(h_url, 2),
            "H_ua": round(h_ua, 2),
            "diagnosis": diagnosis
        }
