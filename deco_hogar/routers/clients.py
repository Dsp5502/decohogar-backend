from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..models import Client
from ..models import User

from ..common import has_roles

from ..schemas import ClientResponseModel, ClientRequestModel

from ..services import ClientService

router = APIRouter(prefix='/clients')


@router.post('/create_client', response_model=ClientResponseModel)
async def create_client(client: ClientRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    client_created = ClientService.create_client_service(client, userRole)
    return client_created


@router.get('/get_clients', response_model=List[ClientResponseModel])
async def get_clients(page: int = 1, limit: int = 10, userRole: User = Depends(has_roles(['admin', 'user']))):
    clients = ClientService.get_clients_service(userRole.id, page, limit)
    return clients


@router.get('/get_client/{client_id}', response_model=ClientResponseModel)
async def get_client(client_id: int, userRole: User = Depends(has_roles(['admin', 'user']))):
    try:
        client = ClientService.get_client_service(client_id, userRole)
        return client
    except HTTPException as e:
        raise e


@router.put('/update_client/{client_id}', response_model=ClientResponseModel)
async def update_client(client_id: int, client: ClientRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    client_updated = ClientService.update_client_service(
        client_id, client, userRole)
    return client_updated


@router.delete('/delete_client/{client_id}')
async def delete_client(client_id: int, userRole: User = Depends(has_roles(['admin']))):
    client = Client.get_or_none(
        Client.id == client_id, Client.user_created_id == userRole.id)
    if client is None:
        raise HTTPException(404, 'El cliente no existe')
    client.delete_instance()
    return {'message': f'El cliente {client.name} ha sido eliminado'}
