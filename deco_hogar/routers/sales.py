from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends


from typing import List


from ..models import Client
from ..models import User
from ..models import Item
from ..models import ClientItem
from ..models import Sale

from ..schemas import SaleRequestModel, SaleResponseModel


from ..common import has_roles


router = APIRouter(prefix='/sales')


@router.post('/create_sale', response_model=SaleResponseModel)
async def create_sale(sale: SaleRequestModel, userRole: User = Depends(has_roles(['admin', 'user']))):
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
        print(item_update)
        item_update.execute()

# Retornar venta
    return sale_created
