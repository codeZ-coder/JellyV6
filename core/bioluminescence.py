"""
Jelly V6 - Bioluminescência Tática (Deception)
Gera logs falsos para atrair atacantes para armadilhas.
Nome: Bioluminescência = luz emitida por seres vivos para atrair presas ou parceiros.

Conceito: Um arquivo 'debug.log' ou similar que contenha "vazamentos" de credenciais
e erros de stack trace falsos. Se um atacante ler isso (via LFI ou acesso indevido),
ele tentará usar as credenciais falsas, revelando sua presença.
"""
import logging
import random
import time
import threading
import os

logger = logging.getLogger(__name__)

class Bioluminescence:
    """Gerador de ruído tático e iscas (Fake Logs)."""

    def __init__(self, log_path: str = "jelly_debug.log"):
        self.log_path = log_path
        self.running = False
        self._thread = None
        
        # Vocabulário de Isca
        self.fake_users = ["admin", "root", "deploy", "db_backup", "jelly_master"]
        self.fake_passwords = ["123456", "password", "Jellyfish@2024", "admin123", "secret_key"]
        self.fake_dbs = ["users_prod", "payments", "jelly_core", "shadow_realm"]
        self.error_templates = [
            "Connection failed to DB '{db}' for user '{user}'. Retrying...",
            "WARNING: Deprecated API call from {ip}. Token: {token}",
            "CRITICAL: Dump saved to /tmp/{dump_file}. Do not share!",
            "DEBUG: Auth attempt failed. Expert password was '{password}'",
            "Traceback (most recent call last):\n  File 'core/secrets.py', line 42, in connect\n    raise ConnectionError('Invalid key: {key}')"
        ]

    def start(self):
        """Inicia o gerador de bioluminescência em background."""
        if self.running: return
        self.running = True
        self._thread = threading.Thread(target=self._emit_light, daemon=True)
        self._thread.start()
        logger.info(f"Bioluminescência ativa: {self.log_path} (Iscas brilhando)")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _emit_light(self):
        """Loop que escreve logs falsos esporadicamente."""
        while self.running:
            try:
                delay = random.uniform(30, 120)  # Intervalo irregular (30s a 2m)
                time.sleep(delay)
                
                if not self.running: break

                lure = self._generate_lure()
                
                with open(self.log_path, "a") as f:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {lure}\n")
                    
                # Opcional: Logar no logger real que uma isca foi plantada
                # logger.debug(f"Isca plantada: {lure[:30]}...")
                
            except Exception as e:
                logger.error(f"Erro na bioluminescência: {e}")

    def _generate_lure(self) -> str:
        """Cria uma string de log convincente."""
        template = random.choice(self.error_templates)
        
        return template.format(
            user=random.choice(self.fake_users),
            password=random.choice(self.fake_passwords),
            db=random.choice(self.fake_dbs),
            ip=f"192.168.1.{random.randint(10, 200)}",
            token=f"v2.local.{random.randint(10000,99999)}",
            dump_file=f"backup_{random.randint(2020, 2025)}.sql",
            key=f"sk_live_{'x'*16}"
        )

# Instância global para ser importada
biolum = Bioluminescence()
