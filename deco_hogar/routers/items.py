from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..models import User
from ..models import Item

from ..schemas import ItemResponseModel, ItemRequestModel

from ..services import ItemService

from ..common import has_roles

router = APIRouter(prefix='/items')


@router.post('/create_item', response_model=ItemResponseModel)
async def create_item(item: ItemRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    item_created = ItemService.item_create_service(item, userRole)
    return item_created


@router.get('/get_items', response_model=List[ItemResponseModel])
async def get_items(page: int = 1, limit: int = 10, userRole: User = Depends(has_roles(['admin', 'user']))):
    items = ItemService.get_items_service(page, limit, userRole)
    return items


@router.get('/get_item/{item_id}', response_model=ItemResponseModel)
async def get_item(item_id: int, userRole: User = Depends(has_roles(['admin', 'user']))):
    item = ItemService.get_item_service(item_id, userRole)
    return item


@router.put('/update_item/{item_id}', response_model=ItemResponseModel)
async def update_item(item_id: int, item: ItemRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    item_updated = ItemService.update_item_service(item_id, item, userRole)
    return item_updated


@router.delete('/delete_item/{item_id}')
async def delete_item(item_id: int, userRole: User = Depends(has_roles(['admin']))):
    ItemService.item_deleted_service(item_id, userRole)
    return {'message': 'Item eliminado exitosamente'}
