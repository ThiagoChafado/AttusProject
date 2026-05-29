# Pipefy GraphQL Mutations
# https://developers.pipefy.com/reference/cards

CREATE_CARD_MUTATION = """
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
"""

# updateCardField é a mutation oficial do pipefy para atualizar um unico valor de campo em um card existente.

UPDATE_CARD_FIELD_MUTATION = """
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
            current_phase {
                name
            }
        }
        success
    }
}
"""


class PipefyClient:

    def build_create_card_payload(self, client):
        """
        constroi o payload do graphql para criar um novo card no Pipefy
        quando um cliente é registrado pela primeira vez
        """
        return {
            "query": CREATE_CARD_MUTATION,
            "variables": {
                "pipe_id": "123456",
                "fields_attributes": [
                    {
                        "field_id": "cliente_nome",
                        "field_value": client.cliente_nome
                    },
                    {
                        "field_id": "cliente_email",
                        "field_value": client.cliente_email
                    },
                    {
                        "field_id": "valor_patrimonio",
                        "field_value": str(client.valor_patrimonio)
                    }
                ]
            }
        }

    def build_update_status_payload(self, card_id: str, status: str):
        """
        constroi o payload do graphql para atualizar o campo de status em um
        card existente no Pipefy 
        """
        return {
            "query": UPDATE_CARD_FIELD_MUTATION,
            "variables": {
                "cardId": card_id,
                "fieldId": "status_cliente",
                "newValue": [status]
            }
        }

    def build_update_priority_payload(self, card_id: str, prioridade: str):
        """
        constroi o payload do graphql para atualizar o campo de prioridade em um
        card existente no Pipefy
        """
        return {
            "query": UPDATE_CARD_FIELD_MUTATION,
            "variables": {
                "cardId": card_id,
                "fieldId": "prioridade",
                "newValue": [prioridade]
            }
        }