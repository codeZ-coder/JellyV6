"""
Jelly V6 - GFP Marker (Green Fluorescent Protein)
Tagging digital persistente para rastrear atacantes individuais (Brainbow tracking).
"""
import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
import logging

logger = logging.getLogger(__name__)

class GFPMiddleware(BaseHTTPMiddleware):
    """
    Injeta um marcador 'biológico' (Cookie/ETag) no cliente.
    Permite rastrear o mesmo 'indivíduo' mesmo que ele troque de IP (pele).
    """
    
    async def dispatch(self, request: Request, call_next):
        # 1. Tenta identificar o marcador GFP existente
        gfp_id = request.cookies.get("jelly_gfp")
        
        # Se nao tem cookie, tenta header (para ferramentas que suportam)
        if not gfp_id:
            gfp_id = request.headers.get("X-Jelly-GFP")

        # 2. Se é um organismo novo, marca com uma nova proteína
        is_new_organism = False
        if not gfp_id:
            gfp_id = str(uuid.uuid4())
            is_new_organism = True
            # logger.info(f"🦠 GFP: Novo organismo marcado [{gfp_id}] IP: {request.client.host}")
        
        # 3. Injeta o ID no escopo da requisição para outros módulos usarem (ex: Logs)
        request.state.gfp_id = gfp_id
        
        # 4. Processa a requisição
        response = await call_next(request)
        
        # 5. Persiste o marcador na resposta (Re-infecção)
        # Cookie HTTPOnly (mais difícil de limpar via script simples)
        response.set_cookie(
            key="jelly_gfp",
            value=gfp_id,
            max_age=31536000, # 1 ano (persistência longa)
            httponly=True,
            samesite="lax"
        )
        
        # Header customizado (para scripts que leem headers)
        response.headers["X-Jelly-GFP"] = gfp_id
        
        # ETag (Bioluminescência passiva - browsers enviam If-None-Match)
        response.headers["ETag"] = f'W/"{gfp_id}"'
        
        return response
