from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from typing import List

from ..models import User
from ..models import Item

from ..schemas import ItemResponseModel, ItemRequestModel

from ..common import has_roles

router = APIRouter(prefix='/items')


@router.post('/create_item', response_model=ItemResponseModel)
async def create_item(item: ItemRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    if Item.select().where(Item.name == item.name).exists():
        raise HTTPException(409, 'El item ya existe')
    item_created = Item.create(
        name=item.name,
        description=item.description,
        price=item.price,
        stock=item.stock,
        user_created_id=userRole.id
    )
    return item_created


@router.get('/get_items', response_model=List[ItemResponseModel])
async def get_items(page: int = 1, limit: int = 10, userRole: User = Depends(has_roles(['admin', 'user']))):
    items = Item.select().where(Item.user_created_id ==
                                userRole.id).order_by(Item.stock).paginate(page, limit)

    return [item for item in items]


@router.get('/get_item/{item_id}', response_model=ItemResponseModel)
async def get_item(item_id: int, userRole: User = Depends(has_roles(['admin', 'user']))):
    item = Item.get_or_none(
        Item.id == item_id, Item.user_created_id == userRole.id)
    if item is None:
        raise HTTPException(404, 'El item no existe')
    return item


@router.put('/update_item/{item_id}', response_model=ItemResponseModel)
async def update_item(item_id: int, item: ItemRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    item_updated = updateitem(item_id, item, userRole)
    return item_updated


def updateitem(item_id, item, userRole):

    item_updated = Item.get_or_none(
        Item.id == item_id, Item.user_created_id == userRole.id)
    if item_updated is None:
        raise HTTPException(404, 'El item no existe')
    item_updated.name = item.name
    item_updated.description = item.description
    item_updated.price = item.price
    item_updated.stock = item.stock
    item_updated.save()
    return item_updated


@router.delete('/delete_item/{item_id}')
async def delete_item(item_id: int, userRole: User = Depends(has_roles(['admin']))):
    item_deleted = Item.get_or_none(
        Item.id == item_id, Item.user_created_id == userRole.id)
    if item_deleted is None:
        raise HTTPException(404, 'El item no existe')
    item_deleted.delete_instance()
    return {'message': 'Item eliminado exitosamente'}
