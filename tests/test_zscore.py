"""
🪼 Jelly V6 - Testes Automatizados (NerveNet Modular)
Testa cada módulo isoladamente: Statocyst, Cnidocyte, Rhopalium.
"""
import pytest
import random
import sys
import os

# Adiciona o diretório raiz ao path para imports funcionarem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.statocyst import Statocyst
from core.cnidocyte import Cnidocyte
from core.persistence import Persistence


# --- TESTES DO STATOCYST (Z-Score + CPU Stress) ---

class TestNetworkAnalysis:
    """Testes para detecção de anomalias via Z-Score"""

    def test_fluxo_normal_nao_dispara_alerta(self):
        """Fluxo estável não deve disparar alarme"""
        stat = Statocyst(max_down_kbps=5000.0)

        for _ in range(20):
            is_anomaly, z, _ = stat.analyze_network(random.uniform(90, 110))

        is_anomaly, z, _ = stat.analyze_network(105)
        assert is_anomaly == False
        assert z < 3.0

    def test_pico_subito_dispara_alerta(self):
        """Pico repentino de tráfego deve disparar Z-Score > 3"""
        stat = Statocyst(max_down_kbps=5000.0)

        for _ in range(15):
            stat.analyze_network(random.uniform(90, 110))

        is_anomaly, z, _ = stat.analyze_network(500)
        assert is_anomaly == True
        assert z > 3.0

    def test_saturacao_absoluta_dispara_panico(self):
        """Tráfego acima de 80% do máximo histórico = pânico"""
        stat = Statocyst(max_down_kbps=1000.0)

        is_anomaly, score, _ = stat.analyze_network(850)
        assert is_anomaly == True
        assert score == 100.0

    def test_aprendizado_atualiza_recorde(self):
        """Novo recorde de velocidade deve ser aprendido"""
        stat = Statocyst(max_down_kbps=1000.0)

        _, _, updated = stat.analyze_network(1500)
        assert updated == True
        assert stat.max_down_kbps == 1500.0


class TestCPUStress:
    """Testes para cálculo de stress de CPU/RAM"""

    def test_cpu_normal_baixo_stress(self):
        """CPU baixa = stress baixo"""
        stat = Statocyst()

        for _ in range(15):
            stat.analyze_cpu_stress(25, 30)

        score = stat.analyze_cpu_stress(25, 30)
        assert score < 40

    def test_cpu_critica_panico(self):
        """CPU > 90% = pânico imediato"""
        stat = Statocyst()
        score = stat.analyze_cpu_stress(95, 50)
        assert score == 100.0

    def test_ram_critica_panico(self):
        """RAM > 95% = pânico imediato"""
        stat = Statocyst()
        score = stat.analyze_cpu_stress(50, 97)
        assert score == 100.0

    def test_pico_cpu_aumenta_stress(self):
        """Pico repentino de CPU aumenta stress relativo"""
        stat = Statocyst()

        for _ in range(15):
            stat.analyze_cpu_stress(30, 40)

        score = stat.analyze_cpu_stress(70, 40)
        assert score > 50


# --- TESTES DO CNIDOCYTE (Defesa) ---

class TestCnidocyte:
    """Testes para o sistema de defesa"""

    def test_anomalia_ativa_defesa(self):
        """Anomalia deve ativar reflexo de defesa"""
        # Mock persistence que não faz nada
        class MockPersistence:
            def registrar_forense_async(self, *args): pass

        cni = Cnidocyte(persistence=MockPersistence())
        reflexo = cni.avaliar_ameaca(True, 900, 1000, 4.5)
        assert reflexo == True

    def test_cooldown_decrementa(self):
        """Cooldown deve decrementar a cada ciclo"""
        class MockPersistence:
            def registrar_forense_async(self, *args): pass

        cni = Cnidocyte(persistence=MockPersistence())
        cni.avaliar_ameaca(True, 900, 1000, 4.5)  # Ativa (15)

        # Após 15 ciclos sem anomalia, deve desativar
        for _ in range(15):
            reflexo = cni.avaliar_ameaca(False, 100, 1000, 0.5)

        assert reflexo == False

    def test_sem_anomalia_sem_defesa(self):
        """Sem anomalia não deve ativar defesa"""
        class MockPersistence:
            def registrar_forense_async(self, *args): pass

        cni = Cnidocyte(persistence=MockPersistence())
        reflexo = cni.avaliar_ameaca(False, 100, 1000, 0.5)
        assert reflexo == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
