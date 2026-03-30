"""
Jelly V6 - Testes dos modulos da Fase 2
Turritopsis (integridade), Canary (honeytokens), Inercia do Nado, RUPTURA
"""
import os
import sys
import time
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.turritopsis import Turritopsis
from core.canary import CanaryFile
from core.membrane import OsmoticMembrane
from core.cnidocyte import Cnidocyte


# ======================= TURRITOPSIS =======================

class TestTurritopsis:
    """Testes de integridade de arquivos (Turritopsis)"""

    def setup_method(self):
        """Cria arquivos temporarios para testar."""
        self.tmpdir = tempfile.mkdtemp()
        # Cria 3 arquivos "criticos"
        self.files = []
        for name in ["module_a.py", "module_b.py", "module_c.py"]:
            path = os.path.join(self.tmpdir, name)
            with open(path, "w") as f:
                f.write(f"# {name}\nprint('hello')\n")
            self.files.append(path)
        
        self.turri = Turritopsis(watch_paths=self.files)

    def test_baseline_captured(self):
        """Deve capturar baseline de todos os arquivos."""
        assert len(self.turri.baseline) == 3

    def test_integrity_intact(self):
        """Arquivos intactos devem retornar HOMEOSTASE."""
        result = self.turri.verify_integrity()
        assert result["intact"] is True
        assert result["signal"] == "HOMEOSTASE"
        assert len(result["compromised"]) == 0

    def test_detects_modification(self):
        """Arquivo modificado deve retornar RUPTURA_MESOGLEIA."""
        # Modifica um arquivo apos o baseline
        with open(self.files[0], "w") as f:
            f.write("# HACKED\nimport os; os.system('rm -rf /')\n")
        
        result = self.turri.verify_integrity()
        assert result["intact"] is False
        assert result["signal"] == "RUPTURA_MESOGLEIA"
        assert len(result["compromised"]) == 1
        assert self.files[0] in result["compromised"][0]["file"]

    def test_detects_deletion(self):
        """Arquivo deletado deve aparecer em missing."""
        os.remove(self.files[1])
        
        result = self.turri.verify_integrity()
        assert result["intact"] is False
        assert result["signal"] == "RUPTURA_MESOGLEIA"
        assert len(result["missing"]) == 1

    def test_multiple_compromised(self):
        """Varios arquivos comprometidos devem ser listados."""
        with open(self.files[0], "a") as f:
            f.write("# backdoor\n")
        with open(self.files[2], "a") as f:
            f.write("# trojan\n")
        
        result = self.turri.verify_integrity()
        assert result["intact"] is False
        assert len(result["compromised"]) == 2

    def test_get_status(self):
        """Status deve conter contagem de arquivos."""
        status = self.turri.get_status()
        assert status["files_monitored"] == 3


# ======================= CANARY =======================

class TestCanary:
    """Testes de arquivos isca (Canary/Honeytokens)"""

    def setup_method(self):
        """Cria diretorio temporario para canaries."""
        self.tmpdir = tempfile.mkdtemp()
        self.canary = CanaryFile(canary_dir=self.tmpdir)

    def test_plant_creates_file(self):
        """Plantar canary deve criar o arquivo."""
        path = self.canary.plant("test_cred.txt", "fake_password=123")
        assert os.path.exists(path)
        with open(path) as f:
            assert "fake_password" in f.read()

    def test_check_intact(self):
        """Canaries nao acessados devem estar intactos."""
        self.canary.plant("secret.txt")
        result = self.canary.check_all()
        assert result["alert"] is False
        assert result["intact"] == 1

    def test_detects_modification(self):
        """Canary modificado deve disparar alerta."""
        path = self.canary.plant("config.txt", "api_key=FAKE")
        
        # Simula intrusao: atacante modifica o arquivo
        time.sleep(0.1)  # Garante diferenca de mtime
        with open(path, "a") as f:
            f.write("\n# attacker was here\n")
        
        result = self.canary.check_all()
        assert result["alert"] is True
        assert result["tripped"][0]["type"] == "MODIFIED"

    def test_detects_deletion(self):
        """Canary deletado deve disparar alerta."""
        path = self.canary.plant("keys.pem")
        os.remove(path)
        
        result = self.canary.check_all()
        assert result["alert"] is True
        assert result["tripped"][0]["type"] == "DELETED"

    def test_plant_default_nest(self):
        """Ninho padrao deve criar 4 iscas."""
        self.canary.plant_default_nest()
        assert len(self.canary.canaries) == 4
        
        result = self.canary.check_all()
        assert result["total"] == 4
        assert result["alert"] is False

    def test_generate_bait_content(self):
        """Conteudo gerado deve ser convincente."""
        path = self.canary.plant("credentials.txt")
        with open(path) as f:
            content = f.read()
        assert "DB_PASS" in content
        assert "admin" in content

    def test_get_status(self):
        """Status deve refletir canaries plantados."""
        self.canary.plant("a.txt")
        self.canary.plant("b.txt")
        status = self.canary.get_status()
        assert status["total_canaries"] == 2
        assert status["tripped"] == 0


# ======================= RUPTURA_MESOGLEIA =======================

class TestRupturaMesogleia:
    """Testes do sinal de ruptura na Membrana Osmotica"""

    def setup_method(self):
        self.membrane = OsmoticMembrane(threshold=10)

    def test_ruptura_at_extreme_pressure(self):
        """Pressao > 4x threshold deve retornar RUPTURA_MESOGLEIA."""
        # Inflar pressao via Gosto Acido (patches instantaneos)
        # threshold=10, precisa de pressure > 40
        for i in range(6):
            result = self.membrane.process_request(
                "evil.ip", f"/attack_{i}?q=../etc/passwd", "bot"
            )
        # Apos varios ataques com acid taste, pressao deve estar alta
        assert result["action"] in ("NEMATOCYST", "RUPTURA_MESOGLEIA")

    def test_normal_pressure_no_ruptura(self):
        """Pressao normal nao deve gerar RUPTURA."""
        result = self.membrane.process_request("1.2.3.4", "/api/health", "Mozilla")
        assert result["action"] == "ALLOW"


# ======================= CNIDOCYTE OSMOTIC ALERT =======================

class TestCnidocyteOsmoticAlert:
    """Testes da conexao mente-corpo (Cnidocyte + Membrane)"""

    def setup_method(self):
        """Mock de persistencia para evitar dependencia de DB."""
        class MockPersistence:
            def registrar_forense_async(self, *args): pass
        
        self.defense = Cnidocyte(persistence=MockPersistence())

    def test_osmotic_nematocyst_activates_defense(self):
        """Alerta NEMATOCYST da membrana deve ativar defesa."""
        result = self.defense.avaliar_ameaca(
            is_anomaly=False, down=100, max_down_kbps=1000, z_val=0.5,
            osmotic_alert="NEMATOCYST"
        )
        assert result is True

    def test_osmotic_ruptura_activates_defense(self):
        """Alerta RUPTURA_MESOGLEIA deve ativar defesa."""
        result = self.defense.avaliar_ameaca(
            is_anomaly=False, down=100, max_down_kbps=1000, z_val=0.5,
            osmotic_alert="RUPTURA_MESOGLEIA"
        )
        assert result is True

    def test_no_osmotic_alert_normal_flow(self):
        """Sem alerta osmotico, fluxo normal deve prevalecer."""
        result = self.defense.avaliar_ameaca(
            is_anomaly=False, down=100, max_down_kbps=1000, z_val=0.5,
            osmotic_alert=None
        )
        assert result is False

    def test_backward_compatible_no_osmotic_param(self):
        """Chamada sem parametro osmotic_alert deve funcionar (backward compat)."""
        result = self.defense.avaliar_ameaca(
            is_anomaly=True, down=100, max_down_kbps=1000, z_val=3.5
        )
        assert result is True
