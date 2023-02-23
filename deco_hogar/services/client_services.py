from fastapi import HTTPException

from ..models import Client, User
from ..schemas import ClientRequestModel


def update_client(client_id: int, client: ClientRequestModel, userRole: User):
    client_updated = Client.get_or_none(
        Client.id == client_id, Client.user_created_id == userRole.id)
    if client_updated is None:
        raise HTTPException(404, 'El cliente no existe')
    client_updated.name = client.name
    client_updated.direction = client.direction
    client_updated.phone = client.phone
    client_updated.email = client.email
    client_updated.save()
    return client_updated
