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
        self.short_term_net = deque(maxlen=10)   # Janela Curta (30s - "Agora")
        self.long_term_net = deque(maxlen=1000)  # Janela Longa (1h - "Normal")
        self.max_down_kbps = max_down_kbps

    def analyze_network(self, novo_fluxo: float) -> tuple:
        """
        Analisa tráfego de rede para anomalias (Statocyst 2.0).
        Retorna (is_anomaly: bool, z_score_or_severity: float, record_updated: bool)
        
        Usa três métodos:
        1. Saturação Absoluta (>80% do máximo histórico) - Pânico
        2. Z-Score de Curto Prazo (Picos repentinos)
        3. Desvio da Baseline (Mudança de Comportamento "Hoje vs Ontem")
        """
        self.short_term_net.append(novo_fluxo)
        self.long_term_net.append(novo_fluxo)

        # 0. APRENDIZADO: atualiza recorde
        record_updated = False
        if novo_fluxo > self.max_down_kbps:
            self.max_down_kbps = novo_fluxo
            record_updated = True

        # 1. GATILHO DE SATURAÇÃO (Absoluto Dinâmico)
        limite_panico = self.max_down_kbps * 0.8
        if novo_fluxo > limite_panico:
            return True, 100.0, record_updated

        # Se não tem histórico suficiente, assume normal
        if len(self.long_term_net) < 20:
            return False, 0.0, record_updated

        # Estatísticas da Baseline (Longo Prazo)
        baseline_mean = statistics.mean(self.long_term_net)
        baseline_std = statistics.stdev(self.long_term_net)
        if baseline_std < 50: baseline_std = 50 # Evita div/0

        # Estatísticas do Agora (Curto Prazo)
        current_mean = statistics.mean(self.short_term_net)

        # 2. DETECÇÃO DE DESVIO (Anomalia de Comportamento)
        # Compara a media de agora com a distribuicao de "sempre"
        z_score_long = (current_mean - baseline_mean) / baseline_std

        # Se o tráfego atual é > 3 sigmas da baseline
        if z_score_long > 3.0:
            return True, z_score_long, record_updated
            
        return False, z_score_long, record_updated

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
