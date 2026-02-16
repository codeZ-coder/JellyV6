"""
Jelly V6 - Heartbeat Organ (Sinal de Vida)
Envia pulsos UDP para monitoramento externo sem expor portas TCP.
"""
import socket
import threading
import time
import json
import logging
import psutil

logger = logging.getLogger(__name__)

class Heartbeat:
    def __init__(self, dest_ip="127.0.0.1", dest_port=9999, interval=60):
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.interval = interval
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self._thread = None

    def start(self):
        if self.running: return
        self.running = True
        self._thread = threading.Thread(target=self._pulse, daemon=True)
        self._thread.start()
        logger.info(f"Heartbeat: Pulsando para {self.dest_ip}:{self.dest_port} (UDP)")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=1.0)

    def _pulse(self):
        while self.running:
            try:
                # Payload compacta
                stats = {
                    "status": "ALIVE",
                    "cpu": psutil.cpu_percent(),
                    "ram": psutil.virtual_memory().percent,
                    "ts": time.time()
                }
                msg = json.dumps(stats).encode('utf-8')
                self.socket.sendto(msg, (self.dest_ip, self.dest_port))
                time.sleep(self.interval)
            except Exception as e:
                logger.error(f"Heartbeat falhou: {e}")
                time.sleep(10) # Backoff

# Instancia global
heartbeat = Heartbeat()
