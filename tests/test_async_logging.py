"""
🧪 Jelly V6 - Teste de Carga Forense (Async)
Verifica se o registro forense bloqueia o event loop principal.
"""
import time
import asyncio
import pytest
from unittest.mock import MagicMock
from core.nervenet import sistema_imunologico
from core.persistence import Persistence

@pytest.mark.asyncio
async def test_forensic_logging_is_non_blocking():
    """
    Simula uma chamada lenta ao banco de dados e verifica se o
    middleware continua respondendo rapidamente (não bloqueia).
    """
    # Mock do Request
    mock_request = MagicMock()
    mock_request.url.path = "/feed"
    mock_request.client.host = "1.2.3.4"

    # Mock do call_next (resposta da API)
    async def mock_call_next(req):
        return "OK"

    # Mock da Persistência LENTA (simula disco ocupado)
    def slow_log(*args):
        time.sleep(0.5)  # Bloqueio de 500ms se rodar na main thread
    
    # Injetar mock na instância global (monkeypatching manual para o teste)
    from core import nervenet
    nervenet.persistence.registrar_forense = slow_log
    
    # Bypass de Auth: Força o segredo e o header serem iguais
    nervenet.JELLY_DNA_SECRET = "AUTH_BYPASS"
    mock_request.headers.get.return_value = "AUTH_BYPASS"
    
    # Forçar defesa a disparar NEMATOCYST
    nervenet.membrane.process_request = MagicMock(return_value={
        "action": "NEMATOCYST",
        "pressure": 999,
        "diagnosis": "TESTE",
        "toxin_path": "assets/toxin.gz",
        "buffer_size": 10
    })

    # Medir tempo de resposta do middleware
    start = time.time()
    response = await sistema_imunologico(mock_request, mock_call_next)
    duration = time.time() - start

    # Asserts
    # Se fosse bloqueante, levaria > 0.5s. Como é async, deve ser instantâneo (< 0.1s)
    # Nota: O middleware retorna StreamingResponse no caso de NEMATOCYST, então ele retorna rápido.
    # O importante é que a linha 'await loop.run_in_executor' não espere o sleep(0.5) acabar.
    
    assert duration < 0.2, f"Middleware bloqueou por {duration:.2f}s (esperado < 0.2s)"
    assert hasattr(response, "body_iterator"), "Deveria retornar StreamingResponse (GZIP Bomb)"
