# Mundo Invest — Client Management & Pipefy Integration

API REST em Python/FastAPI para gerenciamento de clientes e mapeamento de ações para o Pipefy via GraphQL.

---

## Estrutura de Pastas

```
.
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── README.md
└── app/
    ├── main.py                     # Ponto de entrada da aplicação FastAPI
    ├── database.py                 # Engine SQLite e SessionLocal
    ├── pytest.ini                  # Configuração do pytest
    ├── models/
    │   ├── client.py               # ORM: tabela `clientes`
    │   └── webhook_event.py        # ORM: tabela `webhook_events` (idempotência)
    ├── schemas/
    │   ├── client_schema.py        # Pydantic: validação de entrada do cliente
    │   └── webhook_schema.py       # Pydantic: validação de entrada do webhook
    ├── repositories/
    │   ├── client_repository.py    # Acesso a dados: clientes
    │   └── webhook_repository.py   # Acesso a dados: eventos de webhook
    ├── services/
    │   ├── client_service.py       # Regra de negócio: criação de cliente
    │   └── webhook_service.py      # Regra de negócio: processamento de webhook
    ├── routes/
    │   ├── client_routes.py        # Endpoint POST /clientes
    │   └── webhook_routes.py       # Endpoint POST /webhooks/pipefy/card-updated
    ├── integrations/
    │   └── pipefy_client.py        # Mutations GraphQL (createCard, updateCardField)
    └── tests/
        ├── conftest.py             # Fixtures compartilhadas (DB in-memory, TestClient)
        ├── client_test.py          # Testes do fluxo de criação de cliente
        └── webhook_test.py         # Testes do fluxo de webhook
```

---

## Execução com Docker (recomendado)

**Pré-requisito:** Docker Desktop instalado e rodando.

```bash
# 1. Clonar o repositório
git clone https://github.com/ThiagoChafado/AttusProject.git
cd AttusProject

# 2. Subir a API
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`

Para parar:
```bash
docker compose down
```

---

## Execução Local (sem Docker)

**Pré-requisitos:** Python 3.10+

```bash
pip install -r requirements.txt
cd app
uvicorn main:app --reload
```

---

## Executando os Testes

```bash
cd app
python -m pytest tests/ -v
```

---

## Exemplos de Requisição (curl)

### Fluxo 1 — Criar Cliente (`POST /clientes`)

```bash
curl -X POST http://localhost:8000/clientes \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_nome": "João Silva",
    "cliente_email": "joao.silva@example.com",
    "tipo_solicitacao": "Atualização cadastral",
    "valor_patrimonio": 250000
  }'
```

**Resposta esperada (201):**
```json
{
  "id": 1,
  "cliente_nome": "João Silva",
  "cliente_email": "joao.silva@example.com",
  "tipo_solicitacao": "Atualização cadastral",
  "valor_patrimonio": 250000.0
}
```

---

### Fluxo 2 — Simular Webhook (`POST /webhooks/pipefy/card-updated`)

```bash
curl -X POST http://localhost:8000/webhooks/pipefy/card-updated \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt_123",
    "card_id": "card_456",
    "cliente_email": "joao.silva@example.com",
    "timestamp": "2026-05-18T12:00:00Z"
  }'
```

**Resposta esperada (200):**
```json
{
  "event_id": "evt_123",
  "cliente_email": "joao.silva@example.com",
  "status": "Processado",
  "prioridade": "prioridade_alta"
}
```

---

## Mutations GraphQL do Pipefy

As mutations estão implementadas em `app/integrations/pipefy_client.py`.

### `createCard` — usada ao criar um cliente

```graphql
mutation CreateCard(
    $pipe_id: ID!,
    $fields_attributes: [FieldValueInput!]!
) {
    createCard(input: {
        pipe_id: $pipe_id,
        fields_attributes: $fields_attributes
    }) {
        card {
            id
            title
        }
    }
}
```

### `updateCardField` — usada ao processar o webhook

```graphql
mutation UpdateCardField(
    $cardId: ID!,
    $fieldId: String!,
    $newValue: [String]!
) {
    updateCardField(input: {
        card_id: $cardId,
        field_id: $fieldId,
        new_value: $newValue
    }) {
        card {
            id
            title
            current_phase { name }
        }
        success
    }
}
```


---

## Visão de Produção na AWS (Opcional)

Em produção, a estrutura escalaria da seguinte forma:

**API Gateway + Lambda**  
Cada endpoint seria exposto via API Gateway e executado em uma função AWS Lambda com o código FastAPI empacotado via Mangum. O Lambda escala automaticamente conforme a demanda, sem necessidade de gerenciar servidores.

**Banco de Dados**  
O SQLite seria substituído por **Amazon RDS (PostgreSQL)**. Para a tabela de idempotência de webhooks (`webhook_events`), o **DynamoDB** seria uma alternativa de alta performance, com TTL configurado para expirar eventos antigos automaticamente.

**Processamento de Webhooks**  
O endpoint de webhook poderia ser desacoplado usando uma fila **SQS**: o API Gateway recebe a requisição, publica na fila e retorna 202 imediatamente. Uma Lambda separada consome a fila e processa os eventos — garantindo resiliência a picos de tráfego e reprocessamento automático em caso de falha.

**Observabilidade**  
Logs centralizados no **CloudWatch**, alertas via **SNS**, e rastreamento distribuído via **AWS X-Ray** para identificar gargalos.