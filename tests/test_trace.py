from fastapi.testclient import TestClient
from core.nervenet import app 
import logging

client = TestClient(app)

# Silencia logs durante testes
logging.getLogger("NerveNet").setLevel(logging.CRITICAL)

def test_trace_id_injection():
    """Verifica se o X-Jelly-Trace e X-Process-Time sao retornados."""
    response = client.get("/health")
    
    assert response.status_code == 200
    assert "X-Jelly-Trace" in response.headers
    assert "X-Process-Time" in response.headers
    
    trace_id = response.headers["X-Jelly-Trace"]
    assert len(trace_id) > 0
    print(f"\nTrace ID capturado: {trace_id}")

def test_trace_id_persistence():
    """Verifica se o ID muda entre requests (cada request eh unico)."""
    r1 = client.get("/health")
    t1 = r1.headers["X-Jelly-Trace"]
    
    r2 = client.get("/health")
    t2 = r2.headers["X-Jelly-Trace"]
    
    assert t1 != t2
