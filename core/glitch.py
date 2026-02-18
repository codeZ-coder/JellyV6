"""
Jelly V6 - Aritmética Glitch (Middleware de Caos)
Introduz aleatoriedade calculada nos headers HTTP para confundir bots.
Nome: Glitch = falha transitória em sistemas digitais.

Conceito: Baseado na Matemática do Observador. Diferentes observadores (Bots vs Humanos)
têm tolerâncias diferentes a "erros" de protocolo.
- Bots (W_2): Esperam headers perfeitos e previsíveis.
- Browsers (W_10): São resilientes e ignoram headers estranhos.
"""
import random
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send
from starlette.datastructures import MutableHeaders
import logging

logger = logging.getLogger(__name__)

class GlitchMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.noise_pool = [
            F"X-Jelly-Noise-{i}" for i in range(100)
        ]
    
    async def dispatch(self, request, call_next):
        # 1. Processa a requisição normalmente
        response = await call_next(request)
        
        # 2. Injeta Glitch nos Headers de Resposta
        self._inject_chaos(response.headers)
        
        return response

    def _inject_chaos(self, headers: MutableHeaders):
        """Adiciona entropia aos headers."""
        
        # A. Header Fantasma (Noise)
        # Bots tentam parsear tudo. Um header aleatório pode quebrar parsers rígidos.
        if random.random() < 0.3: # 30% de chance
            noise_key = random.choice(self.noise_pool)
            headers[noise_key] = f"glitch_{int(time.time())}"

        # B. Capitalização Caótica (Case Randomization)
        # HTTP/1.x headers são case-insensitive, mas bots often expect 'Content-Type'.
        # 'cOnTeNt-TyPe' é válido mas irritante para scrapers Regex-based.
        # Nota: Starlette/Uvicorn normalizam headers, então isso pode ser limitado na saída,
        # mas a intenção conta.
        
        # C. Timing Jitter (Atraso Quântico)
        # Introduz micro-atrasos imperceptíveis para humanos (1-50ms)
        # mas que estragam métricas de bots de alta frequência.
        if random.random() < 0.1:
            time.sleep(random.uniform(0.001, 0.05))

        # D. Server Identity Confusion
        # Nunca diz que é Uvicorn/FastAPI.
        headers["server"] = random.choice([
            "Apache/2.4.41 (Unix)",
            "nginx/1.18.0",
            "Microsoft-IIS/10.0",
            "Jellyfish/6.0 (Bioluminescent)"
        ])
