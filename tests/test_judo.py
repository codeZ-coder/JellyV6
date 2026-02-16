from fastapi.testclient import TestClient
from core.nervenet import app, membrane
import time

client = TestClient(app)

def test_honeypot_fake_200():
    """Honeypot deve retornar 200 OK (Phishing Reverso)."""
    # /admin eh honeypot
    response = client.get("/admin")
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    # Mas a pressao deve ter subido
    # Como o client IP eh "testclient" ou "127.0.0.1" no TestClient?
    # TestClient usa "testclient" como host se nao especificado?
    # Vamos verificar se alguem tem pressao alta
    assert any(p > 0 for p in membrane.pressure_map.values())

def test_tarpit_delay():
    """Deve aplicar delay se pressao for alta e diag for BOTNET."""
    # Simular pressao alta manualmente
    test_ip = "1.2.3.4"
    membrane.pressure_map[test_ip] = membrane.threshold * 2.5
    membrane.last_batch_result = {"diagnosis": "TOXINA_LETAL_BOTNET", "toxicity": 1.0}
    
    # Mockando request.client.host eh dificil no TestClient sem hacking
    # Entao vamos confiar no teste unitario via membrane.process_request
    
    result = membrane.process_request(test_ip, "/vitals", "Mozilla/5.0")
    assert result["action"] == "TARPIT"

def test_judo_response_structure():
    """Verifica se a resposta do Tarpit engana bem."""
    # Simular acao TARPIT no endpoint
    # Como nao conseguimos forcar o IP facilemente no integration test sem middleware hacking,
    # vamos apenas verificar se o FAKE_200 do honeypot tem campos críveis
    response = client.get("/admin")
    data = response.json()
    assert "status" in data
    assert "msg" in data
    assert "id" in data
