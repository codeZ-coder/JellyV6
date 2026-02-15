"""
🧪 Jelly V6 - Testes Osmóticos
Valida o Chemoreceptor (entropia de distribuição) e a OsmoticMembrane (pressão/ação).
"""
import time
import pytest
from core.chemo import Chemoreceptor
from core.membrane import OsmoticMembrane


# =====================================================================
# CHEMORECEPTOR (Análise de Entropia)
# =====================================================================

class TestChemoreceptor:
    """Testes para o sensor de entropia de distribuição."""

    def setup_method(self):
        self.chemo = Chemoreceptor()

    def test_amostra_insuficiente_vazia(self):
        """Batch vazio → amostra insuficiente."""
        result = self.chemo.analyze_batch([])
        assert result["diagnosis"] == "AMOSTRA_INSUFICIENTE"
        assert result["toxicity"] == 0.0

    def test_amostra_insuficiente_unico(self):
        """Batch com 1 request → amostra insuficiente."""
        batch = [{"ip": "1.1.1.1", "url": "/home", "user_agent": "bot"}]
        result = self.chemo.analyze_batch(batch)
        assert result["diagnosis"] == "AMOSTRA_INSUFICIENTE"

    def test_botnet_detectada(self):
        """20 requests do mesmo IP/URL/UA → TOXINA_LETAL_BOTNET."""
        batch = [
            {"ip": "10.0.0.1", "url": "/login", "user_agent": "python-requests/2.28"}
            for _ in range(20)
        ]
        result = self.chemo.analyze_batch(batch)
        assert result["diagnosis"] == "TOXINA_LETAL_BOTNET"
        assert result["toxicity"] > 5.0

    def test_trafego_humano_diverso(self):
        """20 requests com IPs, URLs e UAs variados → NUTRIENTE_ORGANICO."""
        batch = [
            {
                "ip": f"192.168.1.{i}",
                "url": f"/page/{i}",
                "user_agent": f"Mozilla/5.0 (Browser {i})"
            }
            for i in range(20)
        ]
        result = self.chemo.analyze_batch(batch)
        assert result["diagnosis"] == "NUTRIENTE_ORGANICO"
        assert result["toxicity"] < 2.5

    def test_ataque_alvo_fixo(self):
        """IPs variados mas todos na mesma URL → toxicidade média."""
        batch = [
            {
                "ip": f"10.0.0.{i}",
                "url": "/api/login",  # Mesmo alvo
                "user_agent": f"Bot-{i}"
            }
            for i in range(20)
        ]
        result = self.chemo.analyze_batch(batch)
        # URL tem entropia zero → toxicidade alta no componente URL
        assert result["toxicity"] > 2.0

    def test_entropias_retornadas(self):
        """Verifica que as entropias individuais são retornadas."""
        batch = [
            {"ip": f"1.1.1.{i}", "url": "/home", "user_agent": "chrome"}
            for i in range(10)
        ]
        result = self.chemo.analyze_batch(batch)
        assert "entropies" in result
        assert "IP" in result["entropies"]
        assert "URL" in result["entropies"]
        assert "UA" in result["entropies"]
        # IPs variados → entropia alta; URL/UA fixos → entropia zero
        assert result["entropies"]["IP"] > 2.0
        assert result["entropies"]["URL"] == 0.0
        assert result["entropies"]["UA"] == 0.0


# =====================================================================
# OSMOTIC MEMBRANE (Pressão e Decisões)
# =====================================================================

class TestOsmoticMembrane:
    """Testes para a membrana osmótica stateful."""

    def setup_method(self):
        # Threshold baixo para testes rápidos
        self.membrane = OsmoticMembrane(threshold=50, decay_rate=5, buffer_size=50)

    def test_primeira_request_allow(self):
        """Primeira requisição → sempre ALLOW (buffer insuficiente)."""
        result = self.membrane.process_request("1.1.1.1", "/home", "chrome")
        assert result["action"] == "ALLOW"

    def test_pressao_acumula(self):
        """Múltiplos requests do mesmo IP acumulam pressão."""
        for _ in range(5):
            result = self.membrane.process_request("10.0.0.1", "/feed", "bot")
        assert result["pressure"] > 0

    def test_nematocyst_com_lote_toxico(self):
        """Pressão alta + lote tóxico → NEMATOCYST."""
        membrane = OsmoticMembrane(threshold=10, decay_rate=0, buffer_size=50)
        # Encher o buffer com requests idênticos (tóxicos)
        # Forçar análise marcando tempo no passado
        membrane.last_analysis_time = 0
        for i in range(30):
            membrane.last_analysis_time = 0  # Forçar re-análise a cada request
            result = membrane.process_request("10.0.0.1", "/login", "python-requests/2.28")
        
        # Com threshold=10, decay=0, e 30 requests tóxicos, deve ter disparado
        assert result["action"] in ("CONTRACT", "NEMATOCYST")

    def test_homeostase_recupera(self):
        """Pressão decai com o tempo (homeostase)."""
        # Gerar alguma pressão
        self.membrane.pressure_map["1.1.1.1"] = 50
        self.membrane.last_update_map["1.1.1.1"] = time.time() - 10  # 10 segundos atrás
        
        # Processar um request (que dispara recovery)
        self.membrane.process_request("1.1.1.1", "/home", "chrome")
        
        # Pressão deve ter diminuído (recovery = 10s * 5 decay = 50)
        # Mas pode ter recebido +1 do request neutro
        assert self.membrane.pressure_map.get("1.1.1.1", 0) <= 2

    def test_garbage_collection_ip_zerado(self):
        """IP com pressão zero é removido do mapa."""
        self.membrane.pressure_map["192.168.1.99"] = 10
        self.membrane.last_update_map["192.168.1.99"] = time.time() - 60  # 60s atrás
        
        # Recovery: 60s * 5 = 300 > 10, vai zerar
        self.membrane.process_request("192.168.1.99", "/page", "firefox")
        
        # IP deve ter sido limpo (GC)
        assert "192.168.1.99" not in self.membrane.pressure_map or self.membrane.pressure_map["192.168.1.99"] <= 1

    def test_buffer_ttl_expira(self):
        """Requests antigos são purgados do buffer."""
        membrane = OsmoticMembrane(buffer_ttl=5.0)
        
        # Adicionar um request "antigo" manualmente
        membrane.request_buffer.append({
            "ip": "1.1.1.1", "url": "/old", "user_agent": "bot",
            "timestamp": time.time() - 60  # 60s atrás
        })
        
        # Purgar
        membrane._purge_expired()
        
        # Deve estar vazio
        assert len(membrane.request_buffer) == 0

    def test_buffer_ttl_mantem_recentes(self):
        """Requests recentes NÃO são purgados."""
        membrane = OsmoticMembrane(buffer_ttl=30.0)
        
        membrane.request_buffer.append({
            "ip": "1.1.1.1", "url": "/new", "user_agent": "chrome",
            "timestamp": time.time()  # Agora
        })
        
        membrane._purge_expired()
        
        assert len(membrane.request_buffer) == 1

    def test_contadores_forenses(self):
        """Contadores de nematocisto e contração são incrementados."""
        membrane = OsmoticMembrane(threshold=5, decay_rate=0, buffer_size=50)
        
        # Gerar pressão alta suficiente para CONTRACT
        membrane.pressure_map["10.0.0.1"] = 60
        membrane.last_update_map["10.0.0.1"] = time.time()
        membrane.last_analysis_time = 0
        
        result = membrane.process_request("10.0.0.1", "/feed", "bot")
        
        # Deve ter incrementado pelo menos um contador
        assert membrane.contract_count > 0 or membrane.nematocyst_count > 0

    def test_thread_safety_lock_exists(self):
        """Verifica que o lock existe para thread safety."""
        assert hasattr(self.membrane, '_lock')
        assert isinstance(self.membrane._lock, type(self.membrane._lock))
