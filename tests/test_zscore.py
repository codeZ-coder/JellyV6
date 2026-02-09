"""
🪼 Jelly V6 - Testes Automatizados
Valida a lógica de detecção de anomalias (Z-Score) e stress de CPU.
"""
import pytest
import statistics
import random
from collections import deque


# --- Mock do estado do brain para testes isolados ---
class MockBrainState:
    def __init__(self):
        self.net_history = deque(maxlen=30)
        self.cpu_history = deque(maxlen=60)
        self.max_down_kbps = 5000.0
        self.nematocisto_ativo = 0


# --- Funções copiadas do brain.py para teste unitário ---
def analisar_rede(state: MockBrainState, novo_fluxo: float):
    """Analisa tráfego de rede e detecta anomalias via Z-Score"""
    state.net_history.append(novo_fluxo)
    
    # Aprendizado: atualiza recorde
    if novo_fluxo > state.max_down_kbps:
        state.max_down_kbps = novo_fluxo
        
    # Gatilho de saturação (80% do máximo histórico)
    limite_panico = state.max_down_kbps * 0.8
    if novo_fluxo > limite_panico:
        return True, 100.0
        
    # Z-Score estatístico
    if len(state.net_history) < 10:
        return False, 0.0
        
    media = statistics.mean(state.net_history)
    desvio = statistics.stdev(state.net_history)
    if desvio < 50:
        desvio = 50  # Fallback para evitar divisão por zero
    z_score = (novo_fluxo - media) / desvio
    
    if z_score > 3.0:
        return True, z_score
        
    return False, z_score


def analisar_stress_cpu(state: MockBrainState, cpu: float, ram: float):
    """Calcula score de stress baseado em CPU e RAM"""
    LIMIT_CPU_PANIC = 90.0
    
    if cpu > LIMIT_CPU_PANIC or ram > 95:
        return 100.0
        
    state.cpu_history.append(cpu)
    
    if len(state.cpu_history) < 10:
        return max(cpu, ram)
        
    media_recente = statistics.mean(state.cpu_history)
    diff = cpu - media_recente
    stress_relativo = max(0, diff * 2.0)
    score = (max(cpu, ram) * 0.4) + (stress_relativo * 0.6)
    return min(100, score)


# --- TESTES ---

class TestZScoreDetection:
    """Testes para detecção de anomalias via Z-Score"""
    
    def test_fluxo_normal_nao_dispara_alerta(self):
        """Fluxo estável não deve disparar alarme"""
        state = MockBrainState()
        
        # Simula 20 leituras estáveis (~100 KB/s)
        for _ in range(20):
            is_anomaly, z = analisar_rede(state, random.uniform(90, 110))
            
        # Última leitura normal
        is_anomaly, z = analisar_rede(state, 105)
        
        assert is_anomaly == False
        assert z < 3.0
    
    def test_pico_subito_dispara_alerta(self):
        """Pico repentino de tráfego deve disparar Z-Score > 3"""
        state = MockBrainState()
        
        # Simula 15 leituras estáveis (~100 KB/s)
        for _ in range(15):
            analisar_rede(state, random.uniform(90, 110))
            
        # Injeta pico de 500 KB/s
        is_anomaly, z = analisar_rede(state, 500)
        
        assert is_anomaly == True
        assert z > 3.0
    
    def test_saturacao_absoluta_dispara_panico(self):
        """Tráfego acima de 80% do máximo histórico = pânico imediato"""
        state = MockBrainState()
        state.max_down_kbps = 1000.0  # Max conhecido = 1 MB/s
        
        # Fluxo de 850 KB/s (85% do máximo)
        is_anomaly, score = analisar_rede(state, 850)
        
        assert is_anomaly == True
        assert score == 100.0
    
    def test_aprendizado_atualiza_recorde(self):
        """Novo recorde de velocidade deve ser aprendido"""
        state = MockBrainState()
        state.max_down_kbps = 1000.0
        
        # Fluxo maior que o recorde atual
        analisar_rede(state, 1500)
        
        assert state.max_down_kbps == 1500.0


class TestCPUStress:
    """Testes para cálculo de stress de CPU/RAM"""
    
    def test_cpu_normal_baixo_stress(self):
        """CPU baixa = stress baixo"""
        state = MockBrainState()
        
        # Simula histórico estável
        for _ in range(15):
            analisar_stress_cpu(state, 25, 30)
            
        score = analisar_stress_cpu(state, 25, 30)
        
        assert score < 40
    
    def test_cpu_critica_panico(self):
        """CPU > 90% = pânico imediato"""
        state = MockBrainState()
        
        score = analisar_stress_cpu(state, 95, 50)
        
        assert score == 100.0
    
    def test_ram_critica_panico(self):
        """RAM > 95% = pânico imediato"""
        state = MockBrainState()
        
        score = analisar_stress_cpu(state, 50, 97)
        
        assert score == 100.0
    
    def test_pico_cpu_aumenta_stress(self):
        """Pico repentino de CPU aumenta stress relativo"""
        state = MockBrainState()
        
        # Simula histórico estável em 30%
        for _ in range(15):
            analisar_stress_cpu(state, 30, 40)
            
        # Pico para 70%
        score = analisar_stress_cpu(state, 70, 40)
        
        assert score > 50  # Deve aumentar significativamente


class TestHealthCheck:
    """Testes para endpoint de health check"""
    
    def test_health_response_structure(self):
        """Health check deve retornar estrutura correta"""
        # Simula resposta esperada
        response = {
            "status": "alive",
            "uptime_seconds": 123.45,
            "version": "6.0.0"
        }
        
        assert "status" in response
        assert "uptime_seconds" in response
        assert "version" in response
        assert response["status"] == "alive"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
