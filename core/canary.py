"""
Jelly V6 - Canary Module (Deteccao de Intrusao Passiva)
Cria arquivos isca (canary/decoy) em locais estrategicos.
Se alguem lê ou modifica esses arquivos, e sinal de intrusao.

Inspirado em:
- Stephen Wiesner (quantum money / trap states)
- Canary tokens / honeytokens
"""
import os
import time
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CanaryFile:
    """
    Gerencia arquivos isca que detectam acesso nao autorizado.
    Monitora o atime (ultimo acesso) e mtime (ultima modificacao).
    """

    def __init__(self, canary_dir: str = "canary_nest"):
        """
        Args:
            canary_dir: Diretorio raiz para os canary files.
        """
        self.canary_dir = canary_dir
        self.canaries: Dict[str, dict] = {}
        self._ensure_nest()

    def _ensure_nest(self):
        """Cria o diretorio do ninho se nao existir."""
        os.makedirs(self.canary_dir, exist_ok=True)

    def plant(self, filename: str, content: str = None) -> str:
        """
        Planta um arquivo isca.
        
        Args:
            filename: Nome do arquivo isca (ex: 'credentials.txt')
            content: Conteudo falso. Se None, gera conteudo generico.
        
        Returns:
            Caminho completo do arquivo plantado.
        """
        if content is None:
            content = self._generate_bait(filename)

        filepath = os.path.join(self.canary_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)

        # Captura baseline (atime e mtime)
        stat = os.stat(filepath)
        self.canaries[filepath] = {
            "name": filename,
            "planted_at": time.time(),
            "baseline_atime": stat.st_atime,
            "baseline_mtime": stat.st_mtime,
            "tripped": False,
            "trip_type": None
        }

        logger.info(f"Canary plantado: {filename}")
        return filepath

    def _generate_bait(self, filename: str) -> str:
        """Gera conteudo falso convincente baseado no nome do arquivo."""
        baits = {
            "credentials.txt": "# Database Credentials\nDB_HOST=192.168.1.100\nDB_USER=admin\nDB_PASS=S3cur3P@ss!2024\nDB_PORT=5432\n",
            "backup_keys.pem": "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGcY5unA3aCTq6Rp\nNOTE: THIS IS A FAKE KEY - CANARY TOKEN\n-----END RSA PRIVATE KEY-----\n",
            ".env.production": "SECRET_KEY=xK9#mP2$vL5nR8@jQ4wT7yU0\nAWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE\nAWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n",
            "api_tokens.json": '{\n  "stripe_live": "sk_live_FAKE_canary_token_12345",\n  "github_pat": "ghp_FAKE_canary_token_67890",\n  "note": "rotated quarterly"\n}\n',
        }
        return baits.get(filename, f"# Canary file: {filename}\n# Planted at {time.strftime('%Y-%m-%d %H:%M:%S')}\nSENSITIVE_DATA=canary_trap_{int(time.time())}\n")

    def check_all(self) -> dict:
        """
        Verifica se algum canary foi acessado ou modificado.
        
        Returns:
            dict com:
                - alert (bool): True se algum canary foi tripado
                - tripped (list): Canaries que dispararam
                - intact (int): Quantidade de canaries intactos
        """
        tripped = []

        for filepath, canary in self.canaries.items():
            if not os.path.exists(filepath):
                # Arquivo deletado = intrusao obvia
                canary["tripped"] = True
                canary["trip_type"] = "DELETED"
                tripped.append({
                    "file": canary["name"],
                    "type": "DELETED",
                    "detail": "Arquivo isca foi removido"
                })
                logger.critical(f"CANARY DELETADO: {canary['name']}")
                continue

            stat = os.stat(filepath)

            # Verificar modificacao
            if stat.st_mtime != canary["baseline_mtime"]:
                canary["tripped"] = True
                canary["trip_type"] = "MODIFIED"
                tripped.append({
                    "file": canary["name"],
                    "type": "MODIFIED",
                    "detail": f"mtime mudou: {canary['baseline_mtime']} -> {stat.st_mtime}"
                })
                logger.critical(f"CANARY MODIFICADO: {canary['name']}")

            # Verificar leitura (atime)
            # Nota: atime pode ser desabilitado (noatime mount), entao nao e 100% confiavel
            elif stat.st_atime > canary["baseline_atime"] + 1.0:
                canary["tripped"] = True
                canary["trip_type"] = "READ"
                tripped.append({
                    "file": canary["name"],
                    "type": "READ",
                    "detail": f"Acesso detectado: {stat.st_atime - canary['baseline_atime']:.0f}s apos plantio"
                })
                logger.warning(f"CANARY LIDO: {canary['name']}")

        alert = len(tripped) > 0
        intact = sum(1 for c in self.canaries.values() if not c["tripped"])

        return {
            "alert": alert,
            "tripped": tripped,
            "intact": intact,
            "total": len(self.canaries)
        }

    def plant_default_nest(self):
        """Planta o conjunto padrao de canaries em locais tentadores."""
        defaults = [
            "credentials.txt",
            "backup_keys.pem",
            ".env.production",
            "api_tokens.json",
        ]
        for name in defaults:
            self.plant(name)
        logger.info(f"Ninho de canaries plantado: {len(defaults)} iscas")

    def get_status(self) -> dict:
        """Retorna status rapido para endpoints."""
        tripped_count = sum(1 for c in self.canaries.values() if c["tripped"])
        return {
            "total_canaries": len(self.canaries),
            "tripped": tripped_count,
            "intact": len(self.canaries) - tripped_count,
            "files": [c["name"] for c in self.canaries.values()]
        }
