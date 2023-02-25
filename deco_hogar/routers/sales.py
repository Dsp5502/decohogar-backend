import logging

from peewee import *

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends


from typing import List


from ..models import Client
from ..models import User
from ..models import Item
from ..models import ClientItem
from ..models import Sale

from ..schemas import SaleRequestModel, SaleResponseModel, SaleListResponseModel, ItemModel

from ..services import SaleService


from ..common import has_roles

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/sales')


@router.post('/create_sale', response_model=SaleResponseModel)
async def create_sale(sale: SaleRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
    return SaleService.create_sale_service(sale, userRole)

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


@router.get('/get_sales', response_model=List[SaleListResponseModel])
async def get_sales(page: int = 1, limit: int = 10, userRole: User = Depends(has_roles(['admin', 'user']))):
    return SaleService.get_sales_service(page, limit)


@router.get('/get_sale/{sale_id}', response_model=SaleListResponseModel)
async def get_sale(sale_id: int, userRole: User = Depends(has_roles(['admin', 'user']))):
    return SaleService.get_sale_service(sale_id)


@router.delete('/delete_sale/{sale_id}')
async def delete_sale(sale_id: int, return_stock: bool = False,  userRole: User = Depends(has_roles(['admin']))):
    return SaleService.delete_sale_service(sale_id, return_stock)
