"""
🪼 Jelly V6 - Full System Test Suite
Cobre: Trace ID, Judo Defense, Statocyst 2.0, H-System (Dwell Time), Integração.
"""
from fastapi.testclient import TestClient
from core.nervenet import app, membrane
from core.cnidocyte import Cnidocyte
from core.statocyst import Statocyst
import pytest

client = TestClient(app)


# Mock Persistence for unit tests
class MockPersistence:
    def registrar_forense_async(self, tipo, msg):
        pass


@pytest.fixture
def clean_membrane():
    membrane.pressure_map.clear()
    membrane.request_buffer.clear()
    return membrane


# ===================== 1. TRACE ID =====================
def test_trace_id_header():
    """Trace ID deve estar presente em respostas normais."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert "X-Jelly-Trace" in resp.headers
    assert len(resp.headers["X-Jelly-Trace"]) > 0


# ===================== 2. JUDO DEFENSE =====================
def test_judo_honeypot(clean_membrane):
    """Honeypot (/admin) deve retornar Fake 200 OK."""
    resp = client.get("/admin")
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


# ===================== 3. STATOCYST 2.0 =====================
def test_statocyst_spike_detection():
    """Spike violento deve disparar anomalia via Z-Score."""
    st = Statocyst()
    # Baseline: 50 leituras normais
    for _ in range(50):
        st.analyze_network(100.0)

    # Spike massivo (precisa ser grande para vencer a média móvel)
    is_anomaly, z_val, _ = st.analyze_network(20000.0)
    assert is_anomaly
    assert z_val > 3.0


# ===================== 4. H-SYSTEM DWELL TIME =====================
def test_h_system_dwell_time():
    """Testa Histerese: período refratário impede re-ativação prematura."""
    c = Cnidocyte(persistence=MockPersistence())

    # 1. Disparar defesa (anomalia verdadeira)
    active = c.avaliar_ameaca(True, 1000.0, 1000.0, 5.0)
    assert active
    # Sets to 15, then decrements -> 14
    assert c.nematocisto_ativo == 14
    assert c.refractory_timer == 0

    # 2. Anomalia continua -> renova cooldown (fica em defesa)
    for _ in range(5):
        active = c.avaliar_ameaca(True, 1000.0, 1000.0, 5.0)
        assert active

    # 3. Anomalia PARA -> defesa drena
    c.nematocisto_ativo = 1
    c.refractory_timer = 0
    active = c.avaliar_ameaca(False, 100.0, 1000.0, 0.0)
    # active=1, decrementa para 0, inicia refractory=10
    assert not active
    assert c.nematocisto_ativo == 0
    assert c.refractory_timer == 10

    # 4. Nova anomalia durante período refratário -> IGNORADA
    active = c.avaliar_ameaca(True, 1000.0, 1000.0, 5.0)
    assert not active
    assert c.refractory_timer == 9  # Decrementou

    # 5. Ameaça CRÍTICA (osmótica) -> Bypassa refratário
    active = c.avaliar_ameaca(True, 5000.0, 1000.0, 5.0, osmotic_alert="NEMATOCYST")
    assert active
    assert c.nematocisto_ativo == 14  # 15 - 1 (decrement)
    assert c.refractory_timer == 0  # Reset


# ===================== 5. INTEGRAÇÃO =====================
def test_full_integration_flow(clean_membrane):
    """Request -> Middleware -> Judo/Trace -> Resposta."""
    # 1. Request normal (com Trace)
    r = client.get("/health")
    assert r.status_code == 200
    assert "X-Jelly-Trace" in r.headers

    # 2. Honeypot (Fake 200, sem Trace pois curto-circuita no middleware)
    r = client.get("/admin")
    assert r.status_code == 200
    assert r.json()["status"] == "success"
