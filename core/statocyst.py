"""
🪼 Jelly V6 - Statocyst Module (Equilíbrio Matemático)
Análise estatística: Z-Score de rede e Stress de CPU.
Nome: Statocyst = órgão de equilíbrio das águas-vivas reais.
"""
import statistics
import logging
from collections import deque

logger = logging.getLogger(__name__)

# Limites absolutos (arco reflexo — ignora adaptação)
LIMIT_CPU_PANIC = 90.0


class Statocyst:
    """Equilíbrio da Jelly — matemática pura de detecção de anomalias"""

    def __init__(self, max_down_kbps: float = 5000.0):
        self.cpu_history = deque(maxlen=60)
        self.net_history = deque(maxlen=30)
        self.max_down_kbps = max_down_kbps

    def analyze_network(self, novo_fluxo: float) -> tuple:
        """
        Analisa tráfego de rede para anomalias.
        Retorna (is_anomaly: bool, z_score_or_severity: float)
        
        Usa dois métodos:
        1. Saturação absoluta (>80% do máximo histórico)
        2. Z-Score estatístico (>3.0 desvios padrão)
        """
        self.net_history.append(novo_fluxo)

        # 0. APRENDIZADO: atualiza recorde
        record_updated = False
        if novo_fluxo > self.max_down_kbps:
            self.max_down_kbps = novo_fluxo
            record_updated = True

        # 1. GATILHO DE SATURAÇÃO (Absoluto Dinâmico)
        limite_panico = self.max_down_kbps * 0.8
        if novo_fluxo > limite_panico:
            return True, 100.0, record_updated

        # 2. Z-SCORE (Estatístico)
        if len(self.net_history) < 10:
            return False, 0.0, record_updated

        media = statistics.mean(self.net_history)
        desvio = statistics.stdev(self.net_history)
        if desvio < 50:
            desvio = 50  # Fallback para evitar falsos positivos em rede morta

        z_score = (novo_fluxo - media) / desvio

        if z_score > 3.0:
            return True, z_score, record_updated

        return False, z_score, record_updated

    def analyze_cpu_stress(self, cpu: float, ram: float) -> float:
        """
        Calcula score de stress (0-100) baseado em CPU e RAM.
        Usa média móvel para detectar picos relativos.
        """
        # Arco reflexo: pânico imediato
        if cpu > LIMIT_CPU_PANIC or ram > 95:
            return 100.0

        self.cpu_history.append(cpu)

        if len(self.cpu_history) < 10:
            return max(cpu, ram)

        media_recente = statistics.mean(self.cpu_history)
        diff = cpu - media_recente
        stress_relativo = max(0, diff * 2.0)
        score = (max(cpu, ram) * 0.4) + (stress_relativo * 0.6)
        return min(100, score)
