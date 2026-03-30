"""
Jelly V6 - Testes Fase 4 (Brainbow & GFP)
Verifica coloracao tatica e rastreamento persistente (cookie/etag).
"""
import os
import sys
from fastapi.testclient import TestClient
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.nervenet import app, JELLY_DNA_SECRET, membrane

client = TestClient(app)

HEADERS = {"X-JELLY-DNA": JELLY_DNA_SECRET}

class TestPhase4:
    
    def setup_method(self):
        # Limpa estado da membrana para nao interferir entre testes
        membrane.pressure_map.clear()
        # Forca bioluminescencia a parar para testes de estado "Calmo"
        from core.bioluminescence import biolum
        biolum.running = False

    # --- GFP (Green Fluorescent Protein) ---
    def test_gfp_injection(self):
        """Deve injetar cookie 'jelly_gfp' e ETag se nao existirem."""
        
        # 1. Primeira visita (sem infeccao)
        response = client.get("/health")
        assert response.status_code == 200
        
        # Verifica se recebeu o marcador
        assert "jelly_gfp" in response.cookies
        assert "etag" in response.headers
        assert response.headers["etag"].startswith('W/"')
        
        gfp_id = response.cookies["jelly_gfp"]
        assert len(gfp_id) > 10

    def test_gfp_persistence(self):
        """Se cliente ja tem GFP, deve manter o mesmo ID (rastreamento)."""
        # Simula cliente marcado
        fake_id = "tracker-123-xyz"
        client.cookies.set("jelly_gfp", fake_id)
        
        response = client.get("/health")
        
        # O sistema deve reconhecer e devolver o mesmo ID
        assert response.cookies["jelly_gfp"] == fake_id
        assert fake_id in response.headers["etag"]

    # --- BRAINBOW (Spectral Dashboard) ---
    def test_brainbow_calm_green(self):
        """Em repouso, deve ser Verde/Ciano (#00ffaa)."""
        response = client.get("/vitals", headers=HEADERS)
        data = response.json()
        
        assert "brainbow_color" in data
        assert data["brainbow_color"] == "#00ffaa"
        assert data["agitation_level"] == 0.0

    def test_brainbow_toxic_purple(self):
        """Sob pressao critica, deve virar Roxo (#aa00ff)."""
        # Simula pressao extrema (Ruptura eminente)
        membrane.process_request("1.2.3.4", "/admin", "sqlmap")
        membrane.pressure_map["1.2.3.4"] = membrane.threshold + 10
        
        response = client.get("/vitals", headers=HEADERS)
        data = response.json()
        
        # Deve estar roxo (Toxicidade/Ameixa)
        assert data["brainbow_color"] == "#aa00ff"
        assert data["agitation_level"] == 3.0
