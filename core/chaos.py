"""
Jelly V6 - Chaos Llama (Sistema Imunológico Ativo)
Lhama do Caos: Injeta falhas e ataques simulados para testar a resiliência.
Nome: Inspirado no "Chaos Monkey" da Netflix, mas adaptado para dados/segurança.
"""
import asyncio
import random
import logging
import httpx
import time

logger = logging.getLogger(__name__)

class ChaosLlama:
    def __init__(self, target_url="http://127.0.0.1:8000", interval=3600):
        self.target_url = target_url
        self.interval = interval
        self.running = False
        self._task = None
        self.attacks = [
            self._attack_acid,
            self._attack_pressure,
            self._attack_probe
        ]

    def start(self):
        if self.running: return
        self.running = True
        self._task = asyncio.create_task(self._chaos_loop())
        logger.info("Chaos Llama: 🦙 Lhama do Caos solta no pasto!")

    def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()

    async def _chaos_loop(self):
        while self.running:
            # Dorme um tempo aleatório (0.5x a 1.5x do intervalo)
            sleep_time = self.interval * random.uniform(0.5, 1.5)
            logger.debug(f"Chaos Llama: Dormindo por {sleep_time:.1f}s...")
            try:
                await asyncio.sleep(sleep_time)
            except asyncio.CancelledError:
                break
            
            # Escolhe um ataque
            attack_func = random.choice(self.attacks)
            logger.warning(f"Chaos Llama: ⚔️ INICIANDO AUTO-TESTE ({attack_func.__name__})")
            
            try:
                await attack_func()
            except Exception as e:
                logger.error(f"Chaos Llama falhou no ataque: {e}")

    async def _attack_acid(self):
        """Simula ataque de injeção (Gosto Ácido)."""
        async with httpx.AsyncClient() as client:
            # Tenta acessar /admin com SQLi
            resp = await client.get(f"{self.target_url}/admin?q=' OR 1=1 --")
            logger.info(f"Chaos Llama (Acid): Recebeu {resp.status_code}")

    async def _attack_pressure(self):
        """Simula pico de tráfego."""
        async with httpx.AsyncClient() as client:
            tasks = []
            for _ in range(20):
                tasks.append(client.get(f"{self.target_url}/vitals"))
            await asyncio.gather(*tasks)
            logger.info("Chaos Llama (Pressure): Disparou 20 requests.")

    async def _attack_probe(self):
        """Simula scan furtivo."""
        async with httpx.AsyncClient() as client:
            headers = {"User-Agent": "Nmap/7.92"}
            await client.get(f"{self.target_url}/.env", headers=headers)
            logger.info("Chaos Llama (Probe): Sondou honeypot.")

chaos_llama = ChaosLlama(interval=300) # 5 minutos default
