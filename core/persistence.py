"""
🪼 Jelly V6 - Persistence Module
Gerencia toda interação com SQLite WAL: schema, memória neural e forense.
"""
import sqlite3
import subprocess
import time
import threading
import logging

logger = logging.getLogger(__name__)


class Persistence:
    """Memória de longo prazo da Jelly (SQLite WAL)"""

    def __init__(self, db_name: str = "jelly.db"):
        self.db_name = db_name
        self.last_save = 0
        self._init_db()

    def _init_db(self):
        """Cria as tabelas se não existirem + ativa WAL"""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        c = conn.cursor()

        # 1. Histórico Vital (Expandido)
        c.execute('''CREATE TABLE IF NOT EXISTS vitals_history
                     (timestamp REAL, cpu REAL, ram REAL, disk REAL, 
                      stress REAL, z_score REAL, down_kbps REAL, up_kbps REAL)''')

        # 2. Eventos Forenses (O "Ferrão")
        c.execute('''CREATE TABLE IF NOT EXISTS forensic_events
                     (timestamp REAL, trigger_type TEXT, details TEXT, raw_snapshot TEXT)''')

        # 3. Memória Neural (Key-Value para aprendizado persistente)
        c.execute('''CREATE TABLE IF NOT EXISTS neuro_memory
                     (key TEXT PRIMARY KEY, value REAL)''')

        conn.commit()
        conn.close()
        logger.info("SQLite WAL inicializado")

    def salvar_memoria(self, key: str, value: float):
        """Persiste um valor na memória neural"""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute("INSERT OR REPLACE INTO neuro_memory VALUES (?, ?)", (key, value))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Erro Memória: {e}")

    def carregar_memoria(self, key: str, default: float) -> float:
        """Carrega um valor da memória neural"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.execute("SELECT value FROM neuro_memory WHERE key=?", (key,))
            row = cursor.fetchone()
            conn.close()
            return row[0] if row else default
        except Exception as e:
            logger.error(f"Erro ao carregar memória: {e}")
            return default

    def registrar_evento_forense(self, trigger: str, details: str):
        """
        Captura conexões de rede (ss -tunap) e salva no banco.
        Deve ser chamado em thread separada para não bloquear a API.
        """
        try:
            result = subprocess.run(
                ['ss', '-tunap'],
                capture_output=True, text=True, shell=False
            )
            snapshot = result.stdout

            conn = sqlite3.connect(self.db_name)
            conn.execute(
                "INSERT INTO forensic_events VALUES (?, ?, ?, ?)",
                (time.time(), trigger, details, snapshot)
            )
            conn.commit()
            conn.close()
            logger.warning(f"FORENSE REGISTRADA: {trigger}")
        except Exception as e:
            logger.error(f"Erro Forense: {e}")

    def registrar_forense_async(self, trigger: str, details: str):
        """Dispara registro forense em thread separada (não bloqueia)"""
        threading.Thread(
            target=self.registrar_evento_forense,
            args=(trigger, details)
        ).start()

    def salvar_vitals(self, t: float, cpu: float, ram: float,
                      disk: float, score: float, z_val: float,
                      down: float, up: float):
        """Persistência rotineira (a cada 60s)"""
        if t - self.last_save > 60:
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute(
                    "INSERT INTO vitals_history VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (t, cpu, ram, disk, score, z_val, down, up)
                )
                conn.commit()
                conn.close()
                self.last_save = t
                logger.info(f"Memória: Stress={score:.1f} | Rede Z={z_val:.1f}")
            except Exception as e:
                logger.error(f"Erro SQLite: {e}")
