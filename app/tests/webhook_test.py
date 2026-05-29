def _create_client(client, valor_patrimonio: float, email: str = "joao@example.com"):
    payload = {
        "cliente_nome": "João Silva",
        "cliente_email": email,
        "tipo_solicitacao": "Atualização cadastral",
        "valor_patrimonio": valor_patrimonio,
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 201
    return response.json()


WEBHOOK_PAYLOAD = {
    "event_id": "evt_001",
    "card_id": "card_456",
    "cliente_email": "joao@example.com",
    "timestamp": "2026-05-18T12:00:00Z",
}


def test_webhook_sets_prioridade_alta_for_high_patrimonio(client):
    # clientes com patrimônio >= 200.000 devem receber prioridade_alta
    _create_client(client, valor_patrimonio=250_000)

    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["prioridade"] == "prioridade_alta"
    assert body["status"] == "Processado"

def test_webhook_missing_event_id(client):
    
    # event_id é obrigatorio para garantir idempotencia, payload sem ele deve retornar 422
    payload = {k: v for k, v in WEBHOOK_PAYLOAD.items() if k != "event_id"}

    response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert response.status_code == 422
    
def test_webhook_missing_cliente_email(client):
    
    # cliente_email é obrigatorio para identificar o cliente, payload sem ele deve retornar 422
    payload = {
        k: v for k, v in WEBHOOK_PAYLOAD.items()
        if k != "cliente_email"
    }

    response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert response.status_code == 422
    
def test_webhook_invalid_email(client):
    # cliente_email com formato invalido deve retornar 422
    payload = {
        **WEBHOOK_PAYLOAD,
        "cliente_email": "email-invalido"
    }

    response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert response.status_code == 422
    
    
def test_webhook_empty_event_id(client):
    
    # event_id vazio deve retornar 422
    payload = {
        **WEBHOOK_PAYLOAD,
        "event_id": ""
    }

    response = client.post("/webhooks/pipefy/card-updated", json=payload)

    assert response.status_code == 422
    

def test_webhook_sets_prioridade_normal_for_low_patrimonio(client):
    # clientes com patrimônio < 200.000 devem receber prioridade_normal
    
    _create_client(client, valor_patrimonio=199_999)

    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert body["prioridade"] == "prioridade_normal"
    assert body["status"] == "Processado"


def test_webhook_priority_boundary_exactly_200k(client):
    
    # clientes com patrimônio exatamente 200.000 devem receber prioridade_alta
    _create_client(client, valor_patrimonio=200_000)

    response = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_PAYLOAD)

    assert response.status_code == 200
    assert response.json()["prioridade"] == "prioridade_alta"


def test_webhook_idempotency_blocks_duplicate_event(client):
   # mesmo event_id não pode ser processado mais de uma vez, segunda tentativa deve retornar 409
    _create_client(client, valor_patrimonio=250_000)

    first = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_PAYLOAD)
    assert first.status_code == 200

    second = client.post("/webhooks/pipefy/card-updated", json=WEBHOOK_PAYLOAD)
    assert second.status_code == 409
    assert "já foi processado" in second.json()["detail"]


def test_webhook_returns_404_for_unknown_email(client):
    # se o cliente_email do payload não corresponder a nenhum cliente cadastrado, deve retornar 404
    payload = {**WEBHOOK_PAYLOAD, "cliente_email": "naoexiste@example.com"}
    response = client.post("/webhooks/pipefy/card-updated", json=payload)
    assert response.status_code == 404