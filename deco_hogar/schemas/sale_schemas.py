from pydantic import BaseModel, validator

from typing import Dict, Any

from typing import List

from .response_model import ResponseModel
from .client_schemas import ClientResponseModel


class ItemRequestModel(BaseModel):
    product_id: int
    quantity: int
    price: float

    @validator('product_id')
    def product_id_validator(cls, product_id):
        if product_id < 1:
            raise ValueError('El id del producto debe ser mayor a 0')
        return product_id

    @validator('quantity')
    def quantity_validator(cls, quantity):
        if quantity < 1:
            raise ValueError('La cantidad debe ser mayor a 0')
        return quantity

    @validator('price')
    def price_validator(cls, price):
        if price < 0:
            raise ValueError('El precio debe ser mayor a 0')
        return price


class SaleRequestModel(BaseModel):
    client_id: int
    products: List[ItemRequestModel]
    total_price: float
    frequency_payment_id: int

    @validator('client_id')
    def client_id_validator(cls, client_id):
        if client_id < 1:
            raise ValueError('El id del cliente debe ser mayor a 0')
        return client_id


class FrequencyPaymentResponseModel(ResponseModel):
    id: int
    name: str
    description: str


class SaleResponseModel(ResponseModel):
    id: int
    total_price: float
    frequency_payment_id: FrequencyPaymentResponseModel


class ItemModel(ResponseModel):
    id: int
    quantity: int


class SaleListResponseModel(ResponseModel):
    id: int
    total_price: float
    frequency_payment_id: FrequencyPaymentResponseModel
    client_id: ClientResponseModel
    products: List[ItemModel]
