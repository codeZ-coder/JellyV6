from fastapi.testclient import TestClient
from core.nervenet import app, membrane, chaos_llama
from core.statocyst import Statocyst
import time

client = TestClient(app)

def test_trace_id_integration():
    """Verifica se Trace ID esta presente no header."""
    resp = client.get("/health")
    assert "X-Jelly-Trace" in resp.headers

def test_judo_defense_honeypot():
    """Verifica se honeypot retorna 200 OK."""
    resp = client.get("/admin")
    assert resp.status_code == 200
    assert resp.json()["status"] == "success"

def test_statocyst_v2_logic():
    """Verifica se Statocyst detecta anomalia de baseline."""
    st = Statocyst()
    # Simula baseline estavel
    for _ in range(50):
        st.analyze_network(100.0)
    
    # Pico anormal
    is_anomaly, z_val, _ = st.analyze_network(500.0)
    assert is_anomaly
    assert z_val > 3.0

def test_chaos_llama_init():
    """Verifica se Chaos Llama inicializa corretamente."""
    assert chaos_llama.interval > 0
    assert not chaos_llama.running 
    # Nao iniciamos no teste para nao atrapalhar
