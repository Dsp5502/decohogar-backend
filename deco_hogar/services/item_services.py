from fastapi import HTTPException


from ..models import User, Item
from ..schemas import ItemRequestModel


class ItemService:

    @staticmethod
    def item_create_service(item: ItemRequestModel, userRole: User):
        try:
            items = Item.select()
            existing_names = [item.name.lower() for item in items]
            if item.name.lower() in existing_names:
                raise HTTPException(409, 'El item ya existe')
            item_created = Item.create(
                name=item.name,
                description=item.description,
                price=item.price,
                stock=item.stock,
                user_created_id=userRole.id
            )
            return item_created
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    def get_items_service(page: int, limit: int, userRole: User):
        try:
            items = Item.select().where(Item.user_created_id ==
                                        userRole.id).order_by(Item.stock).paginate(page, limit)
            return [item for item in items]
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    def get_item_service(item_id: int, userRole: User):
        try:
            item = Item.get_or_none(
                Item.id == item_id, Item.user_created_id == userRole.id)
            if item is None:
                raise HTTPException(404, 'El item no existe')
            return item
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    def update_item_service(item_id: int, item: ItemRequestModel, userRole: User):
        try:
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
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    def item_deleted_service(item_id, userRole):
        try:
            item_deleted = Item.get_or_none(
                Item.id == item_id, Item.user_created_id == userRole.id)
            if item_deleted is None:
                raise HTTPException(404, 'El item no existe')
            item_deleted.delete_instance()
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(500, str(e))
