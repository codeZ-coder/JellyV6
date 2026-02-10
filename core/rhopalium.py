"""
🪼 Jelly V6 - Rhopalium Module (Sensores)
Encapsula toda leitura de hardware via psutil.
Nome: Rhopalium = órgão sensorial das águas-vivas reais.
"""
import psutil
import time
import logging

logger = logging.getLogger(__name__)


class Rhopalium:
    """Sensores da Jelly — lê CPU, RAM, Disco e Rede"""

    def __init__(self):
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

    def read_vitals(self) -> dict:
        """
        Lê todos os sensores e retorna métricas processadas.
        Calcula delta de rede (KB/s) automaticamente.
        """
        net = psutil.net_io_counters()
        t = time.time()
        dt = t - self.last_time
        if dt == 0:
            dt = 0.1

        # Velocidade real em KB/s (delta)
        down_kbps = (net.bytes_recv - self.last_net.bytes_recv) / 1024 / dt
        up_kbps = (net.bytes_sent - self.last_net.bytes_sent) / 1024 / dt

        # Atualiza estado para próxima leitura
        self.last_net = net
        self.last_time = t

        return {
            "cpu": psutil.cpu_percent(interval=None),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "down_kbps": down_kbps,
            "up_kbps": up_kbps,
            "timestamp": t
        }
