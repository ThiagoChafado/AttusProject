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


class PipefyClient:

    def build_create_card_payload(self, client):

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