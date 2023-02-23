from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..models import Client
from ..models import User

from ..common import has_roles

from ..schemas import ClientResponseModel, ClientRequestModel

from ..services import update_client_service

router = APIRouter(prefix='/clients')


@router.post('/create_client', response_model=ClientResponseModel)
async def create_client(client: ClientRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
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


@router.get('/get_clients', response_model=List[ClientResponseModel])
async def get_clients(page: int = 1, limit: int = 10, userRole: User = Depends(has_roles(['admin', 'user']))):
    clients = Client.select().where(Client.user_created_id ==
                                    userRole.id).order_by(Client.name).paginate(page, limit)
    print(clients)

    return [client for client in clients]


@router.get('/get_client/{client_id}', response_model=ClientResponseModel)
async def get_client(client_id: int, userRole: User = Depends(has_roles(['admin', 'user']))):
    client = Client.get_or_none(
        Client.id == client_id, Client.user_created_id == userRole.id)
    if client is None:
        raise HTTPException(404, 'El cliente no existe')
    return client


@router.put('/update_client/{client_id}', response_model=ClientResponseModel)
async def update_client(client_id: int, client: ClientRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    client_updated = update_client_service(client_id, client, userRole)
    return client_updated


@router.delete('/delete_client/{client_id}')
async def delete_client(client_id: int, userRole: User = Depends(has_roles(['admin']))):
    client = Client.get_or_none(
        Client.id == client_id, Client.user_created_id == userRole.id)
    if client is None:
        raise HTTPException(404, 'El cliente no existe')
    client.delete_instance()
    return {'message': f'El cliente {client.name} ha sido eliminado'}
