from fastapi import HTTPException

from ..models import Client, User
from ..schemas import ClientRequestModel
from fastapi import HTTPException


class ClientService:
    @staticmethod
    def create_client_service(client: ClientRequestModel, userRole: User):
        try:
            if Client.select().where(Client.name == client.name).exists():
                raise HTTPException(409, 'El cliente ya existe')
            client_created = Client.create(
                name=client.name,
                direction=client.direction,
                phone=client.phone,
                email=client.email,
                user_created_id=userRole.id
            )
            return client_created
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    def get_client_service(client_id: int, userRole: User):
        client = Client.get_or_none(
            Client.id == client_id, Client.user_created_id == userRole.id)
        if client is None:
            raise HTTPException(404, 'El cliente no existe')
        return client

    @staticmethod
    def get_clients_service(user_id: int, page: int = 1, limit: int = 10):
        try:
            clients = Client.select().where(Client.user_created_id == user_id).order_by(
                Client.name).order_by(Client.created_at).paginate(page, limit)
            return [client for client in clients]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_client_service(client_id: int, client: ClientRequestModel, userRole: User):
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
