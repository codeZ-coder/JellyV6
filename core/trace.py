"""
Jelly V6 - Trace ID Middleware (Sistema Nervoso)
Gera um ID único para cada requisição e injeta no contexto.
Permite rastreabilidade de ponta a ponta (Observabilidade).
"""
import uuid
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging

# Configuração de Logger para suportar ContextVar se necessário
# mas por enquanto vamos injetar no request.state

class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Gerar ou recuperar Request ID
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # 2. Injetar no estado da requisição (para acesso nos endpoints)
        request.state.req_id = req_id
        
        # 3. Adicionar ao Logger (Contextual - requer configuração extra de logging, 
        # mas aqui vamos apenas garantir que os logs manuais possam acessar)
        
        start_time = time.time()
        
        # 4. Processar requisição
        response = await call_next(request)
        
        # 5. Calcular duração
        process_time = time.time() - start_time
        
        # 6. Injetar Headers na resposta
        response.headers["X-Jelly-Trace"] = req_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
