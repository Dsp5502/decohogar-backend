from pydantic import BaseModel, validator

from .response_model import ResponseModel


class ItemRequestModel(BaseModel):
    name: str
    description: str
    stock: int
    price: float

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 50:
            raise ValueError(
                'El nombre del item debe tener entre 3 y 50 caracteres')
        return name

    @validator('description')
    def description_validator(cls, description):
        if len(description) < 3 or len(description) > 100:
            raise ValueError(
                'La descripción del item debe tener entre 3 y 100 caracteres')
        return description

    @validator('price')
    def price_validator(cls, price):
        if price <= 0:
            raise ValueError('El precio del item debe ser mayor a 0')
        return price


class ItemResponseModel(ResponseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
