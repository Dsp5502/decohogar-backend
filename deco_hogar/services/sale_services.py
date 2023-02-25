import logging

from peewee import *

from fastapi import HTTPException

from ..models import User, Item, Client, ClientItem, Sale
from ..schemas import SaleRequestModel, SaleResponseModel, SaleListResponseModel, ItemModel

logger = logging.getLogger(__name__)


class SaleService:

    @staticmethod
    def create_sale_service(sale: SaleRequestModel, userRole: User):
        try:
            if Client.get_or_none(Client.id == sale.client_id) is None:
                raise HTTPException(404, 'El cliente no existe')

            # Crear venta   Id para asociar con los productos
            sale_created = Sale.create(
                client_id=sale.client_id,
                user_created_id=userRole.id,
                total_price=sale.total_price,
                frequency_payment_id=sale.frequency_payment_id
            )

            # Crear productos de la venta
            for product in sale.products:
                if Item.get_or_none(Item.id == product.product_id) is None:
                    raise HTTPException(404, 'El producto no existe')

                if Item.get_or_none(Item.id == product.product_id).stock < product.quantity:
                    raise HTTPException(409, 'No hay suficiente stock')

                ClientItem.create(
                    client_id=sale.client_id,
                    item_id=product.product_id,
                    quantity=product.quantity,
                    user_created_id=userRole.id,
                    sale_id=sale_created.id
                )
                # Actualizar stock
                item_update = Item.update(
                    stock=Item.stock - product.quantity).where(Item.id == product.product_id)
                item_update.execute()

            # Retornar venta
            return sale_created

        except DoesNotExist as e:
            raise HTTPException(404, 'No se encontró un registro') from e

        except IntegrityError as e:
            raise HTTPException(
                409, 'Error de integridad en la base de datos') from e

        except Exception as e:
            print(e)
            raise HTTPException(500, 'Error al crear venta')

    @staticmethod
    def get_sales_service(page: int, limit: int):
        try:
            sales = Sale.select().paginate(page, limit)
            sales_list = []
            for sale in sales:
                sale_items = ClientItem.select().where(
                    ClientItem.sale_id == sale.id)
                item_list = []
                for sale_item in sale_items:
                    item = ItemModel(
                        id=sale_item.id,
                        quantity=sale_item.quantity
                    )
                    item_list.append(item)
                sale_response_model = SaleListResponseModel(
                    id=sale.id,
                    total_price=sale.total_price,
                    frequency_payment_id=sale.frequency_payment_id,
                    client_id=sale.client_id,
                    products=item_list
                )
                sales_list.append(sale_response_model)
            return sales_list
        except Exception as e:
            logger.exception("Error al obtener ventas: %s", str(e))
            raise HTTPException(
                500, 'Ocurrió un error al obtener ventas, por favor inténtelo de nuevo más tarde.')

    @staticmethod
    def get_sale_service(sale_id: int):
        try:
            sale = Sale.get_or_none(Sale.id == sale_id)
            if sale is None:
                raise HTTPException(404, 'La venta no existe')
            sale_items = ClientItem.select().where(
                ClientItem.sale_id == sale.id)
            item_list = []
            for sale_item in sale_items:
                item = ItemModel(
                    id=sale_item.id,
                    quantity=sale_item.quantity
                )
                item_list.append(item)
            sale_response_model = SaleListResponseModel(
                id=sale.id,
                total_price=sale.total_price,
                frequency_payment_id=sale.frequency_payment_id,
                client_id=sale.client_id,
                products=item_list
            )
            return sale_response_model
        except Exception as e:
            logger.exception("Error al obtener venta: %s", str(e))
            raise HTTPException(
                500, 'Ocurrió un error al obtener venta, por favor inténtelo de nuevo más tarde.')

    @staticmethod
    def delete_sale_service(sale_id: int, return_stock: bool):
        try:
            sale = Sale.get_or_none(Sale.id == sale_id)
            if sale is None:
                raise HTTPException(404, 'La venta no existe')
            sale_items = ClientItem.select().where(
                ClientItem.sale_id == sale.id)
            for sale_item in sale_items:
                sale_item.delete_instance()
                # Actualizar stock
                if return_stock:
                    item_update = Item.update(
                        stock=Item.stock + sale_item.quantity).where(Item.id == sale_item.item_id)
                    item_update.execute()
            sale.delete_instance()
            return {'message': 'Venta eliminada correctamente'}
        except Exception as e:
            logger.exception("Error al eliminar venta: %s", str(e))
            raise HTTPException(
                500, 'Ocurrió un error al eliminar venta, por favor inténtelo de nuevo más tarde.')
