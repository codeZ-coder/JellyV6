"""
Jelly V6 - Turritopsis Module (Integridade)
Verifica integridade de arquivos criticos via hash SHA-256.
Nome: Turritopsis = genero da agua-viva imortal que reverte ao estagio de polipo.

Conceito: Se arquivos criticos foram modificados, o organismo sinaliza RUPTURA
para que o orquestrador (Docker) reinicie o container a partir de uma imagem limpa.
"""
import hashlib
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class Turritopsis:
    """
    Verificador de integridade baseado na agua-viva imortal.
    Captura baseline de hashes no startup e compara periodicamente.
    """

    def __init__(self, watch_paths: list = None):
        """
        Args:
            watch_paths: Lista de arquivos/diretorios para monitorar.
                        Se None, monitora os modulos core/ por padrao.
        """
        self.watch_paths = watch_paths or self._default_paths()
        self.baseline: Dict[str, str] = {}
        self.compromised_files: list = []
        self._capture_baseline()

    def _default_paths(self) -> list:
        """Retorna os arquivos criticos do organismo."""
        core_dir = os.path.dirname(os.path.abspath(__file__))
        critical_files = []
        for f in os.listdir(core_dir):
            if f.endswith(".py") and not f.startswith("__"):
                critical_files.append(os.path.join(core_dir, f))
        return sorted(critical_files)

    def _hash_file(self, filepath: str) -> Optional[str]:
        """Calcula SHA-256 de um arquivo."""
        try:
            h = hashlib.sha256()
            with open(filepath, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    h.update(chunk)
            return h.hexdigest()
        except (OSError, IOError) as e:
            logger.error(f"Turritopsis: Erro ao ler {filepath}: {e}")
            return None

    def _capture_baseline(self):
        """Captura o estado saudavel (baseline) de todos os arquivos monitorados."""
        self.baseline.clear()
        for path in self.watch_paths:
            file_hash = self._hash_file(path)
            if file_hash:
                self.baseline[path] = file_hash
        logger.info(f"Turritopsis: Baseline capturado ({len(self.baseline)} arquivos)")

    def verify_integrity(self) -> dict:
        """
        Verifica se algum arquivo critico foi modificado desde o baseline.
        
        Returns:
            dict com:
                - intact (bool): True se tudo OK
                - compromised (list): Arquivos modificados
                - missing (list): Arquivos que sumiram
                - signal (str): "HOMEOSTASE" ou "RUPTURA_MESOGLEIA"
        """
        compromised = []
        missing = []

        for path, expected_hash in self.baseline.items():
            if not os.path.exists(path):
                missing.append(path)
                logger.critical(f"Turritopsis: ARQUIVO DESAPARECEU: {path}")
                continue

            current_hash = self._hash_file(path)
            if current_hash != expected_hash:
                compromised.append({
                    "file": path,
                    "expected": expected_hash[:16] + "...",
                    "actual": (current_hash[:16] + "...") if current_hash else "ERRO"
                })
                logger.critical(f"Turritopsis: HASH DIVERGENTE: {os.path.basename(path)}")

        self.compromised_files = compromised

        if compromised or missing:
            return {
                "intact": False,
                "compromised": compromised,
                "missing": missing,
                "signal": "RUPTURA_MESOGLEIA",
                "total_monitored": len(self.baseline)
            }

        return {
            "intact": True,
            "compromised": [],
            "missing": [],
            "signal": "HOMEOSTASE",
            "total_monitored": len(self.baseline)
        }

    def get_status(self) -> dict:
        """Retorna status rapido para o endpoint /vitals."""
        return {
            "files_monitored": len(self.baseline),
            "last_compromised": len(self.compromised_files),
            "files": [os.path.basename(f) for f in self.baseline.keys()]
        }
