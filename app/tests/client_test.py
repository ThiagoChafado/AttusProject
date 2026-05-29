
VALID_PAYLOAD = {
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000,
}

def test_create_client_empty_name(client):
    #nome vazio deve retornar 422
    payload = {**VALID_PAYLOAD, "cliente_nome": ""}
    
    response = client.post("/clientes", json=payload)

    assert response.status_code == 422

def test_create_client_success(client):
    # teste valido deve retornar 201 e os dados corretos
    response = client.post("/clientes", json=VALID_PAYLOAD)

    assert response.status_code == 201
    body = response.json()
    assert body["cliente_email"] == VALID_PAYLOAD["cliente_email"]
    assert body["cliente_nome"] == VALID_PAYLOAD["cliente_nome"]
    assert body["valor_patrimonio"] == VALID_PAYLOAD["valor_patrimonio"]

def test_create_client_negative_patrimony(client):
    # patrimonio negativo deve retornar 422
    payload = {**VALID_PAYLOAD, "valor_patrimonio": -100}

    response = client.post("/clientes", json=payload)

    assert response.status_code == 422

def test_create_client_zero_patrimony(client):
    # patrimonio zero deve ser aceito
    payload = {**VALID_PAYLOAD, "valor_patrimonio": 0}

    response = client.post("/clientes", json=payload)

    assert response.status_code == 201
    
    
def test_create_client_invalid_patrimony_type(client):
    # patrimonio com tipo invalido deve retornar 422
    payload = {**VALID_PAYLOAD, "valor_patrimonio": "muito dinheiro"}

    response = client.post("/clientes", json=payload)

    assert response.status_code == 422
    
    
def test_create_client_missing_body(client):
    # request sem body deve retornar 422
    response = client.post("/clientes")

    assert response.status_code == 422
    
    
def test_create_client_persists_and_rejects_duplicate(client):
    # cliente criado deve ser persistido e duplicado deve retornar 409
    client.post("/clientes", json=VALID_PAYLOAD)

    response = client.post("/clientes", json=VALID_PAYLOAD)
    assert response.status_code == 409
    assert "já cadastrado" in response.json()["detail"]


def test_create_client_invalid_email(client):
    # payload com e-mail invalido deve retornar 422
    payload = {**VALID_PAYLOAD, "cliente_email": "not-an-email"}
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422


def test_create_client_missing_required_field(client):
    # payload sem campo obrigatorio deve retornar 422
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "cliente_nome"}
    response = client.post("/clientes", json=payload)
    assert response.status_code == 422